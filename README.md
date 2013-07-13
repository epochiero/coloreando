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

Instalación
-----------

* Puedes instalar la última versión de github haciendo:

``` 
git clone https://github.com/epochiero/coloreando.git
cd coloreando
python setup.py develop
``` 

Si preferís hacerlo en un virtualenv ejecutá:
	
``` 
virtualenv env
. env/bin/activate
python setup.py develop
```

* Después necesitas iniciar la BD:

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
