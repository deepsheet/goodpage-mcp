# GoodPage MCP Server - Deployment Guide

## 🌍 How Others Can Use Your MCP Server

### Important: MCP Servers Run Locally!

**MCP Servers are NOT remote HTTP services.** Each user runs the MCP Server on their own machine, and it connects to your GoodPage API endpoints.

```
User's Machine:
┌─────────────────────┐
│  Claude Desktop     │
│       ↓ stdio       │
│  MCP Server (Python)│ ──── HTTP Request ────→ Your API Server
└─────────────────────┘                          (goodpage.net)
```

---

## 📦 For Users: How to Install

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/goodpage-mcp.git
cd goodpage-mcp
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Claude Desktop

Edit `claude_desktop_config.json`:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "goodpage": {
      "command": "python",
      "args": ["/absolute/path/to/goodpage-mcp/mcp_server.py"]
    }
  }
}
```

**Replace `/absolute/path/to/goodpage-mcp/` with your actual path!**

### Step 4: Restart Claude Desktop

Quit and reopen Claude Desktop.

### Step 5: Start Using!

Ask Claude:
> "Create a beautiful webpage about artificial intelligence"

---

## 🔧 For Developers: Understanding the Architecture

### What Runs Where?

| Component | Location | Purpose |
|-----------|----------|---------|
| **MCP Server** | User's local machine | Translates AI requests to API calls |
| **GoodPage API** | Your server (goodpage.net) | Generates webpages from text |
| **Claude Desktop** | User's local machine | AI assistant that uses MCP tools |

### Communication Flow

1. User asks Claude to create a webpage
2. Claude calls the MCP Server tool (`text_to_page`)
3. MCP Server makes HTTP request to `https://goodpage.net/api/text-to-page`
4. Your API generates the webpage
5. Response flows back: API → MCP Server → Claude → User

---

## 🌐 API Endpoints Used

The MCP Server connects to these endpoints:

- **Global:** `https://goodpage.net/api/text-to-page`
- **China:** `https://p.isheet.net/api/text-to-page`

Users can choose the region by setting the `region` parameter.

---

## 💰 Quota Management

Each user gets:
- **50 free API calls** per IP address
- **30-day validity** (auto-reset)
- Tracked by their IP when calling your API

You (the API owner) manage quotas on your server, not in the MCP Server.

---

## 🚀 Publishing to MCP Directory

To make your MCP Server discoverable:

### Option 1: Submit to Official MCP Servers

1. Fork the official repository:
   ```bash
   git clone https://github.com/modelcontextprotocol/servers.git
   ```

2. Add your server to the directory
3. Submit a pull request

### Option 2: Publish on GitHub

1. Create a public repository
2. Add clear README with installation instructions
3. Share on social media and communities

### Option 3: List on Community Directories

- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)
- [MCP.so](https://mcp.so/)
- Reddit r/LocalLLaMA
- Hacker News

---

## 📝 Example User Configuration

Here's what a typical user's config looks like:

```json
{
  "mcpServers": {
    "goodpage": {
      "command": "python",
      "args": ["/Users/john/projects/goodpage-mcp/mcp_server.py"],
      "env": {
        "GOODPAGE_TEST_MODE": "false"
      }
    },
    "other-server": {
      "command": "node",
      "args": ["/path/to/other/server.js"]
    }
  }
}
```

---

## ❓ FAQ

### Q: Do I need to run a server for others?
**A:** No! Users run the MCP Server locally on their machines. You only need to keep your GoodPage API running.

### Q: Can users call my API directly?
**A:** Yes! The MCP Server is just a convenient wrapper. Users can also call `https://goodpage.net/api/text-to-page` directly via curl or any HTTP client.

### Q: How do I track usage?
**A:** Your Flask API already tracks usage by IP address. Check your Redis database for quota information.

### Q: Can I charge for API access?
**A:** Yes! Implement API key authentication in your Flask app. Update the MCP Server to include API keys in requests.

### Q: What if my API goes down?
**A:** Users will get error messages from the MCP Server. Make sure your API has good uptime and monitoring.

---

## 🔒 Security Considerations

For production use, consider adding:

1. **API Key Authentication**
   ```python
   headers = {
       "Content-Type": "application/json",
       "X-API-Key": "user-api-key-here"
   }
   ```

2. **Rate Limiting** (already implemented via quota system)

3. **CORS Configuration** (already configured in Flask)

4. **HTTPS Only** (already enabled on goodpage.net)

---

## 📊 Monitoring Your API

Track these metrics:

- Total API calls per day
- Unique IPs using the service
- Average response time
- Error rates
- Quota exhaustion rate

Use your existing logging and Redis data.

---

## 🎯 Next Steps

1. ✅ MCP Server code is ready
2. 📤 Publish to GitHub
3. 📝 Write announcement blog post
4. 📢 Share on social media
5. 📊 Monitor API usage
6. 🔄 Iterate based on feedback

---

## 🆘 Support

If users have issues:

1. Check if Flask API is running: `curl https://goodpage.net/api/health`
2. Verify MCP Server configuration path is correct
3. Check Claude Desktop logs: `~/Library/Logs/Claude/mcp*.log`
4. Ensure Python dependencies are installed

**Contact:** chenkunji@qq.com

---

*Last updated: April 21, 2026*
