# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim as base
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1
# Ignore that pip runs as root
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /root

RUN apt update && apt install --no-install-recommends -y python3-full && apt clean autoclean && apt autoremove --yes && rm -rf /var/lib/{apt,cache,dpkg,log}



FROM base as builder


RUN apt update && apt install --no-install-recommends -y gcc build-essential libssl-dev git
#RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
#    python3 -m pip install --user --no-cache-dir -r requirements.txt && python3 -m pip install --user --no-cache-dir -U pip setuptools

WORKDIR /app
# Copy the source code into the container, and install it only for the user.
ADD . .
RUN python3 -m pip install  --no-warn-script-location --no-cache-dir --user .
ENV PATH=/root/.local/bin:$PATH


FROM base as final
# Move pre-built files to a fresh image and make sure path contains .local/bin
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Expose the port that the application listens on.
ARG PORT=8080   # Default port for the application
EXPOSE $PORT

# Run the application.
CMD SideJITServer --port 8080
