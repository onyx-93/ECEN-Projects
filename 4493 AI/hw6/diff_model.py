from diffusers import StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler
import torch
from PIL import Image

torch.backends.cuda.matmul.allow_tf32 = True

# Load input image (your face or base image)
init_image = Image.open("daniel_headshot.jpg").convert("RGB")

# Get dimensions
w, h = init_image.size
crop_size = min(w, h)
left = (w - crop_size) // 2
top = int((h - crop_size) * 0.3)  # 👈 shift upward (focus on face)
right = left + crop_size
bottom = top + crop_size

# Crop and resize
init_image = init_image.crop((left, top, right, bottom))
init_image = init_image.resize((512, 512))


pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32,
    safety_checker=None,
    requires_safety_checker=False
)

pipe = pipe.to("cuda")

# Stability tweaks
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.disable_xformers_memory_efficient_attention()
pipe.enable_attention_slicing()

# Your assignment prompt (slightly improved)
prompt = (
    "apple memoji style avatar, 3D cartoon, smooth plastic skin, "
    "simple facial features, rounded face, large expressive eyes, "
    "small nose, simplified eyebrows, clean shaven, "
    "male, stoic expression, suit and tie, "
    "centered head and shoulders portrait, "
    "plain white background, studio lighting, no shadows, high quality"
)

negative_prompt = (
    "realistic, photo, hyperrealistic, skin texture, pores, wrinkles, "
    "detailed beard, facial hair, sharp details, harsh shadows, "
    "complex background, clutter, noise, grain, low quality"
)

image = pipe(
    prompt=prompt,
    negative_prompt = negative_prompt,    
    image=init_image,
    strength=0.78,   # key parameter
    num_inference_steps=40,
    guidance_scale=10.0,
    generator=torch.Generator("cuda").manual_seed(1234)
).images[0]

image.save("memoji_avatar.png")
print("✅ Success! Image saved as memoji_avatar.png")