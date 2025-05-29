#  Cómo ejecutar `parqueadero.py` en la terminal (CMD)

##  Introducción
`parqueadero.py` es un programa escrito en Python. Para ejecutarlo correctamente, asegúrate de tener **Python instalado** en tu computadora y usa la **línea de comandos (CMD)**.

##  Estructura de Carpetas
El script debe estar dentro de una carpeta llamada `proyecto`, y dentro de esta debe existir otra carpeta llamada `images`. La estructura debe verse así:

proyecto/
│── parqueadero.py
│── images/

## Pasos para ejecutar el programa:

### 1 Verificar instalación de Python  
   - Abre **CMD** (`Windows + R`, escribe `cmd` y presiona `Enter`).
   - Escribe `python --version` y presiona `Enter`.  
   - Si ves una versión de Python (`Python 3.x.x`), estás listo. Si no, descárgalo desde [python.org](https://www.python.org/downloads/).

### 2 Ubicar la carpeta `proyecto`  
   - Encuentra la carpeta `proyecto` en el **Explorador de Archivos** y copia su ruta completa (Ejemplo: `C:\Users\TuUsuario\Documents\proyecto`).

### 3 Abrir la terminal en la carpeta `proyecto`  
   - Si estás en CMD, usa el siguiente comando para moverte a la carpeta:  
     cd C:\Users\TuUsuario\Documents\proyecto
   - También puedes abrir **CMD** directamente en la carpeta:
     - Abre `proyecto` en **Explorador de Archivos**.
     - Escribe `cmd` en la barra de direcciones y presiona `Enter`.

### 4 Instalar las dependencias  
   Antes de ejecutar el script, instala las siguientes librerías con `pip`:
   pip install pillow  
   pip install tk  
   ⚠️ Si `pip` da error, actualízalo con:
   python -m pip install --upgrade pip  

### 5 Ejecutar el script  
   - Una vez en la carpeta `proyecto`, ejecuta:
     python parqueadero.py  
   - Si Python 3 está instalado pero el comando anterior no funciona, intenta:
     python3 parqueadero.py  
