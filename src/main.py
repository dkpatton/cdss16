import arcade
import json

PLAYER_SPRITE_PATH = "assets/images/player_sheet.png"
PLAYER_SPRITE_META = "assets/images/player_sheet.json"

GRAVITY = 1
JUMP_SPEED = 20

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My Arcade Game"

# Tile/level configuration
TILE_SIZE = 70

# Simple 2D array describing the level layout. Row 0 is the bottom row.
LEVEL_DATA = [
    [1] * 28,
    [0] * 28,
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0] * 28,
]

LEVEL_WIDTH = len(LEVEL_DATA[0]) * TILE_SIZE
PLAYER_SPEED = 5

# Tile ID to sprite path mapping
TILE_MAPPING = {
    1: "assets/images/grassMid.png",
}


class Player(arcade.Sprite):
    """Simple player sprite with basic platformer movement."""

    def __init__(self) -> None:
        super().__init__()

        self.center_x = 50
        self.center_y = SCREEN_HEIGHT / 2

        self.can_jump = False
        self._cur_texture = 0
        self._frame = 0

        self._load_textures()

    def _load_textures(self) -> None:
        """Load the idle and run textures from the sprite sheet."""

        with open(PLAYER_SPRITE_META) as f:
            data = json.load(f)["frames"]
<<<<<<< HEAD

        def load_frame(name: str, *, flip: bool = False) -> arcade.Texture:
            frame = data[name]["frame"]
            return arcade.load_texture(
                PLAYER_SPRITE_PATH,
                x=frame["x"],
                y=frame["y"],
                width=frame["w"],
                height=frame["h"],
                flipped_horizontally=flip,
            )

        idle_name = "player1_front_0"
        run_names = ["player1_left_0", "player1_left_1"]

        # Index 0 -> facing right, index 1 -> facing left
        self.idle_textures = [
            load_frame(idle_name, flip=True),
            load_frame(idle_name),
        ]

        # First two textures face right, last two face left
        self.run_textures = [
            load_frame(run_names[0], flip=True),
            load_frame(run_names[1], flip=True),
            load_frame(run_names[0]),
            load_frame(run_names[1]),
=======

        def load_frame(name: str, *, flip: bool = False) -> arcade.Texture:
            frame = data[name]["frame"]
            return arcade.load_texture(
                PLAYER_SPRITE_PATH,
                x=frame["x"],
                y=frame["y"],
                width=frame["w"],
                height=frame["h"],
                flipped_horizontally=flip,
            )

        idle_name = "player1_front_0"
        run_names = ["player1_left_0", "player1_left_1"]

        self.idle_textures = [load_frame(idle_name), load_frame(idle_name, flip=True)]
        self.run_textures = [
            load_frame(run_names[0]),
            load_frame(run_names[1]),
            load_frame(run_names[0], flip=True),
            load_frame(run_names[1], flip=True),
>>>>>>> main
        ]

        self.texture = self.idle_textures[0]

    def jump(self) -> None:
        if self.can_jump:
            self.change_y = JUMP_SPEED
            self.can_jump = False

    def update(self, platforms: arcade.SpriteList | None = None) -> None:
        """Move the player, apply gravity and handle collisions."""

        # Apply gravity
        self.change_y -= GRAVITY

        # --- Horizontal movement ---
        self.center_x += self.change_x
        if platforms:
            hit_list = arcade.check_for_collision_with_list(self, platforms)
            for tile in hit_list:
                if self.change_x > 0 and self.right > tile.left:
                    self.right = tile.left
                elif self.change_x < 0 and self.left < tile.right:
                    self.left = tile.right

        # --- Vertical movement ---
        self.center_y += self.change_y
        landed = False
        if platforms:
            hit_list = arcade.check_for_collision_with_list(self, platforms)
            for tile in hit_list:
                if self.change_y > 0 and self.top > tile.bottom:
                    self.top = tile.bottom
                    self.change_y = 0
                elif self.change_y <= 0 and self.bottom < tile.top:
                    self.bottom = tile.top
                    self.change_y = 0
                    landed = True

        # Simple ground collision if no platform caught us
        if not landed and self.center_y < self.height / 2:
            self.center_y = self.height / 2
            self.change_y = 0
            landed = True

        self.can_jump = landed

        # Choose facing direction (0=right, 1=left)
        if self.change_x < 0:
            direction = 1
        else:
            direction = 0

        # Select appropriate texture
        if self.change_x == 0:
            self.texture = self.idle_textures[direction]
        else:
            self._frame = (self._frame + 1) % 20
            index = (self._frame // 10) % 2
            self.texture = self.run_textures[index + direction * 2]


class GameView(arcade.View):
    """Main game view."""

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AMAZON)

        # Camera to follow the player
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Player setup
        self.player_sprite = Player()

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Platform tiles
        self.platforms = arcade.SpriteList(use_spatial_hash=True)
        self._load_level()

        # Track pressed keys
        self.left_pressed = False
        self.right_pressed = False

    def _load_level(self) -> None:
        """Create sprites for the level layout."""
        for row_index, row in enumerate(LEVEL_DATA):
            for col_index, tile_id in enumerate(row):
                if tile_id == 0:
                    continue
                texture = TILE_MAPPING.get(tile_id)
                if not texture:
                    continue
                sprite = arcade.Sprite(
                    texture,
                    center_x=col_index * TILE_SIZE + TILE_SIZE / 2,
                    center_y=row_index * TILE_SIZE + TILE_SIZE / 2,
                )
                self.platforms.append(sprite)

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Draw world sprites through the camera so they scroll
        self.camera.use()
        self.platforms.draw()
        self.player_list.draw()

    def on_update(self, delta_time: float):
        """Update game logic."""
        # Update player movement based on key state
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_SPEED
        else:
            self.player_sprite.change_x = 0

        # Update player sprite with platform collisions
        self.player_sprite.update(self.platforms)

        # Keep the player within the level bounds
        half_width = self.player_sprite.width / 2
        self.player_sprite.center_x = max(
            half_width, min(self.player_sprite.center_x, LEVEL_WIDTH - half_width)
        )

        # Follow the player with the camera
        left_boundary = self.player_sprite.center_x - SCREEN_WIDTH / 2
        left_boundary = max(0, min(left_boundary, LEVEL_WIDTH - SCREEN_WIDTH))
        self.camera.move_to((left_boundary, 0))
        self.camera.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = True
        elif symbol in (arcade.key.UP, arcade.key.SPACE):
            self.player_sprite.jump()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = False


def main() -> None:
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = GameView()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
