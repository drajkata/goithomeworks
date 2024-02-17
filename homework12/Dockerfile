FROM python:3.11-alpine

# Ustawiamy zmienną środowiskową
ENV APP_HOME /app

# Oznaczamy port, na którym aplikacja działa wewnątrz kontenera
EXPOSE 5432

# Install & use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

# Kopiujemy inne pliki do katalogu roboczego kontenera
COPY . .

# Uruchomiamy naszą aplikację wewnątrz kontenera
CMD ["python", "main.py"]