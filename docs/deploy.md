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

Modify `docker-compose.yml` and choose a proper password for Postgres (`secret` in the example)

Modify `config.yaml` and do the following changes:

-   set the Postgres password in the `dsn` field.
-   choose a proper Guillotina password (`root` in the example).

Modify `nginx.conf` and do the following changes:

-   set the `server_name` to the domain name of your website
-   change the location (`somepath` in the example) in 2 places (in the `location` directive and in the `sub_filter` directive)

Generate the SSL certificate with the following command (TO BE COMPLETED)

## Start the server

```
docker-compose up -d
```
