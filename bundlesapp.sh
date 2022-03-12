#!/bin/bash

echo $1
if [ -z "$1" ]
  then
    echo "No argument supplied, exiting"
    exit
elif [ "$1" = "setup" ]; then
    echo "Running Setup"
    pip3 install virtualenv || true
    echo "creating new virtual environment"
    python3 -m venv env || true
    echo "installing requirements to $PWD/env/bin" || true
    $PWD/env/bin/pip3 install -r requirements.txt
elif [ "$1" = "delete_bundle" ]; then
    $PWD/env/bin/python3.9 delete_metafields.py
    echo "deleted bundle metafields"
elif [ "$1" = "configure_bundle" ]; then
    echo "configuring bundle"
    $PWD/env/bin/python3.9 configure_bundle.py
    echo "complete!!"
elif [ "$1" = "create_webhook" ]; then
    if [ -z "$2" ]; then
      echo "issue starting server - ngrok not supplied"
      exit
    else
      $PWD/env/bin/python3.9 create_webhook.py $2
    fi
elif [ "$1" = "start_server" ]; then
    echo "starting_server"
    $PWD/env/bin/python3.9 app.py
else
    echo "-----unknown command------"
fi