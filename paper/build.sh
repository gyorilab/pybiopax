#!/bin/bash

# From instructions at https://joss.readthedocs.io/en/latest/submitting.html#docker

docker run --rm \
  --volume $PWD:/data \
  --user $(id -u):$(id -g) \
  --env JOURNAL=joss \
  openjournals/paperdraft
