#!/usr/bin/env python3
"""
Test different parameters with gpt-5-mini to get non-empty responses
"""

import os
import json
import requests
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

API_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.wentuo.ai/v1")
API_KEY = os.getenv("OPENAI_API_KEY", "")

def test_different_configs():
    """Test different configurations to get response from gpt-5-mini"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Different test configurations
    test_configs = [
        {
            "name": "High max_tokens",
            "payload": {
                "model": "gpt-5-mini",
                "messages": [{"role": "user", "content": "Say hello in one word."}],
                "max_tokens": 500,
                "temperature": 0.7
            }
        },
        {
            "name": "No max_tokens limit",
            "payload": {
                "model": "gpt-5-mini",
                "messages": [{"role": "user", "content": "Say hello."}],
                "temperature": 0.7
            }
        },
        {
            "name": "Simple question",
            "payload": {
                "model": "gpt-5-mini",
                "messages": [{"role": "user", "content": "What is 2+2?"}],
                "max_tokens": 100,
                "temperature": 0.1
            }
        },
        {
            "name": "Different model name",
            "payload": {
                "model": "gpt-5-mini-2025-08-07",
                "messages": [{"role": "user", "content": "Hello!"}],
                "max_tokens": 100,
                "temperature": 0.7
            }
        },
        {
            "name": "System message included",
            "payload": {
                "model": "gpt-5-mini",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant. Always provide clear, direct answers."},
                    {"role": "user", "content": "Say 'I am working' if you understand."}
                ],
                "max_tokens": 50,
                "temperature": 0.5
            }
        }
    ]
    
    print("🧪 Testing different configurations with gpt-5-mini")
    print("=" * 60)
    
    for i, config in enumerate(test_configs, 1):
        print(f"\nTest {i}: {config['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat/completions",
                headers=headers,
                json=config["payload"],
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract response content
                content = ""
                if "choices" in data and len(data["choices"]) > 0:
                    choice = data["choices"][0]
                    if "message" in choice and "content" in choice["message"]:
                        content = choice["message"]["content"]
                
                # Print results
                print(f"Status: ✅ {response.status_code}")
                print(f"Model: {data.get('model', 'unknown')}")
                print(f"Finish reason: {choice.get('finish_reason', 'unknown') if 'choices' in data else 'none'}")
                print(f"Content: '{content}'")
                print(f"Content length: {len(content)}")
                
                # Check token usage
                if "usage" in data:
                    usage = data["usage"]
                    print(f"Tokens - Prompt: {usage.get('prompt_tokens', 0)}, "
                          f"Completion: {usage.get('completion_tokens', 0)}, "
                          f"Total: {usage.get('total_tokens', 0)}")
                    
                    if "completion_tokens_details" in usage:
                        details = usage["completion_tokens_details"]
                        reasoning_tokens = details.get("reasoning_tokens", 0)
                        if reasoning_tokens > 0:
                            print(f"Reasoning tokens: {reasoning_tokens}")
                
                if content.strip():
                    print("🎉 SUCCESS: Got non-empty response!")
                    return True, config["name"], content
                else:
                    print("⚠️  Still empty response")
                    
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return False, None, None

def test_alternative_models():
    """Test if there are other available models"""
    print("\n🔍 Testing alternative models")
    print("=" * 40)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        # List available models
        response = requests.get(f"{API_BASE_URL}/models", headers=headers, timeout=10)
        
        if response.status_code == 200:
            models_data = response.json()
            if "data" in models_data:
                models = [m["id"] for m in models_data["data"]]
                print(f"📋 Available models: {models}")
                
                # Test a few other models
                test_models = [m for m in models if m != "gpt-5-mini"][:3]
                
                for model in test_models:
                    print(f"\n🧪 Testing model: {model}")
                    try:
                        test_payload = {
                            "model": model,
                            "messages": [{"role": "user", "content": "Hello! Say 'working' if you can respond."}],
                            "max_tokens": 50
                        }
                        
                        test_response = requests.post(
                            f"{API_BASE_URL}/chat/completions",
                            headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
                            json=test_payload,
                            timeout=20
                        )
                        
                        if test_response.status_code == 200:
                            test_data = test_response.json()
                            if "choices" in test_data and len(test_data["choices"]) > 0:
                                test_content = test_data["choices"][0]["message"]["content"]
                                print(f"✅ {model}: '{test_content}'")
                                if test_content.strip():
                                    return model, test_content
                            else:
                                print(f"⚠️  {model}: No response")
                        else:
                            print(f"❌ {model}: HTTP {test_response.status_code}")
                            
                    except Exception as e:
                        print(f"❌ {model}: {e}")
            else:
                print("❌ No models data in response")
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")
    
    return None, None

def main():
    print("🚀 Testing gpt-5-mini configurations")
    print("=" * 60)
    
    # Test different configurations
    success, working_config, response_content = test_different_configs()
    
    if not success:
        print("\n🔄 gpt-5-mini not giving responses, trying alternative models...")
        working_model, model_response = test_alternative_models()
        
        if working_model:
            print(f"\n🎉 Working alternative: {working_model}")
            print(f"Response: '{model_response}'")
        else:
            print("\n❌ No working models found")
    else:
        print(f"\n🎉 Working configuration: {working_config}")
        print(f"Response: '{response_content}'")
    
    print("\n" + "=" * 60)
    print("📝 Summary and Recommendations")
    print("=" * 60)
    
    if success:
        print("✅ Found working configuration for gpt-5-mini")
        print(f"💡 Use configuration: {working_config}")
    else:
        print("⚠️  gpt-5-mini consistently returns empty responses")
        print("💡 This might be because gpt-5-mini is a reasoning model like o1")
        print("💡 The model might be designed to show only final answers, not reasoning")
        print("💡 Try using a different model from the available list")
        print("💡 Or check Wentuo documentation for special handling of gpt-5-mini")

if __name__ == "__main__":
    main()
