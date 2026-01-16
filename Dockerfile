FROM python:3.11

# 2. Création d'un utilisateur non-root
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# 3. Dossier de travail
WORKDIR /app

# 4. Installation des dépendances 
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 5. Copie du code de l'application
COPY --chown=user . /app
# 6. Lancement de l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]