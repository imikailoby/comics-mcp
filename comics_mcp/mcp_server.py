#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server for Comics MCP
Compatible with Cursor and other MCP clients
"""

import json
import sys
import logging
from typing import Dict, Any, List, Optional
from comics_mcp.core.registry import get_all_tools, get_tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPError(Exception):
    """Base exception for MCP errors"""
    pass

class ToolNotFoundError(MCPError):
    """Raised when tool is not found"""
    pass

class InvalidRequestError(MCPError):
    """Raised when request is invalid"""
    pass

class MCPServer:
    def __init__(self):
        self.tools = get_all_tools()
        self.initialized = False
        
    def send_message(self, message: Dict[str, Any]) -> None:
        """Send a message to the MCP client"""
        try:
            json.dump(message, sys.stdout)
            sys.stdout.write('\n')
            sys.stdout.flush()
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
        
    def read_message(self) -> Optional[Dict[str, Any]]:
        """Read a message from the MCP client"""
        try:
            line = sys.stdin.readline()
            if not line:
                return None
            return json.loads(line)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse message: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading message: {e}")
            return None
    
    def validate_message(self, message: Dict[str, Any]) -> None:
        """Validate incoming message"""
        if not isinstance(message, dict):
            raise InvalidRequestError("Message must be a dictionary")
        
        if "jsonrpc" not in message or message["jsonrpc"] != "2.0":
            raise InvalidRequestError("Invalid JSON-RPC version")
    
    def handle_initialize(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        try:
            self.validate_message(message)
            protocol_version = message.get("protocolVersion", "2024-11-05")
            capabilities = message.get("capabilities", {})
            
            self.send_message({
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": {
                    "protocolVersion": protocol_version,
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "comics-mcp",
                        "version": "1.0.0"
                    }
                }
            })
            
            self.initialized = True
            return {"status": "initialized"}
        except Exception as e:
            logger.error(f"Initialize error: {e}")
            self.send_error(message.get("id"), -32603, f"Internal error: {str(e)}")
            return {"error": str(e)}
    
    def handle_list_tools(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list tools request"""
        try:
            self.validate_message(message)
            tools_list = []
            
            for tool_name, tool_func in self.tools.items():
                tool_info = {
                    "name": tool_name,
                    "description": self._get_tool_description(tool_name),
                    "inputSchema": self._get_tool_schema(tool_name)
                }
                tools_list.append(tool_info)
            
            self.send_message({
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": {
                    "tools": tools_list
                }
            })
            
            return {"tools": tools_list}
        except Exception as e:
            logger.error(f"List tools error: {e}")
            self.send_error(message.get("id"), -32603, f"Internal error: {str(e)}")
            return {"error": str(e)}
    
    def handle_call_tool(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle call tool request"""
        try:
            self.validate_message(message)
            params = message.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if not tool_name:
                raise InvalidRequestError("Tool name is required")
            
            if tool_name not in self.tools:
                raise ToolNotFoundError(f"Tool '{tool_name}' not found")
            
            tool_func = self.tools[tool_name]
            result = tool_func(**arguments)
            
            self.send_message({
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": str(result)
                        }
                    ]
                }
            })
            
            return {"result": result}
            
        except ToolNotFoundError as e:
            logger.warning(f"Tool not found: {e}")
            self.send_error(message.get("id"), -32601, str(e))
            return {"error": str(e)}
        except InvalidRequestError as e:
            logger.warning(f"Invalid request: {e}")
            self.send_error(message.get("id"), -32600, str(e))
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"Tool call error: {e}")
            self.send_error(message.get("id"), -32603, f"Internal error: {str(e)}")
            return {"error": str(e)}
    
    def send_error(self, message_id: Any, code: int, message: str) -> None:
        """Send error response"""
        self.send_message({
            "jsonrpc": "2.0",
            "id": message_id,
            "error": {
                "code": code,
                "message": message
            }
        })
    
    def _get_tool_description(self, tool_name: str) -> str:
        """Get tool description from manifest"""
        try:
            import os
            manifest_path = os.path.join(os.path.dirname(__file__), "..", "tool_manifest.json")
            with open(manifest_path) as f:
                manifest = json.load(f)
            
            for tool in manifest:
                if tool["name"] == tool_name:
                    return tool["description"]
        except Exception as e:
            logger.warning(f"Could not load tool description for {tool_name}: {e}")
        
        return f"Tool {tool_name}"
    
    def _get_tool_schema(self, tool_name: str) -> Dict[str, Any]:
        """Get tool input schema from manifest"""
        try:
            import os
            manifest_path = os.path.join(os.path.dirname(__file__), "..", "tool_manifest.json")
            with open(manifest_path) as f:
                manifest = json.load(f)
            
            for tool in manifest:
                if tool["name"] == tool_name:
                    return tool["parameters"]
        except Exception as e:
            logger.warning(f"Could not load tool schema for {tool_name}: {e}")
        
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Character name"
                }
            },
            "required": ["name"]
        }
    
    def handle_notification(self, message: Dict[str, Any]) -> None:
        """Handle notifications"""
        try:
            self.validate_message(message)
            method = message.get("method")
            
            if method == "notify/exit":
                logger.info("Received exit notification")
                sys.exit(0)
            else:
                logger.warning(f"Unknown notification method: {method}")
        except Exception as e:
            logger.error(f"Notification error: {e}")
    
    def run(self):
        """Main server loop"""
        logger.info("Starting MCP server...")
        
        while True:
            try:
                message = self.read_message()
                if message is None:
                    break
                
                if "id" not in message:
                    self.handle_notification(message)
                    continue
                
                method = message.get("method")
                
                if method == "initialize":
                    self.handle_initialize(message)
                elif method == "tools/list":
                    self.handle_list_tools(message)
                elif method == "tools/call":
                    self.handle_call_tool(message)
                else:
                    self.send_error(message.get("id"), -32601, f"Method '{method}' not found")
                    
            except KeyboardInterrupt:
                logger.info("Server stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                if "id" in message:
                    self.send_error(message.get("id"), -32603, f"Internal error: {str(e)}")

def main():
    """Main entry point"""
    server = MCPServer()
    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 