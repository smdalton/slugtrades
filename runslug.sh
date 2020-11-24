#!/bin/bash

docker build . -t slug_trades:latest
docker run -p 8015:8000 slug_trades:latest

