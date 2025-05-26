import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My Arcade Game"


class GameView(arcade.View):
    """Main game view."""

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """Render the screen."""
        self.clear()
        arcade.draw_text(
            "Game Screen",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            20,
            anchor_x="center",
        )

    def on_update(self, delta_time: float):
        """Update game logic."""
        pass


def main() -> None:
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = GameView()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
