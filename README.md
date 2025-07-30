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

| Plugin      | Description                                         |
|-------------|-----------------------------------------------------|
| `comicvine` | Tools for querying character data from Comic Vine. |

## 🔧 Plugin: `comicvine`

<details>
<summary><code>lookup_character</code> – Quick character search</summary>

Lookup a comic book character to get basic info like real name, publisher, image, and summary. Use this for quick character searches.

</details>

<details>
<summary><code>get_character_details</code> – Detailed character profile</summary>

Get detailed character profile with full biography, aliases, origin, appearance history, and complete description. Use this when you need comprehensive character information.

</details>

## ⚙️ Setup

1. Ensure you have Python 3.11+ installed:

```bash
python3 --version
```

2. Clone the repo and install:

```bash
git clone https://github.com/imikailoby/comics-mcp.git
cd comics-mcp
pip install -e .
```

3. Create `.env` file with your API key:

```bash
echo "COMICVINE_API_KEY=your-api-key" > .env
```

## 🚀 MCP Server

The MCP server communicates via stdin/stdout using JSON-RPC 2.0 protocol.

### Running the Server

```bash
python3 -m comics_mcp.mcp_server
```

### Configuration for MCP Clients

Create a configuration file for your MCP client:

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

## 🤝 Contributing

Contributions are welcome! Feel free to help with:

- Adding new plugin modules (e.g. Marvel API, Fandom Wiki, etc.)
- Improving tool interfaces or descriptions
- Writing documentation or test coverage
- Refactoring or performance improvements

## ⚡ Powered by

- [Comic Vine](https://comicvine.gamespot.com/api/). Not affiliated with or endorsed by Comic Vine.
