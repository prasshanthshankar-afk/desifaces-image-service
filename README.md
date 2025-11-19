# Desifaces Image Service v2

AI-powered image generation service designed for RunPod Serverless deployment.

## Features

- **FastAPI HTTP Server**: RESTful API on port 8000
- **RunPod Serverless Handler**: Native RunPod serverless support
- **GPU Acceleration**: Optimized for NVIDIA GPUs (A40 24GB recommended)
- **Docker Containerized**: Easy deployment and scaling

## Architecture

This service provides two operational modes:

1. **HTTP Server Mode** (default): FastAPI server for direct HTTP requests
2. **RunPod Serverless Mode**: Native RunPod serverless handler

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the HTTP server:
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### Docker Build

Build the Docker image:
```bash
docker build -t desifaces-image-service:v2 .
```

Run locally:
```bash
docker run -p 8000:8000 desifaces-image-service:v2
```

For GPU support:
```bash
docker run --gpus all -p 8000:8000 desifaces-image-service:v2
```

## RunPod Serverless Deployment

### Step 1: Build and Push Docker Image

1. Build the image:
```bash
docker build -t your-dockerhub-username/desifaces-image-service:v2 .
```

2. Push to Docker Hub (or your preferred registry):
```bash
docker push your-dockerhub-username/desifaces-image-service:v2
```

### Step 2: Create RunPod Serverless Endpoint

1. Go to [RunPod Serverless](https://www.runpod.io/console/serverless) → Endpoints
2. Click **"New Endpoint"**
3. Configure the endpoint:
   - **Container Image**: `your-dockerhub-username/desifaces-image-service:v2`
   - **HTTP**: Enabled
   - **Port**: 8000
   - **GPU Type**: A40 (24GB) or your preferred GPU
   - **Container Disk**: 10 GB (minimum)
   - **Volume Disk**: Optional (for model caching)
4. Click **Save/Create**

### Step 3: Test Your Endpoint

Once deployed, you can test the endpoint using the RunPod API or directly via HTTP.

**Example request:**
```bash
curl -X POST "https://your-endpoint-id.runpod.ai/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "width": 512,
    "height": 512,
    "num_inference_steps": 50,
    "guidance_scale": 7.5
  }'
```

## API Endpoints

### `GET /`
Health check and service information.

**Response:**
```json
{
  "service": "Desifaces Image Service",
  "version": "2.0.0",
  "status": "running"
}
```

### `GET /health`
Health check for monitoring.

**Response:**
```json
{
  "status": "healthy"
}
```

### `POST /generate`
Generate an image based on a text prompt.

**Request Body:**
```json
{
  "prompt": "A beautiful sunset over mountains",
  "width": 512,
  "height": 512,
  "num_inference_steps": 50,
  "guidance_scale": 7.5
}
```

**Response:**
```json
{
  "image": "base64_encoded_image_data...",
  "prompt": "A beautiful sunset over mountains",
  "width": 512,
  "height": 512
}
```

## RunPod Serverless Handler

For direct RunPod serverless usage (non-HTTP), use the handler:

```python
# In your Dockerfile CMD
CMD ["python", "handler.py"]
```

**Input format:**
```json
{
  "input": {
    "prompt": "A beautiful sunset over mountains",
    "width": 512,
    "height": 512,
    "num_inference_steps": 50,
    "guidance_scale": 7.5
  }
}
```

## Customization

### Adding Your Own Model

The current implementation includes placeholder image generation. To add your own model:

1. Update `handler.py` and `app.py` with your model loading code
2. Modify the `generate_image()` function to use your model
3. Update `requirements.txt` with any additional dependencies
4. Adjust Dockerfile if needed for model files or additional system dependencies

### Example with Stable Diffusion:

```python
from diffusers import StableDiffusionPipeline

def load_model():
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16
    )
    pipe.to("cuda")
    return pipe

model = load_model()

def generate_image(prompt: str, **kwargs):
    image = model(
        prompt=prompt,
        width=kwargs.get('width', 512),
        height=kwargs.get('height', 512),
        num_inference_steps=kwargs.get('num_inference_steps', 50),
        guidance_scale=kwargs.get('guidance_scale', 7.5)
    ).images[0]
    return image
```

## Environment Variables

- `PYTHONUNBUFFERED=1`: Ensures Python output is not buffered (set in Dockerfile)

## Requirements

- Python 3.10+
- CUDA 12.1+ (for GPU support)
- NVIDIA GPU with 24GB VRAM recommended (A40, RTX 3090, etc.)

## License

[Add your license here]

## Support

For issues or questions, please open an issue on the GitHub repository.