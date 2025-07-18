import re  # noqa: N999
from io import BytesIO

from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image as uiImage
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from PIL import Image as PILImage

answer: str = ""


class AOCTextInput(TextInput):
    def __init__(self: "AOCTextInput", **kwargs: bool | int | str) -> None:
        self.pattern = re.compile("[^0-9A-Z]")
        super().__init__(**kwargs)

    def insert_text(
        self: "AOCTextInput",
        substring: str,
        from_undo: bool = False,
    ) -> None:
        s = re.sub(self.pattern, "", substring)
        super().insert_text(s, from_undo)


class ManualOCR(App):
    image_data = None
    image_widget = None

    def build(self: "ManualOCR") -> BoxLayout:
        root_grid = BoxLayout(orientation="vertical")
        input_grid = BoxLayout(orientation="horizontal")

        ocr_image = PILImage.new("RGB", (240, 120), color=(255, 255, 255))
        data = BytesIO()
        ocr_image.save(data, format="png")
        data.seek(0)

        if self.image_data is None:
            self.image_data = CoreImage(BytesIO(data.read()), ext="png")
        if self.image_widget is None:
            self.image_widget = uiImage(
                size_hint=(1, 10), allow_stretch=True
            )
        assert self.image_widget is not None
        assert hasattr(self.image_data, "texture")
        self.image_widget.texture = self.image_data.texture
        root_grid.add_widget(self.image_widget)

        input_grid.add_widget(
            Label(text="Enter Value", size_hint=(0.3, 1), font_size=20)
        )

        self.text_widget = AOCTextInput(
            multiline=False,
            font_size=20,
            text_validate_unfocus=False,
            input_type="text",
            halign="center",
            write_tab=False,
        )
        self.text_widget.bind(
            on_text_validate=self.submit,
        )
        input_grid.add_widget(self.text_widget)

        self.button_widget = Button(
            text="Submit", size_hint=(0.3, 1), font_size=20
        )
        self.button_widget.bind(on_press=self.submit)
        input_grid.add_widget(self.button_widget)

        root_grid.add_widget(input_grid)

        Clock.schedule_once(self.timeout, 30)

        return root_grid

    @property
    def text(self: "ManualOCR") -> str:
        return str(self.text_widget.text)

    @text.setter
    def text(self: "ManualOCR", value: str) -> None:
        self.text_widget.text = value

    def submit(self: "ManualOCR", _instance: AOCTextInput) -> None:
        print(f'Submitting "{self.text}"')
        global answer  # noqa: PLW0603
        answer = self.text
        app = App.get_running_app()
        assert app is not None
        app.stop()

    def timeout(self: "ManualOCR", _instance: AOCTextInput) -> None:
        print('Timeout. Auto-Submitting "TEST"')
        global answer  # noqa: PLW0603
        answer = "TEST"
        app = App.get_running_app()
        assert app is not None
        app.stop()

    @property
    def image(self: "ManualOCR") -> PILImage.Image:
        data = BytesIO()
        if self.image_data is not None:
            self.image_data.save(data, fmt="png")
            data.seek(0)
            return PILImage.open(data).convert("RGB")
        return PILImage.new(mode="RGB", size=(0, 0))

    @image.setter
    def image(self: "ManualOCR", value: PILImage.Image) -> None:
        data = BytesIO()
        value.save(data, format="png")
        data.seek(0)
        self.image_data = CoreImage(BytesIO(data.read()), ext="png")
        if self.image_widget is None:
            self.image_widget = uiImage(
                size_hint=(1, 10), allow_stretch=True
            )
        assert self.image_widget is not None
        self.image_widget.texture = self.image_data.texture


if __name__ == "__main__":
    m = ManualOCR()
    m.image = PILImage.new("RGB", (30, 12), color=(0, 255, 255))
    m.run()
    print(f'Answer given was "{answer}"')
