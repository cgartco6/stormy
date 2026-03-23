# Stormy AI – The Eternally Evolving Rebel Assistant

Stormy is a bold, region‑aware AI assistant that runs entirely on free tiers and evolves daily without version numbers.

## Quick Start

1. **Clone this repo**
2. **Install dependencies**:
   - Run `python install/install.py` (or `install/install.sh` on Linux/macOS, `install.bat` on Windows)
   - This installs local LLM (Ollama), Python packages, and sets up config.
3. **Configure credentials**:
   - Copy `.env.example` to `.env` and fill in your API keys (optional – local LLM works without).
4. **Run locally**:
   - Backend: `cd backend && python app.py`
   - Frontend: `cd frontend && npm start`
5. **Deploy to free hosting**:
   - Backend: Deploy to Render (free tier) using the Dockerfile.
   - Frontend: Deploy to Netlify/Vercel (free tier) using the provided configs.

## Features

- **Region & unit adaptation** – automatically detects your location and uses metric/imperial, local language.
- **Free‑tier LLM** – uses local Llama 3.1 via Ollama; falls back to Hugging Face free inference if needed.
- **Voice I/O** – local Whisper for STT, Coqui TTS.
- **Music** – streams Bok Radio (98.9 FM) and custom stations.
- **Navigation** – OpenStreetMap + OSRM for free routing.
- **Revenue system** – integrates Stripe, PayPal, PayFast, and direct EFT (manual instructions for FNB/African Bank). Weekly payouts to owners (40% FNB, 20% African Bank, 7% reserve).
- **Self‑evolution** – daily fine‑tuning using user interactions (anonymized) to improve responses without version updates.

## Environment Variables

See `.env.example` for all required keys. Most are optional for local use.

## License

MIT
