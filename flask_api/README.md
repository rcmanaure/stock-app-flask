# FlasK Project by Ruben Castillo

## DOCKER COMMANDS TO USE:

## To build image:

docker-compose build

## To run docker and start the containers :

- docker-compose up -d (use -d flag for daemonized version)
## Swagger URL to how use the endpoints:

http://localhost:5000/swagger

## Virtual trading Stock endpoints:
### method POST to buy and method PUT to sell(Check Swagger to how use the endpoints.)

http://localhost:5000/share
### List the shares owned(Profit/Loss,Held shares,Current value of the shares and Current day reference prices)
http://localhost:5000/list-shares
### List the historic price of shares
http://localhost:5000/stock-prices

# Bonus Blog REST API (Check Swagger to how use the endpoints.)
http://localhost:5000/
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


## To run the tests with Pytest:

pytest
