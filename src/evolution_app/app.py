import os
from itertools import product
from typing import List, Tuple, Dict
from flask import Flask, render_template, send_from_directory, request, jsonify, Response, stream_with_context
from objects.individual import Individual, Brain
from evolution import create_population, evolve


app = Flask(
    __name__,
    static_url_path='',
    static_folder='web/static',
    template_folder='web/templates',
)

DEFAULT_POP_SIZE = 80
DEFAULT_NUM_GENERATIONS = 100
DEFAULT_LIFESPAN = 60
DEFAULT_WORLD_SIZE: Tuple[int, int] = (150, 150)
DEFAULT_NUM_GENES: int = 6
MAX_GENERATIONS: int = 10000
DEFAULT_MUTE_PROBABILITY: float = 0.0001
DEFAULT_MATE_PROBABILITY: float = 0.5

world_size: Tuple[int, int] = DEFAULT_WORLD_SIZE
num_generations: int = DEFAULT_NUM_GENERATIONS
lifespan: int = DEFAULT_LIFESPAN
num_genes: int = DEFAULT_NUM_GENES
mute_probability: float = DEFAULT_MUTE_PROBABILITY
mate_probability: float = DEFAULT_MATE_PROBABILITY
step_idx: int = 0
generation_idx: int = 0

current_coordinates: List[Tuple[int, int]] = None
population: List[Individual] = None
death_boxes: List[Tuple[Tuple[int, int], Tuple[int, int]]] = None
safe_boxes: List[Tuple[Tuple[int, int], Tuple[int, int]]] = None
heat_sources: List[Tuple[int, int]] = None


@app.route('/')
def root():
    global DEFAULT_NUM_GENERATIONS
    global MAX_GENERATIONS
    global DEFAULT_POP_SIZE
    return render_template(
        'root.html',
        world_size=world_size,
        gen_num=0,
        max_generations=MAX_GENERATIONS,
        num_generations=DEFAULT_NUM_GENERATIONS,
        pop_size=DEFAULT_POP_SIZE,
    )


@app.route('/update_population')
def update_population():
    global population
    global current_coordinates
    global lifespan
    global world_size
    global num_genes

    population, current_coordinates = create_population(
        population_size=int(request.args['pop_size']),
        lifespan=lifespan,
        world_size=world_size,
        num_genes=num_genes,
    )
    return jsonify([{'coords': ind.coords, 'color': ind.color} for ind in population])


@app.route('/update_world_size')
def update_world_size():
    global world_size
    global population
    world_size = (int(request.args['worldY']), int(request.args['worldX']))
    for ind in population:
        ind.world_size = world_size
    return f"world_size={world_size}"


@app.route('/update_lifespan')
def update_lifespan():
    global lifespan
    global population
    lifespan = int(request.args['lifespan'])
    for ind in population:
        ind.lifespan = lifespan
    return f"lifespan={lifespan}"


@app.route('/update_num_genes')
def update_num_genes():
    global num_genes
    global population
    num_genes = int(request.args['num_genes'])
    for ind in population:
        ind.brain = Brain.init_random_genes(num_genes)
        ind.express_color()
    return jsonify([{'coords': ind.coords, 'color': ind.color} for ind in population])


@app.route('/update_num_generations')
def update_num_generations():
    global num_generations
    num_generations = int(request.args['num_generations'])
    print(f"num_generations={num_generations}")


@app.route('/update_mute_probability')
def update_mute_probability():
    global mute_probability
    mute_probability = int(request.args['mute_probability'])
    print(f"mute_probability={mute_probability}")


@app.route('/update_mate_probability')
def update_mate_probability():
    global mate_probability
    mate_probability = int(request.args['mate_probability'])
    print(f"mate_probability={mate_probability}")


@app.route('/update_generation_idx')
def update_generation_idx():
    global generation_idx
    generation_idx = int(request.args['generation_idx'])
    print(f"generation_idx={generation_idx}")


@app.route('/update_step_idx')
def update_step_idx():
    global step_idx
    step_idx = int(request.args['step_idx'])
    print(f"step_idx={step_idx}")


@app.route('/evolve_step')
def evolve_step():
    global population
    global current_coordinates
    global lifespan
    global world_size
    global num_genes
    global num_generations
    global mute_probability
    global mate_probability

    population, current_coordinates = evolve(
        population_size=len(population),
        num_genes=num_genes,
        world_size=world_size,
        num_generations=num_generations,
        lifespan=lifespan,
        start_generation=int(request.args['generationIdx']),
        end_generation=min(num_generations-1, int(request.args['generationIdx'])+1),
        start_step=int(request.args['stepIdx']),
        end_step=min(num_generations-1, int(request.args['stepIdx'])+1),
        mute_probability=mute_probability,
        mate_probability=mate_probability,
        death_boxes=None,
        safe_boxes=[
            ((0,0), (20, 15))
        ],
        heat_sources=[],
        population=population,
    )
    return jsonify([{'coords': ind.coords, 'hex_gene_sequence': ind.brain.hex_gene_sequence} for ind in population])


@app.route('/grid')
def grid():
    def inner():
        for i in range(10):
            yield f"<div>This is {i}</div>"
    return Response(inner(), mimetype='text/html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'web', 'static', 'images'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon',
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)