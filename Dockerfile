# This Dockerfile will be referenced by the github action "GHCR Publish"
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APPDIR=/app

# Install any OS pkgs that are required
# RUN apt update \
#   && apt install -y cifs-utils \
#   && rm -rf /var/lib/apt/lists/*

# target directories are created automatically if they don't already exist
COPY src/ ${APPDIR}/
RUN pip install --no-cache-dir -r ${APPDIR}/requirements.txt

WORKDIR ${APPDIR}
# ENTRYPOINT [ ./entrypoint.sh ]
CMD [ "/bin/bash" ]
