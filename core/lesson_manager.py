from dataclasses import dataclass

from core.lesson import Lesson


@dataclass(frozen=True)
class LessonState:
    segment_index: int
    content_index: int
    segment_title: str
    content_text: str
    content_type: str
    is_complete: bool = False
    is_segment_complete: bool = False


class LessonManager:
    def __init__(self, _lesson: Lesson):
        self._lesson = _lesson
        self._segment_index = 0
        self._content_index = 0

    @property
    def state(self) -> LessonState:
        seg = self._lesson.segments[self._segment_index]
        cont = seg.content[self._content_index]
        return LessonState(
            segment_index=self._segment_index,
            content_index=self._content_index,
            segment_title=seg.title,
            content_text=cont.get("text"),
            content_type=cont.get("type"),
            is_complete=self._is_lesson_complete(),
            is_segment_complete=seg.complete,
        )

    def _is_lesson_complete(self) -> bool:
        return all(s.complete for s in self._lesson.segments)

    def next(self):
        seg = self._lesson.segments[self._segment_index]
        self._content_index += 1
        if self._content_index >= len(seg.content):
            seg.complete = True
            self._content_index = 0
            self._segment_index += 1
            if self._segment_index >= len(self._lesson.segments):
                self._segment_index = len(self._lesson.segments) - 1
        return self.state

    def prev(self):
        self._content_index -= 1
        if self._content_index < 0:
            self._segment_index -= 1
            if self._segment_index < 0:
                self._segment_index = 0
            seg = self._lesson.segments[self._segment_index]
            self._content_index = max(0, len(seg.content) - 1)
        return self.state

    def reset(self):
        self._segment_index = 0
        self._content_index = 0
        return self.state
