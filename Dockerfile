FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APPDIR=/app

# target directories are created automatically if they don't already exist
COPY src/ ${APPDIR}/
RUN pip install --no-cache-dir -r ${APPDIR}/requirements.txt

WORKDIR ${APPDIR}
CMD [ "/bin/bash" ]
