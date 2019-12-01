import arcade
import random
import os
import time
import PlayerCharacter

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
# pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

PLAYER_START_X = 60
PLAYER_START_Y = 80

# Constants used to track if the player is facing left or right






class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
       super().__init__(width, height, title)
       # These are 'lists' that keep track of our sprites. Each sprite should
       # go into a list.
       self.player_list = None
       self.wall_list = None
       # Track the current state of what key is pressed
       self.left_pressed = False
       self.right_pressed = False
       self.up_pressed = False
       self.down_pressed = False
       self.jump_needs_reset = False

       self.background_list = None
       # Separate variable that holds the player sprite
       self.player_sprite = None
       # physics engine
       self.physics_engine = None
       arcade.set_background_color(arcade.color.ATOMIC_TANGERINE)

       # Used to keep track of our scrolling
       self.view_bottom = 0
       self.view_left = 0
    def setup(self):

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        #self.player_sprite = arcade.Sprite("right1.gif", CHARACTER_SCALING)
        self.player_sprite = PlayerCharacter.PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # Create the ground
        for x in range(0, 1200, 64):
            wall = arcade.Sprite("road.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

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
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        self.physics_engine.update()


        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
        self.player_list.update_animation(delta_time)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()



if __name__ == "__main__":
    main()
