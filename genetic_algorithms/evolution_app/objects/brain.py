import os
import binascii
import numpy as np
from typing import List, Literal


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
    - 03: not defined.

    ### Gene structure
    Each gene has a 32 bit sequence - 8 hex digits:

    ☐|☐☐☐☐|☐|☐☐|☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
    - Bit 0: indicates if source neuron is input/inner/output neuron.
    - Bits 1:5 (4 bits): identify source neuron.
    - Bit 5: indicates if target neuron is input/inner/output neuron.
    - Bits 6:8 (2 bits): identify target neuron.
    - Bits 8:32 (24 bits): represent the weight of the connection. Numbers between -8388608 and +8388607. So the \
        numbers are scaled by 2e6 so that the range is between -4.1943 and +4.1943.
    """

    NUM_INPUT_NEURONS: Literal[16] = 16
    NUM_INNER_NEURONS: Literal[4] = 4
    NUM_OUTPUT_NEURONS: Literal[4] = 4
    GENE_LENGTH: Literal[32] = 32
    GENE_LENGTH_HEX: Literal[8] = 8
    NEURON_TYPE_INPUT: Literal['input'] = 'input'
    NEURON_TYPE_INNER: Literal['inner'] = 'inner'
    NEURON_TYPE_OUTPUT: Literal['output'] = 'output'
    NEURON_TYPES: List[str] = [NEURON_TYPE_INPUT, NEURON_TYPE_INNER, NEURON_TYPE_OUTPUT]
    # CONNECTION_WEIGHT_SCALE: float = 2e6
    CONNECTION_WEIGHT_SCALE: float = 1e6

    def __init__(
        self,
        hex_gene_sequence: str,
    ) -> None:
        assert(
            len(hex_gene_sequence) % self.GENE_LENGTH_HEX == 0
        ), f"Length of 'hex_gene_sequence' must be multiple of {self.GENE_LENGTH_HEX}."

        self.hex_gene_sequence = hex_gene_sequence
        self.express_genes()

    @classmethod
    def init_random_genes(cls, num_genes: int):
        hex_gene_sequence = binascii.b2a_hex(os.urandom(num_genes*4)).decode()
        return cls(hex_gene_sequence=hex_gene_sequence)

    def express_genes(self):
        self.hex_genes = [''.join(e) for e in zip(*[iter(self.hex_gene_sequence)]*self.GENE_LENGTH_HEX)]
        self.bin_genes = [bin(int(g, 16))[2:].zfill(self.GENE_LENGTH) for g in self.hex_genes]

        self.input_inner_tensor = np.zeros((self.NUM_INPUT_NEURONS, self.NUM_INNER_NEURONS))
        self.inner_output_tensor = np.zeros((self.NUM_INNER_NEURONS, self.NUM_OUTPUT_NEURONS))

        self.inner_inner_tensor = np.zeros((self.NUM_INNER_NEURONS, self.NUM_INNER_NEURONS))
        self.input_output_tensor = np.zeros((self.NUM_INPUT_NEURONS, self.NUM_OUTPUT_NEURONS))
        for gene in self.bin_genes:
            # print(gene)
            source_neuron_type = self.NEURON_TYPES[int(gene[0])]
            # print(f"SOURCE_NEURON_TYPE: {source_neuron_type}")
            source_neuron_id = (
                int(gene[1:1+4], 2)
                if source_neuron_type == self.NEURON_TYPE_INPUT
                else int(gene[3:3+2], 2)
            )
            # print(f"SOURCE_NEURON_ID: {source_neuron_id}")

            target_neuron_type = self.NEURON_TYPES[int(gene[5])+1]
            # print(f"TARGET_NEURON_TYPE: {target_neuron_type}")
            target_neuron_id = int(gene[6:6+2], 2)
            # print(f"TARGET_NEURON_ID: {target_neuron_id}")


            weight = -int(gene[8] + ''.join(['0']*(self.GENE_LENGTH - 8 -1)), 2) + int(gene[9:], 2)
            weight = weight/self.CONNECTION_WEIGHT_SCALE
            # print(f"WEIGHT: {weight}\n")

            if source_neuron_type == self.NEURON_TYPE_INPUT and target_neuron_type == self.NEURON_TYPE_INNER:
                self.input_inner_tensor[source_neuron_id, target_neuron_id] = weight
            elif source_neuron_type == self.NEURON_TYPE_INNER and target_neuron_type == self.NEURON_TYPE_OUTPUT:
                self.inner_output_tensor[source_neuron_id, target_neuron_id] = weight
            elif source_neuron_type == self.NEURON_TYPE_INNER and target_neuron_type == self.NEURON_TYPE_INNER:
                self.inner_inner_tensor[source_neuron_id, target_neuron_id] = weight
            elif source_neuron_type == self.NEURON_TYPE_INPUT and target_neuron_type == self.NEURON_TYPE_OUTPUT:
                self.input_output_tensor[source_neuron_id, target_neuron_id] = weight
        # print(self.input_inner_tensor)

    def output(self, input_vector: np.ndarray) -> np.ndarray:
        input_inner_sum = input_vector @ self.input_inner_tensor
        inner_inner_sum = input_inner_sum @ self.inner_inner_tensor

        inner_result = np.tanh(input_inner_sum + inner_inner_sum)
        inner_output_sum = inner_result @ self.inner_output_tensor
        input_output_sum = input_vector @ self.input_output_tensor

        output_sum = np.tanh(inner_output_sum + input_output_sum)
        return output_sum.ravel()


if __name__ == '__main__':
    num_genes = 2
    brain = Brain.init_random_genes(num_genes)
    print(brain.output(np.asarray([1]*16).reshape(1, -1)))