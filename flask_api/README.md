# FlasK Project by Ruben Castillo

## DOCKER COMMANDS TO USE:

## To build image:

docker-compose build

## To run docker and start the Flask REST API :

- docker-compose up
- Go to http://localhost:5000/

## To run one container :

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

## TO run the tests with Pytest:

pytest
