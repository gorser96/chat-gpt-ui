# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM node:22.3.0-bullseye-slim as builder

RUN mkdir /project
WORKDIR /project

RUN npm install -g @angular/cli

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
CMD ["ng", "serve", "--host", "0.0.0.0"]
