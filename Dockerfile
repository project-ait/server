FROM python:3.10

COPY . /api
WORKDIR /api

RUN pip install -r requirements-deploy.txt

# Create 'database.sqlite' file, adjust permissions on file and its directory
RUN touch /api/database.sqlite && chmod 775 /api/database.sqlite && chmod 775 /api

EXPOSE 1777

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1777"]