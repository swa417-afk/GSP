from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class Paragraph:
    style: str
    runs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Section:
    id: str
    title: str
    blocks: List[Any] = field(default_factory=list)


class DocxModel:
    """
    Structured document model (intermediate representation).
    Used as the single source of truth before DOCX generation.
    """

    def __init__(self):
        self.sections: List[Section] = []

    def add_section(self, section: Section):
        self.sections.append(section)

    def get_section(self, section_id: str) -> Optional[Section]:
        return next((s for s in self.sections if s.id == section_id), None)
