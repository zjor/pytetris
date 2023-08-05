import random
from enum import Enum
from typing import Self

from settings import WIDTH, HEIGHT


class Move(Enum):
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    ROTATE_CW = 3
    ROTATE_CCW = 4


class Shape:
    X_OFFSET = WIDTH // 2 - 1

    def __init__(self, masks: list[list[list[int]]], x: int = 0, y: int = 0, rotation: int = 0):
        self._masks = masks
        self.x = x
        self.y = y
        self.rotation = rotation

    def render(self) -> list[list[int]]:
        field: list[list[int]] = [[0] * WIDTH for _ in range(HEIGHT)]
        mask = self._get_mask()
        for (i, row) in enumerate(mask):
            for (j, cell) in enumerate(row):
                if cell == 1:
                    field[self.y + i][self.x + j + Shape.X_OFFSET] = 1
        return field

    def is_within_field(self) -> bool:
        # a field WIDTH x HEIGHT surrounded by 2 layers of ones
        field = [[0] * (WIDTH + 4) for _ in range(HEIGHT + 4)]

        # cap of ones
        for i in range(WIDTH + 4):
            field[0][i] = 1
            field[1][i] = 1
            field[-1][i] = 1
            field[-2][i] = 1

        for i in range(HEIGHT + 4):
            field[i][0] = 1
            field[i][1] = 1
            field[i][-1] = 1
            field[i][-2] = 1

        dx, dy = 2, 2

        mask = self._get_mask()
        for (i, row) in enumerate(mask):
            for (j, cell) in enumerate(row):
                if cell == 1:
                    if field[self.y + i + dy][self.x + j + Shape.X_OFFSET + dx] == 1:
                        return False
        return True

    def move(self, m: Move) -> Self:
        match m:
            case Move.LEFT:
                return Shape(self._masks, self.x - 1, self.y, self.rotation)
            case Move.RIGHT:
                return Shape(self._masks, self.x + 1, self.y, self.rotation)
            case Move.DOWN:
                return Shape(self._masks, self.x, self.y + 1, self.rotation)
            case Move.ROTATE_CW:
                return Shape(self._masks, self.x, self.y, self.rotation - 1)
            case Move.ROTATE_CCW:
                return Shape(self._masks, self.x, self.y, self.rotation + 1)

    def _get_mask(self) -> list[list[int]]:
        return self._masks[self.rotation % len(self._masks)]


BLOCK_MASKS = [[
    [1, 1],
    [1, 1]
]]

LA_MASKS = [
    [
        [0, 0, 0],
        [1, 1, 1],
        [1, 0, 0]
    ],
    [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 1]
    ],
    [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ],
    [
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]
]

LB_MASKS = [
    [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 1]
    ],
    [
        [0, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ],
    [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    [
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 0]
    ]
]

SA_MASKS = [
    [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ],
    [
        [0, 1, 0],
        [1, 1, 0],
        [1, 0, 0]
    ]
]

SB_MASKS = [
    [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ],
    [
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0]
    ]
]

T_MASKS = [
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    [
        [0, 1, 0],
        [1, 1, 0],
        [0, 1, 0]
    ],
    [
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [0, 1, 0],
        [0, 1, 1],
        [0, 1, 0]
    ]
]

ROD_MASKS = [
    [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]
    ],
    [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
]

ALL_MASKS = [
    BLOCK_MASKS,
    LA_MASKS,
    LB_MASKS,
    SA_MASKS,
    SB_MASKS,
    T_MASKS,
    ROD_MASKS
]


def get_random_shape() -> Shape:
    index = random.randint(0, len(ALL_MASKS) - 1)
    rotations_count = len(ALL_MASKS[index])
    rotation = random.randint(0, rotations_count - 1)
    return Shape(ALL_MASKS[index], rotation=rotation)


def _print_field(field: list[list[int]]) -> None:
    for row in field:
        print(row)


def main():
    shape = Shape(LA_MASKS, y=HEIGHT - 2, rotation=2)
    shape = shape.move(Move.RIGHT)

    print(shape.is_within_field())

    field = shape.render()
    _print_field(field)


if __name__ == "__main__":
    main()
