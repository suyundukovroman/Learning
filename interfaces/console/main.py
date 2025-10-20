import glob
from typing import cast

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Static, Button, ListView, ListItem, Label

from core import lesson, parser
from core.lesson_manager import LessonManager, LessonState


class LessonItem(ListItem):
    def __init__(self, lesson_dict: dict) -> None:
        super().__init__()
        self.lesson_dict = lesson_dict

    def compose(self) -> ComposeResult:
        yield Label(self.lesson_dict["title"])

    def get_path(self) -> str:
        return self.lesson_dict["path"]


class MainApp(App):
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        with Header():
            yield Static("Learning Application")
        with VerticalScroll():
            yield Static("Select a lesson:")
            with ListView(id="lesson_files"):
                for lesson_file in self.get_lesson_files():
                    yield LessonItem(lesson_file)

    @on(ListView.Selected, "#lesson_files")
    def select_lesson(self, event: ListView.Selected):
        lesson_item: LessonItem = cast(LessonItem, event.item)
        cur_lesson = parser.parse(lesson_str=lesson_item.get_path())
        self.push_screen(LessonScreen(cur_lesson))

    def get_lesson_files(self) -> list:
        lesson_files = []
        for file in glob.glob(
            "../../data/*.md",
        ):
            lesson_files.append(
                {"title": file.split("\\")[-1].split(".md")[0], "path": file}
            )
        return lesson_files


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
