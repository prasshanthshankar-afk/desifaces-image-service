# Quick Start Guide

Get the Desifaces Image Service v2 running in minutes!

## 🚀 Option 1: Local Development (No Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Test it (in another terminal)
curl http://localhost:8000/health
```

## 🐳 Option 2: Local with Docker

```bash
# Build and run
docker build -t desifaces:v2 .
docker run -p 8000:8000 desifaces:v2

# Test it
curl http://localhost:8000/health
```

## 🎯 Option 3: Using Make (Recommended)

```bash
# Install dependencies
make install

# Run tests
make test

# Start server
make run
```

## ☁️ Option 4: Deploy to RunPod

### Quick Deploy (5 minutes)

1. **Build & Push Image**
   ```bash
   # Replace with your Docker Hub username
   docker build -t yourusername/desifaces:v2 .
   docker push yourusername/desifaces:v2
   ```

2. **Create Endpoint**
   - Go to [RunPod Serverless](https://www.runpod.io/console/serverless)
   - Click "New Endpoint"
   - Configure:
     - **Image**: `yourusername/desifaces:v2`
     - **HTTP**: ✓ Enabled
     - **Port**: `8000`
     - **GPU**: A40 (24GB)
   - Click "Deploy"

3. **Test Endpoint**
   ```bash
   curl https://your-endpoint-id.runpod.net/health
   ```

## 📝 Generate Your First Image

### Using cURL

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "width": 512,
    "height": 512
  }' | jq .
```

### Using the Client Script

```bash
python client.py http://localhost:8000 \
  --prompt "A beautiful sunset" \
  --width 512 \
  --height 512 \
  --output my_image.png
```

### Using Python

```python
import requests
import base64
from PIL import Image
import io

response = requests.post(
    "http://localhost:8000/generate",
    json={
        "prompt": "A beautiful sunset over mountains",
        "width": 512,
        "height": 512
    }
)

# Save the image
image_data = base64.b64decode(response.json()['image'])
image = Image.open(io.BytesIO(image_data))
image.save("output.png")
```

## 🧪 Verify Everything Works

```bash
make test
```

Expected output:
```
✓ RunPod handler test passed
✓ Health endpoint test passed
✓ Root endpoint test passed
✓ Generate endpoint test passed
✓ All tests passed successfully!
```

## 🔧 Customize with Your Model

Edit `app.py` and `handler.py`:

```python
from diffusers import StableDiffusionPipeline

def load_model():
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5"
    )
    pipe.to("cuda")
    return pipe

def generate_image(prompt: str, **kwargs):
    return model(prompt=prompt, **kwargs).images[0]
```

## 📚 Need More Help?

- **Full Documentation**: See [README.md](README.md)
- **Deployment Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Implementation Details**: See [SUMMARY.md](SUMMARY.md)
- **Commands**: Run `make help`

## ✅ Checklist

- [ ] Service runs locally
- [ ] Tests pass (`make test`)
- [ ] Docker image builds
- [ ] Deployed to RunPod
- [ ] Endpoint responds to requests
- [ ] Ready to customize with your model!

---

**Next Steps**: Integrate your AI model and deploy to production! 🎉
