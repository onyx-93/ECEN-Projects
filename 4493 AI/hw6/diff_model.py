from diffusers import DiffusionPipeline
import torch

# Load the pipeline with optimizations for your 8GB GPU
pipe = DiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,      # Use half precision (saves VRAM)
    safety_checker=None,            # ← Disable the annoying safety checker
    requires_safety_checker=False
)

pipe = pipe.to("cuda")

# Optional: Enable better memory efficiency
pipe.enable_attention_slicing()     # Helps with 8GB cards

print("Generating image...")

image = pipe(
    prompt="a cute cat astronaut floating in space, cartoon style, vibrant colors, highly detailed, 8k",
    negative_prompt="blurry, low quality, deformed, ugly",
    num_inference_steps=30,         # Reduced from 50 → faster
    guidance_scale=7.5,
    height=512,
    width=512
).images[0]

image.save("test_cat.png")
print("✅ Success! Image saved as test_cat.png")