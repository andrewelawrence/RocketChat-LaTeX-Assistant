#!/bin/bash
# load_envs.sh

if [ $# -lt 1 ]; then
  echo "Usage: $0 <script.py> [script args...]"
  exit 1
fi

source config/.env
python config/load_envs.py "$@"
