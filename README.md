# Mais Todos API

### The chalenge
First of all, we've been following [Backend Python Wallet](https://github.com/MaisTodos/backend-python-wallet)
challenge instructions to build an api responsible for validating and storing cashback information based on a fictional 
customer ERP request.

The scope of this project is to build a system that receives customer and bought products data, validates information,
performs proper cashback calculations based on products type and redirects the validated requets to the final api which
is responsible for applying the cashback. Considering the returned data from the cashback api, our api stores either 201 as
positve response with returned information, or any other status code as failed request also taking care of persisted data
for future analysis and conciliation between erp owner and cashback api rulers.

### The present
We started building the basis of our service by creating a [Django Rest Framework](https://www.django-rest-framework.org/) 
project, building the elementary crud routes for customers, products and cashbacks along with their validation and proper
test cases, on a second round of development our concern became to add good documentation for our routes and their http
actions ant to accomplish this step of our challenge the selected solution was [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/),
"yet another swagger generator", for drf projects. A third "sprint" of our project was to build an useful authentication 
scheme that could at once allow access to the api and restrict unauthorized access to its resources. Our choice was to
use [simple jwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/), as the name says, a simple way to 
implement jwt security patterns to our api. To achieve this third goal, we had to create an user class that could be
responsible for handling django default authentication and authorization. Our choice here was to implement an almost 
default django AbstractUser combined with another almost unaltered BaseUserManager. The fourth and last step four this
challenge accomplishment was to overcome default [SQLite3](https://www.sqlite.org/index.html) django database and design 
a minimal candidate architecture that could sustain a production deploy. Here, our choice was to use a compose file 
using docker which would allow us to deploy our project to an aws ec2 with just one command for example. The selected 
architecture was a [Nginx](https://hub.docker.com/_/nginx) serving as proxy load balancer for two django containers with
limited cpu and ram resources and a [PostgreSQL](https://hub.docker.com/_/postgres) database for persistence. 

### The future
We could've spent some time on a fifth but not less important goal: add some monitoring to application and physical 
infrastructure logs. Considering we have an application that is going to have a non-constant request ratio along the day, 
it would be very interesting to have those metrics well documented in order to prepare some more resource efficient
deploy on aws fargate for example.

## Intall and first run
We decided to use docker along with docker-compose to build our application running script. So considering you don't have 
docker and docker-compose on your machine, please follow these instructions for installation:
[Digital Ocean: ubuntu 18.02 docker-compose installation guide](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04-pt).

Once we have docker-compose well set up, we must create a .env at project root in order to store some sensible enviroment
variables. In our case, the needed variables are:
>DB_NAME=postgres\
DB_USER=postgres\
DB_PASSWORD=postgres\
DB_HOST=db DB_PORT=5432

We are passing the true values for these variables considering we've been working on a development server.
At production level, these 4 variables must be altered at the compose file and treated like real secret and SECRET_KEY
inside settings.py should also be within .env file. Here django SECRET_KEY is hardcoded so that user loaded as fixture 
in entrypoint.sh may be used to validade jwt tokens. 

The single command we must now run is ```sudo docker-compose up --build``` in order
to get our application running localhost with swagger ui documentation on root.

Hope yoy enjoy.\
Any doubt, please contact contato@leobalbino.com.

