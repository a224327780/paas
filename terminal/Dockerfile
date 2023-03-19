FROM ghcr.io/a224327780/debian

ENV GOTTY_TAG_VER v1.0.1

RUN apt-get -y update && \
    apt-get install -y curl && \
    curl -sLk https://github.com/yudai/gotty/releases/download/${GOTTY_TAG_VER}/gotty_linux_amd64.tar.gz \
    | tar xzC /usr/local/bin && \
    apt-get purge --auto-remove -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists* && \
    echo "#!/bin/sh" >> /docker-entrypoint.sh \
    && echo "set -e" >> /docker-entrypoint.sh \
    && echo 'exec "$@"' >> /docker-entrypoint.sh \
    && chmod +x /docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["/usr/local/bin/gotty", "--permit-write", "--reconnect", "/bin/bash"]