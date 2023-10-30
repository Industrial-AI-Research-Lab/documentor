# Deployment

## Description

Folder for storing scripts and dockerfiles for deploying the library or its components.

## Content

### Sheet parser research container `sheet-parser`

The container is design for task cell classification and extraction from the sheet files (exel).

#### Structure:

 - `bin/container.sh` - script for building and running container
 - `docker/base.dockerfile` - dockerfile for building base with all needed libraries and programs
 - 'docker/user.dockerfile' - dockerfile for building image with setting user and supervisord

#### Instruction:

```shell
# move to the folder with the container
cd deployment/sheet-parser

# allow execution of the container script
chmod +x bin/container.sh

# build base of image with needed libraries
./bin/container.sh build-base

# build image with setting user
./bin/container.sh build

# run container, port for jupyter notebook will be printed in console
./bin/container.sh start
```