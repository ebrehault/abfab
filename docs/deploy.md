# Deployment

## Prerequisites

Install Docker https://docs.docker.com/get-docker/

## Deploy locally

Copy the example files (`./docker/docker-compose-local.yml`, `./docker/config.yaml`, and `./docker/nginx-local.conf`) from GitHub to this folder.

```
curl -o docker-compose.yml https://raw.githubusercontent.com/ebrehault/abfab/main/docker/docker-compose-local.yml
curl -o config.yaml https://raw.githubusercontent.com/ebrehault/abfab/main/docker/config.yaml
curl -o nginx-local.conf https://raw.githubusercontent.com/ebrehault/abfab/main/docker/nginx-local.conf
```

Note: the first command renames the file `docker-compose-local.yml` to `docker-compose.yml`.

Start the server:

```
docker-compose up
```

You can access AbFab at http://localhost/my-abfab/abfab/index.html

## Deploy in production

### Configuration

Copy the example files (`./docker/docker-compose.yml`, `./docker/config.yaml`, and `./docker/nginx.conf`) from GitHub to this folder.

```
curl -o docker-compose.yml https://raw.githubusercontent.com/ebrehault/abfab/main/docker/docker-compose.yml
curl -o config.yaml https://raw.githubusercontent.com/ebrehault/abfab/main/docker/config.yaml
curl -o nginx.conf https://raw.githubusercontent.com/ebrehault/abfab/main/docker/nginx.conf
```

Create a `.env` file containing the passwords for Guillotina and PostgreSQL and the JWT secret :

```
PASSWORD=secret-1
POSTGRES_PASSWORD=secret-2
JWT_SECRET=secret-3
```

Modify `nginx.conf` and do the following changes:

-   set the `server_name` to the domain name of your website
-   change the root location (`somepath` in the example) in 3 places (in the `location` , `rewrite` and `sub_filter`). `/` is a valid value if you want to serve AbFab on your domain root.

### SSL certificate

For simplicity sake, we explain here how to use Let's Encrypt free SSL certificate. But you can use any other SSL certificate.

Generate the SSL certificate with the following command:

```
sudo docker run -it --rm --name certbot \
    -v "/etc/letsencrypt:/etc/letsencrypt" \
    -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
    -p 80:80 certbot/certbot certonly
```

Replace `<your-domain>` with the proper value in the `reverse-proxy` section in `docker-compose.yml`:

```
services:
    reverse-proxy:
        image: nginx
        volumes:
            - ./nginx.conf:/etc/nginx/nginx.conf
            - /etc/letsencrypt/live/<your-domain>:/ssl
```

### Start the server

```
sudo docker-compose up -d
```

The first launch takes 2 or 3 minutes as it will init the AbFab container.
