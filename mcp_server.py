"""
GoodPage MCP Server
Model Context Protocol server for GoodPage API
Transform text into beautiful web pages with AI-powered styling
"""

from mcp.server.fastmcp import FastMCP
import requests
import json
from typing import Optional

# Create MCP server
mcp = FastMCP("GoodPage API")

# API Configuration
import os
TEST_MODE = os.environ.get('GOODPAGE_TEST_MODE', 'false').lower() == 'true'

if TEST_MODE:
    # Use local server for testing
    API_ENDPOINTS = {
        "global": "http://localhost:8009/api/text-to-page",
        "china": "http://localhost:8009/api/text-to-page"
    }
    print("⚠️  Running in TEST MODE - using local server")
else:
    # Use production servers
    API_ENDPOINTS = {
        "global": "https://goodpage.net/api/text-to-page",
        "china": "https://p.isheet.net/api/text-to-page"
    }


@mcp.tool()
def text_to_page(
    content: str,
    title: Optional[str] = None,
    style: Optional[str] = None,
    content_strategy: str = "strict",
    extra_requirements: str = "",
    response_type: str = "url",
    region: str = "global"
) -> dict:
    """
    Convert plain text to a beautiful web page using GoodPage API.
    
    This tool transforms your text content into professionally designed HTML web pages
    with one API call. Perfect for creating blog posts, documentation, reports, 
    presentations, and any text content that needs visual enhancement.
    
    Args:
        content: The text content to convert (required). Can be plain text or markdown.
                Maximum ~10,000 characters recommended for optimal performance.
        
        title: Article title (optional). If not provided, AI will automatically generate
              a title based on the content. Recommended for better SEO.
        
        style: Template style code (optional). Choose from 17+ professional templates.
              If not specified, AI will select the most appropriate style automatically.
              Common styles: 'minimalist', 'cyberpunk_neon', 'magazine_gradient', 
              'swiss_grid', 'neon_glassmorphism'. Use get_available_templates() to see all.
        
        content_strategy: Content expansion strategy (default: 'strict').
            - 'strict': Follow original content closely, minimal changes
            - 'interpret': Optimize structure and expression while preserving meaning
            - 'expand': Enrich content with additional context and details
        
        extra_requirements: Natural language styling requirements (optional).
            Examples: "Use blue theme", "Add tables for data", "Make it look modern",
                     "Add icons and visual elements"
        
        response_type: Return format (default: 'url').
            - 'url': Return permanent webpage link (recommended for sharing)
            - 'html': Return complete HTML code (for embedding or offline use)
        
        region: API region endpoint (default: 'global').
            - 'global': Use https://goodpage.net (recommended for international users)
            - 'china': Use https://p.isheet.net (optimized for users in China)
    
    Returns:
        Dictionary containing:
            - success: Boolean indicating if the request succeeded
            - data: Full API response including URL/HTML, article_id, etc.
            - message: Human-readable status message
            - access_url: Direct link to the generated page (if response_type='url')
            - article_id: Unique identifier for the generated article
            - quota: Remaining API quota information
    
    Example:
        # Simple usage
        text_to_page(content="AI is transforming how we work and live.")
        
        # Advanced usage with custom styling
        text_to_page(
            content="# Q3 Financial Report\\n\\nRevenue increased by 25%...",
            title="Q3 2026 Financial Report",
            style="swiss_grid",
            content_strategy="strict",
            extra_requirements="Use professional blue theme with data tables",
            response_type="url",
            region="global"
        )
    
    Note:
        - Free tier includes 50 API calls per IP address per 30 days
        - Typical response time: 3-10 seconds depending on content length
        - All generated pages have inline CSS, no external dependencies
    """
    
    # Select API endpoint based on region
    api_url = API_ENDPOINTS.get(region, API_ENDPOINTS["global"])
    
    # Build request payload
    payload = {
        "content": content,
        "response_type": response_type,
        "content_strategy": content_strategy
    }
    
    if title:
        payload["title"] = title
    
    if style:
        payload["style"] = style
    
    if extra_requirements:
        payload["extra_requirements"] = extra_requirements
    
    try:
        # Make API request
        response = requests.post(
            api_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        result = response.json()
        
        if result.get("status") == "success":
            access_url = result.get("full_url", result.get("url"))
            article_id = result.get("article_id", "")
            
            return {
                "success": True,
                "data": result,
                "message": f"✅ Web page generated successfully!",
                "access_url": access_url,
                "article_id": article_id,
                "quota": result.get("quota", {}),
                "usage_tip": "You can share this URL directly or embed the HTML in your application."
            }
        else:
            error_msg = result.get("message", "Unknown error occurred")
            return {
                "success": False,
                "error": error_msg,
                "message": f"❌ Failed to generate web page: {error_msg}",
                "suggestion": "Check your content length (< 10,000 chars) and try again."
            }
    
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timeout",
            "message": "⏱️ API request timed out (60s limit). Please try again with shorter content.",
            "suggestion": "Try splitting long content into smaller chunks."
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Connection error",
            "message": "🌐 Cannot connect to GoodPage API. Check your internet connection.",
            "suggestion": f"Verify the endpoint is accessible: {api_url}"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"🔌 Network error: {str(e)}",
            "suggestion": "Check network connectivity and API endpoint availability."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"⚠️ An unexpected error occurred: {str(e)}",
            "suggestion": "Please try again or contact support at chenkunji@qq.com"
        }


@mcp.tool()
def get_available_templates() -> dict:
    """
    Get list of all available style templates for GoodPage API.
    
    Returns detailed information about each template including:
    - Template code (used in 'style' parameter)
    - Style name and description
    - Best use cases
    - Visual characteristics
    
    Returns:
        Dictionary containing all template information organized by category.
    
    Example:
        templates = get_available_templates()
        # Then use a template code like 'minimalist' in text_to_page()
    """
    
    templates = {
        "professional": {
            "minimalist": {
                "name": "Minimalist",
                "chinese_name": "极简主义",
                "description": "Clean, simple design with focus on readability",
                "best_for": ["Technical documentation", "Reports", "Academic papers", "Professional blogs"],
                "characteristics": ["White space", "Simple typography", "No distractions"]
            },
            "premium_bw": {
                "name": "Premium Black & White",
                "chinese_name": "高级黑白",
                "description": "Elegant black, white & gray palette showcasing typographic beauty",
                "best_for": ["Text-heavy content", "Literary works", "Formal documents"],
                "characteristics": ["Monochrome", "High contrast", "Sophisticated"]
            },
            "swiss_grid": {
                "name": "Swiss Grid",
                "chinese_name": "瑞士网格",
                "description": "Rigorous grid system inspired by Swiss design principles",
                "best_for": ["Data analysis", "Research papers", "Structured content"],
                "characteristics": ["Grid layout", "Systematic", "Precise"]
            },
            "newspaper_classic": {
                "name": "Newspaper Classic",
                "chinese_name": "报纸经典",
                "description": "Traditional newspaper aesthetic with serif fonts",
                "best_for": ["News articles", "Announcements", "Editorial content"],
                "characteristics": ["Serif fonts", "Column layout", "Classic feel"]
            }
        },
        "modern_tech": {
            "neon_glassmorphism": {
                "name": "Neon Glass",
                "chinese_name": "霓虹玻璃",
                "description": "Futuristic glass morphism with neon accents",
                "best_for": ["AI topics", "Technology", "Innovation", "Startups"],
                "characteristics": ["Glass effect", "Neon glow", "Modern"]
            },
            "cyberpunk_neon": {
                "name": "Cyberpunk Neon",
                "chinese_name": "赛博朋克",
                "description": "Dark cyberpunk aesthetic with vibrant neon colors",
                "best_for": ["Cybersecurity", "Gaming", "Tech culture", "Edgy content"],
                "characteristics": ["Dark theme", "Neon colors", "Futuristic"]
            },
            "gradient_glass": {
                "name": "Gradient Glass",
                "chinese_name": "渐变玻璃",
                "description": "Soft gradients with glass morphism effects",
                "best_for": ["Business", "Corporate", "Professional services"],
                "characteristics": ["Soft gradients", "Transparency", "Elegant"]
            },
            "geometric_modern": {
                "name": "Geometric Modern",
                "chinese_name": "几何现代",
                "description": "Bold geometric shapes with modern aesthetics",
                "best_for": ["Architecture", "Design portfolios", "Creative work"],
                "characteristics": ["Geometric patterns", "Bold shapes", "Contemporary"]
            }
        },
        "creative_artistic": {
            "magazine_gradient": {
                "name": "Magazine Gradient",
                "chinese_name": "杂志渐变",
                "description": "Warm gradient backgrounds inspired by modern magazines",
                "best_for": ["Lifestyle", "Fashion", "Travel", "Personal blogs"],
                "characteristics": ["Warm colors", "Magazine style", "Inviting"]
            },
            "bold_waves": {
                "name": "Bold Waves",
                "chinese_name": "大胆波浪",
                "description": "Dynamic wave patterns with bold color choices",
                "best_for": ["Sports", "Youth culture", "Energetic content"],
                "characteristics": ["Wave patterns", "Vibrant", "Dynamic"]
            },
            "handdrawn_notes": {
                "name": "Handdrawn Notes",
                "chinese_name": "手绘笔记",
                "description": "Casual hand-drawn aesthetic perfect for notes",
                "best_for": ["Study notes", "Brainstorming", "Creative ideas", "Tutorials"],
                "characteristics": ["Hand-drawn", "Casual", "Approachable"]
            },
            "brutalist_bold": {
                "name": "Brutalist Bold",
                "chinese_name": "粗野主义",
                "description": "Raw brutalist design with strong personality",
                "best_for": ["Art", "Design expression", "Avant-garde content"],
                "characteristics": ["Raw", "Bold typography", "Unconventional"]
            }
        },
        "specialized_themes": {
            "space_cosmic": {
                "name": "Space Cosmic",
                "chinese_name": "太空宇宙",
                "description": "Deep space theme with cosmic elements",
                "best_for": ["Astronomy", "Space exploration", "Sci-fi", "Science"],
                "characteristics": ["Dark space", "Stars", "Cosmic"]
            },
            "dark_luxury": {
                "name": "Dark Luxury",
                "chinese_name": "暗黑奢华",
                "description": "Sophisticated dark theme with luxury touches",
                "best_for": ["Luxury brands", "Premium products", "High-end services"],
                "characteristics": ["Dark background", "Gold accents", "Premium feel"]
            },
            "pastel_soft": {
                "name": "Pastel Soft",
                "chinese_name": "柔和粉彩",
                "description": "Gentle pastel colors creating a soft atmosphere",
                "best_for": ["Lifestyle", "Wellness", "Children", "Female audience"],
                "characteristics": ["Pastel colors", "Soft", "Gentle"]
            },
            "kawaii_bubbles": {
                "name": "Kawaii Bubbles",
                "chinese_name": "可爱泡泡",
                "description": "Cute Japanese kawaii style with bubble elements",
                "best_for": ["Pets", "Anime", "Entertainment", "Fun content"],
                "characteristics": ["Cute", "Bubbles", "Playful"]
            },
            "minimalist_timeline": {
                "name": "Minimalist Timeline",
                "chinese_name": "时间线",
                "description": "Clean timeline layout for chronological content",
                "best_for": ["History", "Project timelines", "Development process"],
                "characteristics": ["Timeline", "Chronological", "Clear flow"]
            }
        }
    }
    
    # Flatten for easier reference
    all_templates = {}
    for category, items in templates.items():
        for code, info in items.items():
            all_templates[code] = info
    
    return {
        "success": True,
        "templates_by_category": templates,
        "all_templates": all_templates,
        "total_count": len(all_templates),
        "usage_tip": "Pass any template code (e.g., 'minimalist', 'cyberpunk_neon') to the 'style' parameter in text_to_page()"
    }


@mcp.resource("goodpage://quota-info")
def get_quota_info() -> str:
    """
    Get information about GoodPage API quota and usage limits.
    
    This resource provides details about the free tier limitations,
    rate limits, and how to upgrade if needed.
    """
    
    info = """
# GoodPage API Quota Information

## Free Tier Limits
- **Quota:** 50 API calls per IP address
- **Validity Period:** 30 days (automatically resets)
- **Rate Limiting:** No specific rate limit, but please use responsibly

## What Happens When Quota Exceeded?
- API returns HTTP 429 (Too Many Requests)
- Response includes remaining quota information
- Contact support to discuss upgrade options

## Content Guidelines
- **Maximum Length:** ~10,000 characters per request
- **Recommended:** Keep under 5,000 chars for best performance
- **Long Content:** Split into multiple requests if needed

## Performance Expectations
- **Typical Response Time:** 3-10 seconds
- **Factors Affecting Speed:**
  - Content length
  - Complexity of styling requests
  - Server load
  - Network conditions

## Supported Languages
- Chinese (中文) - Fully optimized
- English - Fully optimized
- Other major languages - Auto-detected and supported

## API Endpoints
- **Global:** https://goodpage.net/api/text-to-page
  - Recommended for users outside China
  - Better international connectivity
  
- **China:** https://p.isheet.net/api/text-to-page
  - Optimized for users in mainland China
  - Faster response times in China

## Best Practices
1. Cache results when possible (URLs are permanent)
2. Use appropriate content_strategy for your needs
3. Provide clear extra_requirements for better results
4. Monitor your quota usage in responses

## Support & Upgrades
- **Email:** chenkunji@qq.com
- **Website:** https://goodpage.net (Global) | https://p.isheet.net (China)
- **Documentation:** https://goodpage.net/api-docs-en

## Enterprise Options
For high-volume usage, contact us for:
- Higher quotas
- Custom SLAs
- Priority support
- Dedicated instances
    """
    
    return info


@mcp.prompt()
def goodpage_best_practices() -> str:
    """
    Best practices guide for using GoodPage API effectively.
    
    This prompt provides tips and recommendations for getting
    the best results from the GoodPage API.
    """
    
    return """
# GoodPage API Best Practices

## 1. Choosing the Right Template

Match the template to your content type:

**For Technical Content:**
- `minimalist` - Clean, distraction-free
- `swiss_grid` - Structured, data-friendly
- `premium_bw` - Professional, elegant

**For Creative Content:**
- `magazine_gradient` - Warm, engaging
- `neon_glassmorphism` - Modern, tech-forward
- `handdrawn_notes` - Casual, approachable

**For Business Content:**
- `gradient_glass` - Professional, modern
- `dark_luxury` - Premium, sophisticated
- `newspaper_classic` - Formal, authoritative

## 2. Writing Effective Extra Requirements

Be specific and natural:

✅ **Good Examples:**
- "Use a blue color scheme with data tables"
- "Add icons for each section"
- "Make it look modern and professional"
- "Include a summary box at the top"

❌ **Avoid:**
- Vague: "Make it nice"
- Too technical: "Set font-size to 16px"
- Conflicting: "Make it colorful but minimalist"

## 3. Content Strategy Selection

**Use 'strict' when:**
- Content is already well-written
- You need exact fidelity
- Legal or technical accuracy is critical

**Use 'interpret' when:**
- Content needs better organization
- You want improved flow
- Some restructuring is acceptable

**Use 'expand' when:**
- Content is brief and needs elaboration
- You want additional context
- More detail would be helpful

## 4. Title Optimization

**Provide a title when:**
- SEO is important
- You have a specific title in mind
- Content doesn't have a clear headline

**Let AI generate when:**
- You're unsure what title to use
- Quick prototyping
- Content has obvious main topic

## 5. Response Type Selection

**Use 'url' (recommended):**
- For sharing links
- Permanent hosting
- Easy access
- Automatic updates

**Use 'html':**
- For embedding in your app
- Offline use
- Custom hosting
- Further modification

## 6. Error Handling

Common issues and solutions:

**429 Too Many Requests:**
- You've exceeded the 50-call quota
- Wait for reset or contact support

**Timeout Errors:**
- Content too long (>10,000 chars)
- Split into smaller chunks
- Try again

**Poor Quality Output:**
- Add more specific extra_requirements
- Try a different template
- Use 'interpret' or 'expand' strategy

## 7. Performance Tips

1. **Cache URLs** - Generated pages are permanent
2. **Batch similar requests** - Group related content
3. **Monitor quota** - Check remaining calls in response
4. **Use regional endpoints** - Choose closest server

## 8. Example Workflows

**Quick Blog Post:**
```python
text_to_page(
    content=my_blog_post,
    style="magazine_gradient",
    response_type="url"
)
```

**Technical Documentation:**
```python
text_to_page(
    content=tech_docs,
    style="minimalist",
    content_strategy="strict",
    extra_requirements="Add code blocks and syntax highlighting",
    response_type="url"
)
```

**Business Report:**
```python
text_to_page(
    content=quarterly_report,
    title="Q3 2026 Business Report",
    style="swiss_grid",
    extra_requirements="Include executive summary and data tables",
    response_type="url"
)
```

## 9. Regional Considerations

**For Global Audience:**
- Use `region="global"`
- Endpoint: goodpage.net
- Better international CDN

**For China Audience:**
- Use `region="china"`
- Endpoint: p.isheet.net
- Faster in mainland China

## 10. Getting Help

If you encounter issues:
1. Check quota status with get_quota_info()
2. Review template options with get_available_templates()
3. Simplify your request and test incrementally
4. Contact support: chenkunji@qq.com

Remember: The API is designed to be flexible and forgiving. Don't hesitate to experiment with different combinations!
    """


if __name__ == "__main__":
    # Run the MCP server
    print("🚀 Starting GoodPage MCP Server...")
    print("📝 Available tools:")
    print("   - text_to_page: Convert text to web page")
    print("   - get_available_templates: List all style templates")
    print("📚 Available resources:")
    print("   - goodpage://quota-info: API quota information")
    print("💡 Available prompts:")
    print("   - goodpage_best_practices: Usage best practices")
    print("\n✨ Server ready! Connect with your MCP client.")
    
    mcp.run()
