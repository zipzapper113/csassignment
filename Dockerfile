FROM python:3.9-slim
RUN useradd -m worker
USER worker
WORKDIR /home/worker
COPY --chown=worker:worker requirements.txt requirements.txt
ENV PATH = "$PATH:/home/worker/.local/bin" 
RUN pip install --upgrade pip
RUN pip install wheel setuptools
RUN pip install -r requirements.txt
COPY --chown=worker:worker . .
WORKDIR /home/worker/project
CMD ["python3","api.py"]
