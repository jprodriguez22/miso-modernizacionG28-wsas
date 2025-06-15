FROM node:22.2.0-alpine3.18 as builder
WORKDIR /
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.25.5-alpine
COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /usr/share/nginx/html

COPY --from=builder /dist .

EXPOSE 80

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD [ "nginx", "-g", "daemon off" ]
