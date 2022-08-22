import json
import random
from itertools import product
from typing import List, Tuple
from individual import Individual


population: List[Individual] = None
coordinates: List[Tuple[int, int]] = None
hot_sources: List[Tuple[int, int]] = None


def initialize_coordinates(pop_size: int, world_size: Tuple[int, int]):
    allCoords = [coord for coord in product(range(world_size[0]), range(world_size[1]))]
    random.shuffle(allCoords)
    if pop_size > len(allCoords):
        print('muy grande')
        return None
    return allCoords[:pop_size]


def create_population(
    coordinates: List[Tuple[int, int]],
    lifetime: int,
    world_size: Tuple[int, int],
):
    return [Individual(initial_coords=coord, lifetime=lifetime, world_size=world_size) for coord in coordinates]


def evolve(
    population: List[Individual],
    num_generations: int,
    lifetime: int,
    heat_sources: Tuple[int, int] = [],
):
    for gen_i in range(num_generations):
        for step_i in range(lifetime):
            for ind in population:
                coordinates = [e.coords for e in population]
                ind.sense_env(mate_coordinates=coordinates, heat_sources=heat_sources)
                ind.take_step(mate_coordinates=coordinates)
            yield json.dumps({
                'generation': gen_i,
                'step': step_i,
                'coordinates': [e.coords for e in population]
            })
        # TODO: mating and muting
        coordinates = initialize_coordinates(pop_size=len(population), world_size=population[0].world_size)


if __name__ == '__main__':
    POP_SIZE = 32
    WORLD_SIZE = (150, 150)

    HEAT_SOURCES = []
    LIFETIME = 10
    NUM_GENERATIONS = 10

    coordinates = initialize_coordinates(pop_size=POP_SIZE, world_size=WORLD_SIZE)
    print(coordinates)

    population = create_population(coordinates=coordinates, lifetime=LIFETIME, world_size=WORLD_SIZE)
    print(population)

    evolve(population=population, num_generations=NUM_GENERATIONS, lifetime=LIFETIME, heat_sources=HEAT_SOURCES)
