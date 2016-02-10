Este sitio "lee" la sección de política de los principales sitios de noticias
de Argentina y realiza un simple análisis de sentimiento.

En primer lugar, se detectan las **entidades mencionadas**. Estas entidades
pueden ser personas, lugares geográficos, países, instutuciones
gubernamentales, compañias, etc.

Luego, sobre cada oración donde se encuentra una (1) entidad mencionada, se
buscan las **palabras asociadas**, que fueron previamente clasificadas como
positivas o negativas (con valores de 1 y -1 respectivamente). Dicha clasificación se hizo de forma mixta,
utilizando métodos automáticos para la mayoría, pero con revisiones
manuales.

Por último se computa el sentimiento para cada entidad y cada día, como la
media de la suma de las palabras asociadas positivas y negativas.

Este modelo también se conoce como "bolsa de palabras", es relativamente
simple y su extensión es limitada. Su principal limitación es que no permite
detectar correctamente polaridades más sofisticadas. Por ejemplo, si una
oración dice "Buenos Aires no es una buena ciudad...", el modelo
identificaría "buena", como una palabra positiva, aunque el significado de
la oración es claramente negativo. Del mismo modo, los valores asigandos a
las palabas asociadas están sujetos a interpretaciones diferentes.

Aun con estos problemas, el modelo de bolsa de palabras puede proporcionar un buen
punto de partida para hacer análisis de sentimiento más sofisticados, lo
cual me anoto como tarea pendiente.</p>

#### Referencias
Este sitio está inspirado en [Sentdex](1) y en los tutoriales de
[Python Programming](2). Excelente recurso para aprender Python.

Las herramientas utilizadas son:

* [Python 2.7](3) + [Flask](4) para el web framework.
* [Bootstrap](5)
* [Pygal](6) para los gráficos.

Los sitios de noticias analizados por ahora son los siguientes, aunque
la idea es seguir añadiendo más:

* [La Nación](7)
* [Clarín](8)
* [Página 12](9)
* [Infobae](10)

[1] http://sentdex.com/
[2] https://pythonprogramming.net/
[3] https://www.python.org/
[4] http://flask.pocoo.org/
[5] http://getbootstrap.com/
[6] http://www.pygal.org/en/latest/
[7] http://www.lanacion.com.ar/
[8] http://www.clarin.com/
[9] http://www.pagina12.com.ar
[10] http://www.infobae.com/
