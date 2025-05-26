import arcade

class MyGame(arcade.Window):
    """Main application window"""

    def __init__(self, width=800, height=600, title="My Arcade Game"):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        # Draw stuff here


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
