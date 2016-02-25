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
df['dateStamp'] = pd.to_datetime(df['dateStamp'], format="%Y-%m-%d")
df['counts'] = df.groupby('entidad')['entidad'].transform('count')
df = df.sort(['counts', 'dateStamp'], ascending=False)

# Estas son las entidades que aparecen en el listado de la izquierda.
# Cada entidad esta asociada su ultimo valor medio, que indica si esta
# en alza o en baja. Primero se agrupan las por entidad y fecha.
# Luego se agrupa nuevamente extrayendo el primer valor (o sea el ultimo dia)
# para cada entidad.
entities = df[['entidad', 'dateStamp', 'valor']].groupby(['entidad','dateStamp'],sort=False).mean()
entities = entities.reset_index()
entities= entities.groupby(['entidad'], sort=False).head(1)



@app.route('/', methods=["GET", "POST"])
def homepage():

    # Contenedores locales.
    selected_entity = []
    se_subset = pd.DataFrame()
    asociated_words = pd.DataFrame()
    sources = pd.DataFrame()
    graph_data = []

    # Las lineas que siguen son las acciones del lado del servidor que
    # corren cada vez que el usuario hace click en una entidad.

    if request.method == 'POST':
        selected_entity = request.form.get('entidades', None)
        se_subset = df[df.entidad == selected_entity]
        se_subset = se_subset.sort(['dateStamp'])
        last_week_days = se_subset['dateStamp'].iloc[-7]
        last_week_subset = se_subset[se_subset.dateStamp == last_week_days]


        asociated_words = (last_week_subset[['adjetivo', 'valor']]
                           .groupby('adjetivo').sum()
                           .sort('valor', ascending=False))

        urls = list(pd.unique(last_week_subset.link.ravel()))
        titles = list(pd.unique(last_week_subset.titulo.ravel()))
        sources = pd.DataFrame(urls, titles)

        # Creacion del grafico con Pygal.

        custom_style = Style(background='transparent',
                             plot_background='transparent',
                             title_font_size=32)

        graph = pygal.Line(show_legend=False, x_label_rotation=20, width=1500,
                           height=450, explicit_size=True, range=(-1.2, 1.2),
                           background="transparent", foreground="transparent",
                           plot_background="transparent", margin=0,
                           style=custom_style, show_minor_x_labels = False)

        graph.title = "Sentimiento para '"+selected_entity+"'"
        agg = se_subset.groupby('dateStamp').mean()
        graph.add(selected_entity, list(agg['valor']))
        date = pd.DatetimeIndex(agg.index)
        graph.x_labels = map(str, date)
        graph.x_labels_major = map(str, date[0::5])
        graph_data = graph.render_data_uri()

    return render_template('index.html', entities=entities,
                           graph_data=graph_data,
                           asociated_words=asociated_words,
                           se_subset=se_subset, sources=sources)



@app.route('/comofunciona/', methods=["GET", "POST"])
def comofunciona():
    return render_template('comofunciona.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run()