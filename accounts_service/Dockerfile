FROM python:3.13.7-alpine3.22


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY populate.py .

EXPOSE 8000

CMD ["sh", "-c", "python populate.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]