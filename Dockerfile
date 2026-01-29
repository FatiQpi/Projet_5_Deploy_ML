#  Image de base
FROM python:3.11-slim

#  Répertoire de travail
WORKDIR /code

#  Installation des dépendances
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#  Copie du code et du modèle
COPY ./app /code/app
COPY ./data /code/data

#  Création d'un utilisateur non-root
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

#  Commande de lancement
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]