FROM python:3.10.0-slim

# install needed packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libcairo2-dev 

# clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["daphne", "proassist.asgi:application", "--port", "$PORT", "--bind", "0.0.0.0", "-v2"]



