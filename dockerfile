FROM python:3.10 AS model-downloader
RUN pip install --no-cache-dir sentence-transformers
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1', cache_folder='/tmp/models')"

FROM python:3.10-slim

RUN useradd -ms /bin/bash appuser

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libjpeg-dev \
    zlib1g-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY --from=model-downloader /tmp/models /home/appuser/.cache/torch/sentence_transformers

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app /home/appuser

USER appuser

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

