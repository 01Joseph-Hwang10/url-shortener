#!/bin/bash

cat "../.dockerignore" | awk '!/^#/ && !/^$/' > config/exclude-patterns.txt
