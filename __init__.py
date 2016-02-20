from flask import Flask, render_template
from flask import request
import sqlite3
import pandas as pd
import pygal
from pygal.style import Style

app = Flask(__name__)


DATABASE = '/home/fedecarles/asmd/ASMD.db'


def connect_to_database():
        return sqlite3.connect(DATABASE)

c = connect_to_database()
df = pd.read_sql_query("SELECT * FROM entidades", c)
df['counts'] = df.groupby('entidad')['entidad'].transform('count')
df['dateStamp'] = pd.to_datetime(df['dateStamp'], format="%Y-%m-%d")
df = df[df.counts > 20]
df = df.sort('counts', ascending=False)
entidades = df[['entidad', 'valor', 'counts']].groupby('entidad', sort=False).mean()


@app.route('/', methods=["GET", "POST"])
def homepage():
    t = []
    texto = []
    subset = pd.DataFrame()
    desc = pd.DataFrame()
    sources = pd.DataFrame()
    graph_data = []
    fuente = []
    urls = []
    if request.method == 'POST':
        t = request.form.get('entidades', None)
        subset = df[df.entidad == t]
        subset = subset.sort(['dateStamp'])
        texto = list(subset['adjetivo'])
        ultima_semana = subset['dateStamp'].iloc[-7]
        ultimo_subset = subset[subset.dateStamp == ultima_semana]
        fuente = list(pd.unique(ultimo_subset.fuente.ravel()))

        desc = (ultimo_subset[['adjetivo', 'valor']].groupby('adjetivo').sum().
                sort('valor', ascending=False))

        urls = list(pd.unique(ultimo_subset.link.ravel()))
        titles = list(pd.unique(ultimo_subset.titulo.ravel()))
        sources = pd.DataFrame(urls, titles)


        custom_style = Style(background='transparent',
                             plot_background='transparent',
                             title_font_size=32)

        graph = pygal.Line(show_legend=False, x_label_rotation=20, width=1500,
                           height=450, explicit_size=True, range=(-1, 1),
                           background="transparent", foreground="transparent",
                           plot_background="transparent", margin=0,
                           style=custom_style, show_minor_x_labels = False)

        graph.title = "Sentimiento para '"+t+"'"
        agg = subset.groupby('dateStamp').mean()
        graph.add(t, list(agg['valor']))
        date = pd.DatetimeIndex(agg.index)
        graph.x_labels_major = date[0::10]
        graph.x_labels = map(str, date)
        graph.x_labels_major = map(str, date[0::5])
        graph_data = graph.render_data_uri()

    return render_template('index.html', entidades=entidades, texto=texto,
                           fuente=fuente, graph_data=graph_data, desc=desc,
                           subset=subset, sources=sources)



@app.route('/comofunciona/', methods=["GET", "POST"])
def comofunciona():
    return render_template('comofunciona.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run()