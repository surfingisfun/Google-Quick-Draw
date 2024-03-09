from flask import Flask, render_template, request, jsonify
import requests
import random

app = Flask(__name__)

# Home page that will show the category selection and grid options
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

import random

@app.route('/draw', methods=['POST'])
def draw():
    category = request.form['category']
    rows = int(request.form['rows'])
    columns = int(request.form['columns'])

    drawings = load_drawings(category)
    svgs = []

    # Generate SVGs for the specified grid size
    for _ in range(rows * columns):
        drawing = random.choice(drawings)
        svgs.append(drawing_to_svg(drawing))

    # Pass the SVGs list to the template
    return render_template('drawings.html', svgs=svgs, rows=rows, columns=columns)



import ndjson

def load_drawings(category):
    with open(f'{category}.ndjson') as f:
        data = ndjson.load(f)
    return data

# Example usage
drawings = load_drawings('cat')  # Assuming you have 'cat.ndjson

def drawing_to_svg(drawing, width=200, height=200):
    """Converts Quick, Draw! drawing to SVG path."""
    svg_path = "<svg width='{}' height='{}' xmlns='http://www.w3.org/2000/svg'>".format(width, height)
    for stroke in drawing['drawing']:
        path_data = " ".join(["{},{}".format(x, y) for x, y in zip(stroke[0], stroke[1])])
        svg_path += "<polyline points='{}' stroke='black' fill='none' stroke-width='2'/>".format(path_data)
    svg_path += "</svg>"
    return svg_path
