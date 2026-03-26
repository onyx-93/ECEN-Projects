from diffusers import StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler
import torch
from PIL import Image

torch.backends.cuda.matmul.allow_tf32 = True

# Load your photo
init_image = Image.open("daniel_headshot.jpg").convert("RGB")

w, h = init_image.size

# Improved crop - more centered on face and shoulders
left = int(w * 0.18)
right = int(w * 0.82)
top = int(h * 0.08)
bottom = int(h * 0.78)

init_image = init_image.crop((left, top, right, bottom))
init_image = init_image.resize((512, 512), Image.LANCZOS)

# Load pipeline
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32,
    safety_checker=None,
    requires_safety_checker=False
)

pipe = pipe.to("cuda")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

pipe.disable_xformers_memory_efficient_attention()
pipe.enable_attention_slicing()

# ── Improved Prompt ──
prompt = (
    "Apple Memoji style, 3D cartoon avatar, smooth glossy plastic skin, "
    "simplified cartoon features, rounded head, large shiny eyes with highlights, "
    "small simplified nose, thin eyebrows, clean shaven, no facial hair, "
    "stoic calm expression, neutral serious face, male, "
    "wearing formal suit and tie, green shirt, "
    "head and shoulders portrait, perfectly centered, "
    "plain solid white background, no background details, clean studio lighting, "
    "minimal shadows, high quality, crisp, iconic memoji look"
)

# ── Stronger Negative Prompt ──
negative_prompt = (
    "realistic, photorealistic, photo, human skin texture, pores, wrinkles, beard, stubble, "
    "facial hair, detailed face, realistic eyes, complex background, any background, "
    "shadows, depth of field, blur, noise, grain, low quality, blurry, deformed, "
    "extra limbs, text, watermark, logo, clothing wrinkles, realistic fabric"
)

# Generate
image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    image=init_image,
    strength=0.78,          # Slightly lower = better face fidelity
    num_inference_steps=50, # More steps for cleaner style
    guidance_scale=11.0,    # Stronger prompt adherence
    generator=torch.Generator("cuda").manual_seed(1234)
).images[0]

image.save("memoji_avatar.png")
print("✅ Success! Memoji avatar saved as memoji_avatar.png")