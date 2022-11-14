import copy
import time
import json
import numpy as np
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
    population_size: int,
    lifetime: int,
    world_size: Tuple[int, int],
    num_genes: Optional[int] = None,
) -> List[Individual]:
    return [
        Individual(
            individual_id=f'individual_{i}',
            lifetime=lifetime,
            world_size=world_size,
            num_genes=num_genes,
        )
        for i in range(population_size)
    ]


def print_status(
    world_size,
    current_coordinates,
    heat_sources = [],
    message='',
):
    print('\n'*2 + f"{message:#^{(2*world_size[1]+1)}}")
    for r in range(world_size[0]):
        print('|', end='')
        for c in range(world_size[1]):
            if (r, c) in heat_sources:
                print('X|', end='')
            elif (r, c) in current_coordinates:
                print('o|', end='')
            else:
                print(' |', end='')
        print()
        print('_' + '__'*world_size[1])


def evolve(
    population_size: int,
    num_genes: int,
    world_size: Tuple[int, int],
    num_generations: int,
    lifetime: int,
    start_generation: int = 0,
    start_step: int = 0,
    mute_probability: Optional[float] = None,
    mate_probability: Optional[float] = None,
    death_boxes: List[Tuple[Tuple[int, int], Tuple[int, int]]] = None,
    safe_boxes: List[Tuple[Tuple[int, int], Tuple[int, int]]] = None,
    heat_sources: Tuple[int, int] = [],
):
    population = create_population(
        population_size=population_size,
        lifetime=lifetime,
        world_size=world_size,
        num_genes=num_genes,
    )
    last_survival_rate = 1
    last_survival_type = 'Only new'
    for gen_i in range(start_generation, num_generations):
        print(f"Generation #{gen_i}/{num_generations}")
        generation_size = len(population)
        if generation_size == 0:
            print("Evolution did not succeed.")
            break
        current_coordinates = initialize_coordinates(
            pop_size=generation_size,
            world_size=world_size,
        )
        for coords, ind in zip(current_coordinates, population):
            ind.coords = coords

        for step_i in range(start_step, lifetime):
            for ind in population:
                ind.sense_env(mate_coordinates=current_coordinates, heat_sources=heat_sources)
                if ind.alive is False:
                    population.remove(ind)
                else:
                    _ = ind.take_step(mate_coordinates=current_coordinates)
                current_coordinates = [e.coords for e in population]
            if True:#gen_i == num_generations - 1:
                time.sleep(0.05)
                print_status(
                    world_size=world_size,
                    current_coordinates=current_coordinates,
                    heat_sources=heat_sources,
                    message=(
                        f" Gen {gen_i}/{num_generations}, "
                        f"step {step_i}/{lifetime}, "
                        f"pop size {generation_size} "
                        f"{last_survival_type}, "
                        f"last gen survival rate: {(100*last_survival_rate):.2f}% "
                    ),
                )

        survivors = []
        if safe_boxes:
            survivors += [
                ind
                for ind in population
                if ind.alive and any([
                    (
                        ind.coords[0] >= safe_box[0][0] and ind.coords[0] <= safe_box[1][0]
                        and ind.coords[1] >= safe_box[0][1] and ind.coords[1] <= safe_box[1][1]
                    )
                    for safe_box in safe_boxes
                ])
            ]
        if death_boxes:
            survivors += [
                ind
                for ind in population
                if ind.alive and not any([
                    (
                        ind.coords[0] >= death_box[0][0] and ind.coords[0] <= death_box[1][0]
                        and ind.coords[1] >= death_box[0][1] and ind.coords[1] <= death_box[1][1]
                    )
                    for death_box in death_boxes
                ])
            ]

        num_survivors = len(survivors)
        last_survival_rate = num_survivors/generation_size

        new_generation = []
        for i, (ind1, ind2) in enumerate(combinations(survivors, 2)):
            child1, child2 = mate(
                ind1=ind1,
                ind2=ind2,
                mate_probability=mate_probability,
                child1_id=f"individual_gen{gen_i}_{i}_1",
                child2_id=f"individual_gen{gen_i}_{i}_2",
            )
            if child1 and child2:
                new_generation += [child1, child2]
        num_children = len(new_generation)
        random.shuffle(new_generation)

        if num_children >= population_size:
            population = new_generation[:population_size]
            last_survival_type = 'only new'
        elif num_survivors + num_children >= population_size:
            random.shuffle(survivors)
            population = new_generation + survivors[:population_size-num_children]
            last_survival_type = 'new and some old'
        else:
            random.shuffle(survivors)
            last_survival_type = 'cloned'
            individuals_left = population_size - num_children - num_survivors
            clones = []
            if num_children > 0:
                clones += [
                    copy.copy(new_generation[i%num_children])
                    for i in range(int(np.ceil(individuals_left/2)))
                ]
            if num_survivors > 0:
                clones += [
                    copy.copy(survivors[i%len(survivors)])
                    for i in range(int(individuals_left/2))
                ]
            population = new_generation + survivors + clones

        if mute_probability:
            for ind in population:
                ind.mute(mute_probability=mute_probability)


if __name__ == '__main__':
    POP_SIZE = 200
    WORLD_SIZE = (20, 60)

    HEAT_SOURCES = []
    LIFETIME = 50
    NUM_GENERATIONS = 100
    NUM_GENES = 20

    MUTE_PROBABILITY = 0
    MATE_PROBABILITY = 0.02

    DEATH_BOXES = [
        ((0,0), (20, 45)),
        # ((10,0), (20, 60))
    ]
    SAFE_BOXES = [
        # ((5,15), (15, 45))
    ]
    evolve(
        population_size=POP_SIZE,
        num_genes=NUM_GENES,
        world_size=WORLD_SIZE,
        num_generations=NUM_GENERATIONS,
        lifetime=LIFETIME,
        mute_probability=MUTE_PROBABILITY,
        mate_probability=MATE_PROBABILITY,
        death_boxes=DEATH_BOXES,
        safe_boxes=SAFE_BOXES,
        heat_sources=HEAT_SOURCES,
    )
