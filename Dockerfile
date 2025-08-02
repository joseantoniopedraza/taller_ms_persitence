FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN black .
RUN ruff check . --fix
RUN ruff format .

# RUN chmod +x manage.py

RUN echo '#!/bin/bash\n\
echo "Running migrations..."\n\
python manage.py migrate\n\
\n\
echo "Starting Django server..."\n\
python manage.py runserver 0.0.0.0:3001\n\
' > /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 3001

# Run the entrypoint script
CMD ["/app/entrypoint.sh"] 