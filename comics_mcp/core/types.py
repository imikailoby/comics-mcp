from pydantic import BaseModel, Field
from typing import List, Optional


class CharacterSummary(BaseModel):
    name: str = Field(..., description="Character's display name")
    real_name: Optional[str] = Field(None, description="Character's real/legal name if known")
    summary: str = Field(..., description="Short description or bio summary")
    publisher: Optional[str] = Field(None, description="Publisher or imprint name (e.g. Marvel, DC)")
    image_url: Optional[str] = Field(None, description="URL to a medium-sized character image")
    source_url: Optional[str] = Field(None, description="Canonical URL to the character's page on the source site")


class CharacterDetails(CharacterSummary):
    aliases: List[str] = Field(default_factory=list, description="Known aliases or alternative names")
    origin: Optional[str] = Field(None, description="Character's origin category (e.g. Mutant, Human, Alien)")
    first_appearance: Optional[str] = Field(None, description="Name of the issue where the character first appeared")
    description: Optional[str] = Field(None, description="Extended full description of the character's background")
    site_detail_url: Optional[str] = Field(None, description="Detailed URL for the character's page on the source site")
