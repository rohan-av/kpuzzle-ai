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
  echo -e "\nUninformed Search:"
  python CS3243_P1_41_1.py public_tests_p1/n_equals_${size}/input_${input}.txt output.txt
fi

echo -e "\nInformed Search (Manhattan):"
python CS3243_P1_41_2.py public_tests_p1/n_equals_${size}/input_${input}.txt output2.txt

echo -e "\nInformed Search (Manhattan + LC):"
python CS3243_P1_41_3.py public_tests_p1/n_equals_${size}/input_${input}.txt output3.txt

echo -e "\nEuclidean Distance:"
python CS3243_P1_41_4.py public_tests_p1/n_equals_${size}/input_${input}.txt output4.txt

# to be updated with the final heuristic