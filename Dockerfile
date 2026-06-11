# Load this base image before building:
#   docker load -i data\bestoray-phddns-v1.0.tar
FROM phddns-bestoray:latest

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_MODULE=app.main:app \
    WEB_HOST=0.0.0.0 \
    WEB_PORT=8000 \
    PHDDNS_CMD="/etc/init.d/phddns_service start"

WORKDIR /app

RUN apk add --no-cache \
        ca-certificates \
        py3-pip \
        python3 \
        supervisor \
    && python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:${PATH}"

# Install Python dependencies first to keep Docker layer caching effective.
COPY server/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy your FastAPI source code.
# Expected default entrypoint: server/app/main.py with `app = FastAPI(...)`.
COPY server/app/ /app/app/

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000

VOLUME ["/data/phddns"]

ENTRYPOINT []
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
