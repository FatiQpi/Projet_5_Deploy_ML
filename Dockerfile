<<<<<<< HEAD
FROM python:3.11
=======
# Image de base
FROM python:3.11-slim

# Répertoire de travail
WORKDIR /code

# Installation des dépendances
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copie du code et du modèle
COPY ./app /code/app
COPY ./data /code/data
>>>>>>> feature/api-dev

# Création d'un utilisateur non-root
RUN useradd -m -u 1000 user
USER user
<<<<<<< HEAD
ENV PATH="/home/user/.local/bin:$PATH"

# Dossier de travail
WORKDIR /app

# Installation des dépendances 
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copie du code de l'application
COPY --chown=user . /app

# Lancement de l'application
=======
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Commande de lancement
>>>>>>> feature/api-dev
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]