from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Static, Button

from core import lesson, parser
from core.lesson_manager import LessonManager, LessonState


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
        cur_lesson = parser.parse(lesson_str="../../data/test_lesson.md")
        self.push_screen(LessonScreen(cur_lesson))


class LessonScreen(Screen):
    def __init__(self, cur_lesson: lesson.Lesson):
        super().__init__()
        self._lesson = cur_lesson
        self._manager = LessonManager(cur_lesson)

    def compose(self) -> ComposeResult:
        with Header():
            yield Static(self._lesson.title, id="title")
        with VerticalScroll(id="lesson_container") as container:
            state = self._manager.state
            container.border_title = state.segment_title
            container.border_subtitle = state.content_type
            yield Static(state.content_text, id="lesson_text")
            with Horizontal():
                yield Button("Next", id="next_button")
                yield Button("Back", id="back_button")
            yield Button("Finish Lesson", id="finish_lesson_btn")

    @on(Button.Pressed, "#next_button")
    def next_button(self, event: Button.Pressed):
        state = self._manager.next()
        self.lesson_container_update(state)

    @on(Button.Pressed, "#back_button")
    def back_button(self, event: Button.Pressed):
        state = self._manager.prev()
        self.lesson_container_update(state)

    @on(Button.Pressed, "#finish_lesson_btn")
    def finish_lesson_btn(self, event: Button.Pressed):
        self.app.pop_screen()

    def lesson_container_update(self, state: LessonState):
        self.query_one("#lesson_text", Static).update(state.content_text)
        container = self.query_one("#lesson_container", VerticalScroll)
        container.border_title = state.segment_title
        container.border_subtitle = state.content_type
        container.styles.border = (
            "round",
            "green" if state.is_segment_complete else "white",
        )
        if state.is_complete:
            self.query_one("#title", Static).update(self._lesson.title + " \u2705 ")


if __name__ == "__main__":
    app = MainApp()
    app.run()
