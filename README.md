# BFT - Bienestar y Felicidad Tolima

Este es un sistema desarrollado en Django orientado al cuidado del medio ambiente, el trabajo y la salud, mediante la gestión de programas y actividades que asignan puntuación a los participantes.

## Características principales

- Gestión de usuarios.
- Registro y control de programas y actividades.
- Asignación de puntuación con evidencias por actividad.
- Estadísticas de desempeño (mejor y peor usuario).
- Panel administrativo básico.

## Tecnologías utilizadas

- Django 5.x
- Python 3.x
- SQLite
- Bootstrap (para la interfaz visual)

# Licencia

Este software fue desarrollado por Nicolás Paulo Vega y María Fernanda Molano para Positiva Compañía de Seguros. Sin embargo, los derechos de desarrollo y propiedad intelectual son exclusivos de los autores.

Consulta el archivo LICENSE.txt para más detalles.

## Instalación (modo desarrollo)

```bash
git clone https://github.com/NicolasPauloVega/web_services
cd web_services
python -m venv venv
env\Scripts\activate  # En Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
