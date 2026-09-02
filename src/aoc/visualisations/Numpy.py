# Copyright (c) 2015-2026 Paul Saunders
import logging
from types import TracebackType
from typing import Self

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.backend_bases import Event
from matplotlib.backends import backend_registry
from matplotlib.figure import Figure
from matplotlib.widgets import Button, TextBox

LOG = logging.getLogger()


class Visualiser:
    def __init__(
        self: "Visualiser",
        delay: float = 0.25,
        title: str = "",
        *,
        interactive: bool | None = None,
    ) -> None:
        self.delay = delay
        self.title = title
        self.fig: Figure
        self.ax: Axes
        self.image: plt.AxesImage | None = None
        self.interactive = False

        if interactive is None:
            _, gui = backend_registry.resolve_backend(mpl.get_backend())
            interactive = gui is not None

        self.interactive = interactive

        if self.interactive:
            self.fig, self.ax = plt.subplots()

    def __enter__(self) -> Self:
        plt.ion()

        if self.interactive:
            manager = self.fig.canvas.manager
            if manager is not None:
                toolbar = getattr(manager, "toolbar", None)
                if toolbar is not None and hasattr(toolbar, "hide"):
                    toolbar.hide()
            self.ax.axis("off")
            self.ax.set_aspect("equal")
            if self.title != "":
                self.fig.suptitle(self.title)
            self.fig.show()

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        plt.ioff()
        if self.interactive:
            plt.close(self.fig)

    def _redraw(self) -> None:
        if self.image is None:
            return

        height, width = self.display_array.shape[:2]

        self.image.set_data(self.display_array)
        self.image.set_extent(
            (
                -0.5,
                width - 0.5,
                height - 0.5,
                -0.5,
            )
        )

        self.ax.set_xlim(-0.5, width - 0.5)
        self.ax.set_ylim(height - 0.5, -0.5)

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def update(self, data: np.typing.ArrayLike) -> None:
        if not self.interactive:
            return
        assert isinstance(self.fig, Figure)
        assert isinstance(self.ax, Axes)

        array = np.asarray(data)
        if array.ndim != 2:
            msg = f"Expected a 2D Array, got shape {array.shape}"
            raise ValueError(msg)

        if self.image is None:
            self.image = self.ax.imshow(
                array,
                cmap="binary",
                interpolation="nearest",
            )
        else:
            self.image.set_data(array)
            self.image.set_extent(
                (
                    -0.5,
                    array.shape[1] - 0.5,
                    array.shape[0] - 0.5,
                    -0.5,
                )
            )

        self.ax.set_xlim(-0.5, array.shape[1] - 0.5)
        self.ax.set_ylim(array.shape[0] - 0.5, -0.5)
        self.display_array = array

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

        plt.pause(self.delay)

    def perform_ocr(self, default: str | None = None) -> str | None:
        if not self.interactive:
            if default is not None:
                return default

            msg = (
                "OCR requires an interactive display "
                "and no default was supply"
            )
            raise RuntimeError(msg)
        result = None
        LOG.info(
            "Running Manual OCR over Numpy array (size: %dx%d):",
            self.display_array.shape[0],
            self.display_array.shape[1],
        )

        self.fig.subplots_adjust(bottom=0.2)

        left_ax = self.fig.add_axes((0.10, 0.05, 0.10, 0.06))
        right_ax = self.fig.add_axes((0.21, 0.05, 0.10, 0.06))
        hflip_ax = self.fig.add_axes((0.32, 0.05, 0.10, 0.06))
        vflip_ax = self.fig.add_axes((0.43, 0.05, 0.10, 0.06))
        text_ax = self.fig.add_axes((0.60, 0.05, 0.20, 0.06))
        submit_ax = self.fig.add_axes((0.82, 0.05, 0.12, 0.06))

        left = Button(left_ax, "↺")
        right = Button(right_ax, "↻")
        hflip = Button(hflip_ax, "↔")
        vflip = Button(vflip_ax, "↕")
        textbox = TextBox(text_ax, "Answer: ")
        submit = Button(submit_ax, "Submit")

        def submit_answer(event: Event | str) -> None:
            nonlocal result
            result = textbox.text if isinstance(event, Event) else event
            self.fig.canvas.stop_event_loop()

        submit.on_clicked(submit_answer)
        textbox.on_submit(submit_answer)
        left.on_clicked(self.rotate_left)
        right.on_clicked(self.rotate_right)
        hflip.on_clicked(self.flip_horizontal)
        vflip.on_clicked(self.flip_vertical)

        self.fig.canvas.start_event_loop()

        return result

    def rotate_left(self, _event: Event) -> None:
        LOG.debug("Rotate Left")
        self.display_array = np.rot90(self.display_array)
        self._redraw()

    def rotate_right(self, _event: Event) -> None:
        LOG.debug("Rotate Right")
        self.display_array = np.rot90(self.display_array, -1)
        self._redraw()

    def flip_horizontal(self, _event: Event) -> None:
        LOG.debug("Horizontal Flip")
        self.display_array = np.fliplr(self.display_array)
        self._redraw()

    def flip_vertical(self, _event: Event) -> None:
        LOG.debug("Vertical Flip")
        self.display_array = np.flipud(self.display_array)
        self._redraw()
