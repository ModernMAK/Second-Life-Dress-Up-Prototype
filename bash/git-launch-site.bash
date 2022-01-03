docker kill WepApp-HTTP
docker rm WepApp-HTTP

docker build https://github.com/ModernMAK/Second-Life-Dress-Up-Prototype.git#main -f docker/http.dockerfile -t sldup-webapp-http

docker run -d --rm --name WepApp-HTTP -v "/sockets:/sockets" sldup-webapp-http