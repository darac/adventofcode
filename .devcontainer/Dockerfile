FROM mcr.microsoft.com/devcontainers/python:2-3.12-bullseye

# renovate: github-release depName=prefix-dev/pixi
ARG PIXI_VERSION="v0.80.0"

RUN curl -L -o /usr/local/bin/pixi -fsSL --compressed \
        "https://github.com/prefix-dev/pixi/releases/download/${PIXI_VERSION}/pixi-$(uname -m)-unknown-linux-musl" \
    && chmod +x /usr/local/bin/pixi \
    && pixi info

USER vscode
WORKDIR /home/vscode

RUN echo 'eval "$(pixi completion -s bash)"' >> /home/vscode/.bashrc
