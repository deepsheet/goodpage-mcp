"""
Test script for GoodPage MCP Server
Tests the core functionality without requiring an MCP client
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from mcp_server import text_to_page, get_available_templates, get_quota_info
import requests
import json


def test_get_available_templates():
    """Test getting available templates"""
    print("=" * 80)
    print("TEST 1: Get Available Templates")
    print("=" * 80)
    
    result = get_available_templates()
    
    print(f"\n✅ Success: {result['success']}")
    print(f"📊 Total templates: {result['total_count']}")
    print(f"\n📂 Categories:")
    for category in result['templates_by_category'].keys():
        templates = result['templates_by_category'][category]
        print(f"   - {category}: {len(templates)} templates")
    
    print(f"\n✨ Sample templates:")
    for code, info in list(result['all_templates'].items())[:5]:
        print(f"   - {code}: {info['name']}")
    
    print("\n" + "=" * 80)
    return result['success']


def test_get_quota_info():
    """Test getting quota information"""
    print("\n" + "=" * 80)
    print("TEST 2: Get Quota Information")
    print("=" * 80)
    
    result = get_quota_info()
    
    print("\n📋 Quota Info Preview (first 500 chars):")
    print(result[:500])
    print("...")
    
    # Check if key information is present
    checks = [
        ("Free tier mentioned", "50 API calls" in result),
        ("Validity period", "30 days" in result),
        ("Global endpoint", "goodpage.net" in result),
        ("China endpoint", "p.isheet.net" in result),
        ("Support email", "chenkunji@qq.com" in result)
    ]
    
    print("\n✅ Validation:")
    all_passed = True
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"   {status} {check_name}")
        all_passed = all_passed and passed
    
    print("\n" + "=" * 80)
    return all_passed


def test_text_to_page_basic():
    """Test basic text to page conversion"""
    print("\n" + "=" * 80)
    print("TEST 3: Text to Page - Basic Test")
    print("=" * 80)
    
    test_content = """
    Artificial Intelligence in 2026
    
    AI technology has made remarkable progress. From language models to computer vision, 
    AI is transforming industries worldwide. Machine learning algorithms are now more 
    efficient and accessible than ever before.
    
    Key developments include:
    - Improved natural language understanding
    - Better image generation capabilities
    - Enhanced reasoning abilities
    - More efficient training methods
    """
    
    print(f"\n📝 Test content length: {len(test_content)} characters")
    print("🎯 Testing with default parameters...")
    
    try:
        result = text_to_page(
            content=test_content,
            title="AI in 2026",
            response_type="url",
            region="global"
        )
        
        print(f"\n✅ Request successful: {result['success']}")
        print(f"💬 Message: {result['message']}")
        
        if result['success']:
            print(f"\n🔗 Access URL: {result.get('access_url', 'N/A')}")
            print(f"🆔 Article ID: {result.get('article_id', 'N/A')}")
            
            if 'quota' in result:
                quota = result['quota']
                print(f"\n📊 Quota Status:")
                print(f"   - Remaining: {quota.get('remaining', 'N/A')}")
                print(f"   - Used: {quota.get('used', 'N/A')}")
                print(f"   - Limit: {quota.get('limit', 'N/A')}")
            
            print(f"\n💡 Usage Tip: {result.get('usage_tip', 'N/A')}")
        else:
            print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
            print(f"💡 Suggestion: {result.get('suggestion', 'N/A')}")
        
        print("\n" + "=" * 80)
        return result['success']
        
    except Exception as e:
        print(f"\n❌ Exception occurred: {str(e)}")
        print("\n" + "=" * 80)
        return False


def test_text_to_page_with_style():
    """Test text to page with specific style"""
    print("\n" + "=" * 80)
    print("TEST 4: Text to Page - With Custom Style")
    print("=" * 80)
    
    test_content = """
    Quantum Computing Breakthrough
    
    Scientists have achieved a major milestone in quantum computing. 
    The new quantum processor demonstrates unprecedented stability 
    and computational power.
    """
    
    print(f"\n📝 Testing with cyberpunk_neon style...")
    
    try:
        result = text_to_page(
            content=test_content,
            title="Quantum Computing Breakthrough",
            style="cyberpunk_neon",
            extra_requirements="Use futuristic design with neon accents",
            response_type="url",
            region="global"
        )
        
        print(f"\n✅ Request successful: {result['success']}")
        
        if result['success']:
            print(f"🔗 Access URL: {result.get('access_url', 'N/A')}")
            print(f"🎨 Style: cyberpunk_neon")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 80)
        return result['success']
        
    except Exception as e:
        print(f"\n❌ Exception occurred: {str(e)}")
        print("\n" + "=" * 80)
        return False


def test_text_to_page_china_region():
    """Test text to page with China region"""
    print("\n" + "=" * 80)
    print("TEST 5: Text to Page - China Region")
    print("=" * 80)
    
    test_content = """
    人工智能发展趋势
    
    2026年，人工智能技术继续快速发展。从自然语言处理到计算机视觉，
    AI正在改变各个行业。机器学习算法变得更加高效和易于使用。
    """
    
    print(f"\n📝 Testing with Chinese content and China region...")
    
    try:
        result = text_to_page(
            content=test_content,
            title="人工智能发展趋势",
            response_type="url",
            region="china"
        )
        
        print(f"\n✅ Request successful: {result['success']}")
        
        if result['success']:
            print(f"🔗 Access URL: {result.get('access_url', 'N/A')}")
            print(f"🌏 Region: china (p.isheet.net)")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 80)
        return result['success']
        
    except Exception as e:
        print(f"\n❌ Exception occurred: {str(e)}")
        print("\n" + "=" * 80)
        return False


def test_text_to_page_html_response():
    """Test text to page with HTML response type"""
    print("\n" + "=" * 80)
    print("TEST 6: Text to Page - HTML Response")
    print("=" * 80)
    
    test_content = "This is a test for HTML response type."
    
    print(f"\n📝 Testing with response_type='html'...")
    
    try:
        result = text_to_page(
            content=test_content,
            response_type="html",
            region="global"
        )
        
        print(f"\n✅ Request successful: {result['success']}")
        
        if result['success']:
            html_data = result.get('data', {})
            html_content = html_data.get('html', '')
            print(f"📄 HTML length: {len(html_content)} characters")
            print(f"📄 HTML preview (first 200 chars):\n{html_content[:200]}...")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 80)
        return result['success']
        
    except Exception as e:
        print(f"\n❌ Exception occurred: {str(e)}")
        print("\n" + "=" * 80)
        return False


def main():
    """Run all tests"""
    print("\n" + "🧪" * 40)
    print("GoodPage MCP Server - Test Suite")
    print("🧪" * 40 + "\n")
    
    results = {}
    
    # Run tests
    results['get_available_templates'] = test_get_available_templates()
    results['get_quota_info'] = test_get_quota_info()
    results['text_to_page_basic'] = test_text_to_page_basic()
    results['text_to_page_with_style'] = test_text_to_page_with_style()
    results['text_to_page_china_region'] = test_text_to_page_china_region()
    results['text_to_page_html_response'] = test_text_to_page_html_response()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    failed_tests = total_tests - passed_tests
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "-" * 80)
    print(f"Total: {total_tests} | Passed: {passed_tests} | Failed: {failed_tests}")
    print("=" * 80)
    
    if failed_tests == 0:
        print("\n🎉 All tests passed! MCP Server is ready for deployment.")
    else:
        print(f"\n⚠️  {failed_tests} test(s) failed. Please review the errors above.")
    
    return failed_tests == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
