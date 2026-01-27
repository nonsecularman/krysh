FROM nikolaik/python-nodejs:python3.10-nodejs19

# REMOVE yarn repo (FIX)
RUN rm -f /etc/apt/sources.list.d/yarn.list || true

RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i '/security.debian.org/d' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "-m", "ShrutiMusic"]
