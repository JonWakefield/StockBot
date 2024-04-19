#!/bin/bash

docker build -t stockbot:0.0.1 .

docker rm -f stockbot

docker run --name stockbot stockbot:0.0.1