# FastAPI + phddns single-image container

doc: [https://service.oray.com/question/36626.html]https://service.oray.com/question/36626.html

Project layout expected by the Dockerfile:

```text
.
|-- Dockerfile
|-- supervisord.conf
|-- .env
|-- server/
|   |-- requirements.txt
|   `-- app/
|       `-- main.py
`-- data/
    `-- bestoray-phddns-v1.0.tar
```

`server/app/main.py` should expose a FastAPI instance named `app` by default:

```python
from fastapi import FastAPI

app = FastAPI()
```

Create a local `.env` file before running the container:

```dotenv
OPENAI_API_KEY=replace-with-your-api-key
OPENAI_MODEL=MiniMax-M2.7
OPENAI_BASE_URL=https://api.minimaxi.com/v1
```

Load the Oray phddns base image:

```powershell
docker load -i data\bestoray-phddns-v1.0.tar
```

Build:

```powershell
docker build -t fastapi-phddns:latest .
```

Run:

```powershell
docker run -d `
  --name fastapi-phddns `
  --restart unless-stopped `
  --env-file .env `
  -p 8000:8000 `
  -v phddns-data:/data/phddns `
  fastapi-phddns:latest
```

Get the phddns device status or SN:

```powershell
docker exec fastapi-phddns phddns status
```

In the Oray console, map the external address to the service inside this container:

```text
127.0.0.1:8000
```

If your FastAPI app entrypoint is not `app.main:app`, override it:

```powershell
docker run -d `
  --name fastapi-phddns `
  --env-file .env `
  -e APP_MODULE=my_package.api:app `
  -p 8000:8000 `
  -v phddns-data:/data/phddns `
  fastapi-phddns:latest
```

If your phddns package uses a different foreground command, override it:

```powershell
docker run -d `
  --name fastapi-phddns `
  --env-file .env `
  -e PHDDNS_CMD="/etc/init.d/phddns_service start" `
  -p 8000:8000 `
  -v phddns-data:/data/phddns `
  fastapi-phddns:latest
```
