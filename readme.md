# Contratos Alcaldia Backend
Backend Desarrollado en Python con Django Rest Framework para la gestión de contrataciones en la Alcaldía Municipal de Valledupar

# Instalar Requerimientos del proyecto
- Archivo requirements.txt

# Crear el entorno virtual
Ejecutar comando:
- py -m venv venv

# Comandos para la Ejecución
Creación de modelos en la BD:
- py manage.py makemigrations authApp
- py manage.py migrate

# Ejecución del servidor
- py manage.py runserver

# *En caso de no poder instalar requerimientos mediante el archivo requirements.txt*
- Instalación de Django
  - pip install django
- Instalación paquete Django REST
  - pip install djangorestframework
- Instalación JWT Django (Autenticación JWT)
  - pip install djangorestframework-simplejwt
- Instalación CORS
  - pip install django-cors-headers
- Instalación conector BD PostgreSQL
  - pip install psycopg2