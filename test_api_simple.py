#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple test to verify GoodPage API is working
"""

import requests
import json

def test_api():
    """Test the text-to-page API endpoint"""
    
    print("=" * 80)
    print("Testing GoodPage API - /api/text-to-page")
    print("=" * 80)
    
    url = "http://localhost:8009/api/text-to-page"
    
    payload = {
        "content": "This is a test of the MCP Server integration with GoodPage API.",
        "title": "MCP Server Test",
        "response_type": "url"
    }
    
    print(f"\n📤 Sending request to: {url}")
    print(f"📝 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"\n📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Success!")
            print(f"\nResponse Data:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if data.get('status') == 'success':
                print(f"\n🎉 API is working correctly!")
                print(f"🔗 Generated URL: {data.get('full_url', 'N/A')}")
                print(f"🆔 Article ID: {data.get('article_id', 'N/A')}")
                return True
            else:
                print(f"\n❌ API returned error status: {data.get('message', 'Unknown error')}")
                return False
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error: Cannot connect to localhost:8009")
        print("💡 Make sure the Flask server is running: python app.py")
        return False
    except requests.exceptions.Timeout:
        print("\n❌ Request Timeout")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_api()
    exit(0 if success else 1)
