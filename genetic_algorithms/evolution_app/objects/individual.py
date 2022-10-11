import random
from math import dist
import numpy as np
from typing import Tuple, List
from .brain import Brain
# from .keras_brain import Brain as KerasBrain


class Individual():
    """Class representing an Individual.

    Args:
        initial_coords (Tuple[int, int]): _description_
        lifetime (int): _description_
        world_size (Tuple[int, int]): _description_
    """

    DEFAULT_NUM_GENES = 57

    def __init__(
        self,
        initial_coords: Tuple[int, int],
        lifetime: int,
        world_size: Tuple[int, int],
    ) -> None:
        self.brain = Brain.init_random_genes(self.DEFAULT_NUM_GENES)
        # self.brain = KerasBrain()
        self.coords = initial_coords
        self.lifetime = lifetime
        self.world_size = world_size
        self.input_vector = None
        self.alive = True
        self.step = 0
        self.color = None
    
    def sense_env(
        self,
        mate_coordinates: List[Tuple[int, int]],
        heat_sources: List[Tuple[int, int]],
    ):
        try:
            heat_risk = round(sum([1/dist(self.coords, heat) for heat in heat_sources]), 3)
        except ZeroDivisionError:
            self.alive = False
        
        if heat_risk > 10000:
            self.alive = False

        self.input_vector = np.asarray([
            self.coords[0],  # distance to the top
            self.world_size[0] - self.coords[0] - 1,  # distance to the bottom
            self.coords[1],  # distance to the left wall
            self.world_size[1] - self.coords[1] - 1,  # distance to the right wall
            int((self.coords[0] - 1, self.coords[1] - 1) in mate_coordinates),  # top left
            int((self.coords[0] - 1, self.coords[1]) in mate_coordinates),  # top left
            int((self.coords[0] - 1, self.coords[1] + 1) in mate_coordinates),  # top right
            int((self.coords[0], self.coords[1] - 1) in mate_coordinates),  # left
            int((self.coords[0], self.coords[1] + 1) in mate_coordinates),  # right
            int((self.coords[0] + 1, self.coords[1] - 1) in mate_coordinates),  # bottom left
            int((self.coords[0] + 1, self.coords[1]) in mate_coordinates),  # bottom
            int((self.coords[0] + 1, self.coords[1] + 1) in mate_coordinates),  # bottom right
            heat_risk,  # burn risk
            round(self.step/self.lifetime, 3),  # lifespan
            (random.random() - 0.5)*4,  # random
            (random.random() - 0.5)*4,  # random
        ]).reshape(1, -1)
    
    def valid_coordinates(self, coords: Tuple[int, int], mate_coordinates: List[Tuple[int, int]]):
        return (
            coords[0] >= 0
            and coords[1] >= 0
            and coords[0] < self.world_size[0]
            and coords[1] < self.world_size[1]
            and coords not in mate_coordinates
        )

    def take_step(self, mate_coordinates: List[Tuple[int, int]]):
        output = self.brain.output(self.input_vector)

        kill_threshold = 1
        if output[2] > kill_threshold:
            pass
            # print('I feel like murdering')

        move_positive_threshold = 0.1
        move_negative_threshold = -0.1

        new_coords = None
        if output[0] > 0 and output[1] > 0:
            if output[0] > move_positive_threshold and output[1] > move_positive_threshold:
                # move bottom right
                new_coords = (self.coords[0] + 1, self.coords[1] + 1)
            elif output[0] > move_positive_threshold:
                # move bottom
                new_coords = (self.coords[0] + 1, self.coords[1])
            elif output[1] > move_positive_threshold:
                # move right
                new_coords = (self.coords[0], self.coords[1] + 1)
        elif output[0] > 0 and output[1] < 0:
            if output[0] > move_positive_threshold and output[1] < move_negative_threshold:
                # move bottom left
                new_coords = (self.coords[0] + 1, self.coords[1] - 1)
            elif output[0] > move_positive_threshold:
                # move bottom
                new_coords = (self.coords[0] + 1, self.coords[1])
            elif output[1] < move_negative_threshold:
                # move left
                new_coords = (self.coords[0], self.coords[1] - 1)
        elif output[0] < 0 and output[1] > 0:
            if output[0] < move_negative_threshold and output[1] > move_positive_threshold:
                # move top right
                new_coords = (self.coords[0] - 1, self.coords[1] + 1)
            elif output[0] < move_negative_threshold:
                # move top
                new_coords = (self.coords[0] - 1, self.coords[1])
            elif output[1] > move_positive_threshold:
                # move right
                new_coords = (self.coords[0], self.coords[1] + 1)
        elif output[0] < 0 and output[1] < 0:
            if output[0] < move_negative_threshold and output[1] < move_negative_threshold:
                # move top left
                new_coords = (self.coords[0] - 1, self.coords[1] - 1)
            elif output[0] < move_negative_threshold:
                # move top
                new_coords = (self.coords[0] - 1, self.coords[1])
            elif output[1] < move_negative_threshold:
                # move left
                new_coords = (self.coords[0], self.coords[1] - 1)

        if new_coords and self.valid_coordinates(new_coords, mate_coordinates):
            self.coords = new_coords
        else:
            pass
            # print(f"Not a valid coord: {new_coords}")
            # if new_coords in mate_coordinates:
            #     print(f"Because there is someone else")

        self.step += 1
        return output


def mate(ind1: Individual, ind2: Individual, mate_prob: float):
    """Mate function.

    Args:
        ind1 (Individual): _description_
        ind2 (Individual): _description_
        mate_prob (float): _description_

    Returns:
        Tuple[Individual, Individual]: _description_
    """
    if random.random() < mate_prob:
        return (ind1, ind2)


def mute(ind: Individual, mute_prob: float) -> None:
    """Mute function.

    Args:
        ind (Individual): _description_
        mute_prob (float): _description_
    """
    if random.random() < mute_prob:
        pass