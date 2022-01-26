# Flas Project by Ruben Castillo

## DOCKER COMMANDS TO USE:

## To build image:

docker-compose build

## To run one container:

docker-compose up -d <container_name> (use -d flag for daemonized version)

## To stop all containers:

docker-compose down

## To stop all containers and delete the volumes:

docker-compose down -v

## To list containers

docker ps

## To stop a container

docker stop <container hash>

"See docker-compose for more details"

## Swagger URL:

http://localhost:5000/#/

## To make Git check out files with Unix-style file endings on Windows - at least temporarily - use:

eg error: identity_1 | /usr/bin/env: ‘bash\r’: No such file or directory

git config --global core.autocrlf false

Then run your installation commands involving git clone again.

To restore Git's behavior later, run git config --global core.autocrlf true
