#!/usr/bin/python3
import dash
import math

import dash_cytoscape as cyto
import dash_html_components as html

app = dash.Dash(__name__)

nodes = [
    {
        'data': {'id': short, 'label': label}
    }
    for short, label in (
        ('la', 'Los Angeles'),
        ('nyc', 'New York'),
        ('to', 'Toronto'),
        ('mtl', 'Montreal'),
        ('van', 'Vancouver'),
        ('chi', 'Chicago'),
        ('bos', 'Boston'),
        ('hou', 'Houston')
    )
]

edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        ('van', 'la'),
        ('la', 'chi'),
        ('hou', 'chi'),
        ('to', 'mtl'),
        ('mtl', 'bos'),
        ('nyc', 'bos'),
        ('to', 'hou'),
        ('to', 'nyc'),
        ('la', 'nyc'),
        ('nyc', 'bos')
    )
]
elements = nodes + edges
import code
code.interact(local=locals())

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-layout-6',
        elements=elements,
        style={'width': '100%', 'height': '350px'},
        layout={
            'name': 'breadthfirst',
            'roots': '[id = "nyc"]'
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
