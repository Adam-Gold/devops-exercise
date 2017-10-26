FROM node:8.7
MAINTAINER Adam Gold Balali

COPY bamboo-app /opt/bamboo-app

RUN npm install /opt/bamboo-app

ENV TINI_VERSION 0.16.1
ENV TINI_SHA 5e01734c8b2e6429a1ebcc67e2d86d3bb0c4574dd7819a0aff2dca784580e040

# Use tini as subreaper in Docker container to adopt zombie processes
RUN curl -fsSL https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini-static-amd64 -o /bin/tini \
  && chmod +x /bin/tini && echo "$TINI_SHA  /bin/tini" | sha256sum -c -

EXPOSE 8080

ENTRYPOINT ["/bin/tini", "--", "/usr/local/bin/node", "/opt/bamboo-app/bamboo.js"]
