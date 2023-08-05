from textual import events, on
from textual.app import App, ComposeResult
from textual.message import Message
from textual.screen import Screen, ModalScreen
from textual.widgets import Static

import shapes
from settings import WIDTH, HEIGHT
from shapes import Move


def merge_fields(dst: list[list[int]], src: list[list[int]]) -> list[list[int]]:
    result = [[0] * WIDTH for _ in range(HEIGHT)]
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if dst[row][col] == 0:
                result[row][col] = src[row][col]
            else:
                result[row][col] = dst[row][col]
    return result


def overlaps(one: list[list[int]], two: list[list[int]]) -> bool:
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if one[row][col] > 0 and two[row][col] > 0:
                return True
    return False


class TetrisField(Static):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state: list[list[int]] = []
        self.shape = shapes.get_random_shape()
        self.reset_state()
        self.started = True

    def restart_game(self, dummy: bool):
        self.reset_state()
        self.shape = shapes.get_random_shape()
        self.started = True
        self.render_field()

    def reset_state(self):
        self.state = [[0] * WIDTH for _ in range(HEIGHT)]

    def on_mount(self):
        self.set_interval(0.5, self.tick)

    def tick(self):
        if not self.started:
            return

        next_shape = self.shape.move(Move.DOWN)
        if next_shape.is_within_field() and not overlaps(self.state, next_shape.render()):
            self.shape = next_shape
            self.render_field()
        else:
            self.lock_shape_and_get_next()

    def render_field(self):
        if self.shape.is_within_field():
            mask = self.shape.render()
            frame = merge_fields(self.state, mask)
            data = '\n'.join([''.join('  ' if cell == 0 else '[]' for cell in row) for row in frame])
            self.update(data)
        else:
            raise Exception("Not withing the field")

    def delete_completed_lines(self):
        row = HEIGHT - 1
        while row > 0:
            completed = True
            for cell in self.state[row]:
                if cell == 0:
                    completed = False
                    break
            if completed:
                for i in reversed(range(1, row + 1)):
                    self.state[i] = self.state[i - 1]
            else:
                row -= 1

    def lock_shape_and_get_next(self):
        mask = self.shape.render()
        self.state = merge_fields(self.state, mask)
        self.delete_completed_lines()
        self.shape = shapes.get_random_shape()

        if self.started and overlaps(self.state, self.shape.render()):
            self.started = False
            self.app.push_screen("game_over", self.restart_game)

    def on_key(self, event: events.Key):
        next_shape = self.shape
        last_move_is_down = False
        if event.key == 'a':
            next_shape = self.shape.move(Move.LEFT)
        elif event.key == 'd':
            next_shape = self.shape.move(Move.RIGHT)
        elif event.key == 'w':
            next_shape = self.shape.move(Move.ROTATE_CCW)
        elif event.key == 's':
            next_shape = self.shape.move(Move.ROTATE_CW)
        elif event.key == 'l':
            next_shape = self.shape.move(Move.DOWN)
            last_move_is_down = True
        else:
            return

        if next_shape.is_within_field() and not overlaps(self.state, next_shape.render()):
            self.shape = next_shape
            self.render_field()
        else:
            if last_move_is_down:
                self.lock_shape_and_get_next()
            else:
                self.app.bell()


class WelcomeScreen(Screen):
    BINDINGS = [("space", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Static("Welcome to PyTetris!\n\nPress SPACE to start the game")


class GameOverScreen(ModalScreen[bool]):

    def compose(self) -> ComposeResult:
        yield Static("Game over!\n\nPress SPACE to start again")

    def on_key(self, event: events.Key):
        if event.key == 'space':
            self.dismiss(True)


class TetrisApp(App):
    CSS_PATH = "style.css"
    SCREENS = {
        "welcome": WelcomeScreen(),
        "game_over": GameOverScreen()
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field = TetrisField()

    def compose(self) -> ComposeResult:
        yield self.field

    def on_key(self, event: events.Key) -> None:
        self.field.on_key(event)


def main():
    app = TetrisApp()
    app.run()


if __name__ == "__main__":
    main()
