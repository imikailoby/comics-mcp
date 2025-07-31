from typing import Dict, Any
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """Base class for all plugins"""
    
    @abstractmethod
    def get_tools(self) -> Dict[str, Any]:
        """Return dictionary of tool_name -> tool_function"""
        pass
    
    @abstractmethod
    def get_plugin_name(self) -> str:
        """Return plugin name"""
        pass

class ToolRegistry:
    """Centralized tool registry with plugin support"""
    
    def __init__(self):
        self._tools = {}
        self._plugins = {}
    
    def register_plugin(self, plugin: BasePlugin):
        """Register a plugin"""
        plugin_name = plugin.get_plugin_name()
        self._plugins[plugin_name] = plugin
        tools = plugin.get_tools()
        for tool_name, tool_func in tools.items():
            self._tools[tool_name] = tool_func
    
    def get_tools(self) -> Dict[str, Any]:
        """Get all registered tools"""
        return self._tools.copy()
    
    def get_tool(self, tool_name: str) -> Any:
        """Get specific tool by name"""
        return self._tools.get(tool_name)
