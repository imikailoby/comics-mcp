import requests
from typing import Dict, Any
from comics_mcp.utils.html_cleaner import strip_html
from comics_mcp.utils.env_util import get_env_var
from comics_mcp.core.types import CharacterSummary, CharacterDetails
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
            "comicvine.lookup_character": self.lookup_character,
            "comicvine.get_character_details": self.get_character_details,
        }
    
    def lookup_character(self, name: str) -> dict:
        """Lookup character by name"""
        params = {
            "api_key": self.config.api_key,
            "format": "json",
            "resources": "character",
            "query": name
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
        summary = CharacterSummary(
            name=result.get("name", ""),
            real_name=result.get("real_name"),
            summary=strip_html(result.get("deck") or result.get("description") or ""),
            publisher=result.get("publisher", {}).get("name"),
            image_url=result.get("image", {}).get("medium_url"),
            source_url=result.get("site_detail_url")
        )
        return summary.model_dump()

    def get_character_details(self, name: str) -> dict:
        """Get detailed character information"""
        base = self.lookup_character(name)
        if "error" in base:
            return base

        source_url = base.get("source_url")
        if not source_url:
            return {"error": "Missing source URL"}

        try:
            character_id = source_url.strip("/").split("/")[-1]
        except Exception:
            return {"error": "Could not extract character ID from source URL"}

        detail_url = f"{self.config.base_url}/character/{character_id}/"
        params = {
            "api_key": self.config.api_key,
            "format": "json"
        }
        
        try:
            resp = requests.get(detail_url, headers=self.config.headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json().get("results", {})
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

        details = CharacterDetails(
            **base,
            aliases=data.get("aliases", "").split("\n") if data.get("aliases") else [],
            origin=data.get("origin", {}).get("name"),
            first_appearance=data.get("first_appeared_in_issue", {}).get("name"),
            description=strip_html(data.get("description") or ""),
            site_detail_url=data.get("site_detail_url")
        )
        return details.model_dump()
