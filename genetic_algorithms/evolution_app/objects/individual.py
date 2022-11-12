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

    DEFAULT_NUM_GENES: int = 6
    HEAT_RISK_THRESHOLD: int = 1000

    def __init__(
        self,
        individual_id: str,
        initial_coords: Tuple[int, int],
        lifetime: int,
        world_size: Tuple[int, int],
    ) -> None:
        self.id = individual_id
        self.brain = Brain.init_random_genes(self.DEFAULT_NUM_GENES)
        # self.brain = KerasBrain()
        self.coords = initial_coords
        self.lifetime = lifetime
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
        try:
            heat_risk = round(sum([1/dist(self.coords, heat) for heat in heat_sources]), 3)
        except ZeroDivisionError:
            self.alive = False
        
        if heat_risk > self.HEAT_RISK_THRESHOLD:
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
            (np.random.rand() - 0.5)*4,  # random
            (np.random.rand() - 0.5)*4,  # random
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
                # print(f"Ind {self.id} has changed coordinates from {self.coords} to {new_coords}")
                self.coords = new_coords
        #     else:
        #         print(f"Not a valid coord: {new_coords} {'Because there is someone else' if new_coords in mate_coordinates else ''}")
        # else:
        #     print("Didn't move")

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
            lifetime=ind1.lifetime,
            world_size=ind1.world_size,
        )
        child2 = Individual(
            individual_id=child2_id,
            initial_coords=None,
            lifetime=ind2.lifetime,
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
