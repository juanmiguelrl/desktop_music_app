#!/usr/bin/env python3

from p1 import e2e
import atspi_dump

import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi

#desktop = Atspi.get_desktop(0)
#process,app = e2e.run('../src/p1.py')
#atspi_dump.dump_desktop()
#e2e.tree(app)
#print(app2.get_name())
#name = app.get_name()

#desktop = e2e.Atspi.get_desktop(0)
#e2e.stop(process)

#Ctx = namedtuple("Ctx", "../src/ipm-p1.py")



###############defs######################
def when_pulso_boton(tipo,nombre,ctx):
    boton = interface_contiene_boton(tipo,nombre,ctx.app)
    e2e.do_action(boton,'click')
    return ctx

def given_app_launched(ctx):
    process,app = e2e.run(ctx.path)
    assert app is not None
    return e2e.Ctx(path=ctx.path,process=process,app=app)

def then_veo_boton_descendente(ctx):
    boton = interface_contiene_boton('radio button','Descendente',ctx.app)
    return ctx

def when_pulso_boton_descendente(ctx):
    return when_pulso_boton('radio button','Descendente',ctx)

def then_veo_boton_3M(ctx):
    interface_contiene_boton('push button','Tercera mayor (3M)',ctx.app)
    return ctx

def when_pulso_boton_3M(ctx):
    return when_pulso_boton('push button','Tercera mayor (3M)',ctx)

def interface_contiene_boton(rol,nombre,app):
    boton = next( (obj for _path,obj in e2e.tree(app) if obj.get_role_name() == rol and obj.get_name() == nombre), None)
    assert boton is not None
    return boton

def then_veo_barra_busqueda(ctx):
    interface_contiene_boton('text','Buscar',app)

def texto_barra_busqueda(ctx,texto):
    barra = interface_contiene_boton('text','Buscar',ctx.app)
    assert barra.get_text(0,-1) == texto
    return ctx

def then_veo_boton_cancion_representativa(ctx):
    boton = interface_contiene_boton('radio button','Canción representativa',ctx.app)
    return ctx

def when_pulso_boton_cancion_representativa(ctx):
    boton = interface_contiene_boton('radio button','Canción representativa',ctx.app)
    e2e.do_action(boton,'click')
    return ctx

def then_veo_label_resultados(ctx,nombre):
    label = interface_contiene_boton('label',nombre,ctx.app)
    return ctx

def then_veo_label_cancion(ctx,nombre):
    label = interface_contiene_boton('label',nombre,ctx.app)
    return ctx

def when_escribo(ctx,texto):
    barra = interface_contiene_boton('text','Buscar',ctx.app)
    barra.insert_text(0,texto,6)
    e2e.do_action(barra,'activate')
    return ctx

def then_veo_boton_mostrar_mas_canciones(ctx):
    boton = interface_contiene_boton('push button','Mostrar más canciones',ctx.app)
    return ctx

def when_pulso_boton_mostrar_mas_canciones(ctx):
    return when_pulso_boton('push button','Mostrar más canciones',ctx)

def then_veo_lista_canciones(ctx):
    ctx = then_veo_label_cancion(ctx,'Título: Alcohol, alcohol\nFavorita: SI')
    ctx = then_veo_label_cancion(ctx,'Título: Summertime (Jazz Standard)\nFavorita: NO')
    ctx = then_veo_label_cancion(ctx,'Título: Giant steps (John Coltrane)\nFavorita: NO')
    ctx = then_veo_label_cancion(ctx,"Título: Shoo fly, dont bother me (Canción infantil)'\nFavorita: NO")
    ctx = then_veo_label_cancion(ctx,'Título: Good night ladies \nFavorita: NO')
    return ctx

#############################################################
######################ejecucion pruebas######################
#############################################################

########prueba 1########
initial_ctx = e2e.Ctx(path='../src/ipm-p1.py',process = None,app = None)

e2e.show("""
GIVEN he_lanzado_la_aplicación
THEN veo_boton_descendente
AND veo_boton_3M
""")
ctx = initial_ctx
try:
    ctx = given_app_launched(ctx)
    ctx = then_veo_boton_descendente(ctx)
    ctx = then_veo_boton_3M(ctx)
    e2e.show_passed()
except Exception as e:
    e2e.show_not_passed(e)
e2e.stop(ctx.process)
########prueba 2########
initial_ctx = e2e.Ctx(path='../src/ipm-p1.py',process = None,app = None)

e2e.show("""
GIVEN he_lanzado_la_aplicación
WHEN pulso_boton_descendente
AND pulso_boton_3M
THEN veo_texto_barra_busqueda Resultados para "3M_des"
AND then_veo_label_resultados Resultados para "3M_des"
""")
ctx = initial_ctx
try:
    ctx = given_app_launched(ctx)
    ctx = when_pulso_boton_descendente(ctx)
    ctx = when_pulso_boton_3M(ctx)
    ctx = texto_barra_busqueda(ctx,'3M_des')
    ctx = then_veo_label_resultados(ctx,'Resultados para "3M_des"')
    e2e.show_passed()
except Exception as e:
    e2e.show_not_passed(e)
e2e.stop(ctx.process)

########prueba 3########
initial_ctx = e2e.Ctx(path='../src/ipm-p1.py',process = None,app = None)

e2e.show("""
GIVEN he_lanzado_la_aplicación
WHEN escribo 3M_des
THEN veo_texto_barra_busqueda Resultados para "3M_des"
AND then_veo_label_resultados Resultados para "3M_des"
""")
ctx = initial_ctx
try:
    ctx = given_app_launched(ctx)
    ctx = when_escribo(ctx,'3M_des')
    ctx = texto_barra_busqueda(ctx,'3M_des')
    ctx = then_veo_label_resultados(ctx,'Resultados para "3M_des"')
    e2e.show_passed()
except Exception as e:
    e2e.show_not_passed(e)
e2e.stop(ctx.process)

########prueba 4########
initial_ctx = e2e.Ctx(path='../src/ipm-p1.py',process = None,app = None)

e2e.show("""
GIVEN he_lanzado_la_aplicación
WHEN pulso_boton_descendente
AND pulso_boton_3M
THEN veo_texto_barra_busqueda Resultados para "3M_des"
AND then_veo_label_resultados Resultados para "3M_des"
AND then_veo_boton_cancion_representativa(app)
WHEN pulso_boton_cancion_representativa
AND veo_cancion_favorita
AND veo_botón "mostrar más canciones"
""")
ctx = initial_ctx
try:
    ctx = given_app_launched(ctx)
    ctx = when_pulso_boton_descendente(ctx)
    ctx = when_pulso_boton_3M(ctx)
    ctx = texto_barra_busqueda(ctx,'3M_des')
    ctx = then_veo_label_resultados(ctx,'Resultados para "3M_des"')
    ctx = then_veo_boton_cancion_representativa(ctx)
    ctx = when_pulso_boton_cancion_representativa(ctx)
    ctx = then_veo_label_cancion(ctx,'Título: Alcohol, alcohol\nFavorita: SI')
    ctx = then_veo_boton_mostrar_mas_canciones(ctx)
    e2e.show_passed()
except Exception as e:
    e2e.show_not_passed(e)
e2e.stop(ctx.process)

########prueba 5########
initial_ctx = e2e.Ctx(path='../src/ipm-p1.py',process = None,app = None)

e2e.show("""
GIVEN he_lanzado_la_aplicación
WHEN pulso_boton_descendente
AND pulso_boton_3M
AND pulso_boton_cancion_representativa
AND pulso_botón "mostrar más canciones
THEN veo_lista_canciones
""")
ctx = initial_ctx
try:
    ctx = given_app_launched(ctx)
    ctx = when_pulso_boton_descendente(ctx)
    ctx = when_pulso_boton_3M(ctx)
    ctx = when_pulso_boton_cancion_representativa(ctx)
    ctx = when_pulso_boton_mostrar_mas_canciones(ctx)
    ctx = then_veo_lista_canciones(ctx)
    e2e.show_passed()
except Exception as e:
    e2e.show_not_passed(e)
e2e.stop(ctx.process)

    