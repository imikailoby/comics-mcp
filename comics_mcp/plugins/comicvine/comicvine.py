import requests
from typing import Dict, Any
from comics_mcp.utils.env_util import get_env_var
from comics_mcp.core.types import Character
from comics_mcp.core.protocol import BasePlugin

class ComicVineConfig:
    """Configuration for Comic Vine API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or get_env_var("COMICVINE_API_KEY")
        self.base_url = "https://comicvine.gamespot.com/api"
        self.headers = {
            "User-Agent": "ComicsMCP/1.0",
            "Accept": "application/json"
        }

class ComicVineTool(BasePlugin):
    """Comic Vine API tool implementation"""
    
    def __init__(self, config: ComicVineConfig = None):
        self.config = config or ComicVineConfig()
    
    def get_plugin_name(self) -> str:
        return "comicvine"
    
    def get_tools(self) -> Dict[str, Any]:
        return {
            "comicvine.get_character": self.get_character,
        }
    
    def get_character(self, name: str) -> dict:
        """Lookup character by name"""
        params = {
            "api_key": self.config.api_key,
            "format": "json",
            "resources": "character",
            "query": name,
            "field_list": "aliases,birth,count_of_issue_appearances,deck,image,name,origin,publisher,real_name,site_detail_url"
        }
        
        try:
            response = requests.get(
                f"{self.config.base_url}/search/", 
                headers=self.config.headers, 
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

        if not data.get("results"):
            return {"error": "Character not found"}

        result = data["results"][0]
        character = Character(
            name=result.get("name", ""),
            real_name=result.get("real_name"),
            description=result.get("deck") or "",
            publisher=result.get("publisher", {}).get("name"),
            image_url=result.get("image", {}).get("medium_url"),
            source_url=result.get("site_detail_url"),
            legal_note="Data provided by Comic Vine API",
            aliases=result.get("aliases", "").split("\n") if result.get("aliases") else [],
            origin=result.get("origin", {}).get("name") if isinstance(result.get("origin"), dict) else result.get("origin"),
            birth=result.get("birth"),
            count_of_issue_appearances=result.get("count_of_issue_appearances")
        )
        return character.model_dump()
