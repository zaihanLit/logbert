#!/bin/bash
rm evalue_all.txt
for index in $( seq 0 1123 )
do
    echo $index
    cat evalue-$index.txt >> evalue_all.txt
done
