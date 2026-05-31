# Comfy Cloud — Known Model Names (as of 2026-05)

## Checkpoints (`/api/experiment/models/checkpoints`)

Commonly available on Cloud:
- `flux1-dev-fp8.safetensors` — Flux Dev fp8 (use with `LoadDiffusionModel`, NOT `UNETLoader`)
- `flux1-schnell-fp8.safetensors` — Flux Schnell fp8 (faster, lower quality)
- `v1-5-pruned-emaonly-fp16.safetensors` — SD 1.5
- `sd_xl_base_1.0.safetensors` — SDXL
- `sd3.5_large_fp8_scaled.safetensors` — SD3.5 Large fp8
- `dreamshaper_8.safetensors` — DreamShaper (good for stylized content)
- `realvisxlV50_v50Bakedvae.safetensors` — Realistic Vision XL
- `majicmixRealistic_v7.safetensors` — MajicMix Realistic

## Text Encoders (`/api/experiment/models/text_encoders`)

- `t5xxl_fp16.safetensors` — T5-XXL (required for Flux)
- `clip_l.safetensors` — CLIP-L (required for Flux)

## VAE (`/api/experiment/models/vae`)

- `ae.safetensors` — Flux VAE

## Key Differences from Local

| Component | Local name | Cloud name |
|-----------|-----------|------------|
| Flux UNET | `unet/flux1-dev.safetensors` | `checkpoints/flux1-dev-fp8.safetensors` |
| CLIP/T5 | `clip/t5xxl_fp16.safetensors` | `text_encoders/t5xxl_fp16.safetensors` |
| VAE | `vae/ae.safetensors` | `vae/ae.safetensors` (same) |

## Free Tier Limitation

Free tier can **browse** all model listings via `/api/experiment/models/*` but
returns **429 PAYMENT_REQUIRED** when submitting workflows to `/api/prompt`.
Upgrade to Standard (~$10/mo) for workflow execution.
