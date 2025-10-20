from dataclasses import dataclass
from typing import List


@dataclass
class Segment:
    title: str
    content: List[dict]
    complete: bool = False


@dataclass
class Lesson:
    title: str
    segments: List[Segment]
    complete: bool = False
