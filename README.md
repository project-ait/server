> The API server for [AIT](https://github.com/project-ait/front)

## Development

### Prerequisites

- We developed in Python 3.11 ~ 3.12
- PostgreSQL

```bash
pip install -r requirements.txt
```

### Getting Started

```bash
cp .env.example .env  # and edit for your environment
python main.py  # start the server

# Shows in console 0.0.0.0 (--host argument) 
# but it's actually working on 127.0.0.1
```

### Docker

#### Build API Image

Execute this script:

```bash
python. ./docker/build.py
```

#### Run Compose

```bash
docker-compose up
# or 'docker-compose up -d' for background running
```