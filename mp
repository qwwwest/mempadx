#!/bin/bash 

cd ~/mempadx

source .venv/bin/activate
which python3
echo "Starting Mempad..."
python3 main.py

deactivate

echo "bye."
