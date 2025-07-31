from pydantic import BaseModel, Field
from typing import List, Optional


class Character(BaseModel):
    name: str = Field(..., description="Character's display name")
    real_name: Optional[str] = Field(None, description="Character's real/legal name if known")
    description: str = Field(..., description="Short character description")
    publisher: Optional[str] = Field(None, description="Publisher name (e.g. Marvel, DC)")
    image_url: Optional[str] = Field(None, description="URL to character image")
    source_url: Optional[str] = Field(None, description="URL to character's page")
    legal_note: str = Field(default="Data provided by XYZ", description="Legal notice about data source")
    aliases: List[str] = Field(default_factory=list, description="Known aliases or alternative names")
    origin: Optional[str] = Field(None, description="Character's origin category (e.g. Human, Alien, Robot)")
    birth: Optional[str] = Field(None, description="Character's birth date if known")
    count_of_issue_appearances: Optional[int] = Field(None, description="Number of issues this character appears in")
