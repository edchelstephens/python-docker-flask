# Docker Lifecycle

1. Starts with a dockerfile

- Commands used to assemble an image
- A document containing commands docker should follow to build an image

2. Dockerfile creates Docker Image

- A read-only template with instructions for creating a container
- When we build our application, the end result is an image, which is the artifact that we either store locally or push to a Docker repository like Docker Hub.

3. Images are used to create runtime instances which are called Containers

- Docker container is a runtime instance of an Image running in a Docker engine

# Dockerfile Review

- Debian Image

```
FROM scratch

ADD rootfs.tar.xz /

CMD ["bash"]
```

`FROM scratch`

- Starting point for this image, scratch means start from "scratch", or a blank image.
  This actually exists.

`ADD rootfs.tar.xz /`

- Upload the specified file to the image and, if it is compressed, decompress it to the specified location, in this case at the root of the image

`CMD ["bash"]`

- Defines the command to execute, which is the command to run when this image is ran as a container

# Docker Image Layers

- A docker image consists of read-only layers each of which represents a Dockerfile instruction. The layers are stacked and each one is a delta of change from the previous layer

- We want the least volatile statements at the beginning of the file and the most volatile statements at the end

- So in our case, we don't expect the packages in the requirement.txt to change very often, so we copy it to the image and run pip install at the beginning of the file.
  But we do expect the source code to change frequently, so we copy it at the end.

# Docker Compose

- Docker compose is a tool for defining and running multi-container Docker applications.
  With Compose, you use a YAML file to configure your application's services. Then, with single command,
  you create and start all the services from you configuration.

## Docker Compose Features

1. Multiple Isolated Environments on a single host

- This means that you can do thinkgs like creating multiple copies of a single environment,
  such as for running different brnaches of your code or for a continuous integration server
  or for running multiple applications on your computer that have the same services with the same name.
  For example, you can run two applications that both run a MySQL container, even listening on the same port
  because Docker Compose creates an isolated network t o run all of your application services.

2. Preserve volume data when containers are created/restarted

- When you launch your containers using Docker Compose,if it finds any containers from previous runs,
  then it copies the volumes from the old container to the new container, ensuring that any data that you've created in volumes is not lost.

3. Only recreate containers that have changed

- Docker compose caches the configuration used to create a container,
  so when you restart a services that hasn't changed, it reuses existing containers.
  This means that you can make changes to your environment very quickly.

4. Variables and moving a composition between environments

- Docker Compose supports variables in the Compose file that you can use to customize the composition of different environments.
  This means that you can easily configure a Docker Compose file to deploy locally or to production.

## How Docker Compose Workds

- Docker Compose works by defining a Docker Compose YAML file that references the Dockerfiles for your services and can
  optionally pull in public images. In other words, we'll reference our apps Dockerfile in the docker compose file, and if we don't need to cuztomise an image, we can define it directly in the Docker Compose YAML file.

Example:

```

services:

  # Define a productservice that references the Dockerfile in the product-service directory
  productservice:
    build: product-service


  # Define a service named web, that references the Dockerfile in the nginx directory
  web:
    build: nginx
    ports:
    - "80:80" # Expose port 80 of the internal container to port 80 external to the local machine


  # Define and configure a db service that uses the official MySQL image
  db:
    image: mysql
    # Using the command property, we add a couple additional command line properties
    # First, initialize the database from the file /data/application/init.sql
    # And then we tell MySQL to use native passwords
    command: "--init-file /data/application/init.sql --default-authentication-plugin=mysql_native_password"

    # The init.sql file is a file that we're going to write that creates our databases schema
    # So we mount it from our project's db folder to the /data/application/ directory on the container using a volume
    # This is a way that we can add files or directories to a container for which we do not define a Dockerfile.
    volumes:
      - "./db/init.sql:/data/application/init.sql"

    # Set the environment variable MYSQL_ROOT_PASSWORD=password
    # This means we can login to sql with username 'root' and password 'password'
    environment:
    - MYSQL_ROOT_PASSWORD=password

```

# NOTE: YAML files spacing and indentation are sensitive just like python, must have correct spacing and indentations

# If you see validation errors when running docker compose , the first thing you should do is check that each token,

# like services, or productservice, is properly indented with 2 spaces between levels of indentation

# Docker Compose Commands

`docker-compose build`

- build all docker containers
- This effectively executes docker buid on each service, so if your service hasn't changed, it will use the cached layer and building will be done quickly

`docker-compose up -d`

- start all docker containers, optionally in daemon mode(in the background) using -d

`docker-compose down`

- stop all containers

# Docker Compose

## Services

- A service is define as an abstract definition of a computing resource within an application that can be scaled or replaced independently form other components
- Services are backed by a set of containers ran by the platform according to replication requirements and placement constraints.
