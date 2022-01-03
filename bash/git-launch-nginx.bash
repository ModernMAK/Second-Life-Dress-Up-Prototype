docker kill Website-NGinX
docker rm Website-NGinX

docker build https://github.com/ModernMAK/Second-Life-Dress-Up-Prototype.git#main -f docker/nginx.dockerfile -t sldup-nginx

docker run -d --rm --name Website-NGinX  -v "/etc/letsencrypt:/etc/letsencrypt" -v "/sockets:/sockets" -p 80:80 -p 443:443 sldup-nginx