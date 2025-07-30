from comics_mcp.core.protocol import ToolRegistry
from comics_mcp.plugins.comicvine.comicvine import ComicVineTool, ComicVineConfig

_registry = ToolRegistry()

comicvine_plugin = ComicVineTool(ComicVineConfig())
_registry.register_plugin(comicvine_plugin)

def get_all_tools():
    """Get all registered tools"""
    return _registry.get_tools()

def get_tool(tool_name: str):
    """Get specific tool by name"""
    return _registry.get_tool(tool_name)

def register_plugin(plugin):
    """Register a new plugin"""
    _registry.register_plugin(plugin)
