FROM debian:bookworm-slim
WORKDIR /app

COPY target/x86_64-unknown-linux-gnu/release/simeis-server /usr/local/bin/simeis-server

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/simeis-server"]
