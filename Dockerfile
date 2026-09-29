FROM python:3.13-slim
WORKDIR /app
COPY server.py ./server.py
COPY supplement_fixture ./supplement_fixture
RUN mkdir -p /data/documents && printf hello > /data/documents/hello.txt && printf owned-outside-marker > /data/outside.txt
EXPOSE 8080
CMD ["python", "server.py"]
