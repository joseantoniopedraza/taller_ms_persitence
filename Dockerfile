# 1. Imagen base
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo
WORKDIR /app

# 3. Copiar los archivos del proyecto
COPY requirements.txt .

# 4. Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código
COPY . .

# 6. Exponer el puerto en el que correrá Gunicorn
EXPOSE 8000

# 7. Comando por defecto (puedes cambiarlo según tus necesidades)
CMD ["gunicorn", "taller_ms_persistence.wsgi:application", "--bind", "0.0.0.0:8000"]