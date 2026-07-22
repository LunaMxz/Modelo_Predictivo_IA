from componentes.header import mostrar_header
from componentes.hero import mostrar_hero
from componentes.estado import mostrar_estado
from componentes.pronostico_ia import mostrar_pronostico_ia
from componentes.sensores import mostrar_sensores
from componentes.resumen import mostrar_resumen
from componentes.actividad import mostrar_actividad
from componentes.footer import mostrar_footer


def mostrar_inicio(df):

    mostrar_header(df)

    mostrar_hero()

    mostrar_estado(df)

    mostrar_pronostico_ia(df)

    mostrar_sensores(df)

    mostrar_resumen(df)

    mostrar_actividad(df)

    mostrar_footer(df)