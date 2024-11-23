FROM gorialis/discord.py:latest

# We will mount onto this directory
RUN mkdir -p /app/mappa-pakka/
WORKDIR /app/mappa-pakka/

# Install python dependencies
COPY requirements.txt /app/mappa-pakka/
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]



