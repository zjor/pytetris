from settings import HEIGHT
from shapes import Shape, Move, LA_MASKS, BLOCK_MASKS


class TestShapes:

    def test_is_within_bounds(self):
        shape = Shape(LA_MASKS)
        shape = shape.move(Move.LEFT)
        assert shape.is_within_field()

    def test_block_shape_is_within_bounds(self):
        block = Shape(BLOCK_MASKS)
        block = block.move(Move.RIGHT)
        assert block.is_within_field()

    def test_should_render_la_flat_shape(self):
        shape = Shape(LA_MASKS, y = HEIGHT - 2, rotation=2)
        assert shape.is_within_field()