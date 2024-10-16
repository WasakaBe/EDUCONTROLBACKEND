COMO USAR ESTE LADO DE BACKEND
---

### 1. Instalación  
Es necesario tener **Python** instalado en el sistema operativo. Asegúrate de que sea una versión actualizada para evitar problemas de compatibilidad.

### 2. Descarga  
Después, debes **descargar o clonar** este repositorio desde **GitHub** en tu máquina o en el IDE de tu preferencia.

### 3. Uso  
Antes de ejecutar la aplicación, es necesario instalar un entorno virtual (**VENV**). Utiliza el siguiente comando para instalarlo:  
```bash
pip install python-dotenv
```
Luego, instala todas las dependencias necesarias con el siguiente comando:  
```bash
pip install waitress flask flask-sqlalchemy flask-cors jogging pandas numpy werkzeug
```
- **Nota:** La dependencia `waitress` es solo para uso en local; no es necesaria si el proyecto se desplegará en un hosting o servidor remoto.

### 4. Configuración del archivo .ENV  
En el archivo **.env**, deberás proporcionar los siguientes datos:  
- **USER** y **PWD**: Tu correo electrónico y una clave que se utilizarán para enviar notificaciones por correo.  
- **SQLALCHEMY_DATABASE_URI**: Aquí debes definir la cadena de conexión a la base de datos. Por defecto, se utiliza **SQL Server**, pero puedes configurar otro motor de base de datos según tu preferencia.

---
