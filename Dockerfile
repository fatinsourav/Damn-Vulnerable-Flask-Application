FROM python:3.13-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends build-essential pkg-config default-libmysqlclient-dev libxml2-dev libxslt1-dev && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends tini libmariadb3 libxml2 libxslt1.1 && rm -rf /var/lib/apt/lists/*
# Upgrade the base image's own Python packages (pip, setuptools, wheel and their dependencies), which the image scanner reads from the image itself.
RUN python -m pip install --no-cache-dir --upgrade "pip" "setuptools==84.1.0" "wheel==0.46.2" "jaraco.context==6.1.0" "msgpack==1.2.3" "urllib3==2.8.0"
ENV PYTHONUNBUFFERED=1 PATH=/opt/venv/bin:$PATH
WORKDIR /app
RUN useradd --system --uid 10001 --no-create-home app
COPY --from=builder /opt/venv /opt/venv
COPY app.py test.db ./
COPY templates ./templates
COPY static ./static
USER app
EXPOSE 5000
ENTRYPOINT ["tini", "--"]
CMD ["gunicorn", "--bind", "[::]:5000", "--workers", "2", "app:app"]
