import os
from itertools import product
from typing import List, Tuple, Dict
from flask import Flask, render_template, send_from_directory, request, jsonify, Response, stream_with_context
from objects.individual import Individual
from evolution import initialize_coordinates, create_population, evolve


def generate_grid_array(world_size, coordinates):
    return [
        {
            'row': cell[0],
            'col': cell[1],
            'background-color': 'red' if cell in coordinates else 'white',
        }
        for cell in product(range(world_size[0]), range(world_size[1]))
    ]


app = Flask(
    __name__,
    static_url_path='',
    static_folder='web/static',
    template_folder='web/templates',
)

DEFAULT_POP_SIZE = 10
DEFAULT_NUM_GENERATIONS = 2
MAX_GENERATIONS: int = 10000
STEP: int = 0
GEN: int = 0
world_size: Tuple[int, int] = (100, 100)
coordinates: List[Tuple[int, int]] = initialize_coordinates(pop_size=DEFAULT_POP_SIZE, world_size=world_size)
grid_array: List[Dict] = generate_grid_array(world_size, coordinates)
population: List[Individual] = None
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


@app.route('/update_pop_size')
def update_pop_size():
    global population
    global coordinates
    global world_size
    world_size = (int(request.args['maxY']), int(request.args['maxX']))
    coordinates = initialize_coordinates(pop_size=int(request.args['pop_size']), world_size=world_size)
    return jsonify(coordinates)


@app.route('/start')
def start():
    global population
    global coordinates
    global world_size
    print('Starting evolution')
    population = create_population(coordinates=coordinates, lifetime=2, world_size=world_size)
    return "Genesis"


@app.route('/evolve')
def evolve():
    global population
    global coordinates
    global world_size
    return Response(
        stream_with_context(evolve(
            population=population,
            num_generations=2,
            lifetime=2,
            heat_sources=[],
        ))
    )


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
    app.run(debug=True)