# GoodPage MCP Server

[![MCP](https://img.shields.io/badge/MCP-Server-blue)](https://modelcontextprotocol.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Transform plain text into beautifully designed web pages using the GoodPage API through Model Context Protocol (MCP).

## 🌟 Features

- **17+ Professional Templates**: From minimalist to cyberpunk, choose the perfect style
- **AI-Powered Styling**: Automatic template selection and content optimization
- **Multi-Region Support**: Global and China endpoints for optimal performance
- **Flexible Output**: Get permanent URLs or raw HTML code
- **Quota Management**: 50 free API calls per IP per 30 days
- **Easy Integration**: Works with Claude Desktop, Cursor, and other MCP clients

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
cd mcp-server
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Test the Server Locally

```bash
python mcp_server.py
```

You should see:
```
🚀 Starting GoodPage MCP Server...
📝 Available tools:
   - text_to_page: Convert text to web page
   - get_available_templates: List all style templates
📚 Available resources:
   - goodpage://quota-info: API quota information
💡 Available prompts:
   - goodpage_best_practices: Usage best practices

✨ Server ready! Connect with your MCP client.
```

### 2. Configure with Claude Desktop

Add to your Claude Desktop configuration file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "goodpage": {
      "command": "python",
      "args": ["/path/to/goodpage/mcp-server/mcp_server.py"]
    }
  }
}
```

Restart Claude Desktop after saving the configuration.

### 3. Configure with Cursor

Add to your Cursor MCP settings:

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

## 🛠️ Available Tools

### 1. `text_to_page`

Convert plain text to a beautiful web page.

**Parameters:**
- `content` (required): Text content to convert
- `title` (optional): Article title (AI generates if omitted)
- `style` (optional): Template style code
- `content_strategy` (optional): 'strict' | 'interpret' | 'expand' (default: 'strict')
- `extra_requirements` (optional): Natural language styling instructions
- `response_type` (optional): 'url' | 'html' (default: 'url')
- `region` (optional): 'global' | 'china' (default: 'global')

**Example Usage in Claude:**
```
Create a beautiful webpage from this text about AI technology. 
Use the neon_glassmorphism style and return a shareable URL.
```

### 2. `get_available_templates`

Get detailed information about all available style templates.

**Returns:**
- Template codes, names, descriptions
- Best use cases for each template
- Visual characteristics

**Example Usage:**
```
What templates are available for technical documentation?
```

## 📚 Resources

### `goodpage://quota-info`

Access information about API quotas, limits, and usage guidelines.

**Example Usage:**
```
Check my remaining API quota for GoodPage
```

## 💡 Prompts

### `goodpage_best_practices`

Get comprehensive best practices guide for using GoodPage API effectively.

**Example Usage:**
```
Show me best practices for using GoodPage API
```

## 🎨 Available Templates

### Professional
- `minimalist` - Clean, simple design
- `premium_bw` - Elegant black & white
- `swiss_grid` - Rigorous grid system
- `newspaper_classic` - Traditional newspaper style

### Modern Tech
- `neon_glassmorphism` - Futuristic glass effect
- `cyberpunk_neon` - Dark cyberpunk aesthetic
- `gradient_glass` - Soft gradients with transparency
- `geometric_modern` - Bold geometric shapes

### Creative Artistic
- `magazine_gradient` - Warm magazine style
- `bold_waves` - Dynamic wave patterns
- `handdrawn_notes` - Casual hand-drawn look
- `brutalist_bold` - Raw brutalist design

### Specialized Themes
- `space_cosmic` - Deep space theme
- `dark_luxury` - Sophisticated dark luxury
- `pastel_soft` - Gentle pastel colors
- `kawaii_bubbles` - Cute Japanese kawaii style
- `minimalist_timeline` - Clean timeline layout

## 📖 API Documentation

For complete API documentation, visit:
- **Global:** https://goodpage.net/api-docs-en
- **China:** https://p.isheet.net/api-docs

## 🔧 Development

### Project Structure

```
mcp-server/
├── mcp_server.py       # Main MCP server implementation
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Running Tests

Test the server manually:

```bash
# Start the server
python mcp_server.py

# In another terminal, test with curl (if using stdio transport, use MCP inspector)
# Or use an MCP client like Claude Desktop
```

### Debugging

Enable verbose logging by modifying the server initialization:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🌍 Regional Endpoints

| Region | Endpoint | Best For |
|--------|----------|----------|
| Global | https://goodpage.net/api/text-to-page | International users |
| China | https://p.isheet.net/api/text-to-page | Users in mainland China |

Choose the appropriate region based on your location for optimal performance.

## 📊 Quota Information

- **Free Tier:** 50 API calls per IP address
- **Validity:** 30 days (auto-reset)
- **Max Content Length:** ~10,000 characters
- **Response Time:** 3-10 seconds typical

Monitor your quota in API responses or use the `goodpage://quota-info` resource.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Email:** chenkunji@qq.com
- **Website:** https://goodpage.net (Global) | https://p.isheet.net (China)
- **Issues:** GitHub Issues

## 🔗 Related Projects

- [GoodPage Web Application](https://goodpage.net) - Main web application
- [GoodPage API Documentation](https://goodpage.net/api-docs-en) - Complete API docs
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification

---

Made with ❤️ by the GoodPage Team
