#!/usr/bin/python3

######################################
#
#   Copyright (C) 2019 P.L. Lucas
#
#
# LICENSE: BSD
# You may use this file under the terms of the BSD license as follows:
#
# "Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of developers or companies in the above copyright, Digia Plc and its 
#     Subsidiary(-ies) nor the names of its contributors may be used to 
#     endorse or promote products derived from this software without 
#     specific prior written permission.
#
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
#
#
######################################/


import feedparser
import sqlite3
import calendar
import time
import threading
import sys
import webbrowser

def procesar_blog(sql_conn, blog):
    d = feedparser.parse(blog)
    sql_cursor = sql_conn.cursor()
    for post in d.entries:
        fecha = None
        if 'updated_parsed' in post  and post.updated_parsed != None:
            fecha = post.updated_parsed
        elif 'published_parsed' in post and post.published_parsed != None:
            fecha = post.published_parsed
        elif 'published' in post and post.published != None:
            fecha = post.published
        if fecha==None or not isinstance(fecha,time.struct_time):
            #print(post)
            continue
        #print(fecha)
        sql_cursor.execute("""
            insert or replace into feeds (blog, titulo, enlace, fecha)
            values(?, ?, ?, ?);
        """, (d.feed.title, post.title, post.link, calendar.timegm(fecha)) )
    sql_conn.commit()

def limpiar_base_datos(sql_conn):
    # Se eliminan todas las entradas con una antigüedad de 1 año
    sql_cursor = sql_conn.cursor()
    fecha_hace_un_agno = int(time.time()) - 365*24*60*60
    sql_cursor.execute("delete from feeds where fecha<? ", (fecha_hace_un_agno,))
    sql_conn.commit()

def cabecera_html(fout):
    fin = open("cabecera.html", 'r')
    for line in fin:
        fout.write(line)
    fin.close()

def pie_html(fout):
    fin = open("pie.html", 'r')
    for line in fin:
        fout.write(line)
    fin.close()

def generar_html(sql_conn):
    n = 0
    pagina = 0
    sql_cursor = sql_conn.cursor()
    archivo_actual = 'index.html'.format(pagina)
    archivo_anterior = None
    fout = open('salida/index.html'.format(pagina), 'w')
    cabecera_html(fout)
    # Sólo se muestran las entradas con fecha menor a la actual
    for row in sql_cursor.execute("select blog, titulo, enlace, fecha from feeds where fecha<? order by fecha desc", (int(time.time()),)):
        n += 1
        fecha = time.gmtime(int(row[3]))
        fout.write("""
        <tr>
            <td class='col_blog'>{0}</td><td class='col_fecha'>{3}</td>
            <td class='col_enlace'><a href='{2}' target='blank'>{1}</a></td>
        </tr>
        """.format(row[0], row[1], row[2], "{0}-{1}-{2}".format(fecha[0], fecha[1], fecha[2])))
        if n % 1000 == 0:
            pagina += 1
            fout.write('</table>')
            archivo_siguiente = 'pagina-{0}.html'.format(pagina)
            fout.write("<p>")
            if archivo_anterior!= None:
                fout.write("<a href='{0}'>Anterior</a> | ".format(archivo_anterior))
            fout.write("<a href='{0}'>Siguiente</a></p>".format(archivo_siguiente))
            archivo_anterior = archivo_actual
            archivo_actual = archivo_siguiente
            pie_html(fout)
            fout.close()
            fout = open('salida/pagina-{0}.html'.format(pagina), 'w')
            cabecera_html(fout)
    fout.write('</table>')
    if archivo_anterior!= None:
        fout.write("<p><a href='{0}'>Anterior</a></p>".format(archivo_anterior))
    pie_html(fout)
    fout.close()

def generar_rss(sql_conn):
    n = 0
    sql_cursor = sql_conn.cursor()
    fout = open('salida/feed.xml', 'w')
    fout.write("""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>\n""")
    fin = open('config.txt', 'r')
    fout.write(fin.read())
    fin.close()
    for row in sql_cursor.execute("select blog, titulo, enlace, fecha from feeds order by fecha desc"):
        n += 1
        fecha = time.gmtime(int(row[3]))
        fout.write("""
            <item>
            <title>{blog}: {titulo}</title>
            <link>{enlace}</link>
            <description>{titulo}</description>
            <pubDate>{fecha}</pubDate>
            </item>""".format(blog=row[0], titulo=row[1], enlace=row[2], fecha=time.asctime(fecha)))
        if n > 10:
            break
    fout.write("</channel>\n</rss>")
    fout.close()
 

# Esta clase sirve para gestionar los hilos
class Hilos(threading.Thread):
    def __init__(self, blog, semaforo):
        threading.Thread.__init__(self)
        self.sql_conn = None 
        self.blog = blog
        self.semaforo = semaforo

    def run(self):
        self.semaforo.acquire()
        print('Procesando... {0}'.format(self.blog))
        self.sql_conn = sqlite3.connect('feeds.db')
        procesar_blog(self.sql_conn, self.blog)
        self.sql_conn.commit()
        self.sql_conn.close()
        self.semaforo.release()


# Se abre/crea la base de datos de feeds
# TODO: Hacer una segunda tabla con el nombre del blog
sql_conn = sqlite3.connect('feeds.db')
sql_cursor = sql_conn.cursor()
sql_cursor.execute("""
    create table if not exists feeds
    (
        blog text, titulo text, enlace text, fecha int,
        primary key (enlace)
    );
    """)
sql_conn.commit()


# Se busca el listado de blogs en "blogs_feeds.txt" y se procesan
fin = open("blogs_feeds.txt")
semaforo = threading.Semaphore(10)  # Se permiten 10 a la vez
hilos = []
for blog in fin:
    if blog.startswith('#'):
        continue
    hilo = Hilos(blog, semaforo)
    hilos.append(hilo)
    hilo.start()
fin.close()
for hilo in hilos:
    hilo.join()

# Se borran las entradas antiguas para que la base de datos no se haga enorme
limpiar_base_datos(sql_conn)

# Se generan los html en el directorio salida
generar_html(sql_conn)

# Se genera el RSS
generar_rss(sql_conn)

# Se cierra la base de datos
sql_conn.close()

# Se comprueban los argumentos de la línea de comandos
navegadorOk = True
for arg in sys.argv:
    if '--no-browser' == arg:
        navegadorOk = False

if navegadorOk:
    # Se abre en el navegador la primera página de la salida:
    webbrowser.open('salida/index.html')

