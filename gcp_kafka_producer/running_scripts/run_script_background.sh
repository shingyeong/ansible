#!/bin/bash

# $1 is the command
# $2 is the times that the command will run in the background
n=1

while [ $n -le $2 ]
do
        eval "nohup $1 &"
        n=$(( n+1 ))
done
