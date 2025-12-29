FROM python:3.11-slim 
 
WORKDIR /app 
 
# Dépendances système minimales 
RUN apt-get update && apt-get install -y \ 
    git \ 
    && rm -rf /var/lib/apt/lists/* 
 
# Copier les dépendances 
COPY requirements.txt . 
 
# Installer les libs Python 
RUN pip install --no-cache-dir --upgrade pip \ 
    && pip install --no-cache-dir -r requirements.txt 
# Copier l’application 
COPY . . 
EXPOSE 5000 
CMD ["python", "app.py"] 