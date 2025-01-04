from components.filepicker import FileNamePicker, FileType
from components.sidebar import Sidebar
from ttml import process_lyrics


from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, TextArea


class EditScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Sidebar(id="sidebar")

        yield Horizontal(
            Button("Load from File", id="load"),
            Button("Save", id="save"),
            Button("Reset", id="reset", variant="error")
        )

        yield TextArea.code_editor("", language="text", classes="editor")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""

        editor:TextArea = self.query_one(".editor")

        if event.button.id == "load":
            def get_lyrics(location: str):
                if location != "":
                    editor.text = open(location, 'r').read()

            self.app.push_screen(FileNamePicker(FileType.TEXT), get_lyrics)

        elif event.button.id == "save":
            self.app.CURR_LYRICS = process_lyrics(editor.text)
            self.app.notify("Saved Lyrics")

        elif event.button.id == "reset":
            editor.text = ""