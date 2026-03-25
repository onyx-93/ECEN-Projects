from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import torch

torch.backends.cuda.matmul.allow_tf32 = True

pipe = DiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32,  # <-- FIX
    safety_checker=None,
    requires_safety_checker=False
)

pipe = pipe.to("cuda")

# Optional stability improvements
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.disable_xformers_memory_efficient_attention()

pipe.enable_attention_slicing()

image = pipe(
    prompt="a cute cartoon dog swimming in the beach, bright colors, children's book illustration, happy, friendly, vibrant, detailed",
    negative_prompt="dark, scary, blurry, low quality, deformed, ugly, NSFW",
    num_inference_steps=30,
    guidance_scale=7.5,
    height=512,
    width=512,
    generator=torch.Generator("cuda").manual_seed(1234)
).images[0]

image.save("test_dog.png")
print('Succes! Image saved as test_dog.png')