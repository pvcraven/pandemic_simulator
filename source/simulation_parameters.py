from dataclasses import dataclass


@dataclass
class SimulationParameters:
    population_count: int
    person_size: int
    frames_to_result: int
    chance_of_infection: float
    chance_for_immunity: float
    chance_for_death: float
    initial_top_speed: int
    reporting_interval: int
    initial_infected_people: int
    initial_immune_people: int
    vertical_walls: int
    door_size: int
