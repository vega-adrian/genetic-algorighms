import random
from math import dist
from tabnanny import verbose
import numpy as np
from typing import Tuple, List, Union
from tensorflow import keras


class Brain():
    """Brain object.

    Each brain step will sensor the environment and take a decision.

    ### Inputs

    - Positioning neurons:
        - 00: distance to the top.
        - 01: distance to the bottom.
        - 02: distance to the left wall.
        - 03: distance to the right wall.
    - Obstacle binary neurons:
        - 04: top left cell is blocked/open.
        - 05: top cell is blocked/open.
        - 06: top right cell is blocked/open.
        - 07: left cell is blocked/open.
        - 08: right cell is blocked/open.
        - 09: bottom left cell is blocked/open.
        - 10: bottom cell is blocked/open.
        - 11: bottom right cell is blocked/open.
    - Danger neurons:
        - 12: burn risk measure (sum of the inverse distance to heat sources).
    - Age neuron:
        - 13: life measure (step/max_steps).
    - Random neurons:
        - 14: random valued neuron.
        - 15: random valued neuron.
    ### Outputs
    - 00: move left/right, negative values left, positive values, right.
    - 01: move up/down, negative is up, positive is down.
    - 02: kill closest individual.
    """

    NUM_INPUT_NEURONS = 16
    NUM_INNER_NEURONS = 1
    NUM_OUTPUT_NEURONS = 3

    def __init__(self) -> None:
        self.input_layer = keras.Input(shape=(Brain.NUM_INPUT_NEURONS,), dtype='int32', name='sensory')
        #self.inner_layer = keras.layers.Dense(Brain.NUM_INNER_NEURONS, activation='tanh', name='internal')(self.input_layer)
        self.output_layer = keras.layers.Dense(Brain.NUM_OUTPUT_NEURONS, activation='tanh', name='output')(self.input_layer)
        self.nn = keras.Model(inputs=[self.input_layer], outputs=[self.output_layer])

    def output(self, input_vector):
        return self.nn.predict(input_vector, verbose=0)[0]


class Individual():
    """Class representing an Individual.

    Args:
        initial_coords (Tuple[int, int]): _description_
        lifetime (int): _description_
        world_size (Tuple[int, int]): _description_
    """

    DEFAULT_NUM_GENES = 4

    def __init__(
        self,
        initial_coords: Tuple[int, int],
        lifetime: int,
        world_size: Tuple[int, int],
    ) -> None:
        self.brain = Brain()
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
            print('I feel like murdering')

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
            print(f"Not a valid coord: {new_coords}")
            if new_coords in mate_coordinates:
                print(f"Because there is someone else")

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