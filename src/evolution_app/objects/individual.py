from math import dist
import numpy as np
from typing import Tuple, List, Optional
from .brain import Brain
# from .keras_brain import Brain as KerasBrain


class Individual():
    """Class representing an Individual.

    Args:
        initial_coords (Tuple[int, int]): _description_
        lifespan (int): _description_
        world_size (Tuple[int, int]): _description_
    """

    DEFAULT_NUM_GENES: int = 30
    HEAT_RISK_THRESHOLD: int = 0.1

    def __init__(
        self,
        individual_id: str,
        lifespan: int,
        world_size: Tuple[int, int],
        initial_coords: Optional[Tuple[int, int]] = None,
        num_genes: Optional[int] = None,
    ) -> None:
        self.id = individual_id
        self.brain = Brain.init_random_genes(num_genes or self.DEFAULT_NUM_GENES)
        self.coords = initial_coords
        self.lifespan = lifespan
        self.world_size = world_size
        self.input_vector = None
        self.alive = True
        self.step = 0
        self.express_color()

    def express_color(self):
        self.color = self.brain.hex_gene_sequence

    def sense_env(
        self,
        mate_coordinates: List[Tuple[int, int]],
        heat_sources: List[Tuple[int, int]],
    ):
        heat_risk = 0
        if heat_sources:
            try:
                heat_risk = np.round(np.sum([1/dist(self.coords, heat) for heat in heat_sources]), 3)
                if heat_risk > self.HEAT_RISK_THRESHOLD:
                    self.alive = False
            except ZeroDivisionError:
                self.alive = False

        if self.alive:
            self.input_vector = np.array([
                np.uint16(self.coords[0]),  # distance to the top
                np.uint16(self.world_size[0] - self.coords[0] - 1),  # distance to the bottom
                np.uint16(self.coords[1]),  # distance to the left wall
                np.uint16(self.world_size[1] - self.coords[1] - 1),  # distance to the right wall
                np.uint8((self.coords[0] - 1, self.coords[1] - 1) in mate_coordinates),  # top left
                np.uint8((self.coords[0] - 1, self.coords[1]) in mate_coordinates),  # top
                np.uint8((self.coords[0] - 1, self.coords[1] + 1) in mate_coordinates),  # top right
                np.uint8((self.coords[0], self.coords[1] - 1) in mate_coordinates),  # left
                np.uint8((self.coords[0], self.coords[1] + 1) in mate_coordinates),  # right
                np.uint8((self.coords[0] + 1, self.coords[1] - 1) in mate_coordinates),  # bottom left
                np.uint8((self.coords[0] + 1, self.coords[1]) in mate_coordinates),  # bottom
                np.uint8((self.coords[0] + 1, self.coords[1] + 1) in mate_coordinates),  # bottom right
                heat_risk,  # burn risk
                np.round(self.step/self.lifespan, 3),  # lifespan
                (np.random.rand() - 0.5),  # random
                (np.random.rand() - 0.5),  # random
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

        move_positive_threshold = 0.0
        move_negative_threshold = -0.0

        coords_delta = [0, 0]
        if output[0] > move_positive_threshold:
            coords_delta[0] = 1
        elif output[0] < move_negative_threshold:
            coords_delta[0] = -1

        if output[1] > move_positive_threshold:
            coords_delta[1] = 1
        elif output[1] < move_negative_threshold:
            coords_delta[1] = -1
        
        if coords_delta != [0, 0]:
            new_coords = tuple(sum(e) for e in zip(self.coords, coords_delta))
            if self.valid_coordinates(new_coords, mate_coordinates):
                self.coords = new_coords

        self.step += 1
        return output

    def mute(self, mute_probability: float) -> None:
        """Mute function.

        Args:
            mute_probability (float): _description_
        """
        new_hex_gene_sequence = ''.join([
            (
                hex(np.random.randint(0, 16))[2:]
                if np.random.rand() < mute_probability
                else self.brain.hex_gene_sequence[i]
            )
            for i in range(len(self.brain.hex_gene_sequence))
        ])
        if new_hex_gene_sequence != self.brain.hex_gene_sequence:
            self.brain.hex_gene_sequence = new_hex_gene_sequence
            self.brain.express_genes()


def mate(
    ind1: Individual,
    ind2: Individual,
    mate_probability: float,
    child1_id: str,
    child2_id: str,
) -> Tuple[Individual, Individual]:
    """Mate function.

    Args:
        ind1 (Individual): _description_
        ind2 (Individual): _description_
        mate_probability (float): _description_

    Returns:
        Tuple[Individual, Individual]: _description_
    """
    if np.random.rand() < mate_probability:
        child1 = Individual(
            individual_id=child1_id,
            initial_coords=None,
            lifespan=ind1.lifespan,
            world_size=ind1.world_size,
        )
        child2 = Individual(
            individual_id=child2_id,
            initial_coords=None,
            lifespan=ind2.lifespan,
            world_size=ind2.world_size,
        )
        
        half_sequence = int(len(ind1.brain.hex_gene_sequence)/2)
        child1_seq = ind1.brain.hex_gene_sequence[:half_sequence] + ind2.brain.hex_gene_sequence[half_sequence:]
        child2_seq = ind2.brain.hex_gene_sequence[:half_sequence] + ind1.brain.hex_gene_sequence[half_sequence:]
        child1.brain = Brain(hex_gene_sequence=child1_seq)
        child1.express_color()
        child2.brain = Brain(hex_gene_sequence=child2_seq)
        child2.express_color()
        return (child1, child2)
    else:
        return (None, None)
