# wsgi.py
import sys
import os

# Añade el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa tu aplicación desde app.py
from app import app  # Importa la instancia Flask llamada 'app'

if __name__ == "__main__":
    app.run()