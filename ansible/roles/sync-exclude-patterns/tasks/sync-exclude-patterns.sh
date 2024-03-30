#!/bin/bash

echo $(pwd)

cat "../.dockerignore" | awk '!/^#/ && !/^$/' > config/exclude-patterns.txt
