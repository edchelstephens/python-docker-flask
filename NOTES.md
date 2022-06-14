# Docker Lifecycle

1. Starts with a dockerfile

- Commands used to assemble an image
- A document containing commands docker should follow to build an image

2. Dockerfile creates Docker Image

- A read-only template with instructions for creating a container
- When we build our application, the end result is an image, which is the artifact that we either store locally or push to a Docker repository like Docker Hub.

3. Images are used to create runtime instances which are called Containers

- Docker container is a runtime instance of an Image running in a Docker engine
