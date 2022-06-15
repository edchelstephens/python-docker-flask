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
