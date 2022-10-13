import json
import random
from itertools import product
from typing import List, Tuple, Optional
from objects.individual import Individual


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
    return [
        Individual(
            individual_id=f'ind_{i}',
            initial_coords=coord,
            lifetime=lifetime,
            world_size=world_size,
        )
        for i, coord in enumerate(coordinates)
    ]


def evolve(
    population: List[Individual],
    num_generations: int,
    lifetime: int,
    start_generation: int = 0,
    start_step: int = 0,
    mute_probability: Optional[float] = None,
    mate_probability: Optional[float] = None,
    heat_sources: Tuple[int, int] = [],
):
    for gen_i in range(start_generation, num_generations):
        print(f"Generation #{gen_i}/{num_generations}")
        for step_i in range(start_step, lifetime):
            for ind in population:
                current_coordinates = [e.coords for e in population]
                ind.sense_env(mate_coordinates=current_coordinates, heat_sources=heat_sources)
                output = ind.take_step(mate_coordinates=current_coordinates)
                # print(output)
                # print(ind.coords)
            iteration_info = {
                'generation': gen_i,
                'step': step_i,
                'current_coordinates': [e.coords for e in population]
            }
            # json.dumps(iteration_info)

        if mute_probability:
            for ind in population:
                ind.mute(mute_probability=mute_probability)
        if mate_probability:
            print("Let's procreate.")
        # TODO: removing all dead individuals, mating and muting
        # coordinates = initialize_coordinates(pop_size=len(population), world_size=population[0].world_size)
        print([e.coords for e in population])


if __name__ == '__main__':
    POP_SIZE = 10
    WORLD_SIZE = (150, 150)

    HEAT_SOURCES = []
    LIFETIME = 100
    NUM_GENERATIONS = 2

    MUTE_PROBABILITY = 0.01
    MATE_PROBABILITY = 0.01

    coordinates = initialize_coordinates(pop_size=POP_SIZE, world_size=WORLD_SIZE)
    print(coordinates)

    population = create_population(coordinates=coordinates, lifetime=LIFETIME, world_size=WORLD_SIZE)

    evolve(population=population, num_generations=NUM_GENERATIONS, lifetime=LIFETIME, heat_sources=HEAT_SOURCES)
