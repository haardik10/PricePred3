#!/usr/bin/env bash
# Update the package manager and install required build tools
apt-get update && apt-get install -y build-essential gfortran libopenblas-dev liblapack-dev
