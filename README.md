coloreando
==========

Coloreemos entre todos!


Dependencias de sistema
-----------------------
Necesitas instalar algunas dependencias en tu sistema. Esto dependerá un poco del SO que estes usando.

 * Es necesario instalar los archivos de desarrollo de libevent y de sqlite.
 * Y necesitas el redis-server.

Por ejemplo en Fedora Linux sería:

``` 
sudo yum install libevent-devel sqlite-devel redis
``` 

Iniciar
-------

* Es conveniente que generes tu propio virtualenv para la instalación de dependencias:

``` 
mkvirtualenv coloreando
``` 

* Después puedes instalarlas corriendo:

``` 
pip install -r requirements.txt
``` 

* Iniciar ls BD:

``` 
python ./manage.py syncdb --settings=coloreando.settings.prod
``` 

* Ahora ya podemos iniciar el servidor, que por defecto podemos acceder en http://127.0.0.1:8000/:

``` 
honcho start
``` 

Demo
----
  http://tharsus.com.ar:8000
