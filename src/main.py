import arcade

PLAYER_SPRITE_PATH = "assets/images/player_sheet.png"

GRAVITY = 1
JUMP_SPEED = 20

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My Arcade Game"
LEVEL_WIDTH = 2000
PLAYER_SPEED = 5


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

        # Frames are 32x32 pixels. The sheet has two frames side by side.
        self.idle_textures = [
            arcade.load_texture(PLAYER_SPRITE_PATH, x=0, y=0, width=32, height=32),
            arcade.load_texture(
                PLAYER_SPRITE_PATH, x=0, y=0, width=32, height=32, flipped_horizontally=True
            ),
        ]

        self.run_textures = [
            arcade.load_texture(PLAYER_SPRITE_PATH, x=0, y=0, width=32, height=32),
            arcade.load_texture(PLAYER_SPRITE_PATH, x=32, y=0, width=32, height=32),
            arcade.load_texture(
                PLAYER_SPRITE_PATH, x=0, y=0, width=32, height=32, flipped_horizontally=True
            ),
            arcade.load_texture(
                PLAYER_SPRITE_PATH, x=32, y=0, width=32, height=32, flipped_horizontally=True
            ),
        ]

        self.texture = self.idle_textures[0]

    def jump(self) -> None:
        if self.can_jump:
            self.change_y = JUMP_SPEED
            self.can_jump = False

    def update(self) -> None:
        """Move the player and apply gravity."""

        # Apply gravity
        self.change_y -= GRAVITY

        # Move sprite
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Simple ground collision
        if self.center_y < self.height / 2:
            self.center_y = self.height / 2
            self.change_y = 0
            self.can_jump = True
        else:
            self.can_jump = False

        # Choose facing direction
        if self.change_x < 0:
            direction = 1  # left textures at index 1/3
        else:
            direction = 0  # right textures at index 0/2

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

        # Track pressed keys
        self.left_pressed = False
        self.right_pressed = False

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Draw world sprites through the camera so they scroll
        self.camera.use()
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

        self.player_list.update()

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
