FROM nginx
# Setup Env
EXPOSE 80 443

COPY ../nginx/http.conf /etc/nginx/nginx.conf