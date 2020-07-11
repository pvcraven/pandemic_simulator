import arcade
import random

from constants import *


class Person(arcade.SpriteCircle):
    def __init__(self, simulation_parameters):
        super().__init__(simulation_parameters.person_size, NORMAL_COLOR)
        self.simulation_parameters = simulation_parameters
        self.currently_infected = False
        self.ever_infected = False
        self.immune = False
        self.infected_frame_count = 0

    def immunize(self):
        self.immune = True
        self.texture = arcade.make_circle_texture(self.simulation_parameters.person_size * 2, IMMUNE_COLOR)

    def infect(self):
        if self.immune:
            return

        self.currently_infected = True
        self.ever_infected = True
        self.texture = arcade.make_circle_texture(self.simulation_parameters.person_size * 2, INFECTED_COLOR)

    def update(self):
        if self.currently_infected:
            self.infected_frame_count += 1

        if self.currently_infected and self.infected_frame_count > self.simulation_parameters.frames_to_result:

            if random.random() < self.simulation_parameters.chance_for_death:
                self.remove_from_sprite_lists()

            if random.random() < self.simulation_parameters.chance_for_immunity:
                self.currently_infected = False
                self.immune = True
                self.texture = arcade.make_circle_texture(self.simulation_parameters.person_size * 2, IMMUNE_COLOR)
