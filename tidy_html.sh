#!/bin/bash

if [[ $# -eq 0 ]]
then
    echo "Need to specify which html file to tidy up as argument"
else
    #tidy -qim --indent-spaces 4 $1  --vertical-space auto
    tidy -im --indent-spaces 4 $1 
fi
