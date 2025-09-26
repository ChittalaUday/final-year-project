#!/usr/bin/env python3
"""
CLIP API Test Client
Tests the Node.js server's CLIP image comparison endpoint
"""

import requests
import argparse
import sys
import os

API_BASE_URL = "http://localhost:5003/api/clip"

def test_api_info():
    """Test the API info endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/info")
        if response.status_code == 200:
            data = response.json()
            print("✅ API Info Retrieved Successfully:")
            if data.get('body'):
                info = data['body']
                print(f"   Description: {info.get('description', 'N/A')}")
                print(f"   Supported Formats: {', '.join(info.get('supported_formats', []))}")
                print(f"   Max File Size: {info.get('max_file_size', 'N/A')}")
                print(f"   Endpoints: {len(info.get('endpoints', {}))} available")
        else:
            print(f"❌ API Info Error: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ API Info Error: {e}")

def test_image_comparison(image1_path, image2_path, tag=None):
    """Test the image comparison endpoint"""
    
    # Check if files exist
    if not os.path.exists(image1_path):
        print(f"❌ Comparison Error: Image 1 not found: {image1_path}")
        return
    
    if not os.path.exists(image2_path):
        print(f"❌ Comparison Error: Image 2 not found: {image2_path}")
        return
    
    try:
        print("🔍 Comparing Images...")
        
        # Prepare data
        data = {}
        if tag:
            data['tag'] = tag
        
        # Prepare files
        with open(image1_path, 'rb') as f1, open(image2_path, 'rb') as f2:
            files = {
                'image1': (os.path.basename(image1_path), f1, 'image/png'),
                'image2': (os.path.basename(image2_path), f2, 'image/png')
            }
            
            # Make request
            response = requests.post(f"{API_BASE_URL}/compare", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Image Comparison Successful!")
            
            if result.get('body'):
                body = result['body']
                
                # Display similarity scores
                if 'image_similarity' in body:
                    print(f"   📊 Image Similarity: {body['image_similarity']:.4f}")
                
                if 'text_similarity' in body:
                    print(f"   📝 Text Similarity: {body['text_similarity']:.4f}")
                
                # Display decision
                if 'decision' in body:
                    print(f"   🎯 Decision: {body['decision']}")
                
                # Display raw output
                if 'raw_output' in body:
                    print("   📋 Raw Output:")
                    for line in body['raw_output'].split('\\n'):
                        if line.strip():
                            print(f"      {line.strip()}")
        else:
            print(f"❌ Comparison Error: HTTP {response.status_code}")
            error_response = response.json()
            print(f"   Message: {error_response.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Comparison Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="🚀 CLIP API Test Client")
    parser.add_argument("--info", action="store_true", help="Get API information")
    parser.add_argument("--image1", help="Path to first image")
    parser.add_argument("--image2", help="Path to second image") 
    parser.add_argument("--tag", help="Optional text tag for comparison")
    
    args = parser.parse_args()
    
    print("🚀 CLIP API Test Client")
    print(f"🌐 API URL: {API_BASE_URL}")
    
    if args.info:
        print("📋 Testing API Info...")
        test_api_info()
    elif args.image1 and args.image2:
        test_image_comparison(args.image1, args.image2, args.tag)
    else:
        print("❌ Please specify --info or provide --image1 and --image2")
        parser.print_help()

if __name__ == "__main__":
    main()