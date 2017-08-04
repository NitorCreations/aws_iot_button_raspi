#!/bin/bash

apt-get install -yq \
    sense-hat && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

python countdown.py
