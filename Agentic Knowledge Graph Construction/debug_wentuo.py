#!/usr/bin/env python3
"""
Debug script for Wentuo API to diagnose empty response issue
"""

import os
import json
import requests
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

API_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.wentuo.ai/v1")
API_KEY = os.getenv("OPENAI_API_KEY", "")

print("🔧 Debugging Wentuo API")
print("=" * 40)
print(f"📡 API Base URL: {API_BASE_URL}")
print(f"🔑 API Key: {API_KEY[:10]}..." if len(API_KEY) > 10 else f"🔑 API Key: {API_KEY}")
print()

def test_direct_request():
    """Test direct HTTP request to Wentuo API"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "gpt-5-mini",
        "messages": [
            {"role": "user", "content": "Hello! Please say 'I am working correctly' in your response."}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    print("📤 Sending request...")
    print(f"URL: {API_BASE_URL}/chat/completions")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print()
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            response_data = response.json()
            print("📥 Full Response:")
            print(json.dumps(response_data, indent=2))
            print()
            
            # Check for content
            if "choices" in response_data and len(response_data["choices"]) > 0:
                choice = response_data["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    content = choice["message"]["content"]
                    print(f"✅ Response Content: '{content}'")
                    
                    if not content or content.strip() == "":
                        print("⚠️  Content is empty or whitespace only!")
                        return False
                    else:
                        print("✅ Content looks good!")
                        return True
                else:
                    print("❌ No message content in response")
                    return False
            else:
                print("❌ No choices in response")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_with_litellm():
    """Test with LiteLLM to see the exact issue"""
    print("\n🔧 Testing with LiteLLM")
    print("-" * 30)
    
    try:
        import litellm
        
        # Set environment variables
        os.environ["OPENAI_API_KEY"] = API_KEY
        os.environ["OPENAI_BASE_URL"] = API_BASE_URL
        
        # Test different model name formats
        model_names = ["gpt-5-mini", "openai/gpt-5-mini"]
        
        for model_name in model_names:
            print(f"Testing model name: {model_name}")
            try:
                response = litellm.completion(
                    model=model_name,
                    messages=[{"role": "user", "content": "Say 'LiteLLM test successful' if you can hear me."}],
                    max_tokens=50,
                    temperature=0.5
                )
                
                content = response.choices[0].message.content
                print(f"✅ LiteLLM Response: '{content}'")
                
                if not content or content.strip() == "":
                    print("⚠️  LiteLLM also getting empty content!")
                else:
                    print("✅ LiteLLM working correctly!")
                return True
                
            except Exception as e:
                print(f"❌ LiteLLM failed with {model_name}: {str(e)[:100]}...")
                continue
        
        print("❌ All LiteLLM attempts failed")
        return False
        
    except ImportError:
        print("❌ LiteLLM not available")
        return False

def main():
    print("🚀 Starting Wentuo API Debug Session")
    print("=" * 50)
    
    # Test direct request first
    direct_success = test_direct_request()
    
    # Test LiteLLM
    litellm_success = test_with_litellm()
    
    print("\n" + "=" * 50)
    print("📋 Debug Summary")
    print("=" * 50)
    
    print(f"Direct API Request: {'✅ PASS' if direct_success else '❌ FAIL'}")
    print(f"LiteLLM Test: {'✅ PASS' if litellm_success else '❌ FAIL'}")
    
    print("\n💡 Recommendations:")
    if not direct_success:
        print("1. ❌ Check your API key and Wentuo account")
        print("2. ❌ Verify the model 'gpt-5-mini' is available")
        print("3. ❌ Check Wentuo API documentation for correct parameters")
    elif not litellm_success:
        print("1. ⚠️  Direct API works but LiteLLM has issues")
        print("2. 💡 Consider using direct HTTP requests instead of LiteLLM")
    else:
        print("🎉 Both methods working - check notebook configuration")

if __name__ == "__main__":
    main()
