import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My Arcade Game"
LEVEL_WIDTH = 2000
PLAYER_SPEED = 5



class GameView(arcade.View):
    """Main game view."""

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AMAZON)

        # Camera to follow the player
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Player setup
        self.player_sprite = arcade.SpriteSolidColor(40, 40, arcade.color.BLUE)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = SCREEN_HEIGHT / 2

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
