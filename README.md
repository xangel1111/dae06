Pasos de Instalación
1. Clonar el Repositorio
bashgit clone https://github.com/usuario/dae06.git
cd nombre-del-repositorio
2. Crear y Activar un Entorno Virtual
En Windows:
python -m venv venv
venv\Scripts\activate
En macOS/Linux:
python3 -m venv venv
source venv/bin/activate
3. Instalar Dependencias
pip install -r requirements.txt
Si no existe el archivo requirements.txt, instala Django:
pip install django
4. Iniciar el Proyecto
Windows:
python config/manage.py runserver
macOS/Linux:
python3 config/manage.py runserver
5.
IR A: localhost:8000