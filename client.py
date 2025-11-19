#!/usr/bin/env python3
"""
Example client for Desifaces Image Service
Demonstrates how to interact with the deployed service
"""

import requests
import base64
import io
from PIL import Image
import argparse
import json


def generate_image(endpoint_url: str, prompt: str, width: int = 512, height: int = 512, 
                   num_steps: int = 50, guidance: float = 7.5, output_file: str = "output.png"):
    """
    Generate an image using the Desifaces Image Service
    
    Args:
        endpoint_url: Base URL of the service (e.g., https://your-endpoint.runpod.net)
        prompt: Text description of the image to generate
        width: Image width in pixels
        height: Image height in pixels
        num_steps: Number of inference steps
        guidance: Guidance scale
        output_file: Path to save the output image
    """
    # Prepare the request
    url = f"{endpoint_url.rstrip('/')}/generate"
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "num_inference_steps": num_steps,
        "guidance_scale": guidance
    }
    
    print(f"Generating image with prompt: '{prompt}'")
    print(f"Parameters: {width}x{height}, steps={num_steps}, guidance={guidance}")
    
    # Make the request
    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        
        # Decode the base64 image
        image_data = base64.b64decode(result['image'])
        image = Image.open(io.BytesIO(image_data))
        
        # Save the image
        image.save(output_file)
        
        print(f"✓ Image generated successfully!")
        print(f"  Size: {result['width']}x{result['height']}")
        print(f"  Saved to: {output_file}")
        
        return image
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        raise
    except Exception as e:
        print(f"✗ Error processing image: {e}")
        raise


def check_health(endpoint_url: str):
    """
    Check if the service is healthy
    
    Args:
        endpoint_url: Base URL of the service
    """
    url = f"{endpoint_url.rstrip('/')}/health"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('status') == 'healthy':
            print("✓ Service is healthy")
            return True
        else:
            print(f"✗ Service status: {result}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Health check failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Desifaces Image Service"
    )
    
    parser.add_argument(
        "endpoint",
        help="Service endpoint URL (e.g., http://localhost:8000 or https://your-endpoint.runpod.net)"
    )
    
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Text description of the image to generate"
    )
    
    parser.add_argument(
        "--width", "-w",
        type=int,
        default=512,
        help="Image width in pixels (default: 512)"
    )
    
    parser.add_argument(
        "--height", "-H",
        type=int,
        default=512,
        help="Image height in pixels (default: 512)"
    )
    
    parser.add_argument(
        "--steps", "-s",
        type=int,
        default=50,
        help="Number of inference steps (default: 50)"
    )
    
    parser.add_argument(
        "--guidance", "-g",
        type=float,
        default=7.5,
        help="Guidance scale (default: 7.5)"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="output.png",
        help="Output file path (default: output.png)"
    )
    
    parser.add_argument(
        "--health-check",
        action="store_true",
        help="Only check service health without generating an image"
    )
    
    args = parser.parse_args()
    
    # Perform health check if requested
    if args.health_check:
        check_health(args.endpoint)
        return
    
    # Check health first
    print("Checking service health...")
    if not check_health(args.endpoint):
        print("Warning: Service may not be available")
    
    print()
    
    # Generate image
    generate_image(
        endpoint_url=args.endpoint,
        prompt=args.prompt,
        width=args.width,
        height=args.height,
        num_steps=args.steps,
        guidance=args.guidance,
        output_file=args.output
    )


if __name__ == "__main__":
    main()
