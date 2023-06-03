#! /usr/bin/bash

# This script counts number of python(for now) lines in a project
# Command line params: 
#   a) project position(should be the same dir if not specified)
#   b) boolean param indicating whether or not to count empty lines(default is False)
#   c) ... ?

lines_sum=0;
file_number=0;

# TODO: use $1 here instead of '.'
for py_file in $(find . -type f -iname '*.py'); do 
	(( lines_sum += $(cat $py_file | wc -l) ));
	(( file_number += 1 ));
	printf "%-3d%s\n" $file_number $py_file; 
done; 

printf "\nTotal count: %d\n" $lines_sum;

read

exit 0;
