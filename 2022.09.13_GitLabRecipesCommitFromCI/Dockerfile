FROM rust:latest AS builder
RUN set -eux; \
    cargo install ripgrep;

FROM rust:latest

# Copy binaries, tools, libraries, etc. into final image.
COPY --from=builder /usr/local/cargo/bin/rg /usr/local/bin/

RUN set -eux; \
    # Add clippy
    rustup component add clippy; \
    #
    # INSTALL EXTERNAL LIBRARIES AND TOOLS HERE
    #
    # Clean up (if you installed anything with apt or cargo)
    rm -rf /var/lib/apt/lists/*; \
    rm -rf /usr/local/cargo/registry;

CMD ["bash"]
