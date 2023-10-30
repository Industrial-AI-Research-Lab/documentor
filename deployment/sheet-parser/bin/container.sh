#!/usr/bin/env bash

set -e

if [[ -z "$USER_NAME" ]]; then
  username=$(whoami)
else
  username="$USER_NAME"
fi

user_id="$(id -u)"

#if [[ $username == "root" ]]; then
#  username="muskrat"
#  user_id="124"
#fi

image_name=sheet-parser
base_image=base-${image_name}
image=${username}-${image_name}
registry="node2.bdcl:5000"
max_start_attempts=15
dockerfile_dir="./docker"

echo "Running with user: ${username}"

function build_artm() {
  docker build --build-arg IMAGE="${base_image}:latest" \
    -t "${base_image}:latest" \
    -f ${dockerfile_dir}/artm.dockerfile \
    ${dockerfile_dir}
}

function build_base() {
  docker build -t "${base_image}:latest" -f ${dockerfile_dir}/base.dockerfile ${dockerfile_dir}
}

function pull() {
  docker pull "${registry}/${base_image}:latest"
  docker tag "${registry}/${base_image}:latest" "${base_image}:latest"
}

function push_base() {
  docker tag "${base_image}:latest" "${registry}/${base_image}:latest"
  docker push "${registry}/${base_image}:latest"
}

function build() {
  docker build --build-arg IMAGE="${base_image}:latest" \
    --build-arg JUSER_ID=${user_id} \
    --build-arg JUSER=${username} \
    -t "${image}:latest" \
    -f ${dockerfile_dir}/user.dockerfile \
    ${dockerfile_dir}
}

function pull() {
  docker pull "${registry}/${image}:latest"
  docker tag "${registry}/${image}:latest" "${image}:latest"
}

function push() {
  docker tag "${image}:latest" "${registry}/${image}:latest"
  docker push "${registry}/${image}:latest"
}

function start() {
  attempt=0

  while [ ${attempt} -lt ${max_start_attempts} ]; do
    echo "Trying to launch container. Attempt: "${attempt}
    echo "Image: "${image}
    jupyter_port=$(shuf -i 8000-10000 -n 1)
    tensorboard_port=$((jupyter_port + 1))
    supervisord_port=$((jupyter_port + 2))
    out=$(docker run \
      -m 80g --cpuset-cpus=0-35 \
      -d \
      --shm-size="20g" \
      -p "${jupyter_port}":8888 \
      -p ${tensorboard_port}:6006 \
      -p ${supervisord_port}:9001 \
      -v "${HOME}":/home/jovyan/notebooks \
      -v /mnt/ess_storage/DN_1/:/mnt/ess_storage/DN_1/ \
      -v /raid/sg_user_data/:/raid/sg_user_data \
      -v /mnt/shdstorage:/mnt/shdstorage \
      ${image} \
      2>&1)
    echo "Trying to launch container. Attempt: "${attempt}
    ecode=$?
    if [ ${ecode} -eq 0 ]; then
      echo "Container has been successfully launched listening on the ports:
        - ${jupyter_port} for jupyterlab
        - ${tensorboard_port} for tensorboard
        - ${supervisord_port} for supervisord
        Don't forget to enable the use of extensions for the Jupiterlab!
        "
      break
    fi

    if [[ $out != *"port is already allocated"* ]]; then
      # shellcheck disable=SC2028
      echo "Docker error: \n ""$out"
      exit 1
    else
      echo "Chosen ports are already bound trying another time"
    fi

    attempt=$((attempt + 1))
  done

  if [ ${attempt} -eq ${max_start_attempts} ]; then
    echo "Not found free ports. Aborting."
    exit 1
  fi
}

function stop() {
  docker ps | grep ${username}- | awk '{ print $1 }' | xargs --no-run-if-empty docker stop
}

function rm() {
  docker ps -a | grep ${username}- | grep Exited | awk '{ print $1 }' | xargs --no-run-if-empty docker rm
}

function list() {
  docker ps -a | grep ${username}-
}

function list_running() {
  docker ps | grep ${username}-
}

function ports() {
  docker ps | grep ${username}- | awk '{ print $1 }' | xargs --no-run-if-empty docker inspect -f "{{ .NetworkSettings.Ports }}"
}

function help() {
  echo "This is a helper script to build and run your personal container with correct user inside.
It has the following commands:
    install - build an image and deploy it to the local registry (will  be accessible from all servers)
    build - build an image with correct user inside.
    pull - pull an image belonging to the current user from the predefined registry ${registry}.
    push - push an image belonging to the current user to the predefined registry ${registry}.
    install-base - same as install, but for base (not user-dependent) image
    build-base - same as build, but for base (not user-dependent) image
    pull-base - same as pull, but for base (not user-dependent) image
    push-base - same as push, but for base (not user-dependent) image
    install-artm - building a new image based on a user image with artm inside
    start - run container with previously build image.
    stop - stop all conatiners belonging to the current user.
    rm - removes all stopped containers belonging to the current user.
    list - list all containers belonging to the current user.
    list-running - list all containers currently executing belonging to the current user.
    help - prints this message.
"
}

function main() {
  cmd=$1
  shift 1

  case "$cmd" in
  "install")
    build "${@}"
    push
    ;;

  "build")
    build "${@}"
    ;;

  "pull")
    pull
    ;;

  "push")
    push
    ;;

  "install-base")
    build_base
    push_base
    ;;

  "build-base")
    build_base
    ;;

  "pull-base")
    pull_base
    ;;

  "push-base")
    push_base
    ;;

  "build-artm")
    build_artm
    ;;

  "start")
    start "${@}"
    ;;

  "stop")
    stop "${@}"
    ;;

  "rm")
    rm "${@}"
    ;;

  "list")
    list "${@}"
    ;;

  "list-running")
    list_running "${@}"
    ;;

  "ports")
    ports
    ;;

  "help")
    help
    ;;

  *)
    echo "Unknown command: ""$cmd"
    ;;
  esac
}

main "${@}"
