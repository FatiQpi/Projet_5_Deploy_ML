FROM python:3.11

# Création d'un utilisateur non-root
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Dossier de travail
WORKDIR /app

# Installation des dépendances 
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copie du code de l'application
COPY --chown=user . /app

# Lancement de l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]