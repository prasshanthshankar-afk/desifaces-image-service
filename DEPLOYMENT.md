# RunPod Serverless Deployment Guide

This guide walks you through deploying the Desifaces Image Service v2 to RunPod Serverless.

## Prerequisites

- Docker installed locally
- Docker Hub account (or alternative container registry)
- RunPod account with credits

## Step-by-Step Deployment

### 1. Build the Docker Image

From the repository root, build the Docker image:

```bash
docker build -t desifaces-image-service:v2 .
```

**Note**: The build may take several minutes as it downloads CUDA base image and Python dependencies.

### 2. Tag and Push to Registry

Replace `your-dockerhub-username` with your actual Docker Hub username:

```bash
# Tag the image
docker tag desifaces-image-service:v2 your-dockerhub-username/desifaces-image-service:v2

# Login to Docker Hub
docker login

# Push the image
docker push your-dockerhub-username/desifaces-image-service:v2
```

**Alternative registries**: You can also use:
- GitHub Container Registry (ghcr.io)
- Google Container Registry (gcr.io)
- AWS ECR
- Any other OCI-compliant registry

### 3. Create RunPod Serverless Endpoint

1. **Navigate to RunPod Console**
   - Go to https://www.runpod.io/console/serverless
   - Click on **"Endpoints"** in the sidebar

2. **Create New Endpoint**
   - Click the **"New Endpoint"** button

3. **Configure Endpoint Settings**

   **Basic Configuration:**
   - **Name**: `desifaces-image-service-v2`
   - **Container Image**: `your-dockerhub-username/desifaces-image-service:v2`
   
   **Container Configuration:**
   - **HTTP**: ✓ Enabled
   - **HTTP Port**: `8000`
   - **Container Disk**: `10 GB` (minimum)
   - **Volume Disk**: `0 GB` (optional, increase if caching models)
   
   **GPU Configuration:**
   - **GPU Type**: Select `A40 (24GB)` or your preferred GPU
   - **Min Workers**: `0` (for auto-scaling)
   - **Max Workers**: `3` (or as needed)
   - **Idle Timeout**: `5 seconds`
   - **Execution Timeout**: `300 seconds` (adjust based on your needs)
   
   **Advanced Settings (Optional):**
   - **Environment Variables**: Add any required env vars
   - **Volume Mount**: Configure if using persistent storage

4. **Save and Deploy**
   - Click **"Deploy"** or **"Save"**
   - Wait for the endpoint to initialize (may take a few minutes)

### 4. Test Your Endpoint

Once deployed, RunPod provides you with an endpoint URL. Test it:

#### Using cURL:

```bash
# Health check
curl https://your-endpoint-id-xxxxxx.runpod.net/health

# Generate image
curl -X POST https://your-endpoint-id-xxxxxx.runpod.net/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "width": 512,
    "height": 512,
    "num_inference_steps": 50,
    "guidance_scale": 7.5
  }'
```

#### Using Python:

```python
import requests
import base64
from PIL import Image
import io

url = "https://your-endpoint-id-xxxxxx.runpod.net/generate"

payload = {
    "prompt": "A beautiful sunset over mountains",
    "width": 512,
    "height": 512,
    "num_inference_steps": 50,
    "guidance_scale": 7.5
}

response = requests.post(url, json=payload)
result = response.json()

# Decode and save image
image_data = base64.b64decode(result['image'])
image = Image.open(io.BytesIO(image_data))
image.save('output.png')
print(f"Image saved: {result['width']}x{result['height']}")
```

### 5. Monitor and Scale

- **Monitor Usage**: Check the RunPod dashboard for request metrics, GPU usage, and costs
- **Adjust Workers**: Modify min/max workers based on traffic patterns
- **Update Image**: Push new versions and update the endpoint configuration

## Troubleshooting

### Container Fails to Start

- Check the logs in RunPod dashboard
- Verify the Docker image is publicly accessible or credentials are configured
- Ensure the port is set to 8000

### High Cold Start Times

- Increase min workers to keep instances warm
- Optimize Docker image size
- Consider using a volume mount for model caching

### Out of Memory Errors

- Increase GPU type (e.g., from A40 to A100)
- Optimize model loading and inference
- Reduce batch sizes or image dimensions

### HTTP Timeout Errors

- Increase the execution timeout in endpoint settings
- Optimize inference speed
- Consider async processing for long-running tasks

## Cost Optimization

- **Auto-scaling**: Use min workers = 0 for infrequent workloads
- **GPU Selection**: Choose the smallest GPU that meets your needs
- **Efficient Models**: Use optimized models (quantized, pruned, distilled)
- **Request Batching**: Process multiple requests together when possible

## Security Best Practices

- Use environment variables for sensitive configuration
- Enable authentication on your RunPod endpoint
- Validate and sanitize all input
- Keep dependencies updated
- Monitor for unusual activity

## Next Steps

- Customize the model in `handler.py` and `app.py`
- Add authentication middleware
- Implement request queuing for high traffic
- Set up monitoring and alerting
- Configure auto-scaling policies

For support, refer to:
- [RunPod Documentation](https://docs.runpod.io/)
- [This repository's README](README.md)
- Open an issue on GitHub
