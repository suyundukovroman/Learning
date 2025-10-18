from core.lesson import Lesson

class LessonManager:
    def __init__(self, _lesson: Lesson):
        self._lesson = _lesson
        self._segment_index = 0
        self._content_index = 0

    def next_sentence(self) -> str:
        self._content_index += 1
        segment = self._lesson.segments[self._segment_index]
        if self._content_index >= len(segment.content):
            if self._segment_index + 1 >= len(self._lesson.segments):
                segment.complete = True
                self._content_index -= 1
                return "Lesson complete"
            self.next_segment()
        return self.get_content_text()

    def previous_sentence(self) -> str:
        self._content_index -= 1
        segment = self._lesson.segments[self._segment_index]
        if self._content_index < 0:
            self.previous_segment()
            if self._segment_index < 0:
                self._segment_index = 0
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

    def next_segment(self):
        segment = self._lesson.segments[self._segment_index]
        segment.complete = True
        self._segment_index += 1
        self._content_index = 0

    def previous_segment(self):
        self._segment_index -= 1
        self._content_index = 0

    def is_segment_complete(self) -> bool:
        segment = self._lesson.segments[self._segment_index]
        return segment.complete
