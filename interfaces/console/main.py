from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Static, Button

from core import lesson, parser
from core.lesson_manager import LessonManager


class MainApp(App):
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        with Header():
            yield Static("Learning Application")
        with Vertical():
            yield Button("Start Lesson", id="start_lesson_btn")
            yield Static("PLACEHOLDER")

    @on(Button.Pressed, "#start_lesson_btn")
    def start_lesson_btn(self, event: Button.Pressed):
        cur_lesson = parser.parse(lesson_str='../../data/test_lesson.md')
        self.push_screen(LessonScreen(cur_lesson))

class LessonScreen(Screen):

    def __init__(self, cur_lesson: lesson.Lesson):
        super().__init__()
        self._lesson = cur_lesson
        self._manager = LessonManager(cur_lesson)

    def compose(self) -> ComposeResult:
        with Header():
            yield Static(self._lesson.title)
        with VerticalScroll(id="lesson_container") as container:
            container.border_title = self._manager.get_segment_title()
            container.border_subtitle = self._manager.get_content_type()
            yield Static(self._manager.get_content_text(), id="lesson_text")
            with Horizontal():
                yield Button("Next" , id="next_button")
                yield Button("Back" , id="back_button")
            yield  Button("Finish Lesson", id="finish_lesson_btn")

    @on(Button.Pressed, "#next_button")
    def next_button(self, event: Button.Pressed):
        self.query_one("#lesson_text", Static).update(self._manager.next_sentence())
        self.lesson_container_update()

    @on(Button.Pressed, "#back_button")
    def back_button(self, event: Button.Pressed):
        self.query_one("#lesson_text", Static).update(self._manager.previous_sentence())
        self.lesson_container_update()

    @on(Button.Pressed, "#finish_lesson_btn")
    def finish_lesson_btn(self, event: Button.Pressed):
        self.app.pop_screen()

    def lesson_container_update(self):
        container = self.query_one("#lesson_container", VerticalScroll)
        container.border_subtitle = self._manager.get_content_type()
        container.border_title = self._manager.get_segment_title()
        if self._manager.is_segment_complete():
            container.styles.border = ("round", "green")
        else:
            container.styles.border = ("round", "white")


if __name__ == '__main__':
    app = MainApp()
    app.run()