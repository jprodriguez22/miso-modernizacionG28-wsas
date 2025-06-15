#!/bin/sh

ROOT_DIR=/usr/share/nginx/html

for file in $ROOT_DIR/js/app.*.js* $ROOT_DIR/index.html $ROOT_DIR/precache-manifest*.js;
do
    sed -i 's|API_DOMAIN_SECRET|'${VITE_API_DOMAIN}'|g' $file
    sed -i 's|RABBITMQ_HOST_SECRET|'${VITE_RABBITMQ_HOST}'|g' $file
    sed -i 's|RABBITMQ_USER_SECRET|'${VITE_RABBITMQ_USER}'|g' $file
    sed -i 's|RABBITMQ_PWD_SECRET|'${VITE_RABBITMQ_PWD}'|g' $file
    sed -i 's|RABBITMQ_QUEUE_SECRET|'${VITE_RABBITMQ_QUEUE}'|g' $file
done