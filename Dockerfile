# Stap 1: Kies een basisimage met Python
FROM python:3.11.9
# Stap 2: Stel de werkdirectory in in de container
WORKDIR /app
# Stap 3: Kopieer het requirements-bestand naar de container
COPY requirements.txt /app
# Stap 4: Installeer de Python-afhankelijkheden
RUN pip install --no-cache-dir -r requirements.txt
# Stap 5: Kopieer de rest van de code naar de container
COPY . /app
