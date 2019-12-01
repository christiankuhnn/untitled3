import arcade
import random
import os
import time

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Platformer'
# Constants used to scale our sprites
TILE_SCALING = 0.3
CHARACTER_SCALING = .4
# Movement speed of player
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 15


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
       super().__init__(width, height, title)
       # These are 'lists' that keep track of our sprites. Each sprite should
       # go into a list.
       self.player_list = None
       self.wall_list = None

       # Separate variable that holds the player sprite
       self.player_sprite = None
       # physics engine
       self.physics_engine = None
       arcade.set_background_color(arcade.color.ATOMIC_TANGERINE)

    def setup(self):

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite("right1.gif", CHARACTER_SCALING)
        self.player_sprite.center_x = 80
        self.player_sprite.center_y = 200
        self.player_list.append(self.player_sprite)

        # Create the ground
        for x in range(0, 1200, 64):
            wall = arcade.Sprite("road.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

         # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96],
                           [256, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite("hydrant.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        #setup physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY)
    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Your drawing code goes here
        # Draw our sprites
        self.player_list.draw()
        self.wall_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        self.physics_engine.update()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()



if __name__ == "__main__":
    main()
