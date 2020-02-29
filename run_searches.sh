#!/bin/bash
# bash script to run tests for a particular input

echo "Choose size: "
read size

echo "Choose input: "
read input

echo "Skip uninformed search? 0 for no, 1 for yes: "
read skip

> output.txt
> output2.txt
> output3.txt

if [ $skip -eq 0 ]; then
  python CS3243_P1_41_5.py public_tests_p1/n_equals_${size}/input_${input}.txt output.txt 1
  else
  python CS3243_P1_41_5.py public_tests_p1/n_equals_${size}/input_${input}.txt output.txt
fi
