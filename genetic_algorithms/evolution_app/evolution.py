import time
import json
import random
from itertools import product, combinations
from typing import List, Tuple, Optional
from objects.individual import Individual, mate


def initialize_coordinates(
    pop_size: int,
    world_size: Tuple[int, int],
) -> List[Tuple[int, int]]:
    every_coord = [coord for coord in product(range(world_size[0]), range(world_size[1]))]
    if pop_size > len(every_coord):
        raise Exception(f"Population size of {pop_size} is too big for a {world_size} world.")
    else:
        random.shuffle(every_coord)
        return every_coord[:pop_size]


def create_population(
    coordinates: List[Tuple[int, int]],
    lifetime: int,
    world_size: Tuple[int, int],
) -> List[Individual]:
    return [
        Individual(
            individual_id=f'individual_{i}',
            initial_coords=coord,
            lifetime=lifetime,
            world_size=world_size,
        )
        for i, coord in enumerate(coordinates)
    ]


def print_status(world_size, current_coordinates, message=''):
    print('\n'*2 + f"{message:#^{(2*world_size[1]+1)}}")
    for r in range(world_size[0]):
        print('|', end='')
        for c in range(world_size[1]):
            if (r, c) in current_coordinates:
                print('o|', end='')
            else:
                print(' |', end='')
        print()
        print('_' + '__'*world_size[1])


def evolve(
    population: List[Individual],
    world_size: Tuple[int, int],
    num_generations: int,
    lifetime: int,
    start_generation: int = 0,
    start_step: int = 0,
    mute_probability: Optional[float] = None,
    mate_probability: Optional[float] = None,
    death_rectangles: List[Tuple[Tuple[int, int], Tuple[int, int]]] = None,
    heat_sources: Tuple[int, int] = [],
):
    initial_population_size = len(population)
    for gen_i in range(start_generation, num_generations):
        print(f"Generation #{gen_i}/{num_generations}")
        current_coordinates = initialize_coordinates(
            pop_size=len(population),
            world_size=world_size,
        )
        for coords, ind in zip(current_coordinates, population):
            ind.coords = coords

        for step_i in range(start_step, lifetime):
            for ind in population:
                ind.sense_env(mate_coordinates=current_coordinates, heat_sources=heat_sources)
                output = ind.take_step(mate_coordinates=current_coordinates)
                current_coordinates = [e.coords for e in population]
            time.sleep(0.05)
            print_status(world_size=world_size, current_coordinates=current_coordinates, message=f"Gen {gen_i}/{num_generations}")

        if death_rectangles:
            population = [
                ind
                for ind in population
                if not any([
                    (
                        ind.coords[0] >= death_rectangle[0][0] and ind.coords[0] <= death_rectangle[1][0]
                        and ind.coords[1] >= death_rectangle[0][1] and ind.coords[1] <= death_rectangle[1][1]
                    )
                    for death_rectangle in death_rectangles
                ])
            ]
        if heat_sources:
            print('heat sources')

        new_generation = []
        for ind1, ind2 in combinations(population, 2):
            child1, child2 = mate(
                ind1=ind1,
                ind2=ind2,
                mate_probability=mate_probability,
                child1_id=f"individual_{len(population)}",
                child2_id=f"individual_{len(population)+1}",
            )
            if child1 and child2:
                new_generation += [child1, child2]
        random.shuffle(new_generation)
        random.shuffle(population)
        population = new_generation + population + population
        population = population[:initial_population_size + 5]

        if mute_probability:
            for ind in population:
                ind.mute(mute_probability=mute_probability)
        time.sleep(0.5)


if __name__ == '__main__':
    POP_SIZE = 200
    WORLD_SIZE = (20, 70)

    HEAT_SOURCES = []
    LIFETIME = 50
    NUM_GENERATIONS = 100

    MUTE_PROBABILITY = 0.0001
    MATE_PROBABILITY = 0.01

    DEATH_RECTANGLES = [
        ((0, 0), (20, 30)),
        ((15, 0), (20, 70)),
    ]

    coordinates = initialize_coordinates(pop_size=POP_SIZE, world_size=WORLD_SIZE)
    print(coordinates)

    population = create_population(coordinates=coordinates, lifetime=LIFETIME, world_size=WORLD_SIZE)

    evolve(
        population=population,
        world_size=WORLD_SIZE,
        num_generations=NUM_GENERATIONS,
        lifetime=LIFETIME,
        mute_probability=MUTE_PROBABILITY,
        mate_probability=MATE_PROBABILITY,
        death_rectangles=DEATH_RECTANGLES,
        heat_sources=HEAT_SOURCES,
    )
