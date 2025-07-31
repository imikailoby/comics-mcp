# Comics MCP (🦸🦹)

A Model Context Protocol (MCP) server with plugin architecture for comic-related data sources.

**Requirements:** Python 3.11+

## 🚀 Quick Start

```bash
# 1. Install
pip install -e .

# 2. Create .env file with your API key
echo "COMICVINE_API_KEY=your-api-key" > .env

# 3. Run server
python3 -m comics_mcp.mcp_server
```

## 🧩 Available Plugins

| Plugin | Tools | Description |
|--------|-------|-------------|
| `comicvine` | `get_character` | Get comprehensive character information including aliases, origin, and appearance count. Optimized for fast response times. |

## 🔧 Setup

1. **Get Comic Vine API Key:**
   - Register at [Comic Vine](https://comicvine.gamespot.com/api/)
   - Request an API key

2. **Install and Configure:**
   ```bash
   git clone https://github.com/imikailoby/comics-mcp.git
   cd comics-mcp
   pip install -e .
   echo "COMICVINE_API_KEY=your-api-key" > .env
   ```

3. **Configure MCP Client:**
   ```json
   {
     "mcpServers": {
       "comics-mcp": {
         "command": "python3",
         "args": ["-m", "comics_mcp.mcp_server"],
         "env": {
           "PYTHONPATH": "/path/to/your/comics-mcp",
           "COMICVINE_API_KEY": "your_api_key"
         }
       }
     }
   }
   ```

## 📊 Character Data Fields

The comicvine plugin returns comprehensive character information including:
- **Basic Info:** name, real_name, description, publisher
- **Media:** image_url, source_url
- **Details:** aliases, origin, birth date, count_of_issue_appearances
- **Legal:** legal_note with data source attribution

## 🤝 Contributing

Contributions are welcome! Feel free to help with:
- Adding new data sources (Marvel API, DC API, etc.)
- Adding new plugins or tools to existing plugins
- Improving plugin interfaces or descriptions
- Writing documentation or test coverage
- Performance optimizations

## ⚡ Powered by

- [Comic Vine](https://comicvine.gamespot.com/api/). Not affiliated with or endorsed by Comic Vine.
