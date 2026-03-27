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

# PROBLEM 1 — Memoji Style
prompt = (
"Apple Memoji style, 3D cartoon avatar, smooth glossy plastic skin, "
    "simplified cartoon features, large shiny eyes with bright highlights, "
    "small rounded nose, thin eyebrows, clean shaven, no facial hair, "
    "short curly dark hair, stoic calm neutral expression, serious face, "
    "male, wearing navy blue suit jacket, white collared shirt, blue patterned tie, "
    "head and shoulders portrait, perfectly centered, "
    "plain solid white background, no background details, clean studio lighting, "
    "minimal shadows, high quality, crisp, iconic Apple Memoji look"
)

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

'''
# PROBLEM 2 — Comic Book Café
prompt = (
"   comic book style digital avatar, graphic novel art, vibrant colors, bold black ink outlines, "
    "highly detailed, colored comic illustration, 2d comic panel, dynamic composition, "
    "adult male, short dark curly hair, full dark beard, stoic calm expression, "
    "wearing navy blue suit jacket, white collared dress shirt, blue patterned tie, "
    "cozy café interior background, large windows with sunlight, shelves with pastries and coffee signs, "
    "high quality, crisp lines, professional comic art style"
)

negative_prompt = (
    "realistic, photorealistic, photo, human skin texture, 3d render, blurry, low quality, "
    "deformed, extra limbs, bad anatomy, text, watermark, logo, grain, noise, "
    "realistic fabric, wrinkles, shadows, depth of field, cartoonish, anime, "
    "memoji, 3d cartoon, green shirt, casual clothing"
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

image.save("comic_cafe_avatar.png")
print("✅ Saved: comic_cafe_avatar.png")  


# PROBLEM 3 — Elf Headshot
prompt = (
    "close-up headshot portrait of a male high-fantasy elf, pointed elf ears clearly visible, "
    "short dark curly hair, full well-groomed beard, stoic calm neutral expression, hazel eyes, "
    "sharp jawline, smooth skin, detailed fantasy features, "
    "lush enchanted forest background with tall ancient trees, soft glowing light rays through leaves, "
    "mystical atmosphere, head and shoulders only, perfectly centered, "
    "highly detailed, epic fantasy digital art, cinematic lighting, sharp focus, masterpiece, 8k"
)

negative_prompt = (
    "hands, arms, full body, deformed ears, blurry, low quality, bad anatomy, extra limbs, "
    "text, watermark, logo, photorealistic, modern clothing, city background, ugly, "
    "cartoonish, noise, grain, overexposed, underexposed"
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

image.save("elf_avatar.png")
print("✅ Saved: elf_avatar.png")

    # PROBLEM 4 — Cyberpunk Neon Avatar
prompt = (
    "cyberpunk digital avatar headshot, futuristic neon cityscape background with glowing holograms and rain reflections, "
    "male with short dark curly hair, full beard, stoic serious expression, hazel eyes, "
    "wearing high-tech navy blue suit with glowing blue circuit patterns and neon accents, "
    "white collared shirt, blue patterned tie with digital glow, "
    "head and shoulders only, perfectly centered, dramatic neon lighting, cyber reflections on skin, "
    "highly detailed, blade-runner aesthetic, vibrant neon colors, crisp lines, masterpiece, 8k"
)

negative_prompt = (
    "hands, arms, full body, blurry, low quality, bad anatomy, extra limbs, "
    "text, watermark, logo, photorealistic photo, fantasy, medieval, cartoonish, "
    "noise, grain, overexposed, underexposed, green shirt"
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

image.save("cyberpunk_avatar.png")
print("✅ Saved: cyberpunk_avatar.png")     '''
