FROM python:3.7-slim-stretch
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
  build-essential \
  libhunspell-dev

# Copy app source.
WORKDIR /app/spamfilter
COPY . .

# Install requirements.
RUN pip install --no-cache-dir -r requirements.txt

# Prepare environment.
EXPOSE 8080
EXPOSE 9191

# Start command.
CMD ["sh", "start.sh"]
