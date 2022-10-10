import os
import binascii
import numpy as np


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

    ### Gene structure
    Each gene has a 32 bit sequence - 8 hex digits:

    ☐|☐☐☐☐|☐|☐☐|☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
    - 1st bit: indicates if source neuron is input/inner/output neuron.
    - Next 4 bits: identify source neuron.
    - Next 1 bit: indicates if target neuron is input/inner/output neuron.
    - Next 2 bits: identify target neuron.
    - Next 24 bits: represent the weight of the connection.
    """

    NUM_INPUT_NEURONS = 16
    NUM_INNER_NEURONS = 4
    NUM_OUTPUT_NEURONS = 4
    GENE_LENGTH = 32
    GENE_LENGTH_HEX = 8
    NEURON_TYPES = ['input', 'inner', 'output']

    def __init__(
        self,
        hex_gene_sequence: str = None,
        bin_gene_sequence: str = None,
    ) -> None:
        assert(
            (hex_gene_sequence and not bin_gene_sequence)
            or (not hex_gene_sequence and bin_gene_sequence)
        ), "Only one gene sequence must be passed."
        
        if hex_gene_sequence:
            assert(
                len(hex_gene_sequence) % self.GENE_LENGTH_HEX == 0
            ), f"Length of 'hex_gene_sequence' must be multiple of {self.GENE_LENGTH_HEX}."
            self.hex_genes = [''.join(e) for e in zip(*[iter(hex_gene_sequence)]*self.GENE_LENGTH_HEX)]
            self.bin_genes = [bin(int(g, 16))[2:].zfill(self.GENE_LENGTH) for g in self.hex_genes]
        else:
            self.bin_genes = [''.join(e) for e in zip(*[iter(bin_gene_sequence)]*self.GENE_LENGTH)]
        
        self.express_genes()

    @classmethod
    def init_random_genes(cls, num_genes):
        hex_gene_sequence = binascii.b2a_hex(os.urandom(num_genes*4)).decode()
        return cls(hex_gene_sequence=hex_gene_sequence)

    def express_genes(self):
        self.input_inner_tensor = np.zeros((self.NUM_INPUT_NEURONS, self.NUM_INNER_NEURONS))
        self.inner_output_tensor = np.zeros((self.NUM_INNER_NEURONS, self.NUM_OUTPUT_NEURONS))

        self.inner_inner_tensor = np.zeros((self.NUM_INNER_NEURONS, self.NUM_INNER_NEURONS))
        self.input_output_tensor = np.zeros((self.NUM_INPUT_NEURONS, self.NUM_OUTPUT_NEURONS))
        for gene in self.bin_genes:
            # print(gene)
            source_neuron_type = self.NEURON_TYPES[int(gene[0])]
            # print(f"SOURCE_NEURON_TYPE: {source_neuron_type}")
            source_neuron_id = int(gene[1:1+4], 2) if source_neuron_type == 'input' else int(gene[3:3+2], 2)
            # print(f"SOURCE_NEURON_ID: {source_neuron_id}")

            target_neuron_type = self.NEURON_TYPES[int(gene[5])+1]
            # print(f"TARGET_NEURON_TYPE: {target_neuron_type}")
            target_neuron_id = int(gene[6:6+2], 2)
            # print(f"TARGET_NEURON_ID: {target_neuron_id}")

            weight = int(gene[8:], 2)
            # print(f"WEIGHT: {weight}\n")

            if source_neuron_type == 'input' and target_neuron_type == 'inner':
                self.input_inner_tensor[source_neuron_id, target_neuron_id] = weight
            elif source_neuron_type == 'inner' and target_neuron_type == 'output':
                self.inner_output_tensor[source_neuron_id, target_neuron_id] = weight
            elif source_neuron_type == 'inner' and target_neuron_type == 'inner':
                self.inner_inner_tensor[source_neuron_id, target_neuron_id] = weight
            elif source_neuron_type == 'input' and target_neuron_type == 'output':
                self.input_output_tensor[source_neuron_id, target_neuron_id] = weight
        # print(self.input_inner_tensor)

    def output(self, input_vector):
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
    print(brain.act(np.asarray([1]*16).reshape(1, -1)))