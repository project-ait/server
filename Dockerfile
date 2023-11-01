FROM python:3.10

COPY . /api
WORKDIR /api

RUN pip install -r requirements-deploy.txt

RUN touch /api/database.sqlite \
    && chmod 664 /api/database.sqlite \
    && chmod 775 /api

EXPOSE 1777

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1777"]