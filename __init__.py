from flask import Flask, render_template
from flask import request
import sqlite3
import pandas as pd
import pygal


app = Flask(__name__)


DATABASE = '/home/fedecarles/asmd/ASMD.db'


def connect_to_database():
        return sqlite3.connect(DATABASE)


@app.route('/', methods=["GET", "POST"])
def homepage():
    c = connect_to_database()
    df = pd.read_sql_query("SELECT * FROM entidades", c)
    df['counts'] = df.groupby('entidad')['entidad'].transform('count')
    df = df[df.counts > 10]
    df = df.sort('counts', ascending=False)
    entidades = list(pd.unique(df.entidad.ravel()))
    t = []
    texto = []
    subset = pd.DataFrame()
    desc = pd.DataFrame()
    noticias = pd.DataFrame()
    graph_data = []
    fuente = []
    urls = []
    if request.method == 'POST':
        t = request.form.get('entidades')
        subset = df[df.entidad == t]
        texto = list(subset['adjetivo'])
        fuente = list(pd.unique(subset.fuente.ravel()))
        desc = (subset[['adjetivo', 'valor']].groupby('adjetivo').sum().
                sort('valor', ascending=False))
        urls = list(pd.unique(subset.link.ravel()))
        titulares = list(pd.unique(subset.titulo.ravel()))
        noticias = pd.DataFrame(urls[:20], titulares[:20])

        graph = pygal.Line(show_legend=False, x_label_rotation=20, width=1500,
                           height=530, explicit_size=True, range=(-1, 1),
                           background="transparent", foreground="transparent",
                           plot_background="transparent")
        graph.title = "Sentimiento para "+t
        date = set(subset['dateStamp'])
        graph.x_labels = map(str, date)
        agg = subset.groupby('dateStamp').mean()
        graph.add(t, list(agg['valor']))
        graph_data = graph.render_data_uri()

    return render_template('index.html', entidades=entidades, texto=texto,
                           fuente=fuente, graph_data=graph_data, desc=desc,
                           noticias=noticias, subset=subset)


if __name__ == "__main__":
    app.run()
