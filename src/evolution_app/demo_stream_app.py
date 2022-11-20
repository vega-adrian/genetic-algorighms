from flask import Flask, Response, render_template, request
import time


app = Flask(
    __name__,
    static_url_path='',
    static_folder='web/static',
    template_folder='web/templates',
)


@app.route('/')
def root():
    return render_template('demo_index.html')


@app.route('/stream')
def stream():
    args = request.args
    return {'text': f"This is iteration {args['it']}"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)