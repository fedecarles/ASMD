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


@app.route('/', methods=["GET", "POST"])
def homepage():
    c = connect_to_database()
    df = pd.read_sql_query("SELECT * FROM entidades", c)
    df['counts'] = df.groupby('entidad')['entidad'].transform('count')
    df['dateStamp'] = pd.to_datetime(df['dateStamp'], format="%Y-%m-%d")
    df = df[df.counts > 20]
    df = df.sort('counts', ascending=False)

    entidades = df[['entidad', 'valor', 'counts']].groupby('entidad', sort=False).mean()



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
        subset = subset.sort(['dateStamp'])
        texto = list(subset['adjetivo'])
        fuente = list(pd.unique(subset.fuente.ravel()))
        desc = (subset[['adjetivo', 'valor']].groupby('adjetivo').sum().
                sort('valor', ascending=False))
        urls = list(pd.unique(subset.link.ravel()))
        titulares = list(pd.unique(subset.titulo.ravel()))
        noticias = pd.DataFrame(urls[:10], titulares[:10])

        custom_style = Style(background='transparent',
                             plot_background='transparent',
                             title_font_size=32, label_font_size=18)

        graph = pygal.Line(show_legend=False, x_label_rotation=20, width=1500,
                           height=450, explicit_size=True, range=(-1, 1),
                           background="transparent", foreground="transparent",
                           plot_background="transparent", margin=0,
                           style=custom_style)

        graph.title = "Sentimiento para '"+t+"'"
        agg = subset.groupby('dateStamp').mean()
        graph.add(t, list(agg['valor']))
        date = pd.DatetimeIndex(agg.index).normalize()
        # date = agg.index.apply(pd.datetools.normalize_date)
        graph.x_labels = map(str, date)
        graph_data = graph.render_data_uri()

    return render_template('index.html', entidades=entidades, texto=texto,
                           fuente=fuente, graph_data=graph_data, desc=desc,
                           noticias=noticias, subset=subset)


@app.route('/comofunciona/', methods=["GET", "POST"])
def comofunciona():
    return render_template('comofunciona.html')


if __name__ == "__main__":
    app.run()
