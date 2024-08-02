import pygame
import random
import numpy as np
from settings import *

class Particle(pygame.sprite.Sprite):
    def __init__(self, radius, position, angle, speed, mass, color):
        pygame.sprite.Sprite.__init__(self)
        self.mass        = mass
        self.radius      = radius
        self.angle       = angle 
        self.position    = np.array([*position])
        self.speed       = speed
        self.velocity    = np.array([self.speed*np.cos(self.angle), self.speed*np.sin(self.angle)])
        self.si_speed    = 0
        self.color       = color
        self.sorted_v_left = None
        self.sorted_v_right = None
        self.sorted_left  = None
        self.sorted_right = None

    def update(self, boundary, maxwell_demon=False):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # update the collisions with the wall (top, bottom, left, right)
        # toggle maxwell's demon

        # y collisions with boundary
        if (self.position[1] < self.radius) or (self.position[1] > BOX_HEIGHT-self.radius):
                self.velocity = np.array([self.velocity[0], -self.velocity[1]])

        # x collisions with boundary
        if (self.position[0] <= self.radius) or (self.position[0] >= BOX_WIDTH-self.radius):
            self.velocity = np.array([-self.velocity[0], self.velocity[1]])

          
        """
        Maxwell Demon
        how the particles are sorted in the volume is dependent upon their speeds only
        the collisions will happen after the particle is designated the flag
        """
             
        if maxwell_demon:

            # sort by speeds
            if self.speed >= maxwell_demon:# and (self.position[0] <= BOX_WIDTH/2-self.radius):
                self.sorted_v_right = True
                self.sorted_v_left = False
            if self.speed < maxwell_demon:# and (self.position[0] > BOX_WIDTH/2+self.radius):
                self.sorted_v_right= False
                self.sorted_v_left = True

            collision_factor = 10
            # sort by positions
            if (self.position[0] > self.radius) and (self.position[0] < boundary-self.radius):
                self.sorted_right = False
                self.sorted_left = True
            if (self.position[0] >= boundary+self.radius) and (self.position[0] < BOX_WIDTH-self.radius):
                self.sorted_right = True
                self.sorted_left = False

            # x collisions that depend on demon 
            if self.sorted_left and self.sorted_v_left:
                if (self.position[0] >= (boundary - self.radius)): # check collision
                    self.velocity = np.array([-self.velocity[0], self.velocity[1]])

            if self.sorted_right and self.sorted_v_right:
                if (self.position[0] < (boundary + self.radius)): # check collision
                    self.velocity = np.array([-self.velocity[0], self.velocity[1]])

        # calculate the speed of the particle by taking the norm of its velocity
        self.speed = np.linalg.norm(self.velocity)