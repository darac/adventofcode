from collections.abc import Callable  # noqa: N999

import pygame


class TwoDAnimationViewer:
    """Repeatedly calls a function and visualises the grid of numbers."""

    def __init__(
        self: "TwoDAnimationViewer",
        update_func: Callable,
        puzzle_input: str,
        display_size: tuple[int, int],
    ) -> None:
        """
        Visualises an array of values.

        Creates a display of size `display_size`, then calls `update_func` repeatedly,
        expecting it to return the current solution and a frame of animation.
        Upon receiving a StopIteration, the animation will stop and the last solution
        will be returned.

        Args:
            update_func (Callable): A function, probably part of the puzzle solution.
                Each time the function is called, it should return:
                * The current solution
                * One frame of the animation as a numpy array.
            puzzle_input (str): The puzzle input, passed to `update_func`.
            display_size (Tuple[int, int]): The size of the display window, in pixels.
        """
        self.iterator = update_func(puzzle_input)
        self.answer = None
        pygame.init()
        self.display = pygame.display.set_mode(display_size)

    @property
    def title(self: "TwoDAnimationViewer") -> str:
        """Returns the title of the window

        Returns:
            str: The pygame caption
        """
        return pygame.display.get_caption()[0]

    @title.setter
    def title(self: "TwoDAnimationViewer", title: str) -> None:
        """Sets the title of the pygame window.

        Args:
            title (str): The title to set
        """
        pygame.display.set_caption(title)

    def start(self: "TwoDAnimationViewer") -> int | None:
        running = True
        while running:
            if self.display is not None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                try:
                    self.answer, z = next(self.iterator)
                except StopIteration:
                    pygame.quit()
                    return self.answer
                surface = pygame.surfarray.make_surface(z)
                scaled_surface = pygame.transform.scale(surface, self.display.get_size())
                self.display.blit(scaled_surface, (0, 0))
                self.title = str(self.answer)

                pygame.display.update()
            else:
                for a, _ in self.iterator:
                    self.answer = a

        if self.display is not None:
            pygame.quit()
        return None
