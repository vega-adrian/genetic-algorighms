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