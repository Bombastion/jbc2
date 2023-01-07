FROM python:3.10

WORKDIR /opt/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:./src"


EXPOSE 5000
EXPOSE 80

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]
