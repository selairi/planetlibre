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

Una vez ejecutado el comando "python3 planet.py", se generará en la carpeta "salida" una serie de archivos html con las entradas leídas desde los blogs.

# Modificación / introducción de nuevos blogs

Hay que modificar el archivo "blogs_feeds.txt" con los feeds de los blogs que se deseen añadir. Se debe colocar uno por línea.