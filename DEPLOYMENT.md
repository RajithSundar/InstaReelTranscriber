# InstaReelTranscriber - Deployment Guide

Complete guide for deploying InstaReelTranscriber using various methods.

---

## 🚀 Quick Start Options

| Method | Difficulty | Best For |
|--------|------------|----------|
| **Local Setup** | Easy | Development, personal use |
| **Docker** | Easy | Production, isolation |
| **Cloud** | Medium | Public hosting |

---

## Option 1: Local One-Click Setup (Recommended)

### Windows

```batch
# 1. Clone the repository
git clone https://github.com/RajithSundar/InstaTranscriber.git
cd InstaTranscriber

# 2. Run setup (installs everything)
setup_and_download.bat

# 3. Start the application
start.bat
```

### macOS / Linux

```bash
# 1. Clone the repository
git clone https://github.com/RajithSundar/InstaTranscriber.git
cd InstaTranscriber

# 2. Make scripts executable
chmod +x setup.sh start.sh

# 3. Run setup
./setup.sh

# 4. Start the application
./start.sh
```

### What the Setup Does

1. ✅ Checks Python 3.8+, Node.js 18+, FFmpeg
2. ✅ Creates Python virtual environment
3. ✅ Installs all backend dependencies
4. ✅ Installs frontend dependencies
5. ✅ Downloads AI model (~140MB)
6. ✅ Creates `.env` configuration file

---

## Option 2: Docker Deployment

### Prerequisites
- Docker Desktop installed and running

### Quick Start

```bash
# Clone and navigate
git clone https://github.com/RajithSundar/InstaTranscriber.git
cd InstaTranscriber

# Build and run (first time takes ~5-10 minutes)
docker-compose up

# Stop when done
docker-compose down
```

### Custom Configuration

Create a `.env` file before running:

```env
WHISPER_MODEL=base      # tiny, base, small, medium, large
API_PORT=8000           # Backend port
FRONTEND_PORT=3000      # Frontend port
```

### Useful Commands

```bash
# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose build --no-cache

# Remove all containers and volumes
docker-compose down -v
```

---

## Option 3: Cloud Deployment

### Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/XXXXXX)

1. Click the deploy button above
2. Connect your GitHub account
3. Railway auto-provisions everything

### Render

1. Create a new **Web Service** for backend
2. Create another for frontend
3. Set environment variables:
   - `WHISPER_MODEL=base`
   - `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`

### Manual Cloud Deployment

For AWS, GCP, or other providers:

1. Build Docker images:
   ```bash
   docker build -f Dockerfile.backend -t insta-backend .
   docker build -f Dockerfile.frontend -t insta-frontend .
   ```

2. Push to container registry (ECR, GCR, Docker Hub)

3. Deploy using your cloud provider's container service

---

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WHISPER_MODEL` | `base` | AI model (tiny/base/small/medium/large) |
| `API_PORT` | `8000` | Backend API port |
| `FRONTEND_PORT` | `3000` | Frontend web port |
| `CORS_ORIGIN` | `http://localhost:3000` | Allowed frontend origin |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

### Model Selection

| Model | Size | Speed | Accuracy | RAM |
|-------|------|-------|----------|-----|
| `tiny` | 39M | ⚡⚡⚡ | Basic | 1GB |
| `base` | 74M | ⚡⚡ | Good | 1GB |
| `small` | 244M | ⚡ | Better | 2GB |
| `medium` | 769M | 🐢 | High | 5GB |
| `large` | 1550M | 🐢🐢 | Best | 10GB |

---

## Troubleshooting

### Setup Issues

| Problem | Solution |
|---------|----------|
| Python not found | Install Python 3.8+ and add to PATH |
| Node.js not found | Install from https://nodejs.org |
| FFmpeg not found | See FFmpeg installation below |
| Model download fails | Check internet, retry with `python src/model_downloader.py --model base` |

### FFmpeg Installation

**Windows:**
```powershell
winget install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update && sudo apt install ffmpeg
```

### Runtime Issues

| Problem | Solution |
|---------|----------|
| Backend won't start | Check port 8000 is free, check logs |
| Frontend won't start | Run `cd frontend && npm install` |
| "Backend Offline" in UI | Start backend first, check CORS settings |
| Transcription fails | Ensure FFmpeg is installed, check reel is public |

---

## Ports & URLs

| Service | Default URL |
|---------|-------------|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Health Check | http://localhost:8000/health |

---

## Next Steps

After deployment:
1. Open http://localhost:3000
2. Paste any public Instagram Reel URL
3. Click "Transcribe" and wait for results

Happy transcribing! 🎙️
