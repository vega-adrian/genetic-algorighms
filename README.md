# Genetic algorithms (WIP)
This repo implements an evolution app. The population consists of a bunch of individuals that will try to survive in a given environment.

The environment has some characteristics, such as:
- **World size**: the world we'll create is a 2-D world with a given height and a given width.
- **Population size**: we define the number of individuals we want to create as the initial population.
- **Max number of generations**: the number of generations we want our population to evolve.
- **Death boxes**: we can define rectangles within our 2-D world where every individual that lies in them won't survive and won't be able to reproduce and replicate its DNA to the next generation.
- **Safe boxes**: as the opposite of death boxes, we can define rectangles where every individual lying in them will survive and thus will have the opportunity to reproduce itself.
- **Mate probability**: we can stablish a probability of mating. Once the individuals survived they can mate with other individuals with certain probability.
- **Mute probability**: every descendant will mute its gene sequence with certain probability than we can define.

Each of the individuals has certain features as well, such as:
- **Gene sequence**: this sequence will characterize the individual and the neuron connections within its brain.
- **Brain**: each individual has a brain that is modeled as a *neural network*. The connections among the neurons are defined by the gene sequence.
- **ID**: each individual has a unique ID based on 
- **Lifespan**: in each generation, the individuals have a lifespan, i.e. number of steps they can take.
- **Coordinates**: each individual has a pair of coordinates that places them in the 2-D world. This coordinates get updated during the lifespan of the the individual.

## Brain

### Gene sequence

### Neural network configuration

## Usage
```
python evolution_app.py
```

## Build docker image