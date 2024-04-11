FROM rust:latest as builder

ARG APP_NAME=is_even
ENV APP_NAME=${APP_NAME}

WORKDIR /app

RUN apt-get update -y && apt-get upgrade -y && apt-get install musl-tools -y

COPY Cargo.toml Cargo.lock ./
RUN mkdir src/ && echo "fn main() {}" > src/main.rs
RUN rustup target add x86_64-unknown-linux-musl

RUN cargo build --release --target x86_64-unknown-linux-musl
COPY src src
RUN touch src/main.rs
RUN cargo build --release --target x86_64-unknown-linux-musl

RUN strip target/x86_64-unknown-linux-musl/release/$APP_NAME


FROM alpine:latest

ARG APP_NAME=is_even
ENV APP_NAME=${APP_NAME}
ENV ROCKET_PROFILE=release

WORKDIR /app
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/$APP_NAME .
COPY ./Rocket.toml /app/Rocket.toml

CMD ./$APP_NAME
