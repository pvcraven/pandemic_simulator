"""
Infection Simulator
"""

import arcade

from simulation_parameters import SimulationParameters
from constants import *
from game_window import GameWindow
from plot_results import plot_results


def main():
    """ Main method """

    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    simulation_parameters = SimulationParameters(
        population_count=650,
        person_size=7,
        frames_to_result=200,
        chance_of_infection=0.6,
        chance_for_immunity=1.0,
        chance_for_death=0.05,
        initial_top_speed=250,
        reporting_interval=10,
        initial_infected_people=1,
        initial_immune_people=0,
        vertical_walls=4,
        door_size=100,
    )
    # for chance_of_infection in [0.4, 0.7]:
    #   simulation_parameters.chance_of_infection = chance_of_infection

    window.setup(simulation_parameters)
    arcade.run()
    plot_results(window)

    window.close()


if __name__ == "__main__":
    main()
    print("Done")
