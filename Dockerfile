FROM python:3.11-slim as requirements-stage
ARG mode=dev
WORKDIR /tmp

RUN pip install poetry-plugin-export
COPY ./pyproject.toml ./poetry.lock* ./

RUN if [ "$mode" = "dev" ]; then \
        poetry export --with dev --without-hashes --format=requirements.txt > requirements.txt; \
    elif [ "$mode" = "prod" ]; then \
        poetry export --with prod --without-hashes --format=requirements.txt > requirements.txt; \
    else \
        poetry export --without-hashes --format=requirements.txt > requirements.txt; \
    fi


FROM python:3.11
WORKDIR /blog

ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random
ENV PYTHONDONTWRITEBYTECODE 1

COPY --from=requirements-stage /tmp/requirements.txt /blog/requirements.txt

RUN pip install --no-compile --no-cache-dir --upgrade -r /blog/requirements.txt

COPY . /blog

RUN chmod +x ./scripts/*.sh

EXPOSE 8080

CMD ["/bin/sh", "-c", "./scripts/migrate.sh && ./scripts/run.sh"]