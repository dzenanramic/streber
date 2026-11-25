FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# nltk odbija hardlink-ovane fajlove iz venv-a (uv hardlink-uje pakete),
# pa stopwords preuzimamo na zasebnu lokaciju sa novim inode-om.
ENV NLTK_DATA=/app/nltk_data
RUN uv run python -c "import nltk; nltk.download('stopwords', download_dir='/app/nltk_data', quiet=True); nltk.download('punkt', download_dir='/app/nltk_data', quiet=True)"

COPY app ./app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
