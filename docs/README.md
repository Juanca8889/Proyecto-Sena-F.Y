# Documentación del Proyecto

## 1. Distribución de Ramas (Git Flow)

- **main** → Rama principal y estable del proyecto. Contiene el código final listo para producción.  
- **develop** → Rama de desarrollo general. Aquí se integran los cambios de cada desarrollador antes de pasar a `main`.  
- **cata**, **val**, **ceron**, **laura**, **camilo** → Ramas individuales de desarrollo. Cada desarrollador trabaja en su respectiva rama y luego realiza *merge* hacia `develop`.  

---

## 2. Requisitos del Proyecto

| Componente | Versión recomendada |
|-------------|--------------------|
| Python | 3.13.6 |
| Pip | 25.2 |
| Base de datos | MySQL con conector `mysql-connector-python` |



## 3. Verificación de Instalaciones

Ejecutar los siguientes comandos en la terminal o CMD para verificar las versiones instaladas:


python -V
pip --version




## 4. Instalación de Dependencias Principales

Si no se tienen instaladas las herramientas necesarias:


python -m ensurepip --default-pip
pip install mysql-connector-python




## 5. Actualización de Herramientas

Actualizar las versiones de Python y Pip:

bash
python -m pip install --upgrade pip
winget upgrade --id Python.Python.3



## 6. Instalación del Proyecto en Otra Máquina

1. Clonar o copiar el proyecto.  
2. Crear un entorno virtual (recomendado):

   **En Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **En Linux/Mac:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Instalar las dependencias del archivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```


## 7. Generar Archivo de Dependencias

Si se instalan nuevas librerías, actualizar el archivo `requirements.txt` con:


pip freeze > requirements.txt




## 8. Dependencias del Proyecto

Listado de paquetes utilizados en el entorno actual:

```txt
annotated-types==0.7.0
anyio==4.9.0
attrs==25.3.0
blinker==1.9.0
certifi==2025.8.3
cffi==2.0.0
charset-normalizer==3.4.3
click==8.2.1
colorama==0.4.6
contourpy==1.3.3
cycler==0.12.1
et_xmlfile==2.0.0
fastapi==0.115.12
Flask==3.1.2
flet==0.28.3
flet-desktop==0.28.3
flet-web==0.28.3
fonttools==4.59.2
fpdf==1.7.2
h11==0.16.0
httpcore==1.0.9
httptools==0.6.4
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
kiwisolver==1.4.9
MarkupSafe==3.0.2
matplotlib==3.10.6
mysql-connector-python==9.4.0
numpy==2.3.3
oauthlib==3.2.2
openpyxl==3.1.5
outcome==1.3.0.post0
packaging==25.0
pandas==2.3.3
pillow==11.3.0
pycparser==2.23
pydantic==2.11.5
pydantic_core==2.33.2
PyMySQL==1.1.1
pyparsing==3.2.4
PySocks==1.7.1
python-dateutil==2.9.0.post0
python-dotenv==1.1.0
pytz==2025.2
PyYAML==6.0.2
repath==0.9.0
requests==2.32.5
selenium==4.35.0
setuptools==80.9.0
six==1.17.0
sniffio==1.3.1
sortedcontainers==2.4.0
starlette==0.46.2
tabulate==0.9.0
tk==0.1.0
trio==0.30.0
trio-websocket==0.12.2
typing-inspection==0.4.1
typing_extensions==4.14.1
tzdata==2025.2
urllib3==2.5.0
uvicorn==0.34.2
watchfiles==1.0.5
webdriver-manager==4.0.2
websocket-client==1.8.0
websockets==15.0.1
Werkzeug==3.1.3
wsproto==1.2.0
```

---

## 9. Buenas Prácticas de Uso del Repositorio

- No incluir la carpeta `venv/` en el repositorio (usar `.gitignore`).  
- Confirmar la conexión a MySQL antes de ejecutar el proyecto.  
- Cada desarrollador debe crear su rama a partir de `develop` y luego realizar *merge* una vez completada su tarea.  
- Mantener actualizado el archivo `requirements.txt` cuando se agreguen o eliminen dependencias.
