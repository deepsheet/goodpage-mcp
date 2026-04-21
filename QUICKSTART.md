# GoodPage MCP Server - Quick Start Guide

## 🚀 5-Minute Setup

### 1. Install Dependencies

```bash
cd mcp-server
pip install -r requirements.txt
```

### 2. Test Locally (Optional but Recommended)

Start your Flask server first:
```bash
cd ..
python app.py
```

Then test the MCP Server:
```bash
cd mcp-server
GOODPAGE_TEST_MODE=true python test_mcp_server.py
```

Expected output:
```
🎉 All tests passed! MCP Server is ready for deployment.
```

### 3. Configure with Your MCP Client

#### For Claude Desktop

Edit `claude_desktop_config.json`:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "goodpage": {
      "command": "python",
      "args": ["/absolute/path/to/goodpage/mcp-server/mcp_server.py"]
    }
  }
}
```

**Important:** Use the **absolute path** to `mcp_server.py`.

#### For Cursor

Add to Cursor's MCP settings:

```json
{
  "mcpServers": {
    "goodpage": {
      "command": "python",
      "args": ["YOUR_ABSOLUTE_PATH/goodpage/mcp-server/mcp_server.py"]
    }
  }
}
```

### 4. Restart Your MCP Client

- **Claude Desktop:** Quit and reopen
- **Cursor:** Reload window (Cmd+Shift+P → "Reload Window")

### 5. Verify Installation

Ask your AI assistant:

> "What templates are available in GoodPage?"

or

> "Create a webpage from this text: AI is transforming the world"

If it responds with template information or generates a page, success! 🎉

---

## 🧪 Testing

### Run Full Test Suite

```bash
GOODPAGE_TEST_MODE=true python test_mcp_server.py
```

This tests:
- ✅ Template listing
- ✅ Quota information
- ✅ Text to URL conversion
- ✅ Custom styling
- ✅ Regional endpoints
- ✅ HTML response format

### Test Individual Features

```python
from mcp_server import text_to_page, get_available_templates

# Get templates
templates = get_available_templates()
print(f"Available: {templates['total_count']} templates")

# Create a page
result = text_to_page(
    content="Hello World!",
    title="My First Page",
    style="minimalist"
)
print(f"URL: {result['access_url']}")
```

---

## 🔧 Troubleshooting

### Issue: "Cannot connect to GoodPage API"

**Solution:** Make sure your Flask server is running:
```bash
python app.py
```

### Issue: "Module not found: mcp"

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Tools not showing up in Claude/Cursor

**Solutions:**
1. Check the absolute path in config is correct
2. Restart the MCP client completely
3. Check logs for errors:
   ```bash
   # Claude Desktop logs
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```

### Issue: 404 Not Found

**Solution:** The `/api/text-to-page` endpoint might not be registered. Restart your Flask server:
```bash
# Stop old server
lsof -ti:8009 | xargs kill -9

# Start new server
python app.py
```

---

## 📊 Usage Examples

### Example 1: Simple Blog Post

```
Create a beautiful webpage about machine learning trends in 2026. 
Use a modern tech style and give me a shareable URL.
```

### Example 2: Technical Documentation

```
Convert this technical documentation to a webpage using the swiss_grid template.
Make sure to preserve all code blocks and add syntax highlighting.
```

### Example 3: Business Report

```
I have a quarterly report. Format it professionally with data tables.
Use a business-appropriate style and return the HTML code so I can embed it.
```

### Example 4: Chinese Content

```
将这段中文文本转换成网页，使用杂志渐变风格：

人工智能正在改变我们的生活方式...
```

---

## 🌍 Production Deployment

When deploying to production (not using localhost):

1. **Remove test mode:**
   ```python
   # In mcp_server.py, set TEST_MODE = False or remove env var
   TEST_MODE = False
   ```

2. **Update API endpoints if needed:**
   ```python
   API_ENDPOINTS = {
       "global": "https://goodpage.net/api/text-to-page",
       "china": "https://p.isheet.net/api/text-to-page"
   }
   ```

3. **Deploy to a server with public access**

4. **Update MCP client config** to point to the deployed server

---

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore all 17+ templates with `get_available_templates()`
- Check quota limits with the `goodpage://quota-info` resource
- Learn best practices with the `goodpage_best_practices` prompt

---

## 🆘 Need Help?

- **Email:** chenkunji@qq.com
- **Website:** https://goodpage.net
- **Issues:** GitHub Issues

Happy creating! 🎨✨
