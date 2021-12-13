FROM python:3.9.1

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

COPY ./requirements.txt /
RUN pip install -r ./requirements.txt

COPY ./entrypoint.sh ./start.sh /

# Fix windows docker bug, convert CRLF to LF
#RUN sed -i 's/\r$//g' /start.sh && chmod +x /start.sh && sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh
RUN chmod +x /start.sh && chmod +x /entrypoint.sh

WORKDIR /app