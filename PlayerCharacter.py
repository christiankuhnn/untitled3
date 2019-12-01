import arcade
import random
import os
import MyGame
CHARACTER_SCALING = .4
RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename, scale=CHARACTER_SCALING),
        arcade.load_texture(filename, scale=CHARACTER_SCALING, mirrored=True)
    ]

class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        #sets up the parent class
        super().__init__()
        #face right by default
        self.character_face_direction = RIGHT_FACING

        #flip between image sequences
        self.cur_texture = 0

        #track our state
        self.jumping = False

        #adjust the collision box

        #load the textures
        main_path = 'images/right'

        #idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}0.gif")
        self.jump_texture_pair = load_texture_pair(f"{main_path}21.gif")

        #Load the textures for walking
        self.walk_textures = []
        for i in range(12):
            texture = arcade.load_texture(f"{main_path}{i}.gif")
            self.walk_textures.append(texture)
    def update_animation(self, delta_time: float = 1/60):
        #Do we need to face left or right?
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        #idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return


        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
