# Use the standard Nginx image from Docker Hub
FROM nginx:1.13.5

RUN mkdir -p /var/lib/reverse-proxy/cache && chmod -R 777 /var/lib/reverse-proxy/cache

# Copy the configuration file from  the current directory and paste
# it inside the container to use it as Nginx's default config.
COPY nginx.conf /etc/nginx/nginx.conf.template
COPY proxy-settings.conf /etc/nginx/proxy-settings.conf

EXPOSE $API_PORT

# Start Nginx when the container has provisioned.
CMD /bin/bash -c "envsubst '\$API_PORT' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"