# Simple program to break up `ms` file output into two files. 

This script serves a pretty specific purpose for me to assess accuracy of selective sweeps from two subsamples.

Unlikely useful to others, but you never know. 

```
python ms_sub.py -h
usage: ms_sub.py [-h] --prefix PREFIX ms_file

Split ms output in two!

positional arguments:
  ms_file               File containing ms output -- assumes no line for a tree string.

options:
  -h, --help            show this help message and exit
  --prefix PREFIX, -p PREFIX
                        The output prefix to using when generating the output files
```
