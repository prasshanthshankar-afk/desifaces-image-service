#!/usr/bin/env python3
"""
Test script for Desifaces Image Service
Validates both HTTP server and RunPod handler functionality
"""

import json
import time
import requests
import subprocess
import sys
from handler import handler


def test_handler():
    """Test the RunPod handler"""
    print("Testing RunPod handler...")
    
    result = handler({
        'input': {
            'prompt': 'Test image',
            'width': 128,
            'height': 128
        }
    })
    
    assert 'image' in result, "Handler should return image"
    assert result['prompt'] == 'Test image', "Handler should return prompt"
    assert result['width'] == 128, "Handler should return width"
    assert result['height'] == 128, "Handler should return height"
    
    print("✓ RunPod handler test passed")


def test_http_server():
    """Test the HTTP server endpoints"""
    print("\nTesting HTTP server...")
    
    # Start the server
    process = subprocess.Popen(
        ['python3', 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test health endpoint
        response = requests.get('http://localhost:8000/health')
        assert response.status_code == 200, "Health endpoint should return 200"
        assert response.json()['status'] == 'healthy', "Health endpoint should return healthy status"
        print("✓ Health endpoint test passed")
        
        # Test root endpoint
        response = requests.get('http://localhost:8000/')
        assert response.status_code == 200, "Root endpoint should return 200"
        assert response.json()['service'] == 'Desifaces Image Service', "Root should return service name"
        print("✓ Root endpoint test passed")
        
        # Test generate endpoint
        response = requests.post(
            'http://localhost:8000/generate',
            json={
                'prompt': 'Test image',
                'width': 128,
                'height': 128
            }
        )
        assert response.status_code == 200, "Generate endpoint should return 200"
        data = response.json()
        assert 'image' in data, "Generate should return image"
        assert data['prompt'] == 'Test image', "Generate should return prompt"
        print("✓ Generate endpoint test passed")
        
    finally:
        # Stop the server
        process.terminate()
        process.wait(timeout=5)
    
    print("\n✓ All HTTP server tests passed")


if __name__ == "__main__":
    try:
        test_handler()
        test_http_server()
        print("\n" + "="*50)
        print("All tests passed successfully! ✓")
        print("="*50)
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
