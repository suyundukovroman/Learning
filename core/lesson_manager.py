from core.lesson import Lesson

class LessonManager:
    def __init__(self, _lesson: Lesson):
        self._lesson = _lesson
        self._segment_index = 0
        self._content_index = 0

    def next_sentence(self) -> str:
        self._content_index += 1
        return self.get_content_text()

    def previous_sentence(self) -> str:
        self._content_index -= 1
        return self.get_content_text()

    def get_segment_title(self) -> str:
        segment = self._lesson.segments[self._segment_index]
        return segment.title

    def get_content_type(self) -> str:
        segment = self._lesson.segments[self._segment_index]
        return segment.content[self._content_index].get('type')

    def get_content_text(self) -> str:
        segment = self._lesson.segments[self._segment_index]
        return segment.content[self._content_index].get('text')

