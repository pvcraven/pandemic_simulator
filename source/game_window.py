from typing import Optional

import random
import math

import arcade

from person import Person
from constants import *


class GameWindow(arcade.Window):
    """ Main Window """

    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title)
        # super().__init__(int(width * .6666), int(height * .6666), title)

        # self.set_viewport(100, SCREEN_WIDTH * 2, 100, SCREEN_HEIGHT * 2)

        self.center_window()

        self.item_list: Optional[arcade.SpriteList] = None
        self.wall_list: Optional[arcade.SpriteList] = None

        # Physics engine
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

        self.frame_count = 0

        self.simulation_parameters = None

        # Set background color
        arcade.set_background_color(BACKGROUND_COLOR)

        self.currently_infected_count = []
        self.ever_infected_count = []
        self.immune_count = []
        self.dead_count = []
        self.total_population = []

    def setup(self, simulation_parameters):
        """ Set up everything with the game """

        self.simulation_parameters = simulation_parameters

        # Create the sprite lists
        self.item_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Create data stats
        self.currently_infected_count = []
        self.ever_infected_count = []
        self.immune_count = []
        self.dead_count = []
        self.total_population = []

        # --- Pymunk Physics Engine Setup ---

        damping = 1.0
        gravity = (0, 0)

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)

        # Create our population
        for i in range(simulation_parameters.population_count):
            item = Person(simulation_parameters)
            item.center_x = random.randrange(simulation_parameters.person_size * 2,
                                             SCREEN_WIDTH - simulation_parameters.person_size * 2)
            item.center_y = random.randrange(simulation_parameters.person_size * 2,
                                             SCREEN_HEIGHT - simulation_parameters.person_size * 2)

            self.item_list.append(item)

        self.physics_engine.add_sprite_list(self.item_list,
                                            friction=0,
                                            collision_type="item",
                                            elasticity=1.0)

        def hit_handler(sprite_a, sprite_b, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            if sprite_a.currently_infected \
                    and not sprite_b.currently_infected \
                    and random.random() <= simulation_parameters.chance_of_infection:
                sprite_b.infect()

            if sprite_b.currently_infected \
                    and not sprite_a.currently_infected \
                    and random.random() <= simulation_parameters.chance_of_infection:
                sprite_a.infect()

        self.physics_engine.add_collision_handler("item", "item", post_handler=hit_handler)

        # Give items an initial speed
        for item in self.item_list:
            direction = random.uniform(0, 2 * math.pi)
            speed = random.randrange(simulation_parameters.initial_top_speed)
            x = math.sin(direction) * speed
            y = math.cos(direction) * speed
            impulse = (x, y)
            self.physics_engine.apply_impulse(item, impulse)

        # Infect our initial population
        for i in range(simulation_parameters.initial_infected_people):
            self.item_list[i].infect()

        # Immunize our initial population
        for j in range(simulation_parameters.initial_infected_people,
                       simulation_parameters.initial_immune_people + simulation_parameters.initial_infected_people):
            self.item_list[j].immunize()

        # Bottom
        wall = arcade.SpriteSolidColor(SCREEN_WIDTH, 10, WALL_COLOR)
        wall.position = SCREEN_WIDTH / 2, SCREEN_HEIGHT - 5
        self.wall_list.append(wall)

        # Top
        wall = arcade.SpriteSolidColor(SCREEN_WIDTH, 10, WALL_COLOR)
        wall.position = SCREEN_WIDTH / 2, 5
        self.wall_list.append(wall)

        # Left
        wall = arcade.SpriteSolidColor(10, SCREEN_HEIGHT, WALL_COLOR)
        wall.position = 5, SCREEN_HEIGHT / 2
        self.wall_list.append(wall)

        # Right
        wall = arcade.SpriteSolidColor(10, SCREEN_HEIGHT, WALL_COLOR)
        wall.position = SCREEN_WIDTH - 5, SCREEN_HEIGHT / 2
        self.wall_list.append(wall)

        for i in range(simulation_parameters.vertical_walls):
            distance = SCREEN_WIDTH // simulation_parameters.vertical_walls + 1
            wall_size = SCREEN_HEIGHT // 2 - self.simulation_parameters.door_size // 2
            wall_y_pos = wall_size // 2

            # Bottom
            wall = arcade.SpriteSolidColor(10, wall_size, WALL_COLOR)
            wall.position = distance * i, wall_y_pos
            self.wall_list.append(wall)

            # Top
            wall = arcade.SpriteSolidColor(10, wall_size, WALL_COLOR)
            wall.position = distance * i, SCREEN_HEIGHT - wall_y_pos
            self.wall_list.append(wall)

        # Add the walls to the physics engine
        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=0,
                                            collision_type="wall",
                                            elasticity=1.0,
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # start_time = time.time()

        # See if we need to report our data
        if self.frame_count % self.simulation_parameters.reporting_interval == 0:
            currently_infected_count = 0
            ever_infected_count = 0
            immune_count = 0

            for item in self.item_list:
                if item.currently_infected:
                    currently_infected_count += 1
                if item.ever_infected:
                    ever_infected_count += 1
                if item.immune:
                    immune_count += 1

            dead_count = self.simulation_parameters.population_count - len(self.item_list)

            # Add to lists for later graphing
            self.currently_infected_count.append(currently_infected_count)
            self.dead_count.append(dead_count)
            self.ever_infected_count.append(ever_infected_count + dead_count)
            self.immune_count.append(immune_count)
            self.total_population.append(len(self.item_list))

            print(f"{self.frame_count}, {currently_infected_count}, {immune_count}, {dead_count}")

            if currently_infected_count == 0:
                import pyglet
                pyglet.app.exit()

        # Update frame count
        self.frame_count += 1

        # Move stuff
        self.physics_engine.step()

        # Update our people
        self.item_list.update()

        # end_time = time.time()
        # my_time = end_time - start_time
        # print(f"{my_time:8.5f}")

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()

        # Draw the sprites
        self.item_list.draw()
        self.wall_list.draw()

        # Calculate percentages
        infected_count = 0
        immune_count = 0
        for item in self.item_list:
            if item.currently_infected:
                infected_count += 1
            if item.immune:
                immune_count += 1

        percent_infected = infected_count / self.simulation_parameters.population_count * 100
        percent_immune = immune_count / self.simulation_parameters.population_count * 100
        number_dead = self.simulation_parameters.population_count - len(self.item_list)
        percent_dead = number_dead / self.simulation_parameters.population_count * 100

        # Draw the percentages
        text = f"Percent dead: {percent_dead:5.1f}"
        arcade.draw_text(text, 10, 70, arcade.color.WHITE, 18)

        text = f"Percent infected: {percent_infected:5.1f}"
        arcade.draw_text(text, 10, 40, arcade.color.WHITE, 18)

        text = f"Percent immune: {percent_immune:5.1f}"
        arcade.draw_text(text, 10, 10, arcade.color.WHITE, 18)
