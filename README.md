# planetlibre
Simple RSS reader like a planet side.

# Lector simple de RSS

Este es un sencillo lector de RSS basado en python3. La lectura de las entradas se realiza de forma similar a un planet. Por defecto viene configurado con una serie de feeds para blogs que tratan sobre software libre.

# Instalación

Sólo hay que descargarlo e instalar el siguiente paquete:

    sudo apt-get install feedparser

Después se ejecuta con:

    python3 planet.py

# Salida generada

Una vez ejecutado el comando "python3 planet.py", se generará en la carpeta "salida" una serie de archivos html con las entradas leídas desde los blogs. Por defecto, se abrirá el navegador para comenzar a leer las entradas una vez finalizado el proceso.

# Modificación / introducción de nuevos blogs

Hay que modificar el archivo "blogs_feeds.txt" con los feeds de los blogs que se deseen añadir. Se debe colocar uno por línea.

# Actualización automática y subida a Github

También se puede crear un planet y subir las actualizaciones a un servidor para compartirlas con el resto de usuarios de Internet.

El script "commit.sh" permite automatizar el proceso de generación de las entradas y subirlas a Github. Por seguridad se recomienda tener dos carpetas, en una se tendrán los archivos de este repositorio. En la otra se tendrá un repositorio personal que representará la página web que se desea que Github sirva en la web.

Se deben editar los parámetros de las primeras líneas del archivo "commit.sh". Los datos a rellenar vienen explicados en los comentarios.

Después se debe ejecutar el comando "crontab -e" para introducir cada cuanto se debe ejecutar "commit.sh". Por ejemplo, para ejecutarlo cada 12 horas, se escribirá:

    0 */12 * * * bash /ruta-a-commit.sh/commit.sh

# Personalización

Los archivos "cabecera.html" y "pie.html" permiten personalizar las páginas generadas. Lo que se añada a "cabecera.html" se copiará al comienzo de la página. Lo que se añada a "pie.html" se copiará al final de la página.

El archivo "config.txt" permite completar los datos necesarios para que se pueda generar un RSS. Este RSS generado estará disponible en el archivo "feed.xml". Para que los usuarios puedan añadir el RSS deben apuntar a:

    "URL de nuestro sitio"/feed.xml