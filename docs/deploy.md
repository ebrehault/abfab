# Deployment

## Prerequisites

Install Docker https://docs.docker.com/get-docker/

## Configuration

Create a folder:

```
mkdir abfab
cd abfab
```

Copy the example files (`./docker/docker-compose.yml`, `./docker/config.yaml`, and `./docker/nginx.conf`) from GitHub to this folder.

```
curl -o docker-compose.yml https://raw.githubusercontent.com/ebrehault/abfab/main/docker/docker-compose.yml
curl -o config.yaml https://raw.githubusercontent.com/ebrehault/abfab/main/docker/config.yaml
curl -o nginx.conf https://raw.githubusercontent.com/ebrehault/abfab/main/docker/nginx.conf
```

Create a `.env` file containing the passwords for PostgreSQL and for the Guillotina server itself:

```
PASSWORD=secret-1
POSTGRES_PASSWORD=secret-2
```

Modify `nginx.conf` and do the following changes:

-   set the `server_name` to the domain name of your website
-   change the location (`somepath` in the example) in 2 places (in the `location` directive and in the `sub_filter` directive)

Generate the SSL certificate with the following command (TO BE COMPLETED)

## Start the server

```
sudo docker-compose up -d
```

The first launch takes 2 or 3 minutes as it will init the AbFab container.
