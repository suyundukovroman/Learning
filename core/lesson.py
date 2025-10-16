from dataclasses import dataclass
from typing import List

@dataclass
class Segment:
    title: str
    theory: str
    practice: str
    answer: str

@dataclass
class Lesson:
    title: str
    segments: List[Segment]
