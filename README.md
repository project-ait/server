> The API server for [AIT](https://github.com/project-ait/front)

## Development

## Requirement
- python >=3.11.4
- pip
- ffmpeg

### Prerequisites

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

```bash
docker build tag ait-server .
```
