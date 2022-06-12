from flask import Flask, redirect, render_template, request, url_for
from flask_example import app
from flask_example.input import CourseForm
from flask_example import Rainbow_matching as rm


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import networkx as nx
import io
import base64


@app.route('/', methods=('GET', 'POST'))
def index():
    form = CourseForm()
    if form.validate_on_submit():
        global size
        size = form.size.data
        global k
        k = form.k.data
        return redirect(url_for('add_colors'))
    return render_template('main.html', form=form)

@app.route('/add_edges/', methods=('GET', 'POST'))
def add_colors():
    if request.method == 'POST':
        img = io.BytesIO()
        G = nx.path_graph(size)
        pos = nx.spring_layout(G, seed=47)  # Seed layout for reproducibility
        for i in range(size-1):
            select = request.form.get(str(i))
            G.edges[i,i+1]["color"] = select

        Res = rm.rainbow_matching(G, k)
        if not Res.edges:
            return redirect(url_for('no_result'))
        for i in range(size-1):
            width = 2
            if ((i,i+1) in Res.edges):
                width = 8
            nx.draw_networkx(G,
                             pos=pos,
                             edgelist=[(i, i + 1)],
                             width=width,
                             edge_color=color_graph(G.edges[i,i+1]["color"]))
        plt.savefig(img, format='png')
        plt.clf()
        img.flush()
        img.seek(0)
        global plot_graph_url
        plot_graph_url = base64.b64encode(img.getvalue()).decode()
        return redirect(url_for('result'))
    colours = ["Blue", "Orange", "Green", "Red", "Purple", "Brown", "Pink", "Gray"]
    return render_template('colors.html', size = range(size-1), colours=colours)


@app.route('/result/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        form = CourseForm()
        return redirect(url_for('index'))
    return render_template('result.html', plot_url=plot_graph_url)

@app.route('/no-result/', methods=['GET', 'POST'])
def no_result():
    if request.method == 'POST':
        form = CourseForm()
        return redirect(url_for('index'))
    return render_template('no-result.html')


def color_graph(color):
    if color == "Blue":
        return "tab:blue"
    elif color == "Orange":
        return "tab:orange"
    elif color == "Green":
        return "tab:green"
    elif color == "Red":
        return "tab:red"
    elif color == "Purple":
        return "tab:purple"
    elif color == "Brown":
        return "tab:brown"
    elif color == "Pink":
        return "tab:pink"
    elif color == "Gray":
        return "tab:gray"


#if __name__ == '__main__':
#    app.run(debug=True)