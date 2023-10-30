#!/bin/bash

set -e

if [[ -z "${JUSER_ID+x}" ]]; then
  echo "Required variable JUSER_ID is not set. Interrupting..."
  exit 1
fi

if [[ -z "${JUSER+x}" ]]; then
  echo "Required variable JUSER is not set. Interrupting..."
  exit 1
fi

echo "Creating user ${JUSER}"

useradd -u ${JUSER_ID} -d /home/jovyan ${JUSER}
python -c "from jinja2 import Template; import sys; print( Template(sys.stdin.read()).render(user='${JUSER}') )" < supervisord.conf.j2 > /etc/supervisor/supervisord.conf