# Insight Data Engineering - Coding Challenge

## Table of contents
1. [Challange summary](README.md#challange-summary)
2. [Run the code](README.md#run-the-code) 
3. [About the algorithm](README.md#about-the-algorithm)
4. [Testing](README.md#testing)


## Challange summary 
[Back to Table of contents](README.md#table-of-contents)

"Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears. You will thus be calculating the average degree over a 60-second sliding window.
To clarify, a Twitter hashtag graph is a graph connecting all the hashtags that have been mentioned together in a single tweet." 

See the [original challange description](https://github.com/jlantos/coding-challenge) for further details on the hashtag graph and sliding window.

## Run the code
[Back to Table of contents](README.md#table-of-contents)

run.sh located in the root runs src/average&#95;degree.py to calculate the average hashtag graph degrees. average_degree.py requires two arguments an input and an output file with path. 

Example usage: python src/average&#95;degree.py tweet&#95;input/tweets.txt tweet&#95;output/output.txt

average&#95;degree.py uses only the Python Standard Library ( datetime, heapq, json, math, sys, time).
The code has been written and tested in Python 2.7.6 on a Linux 3.13.0-37-generic #64-Ubuntu machine.


## About the algorithm
[Back to Table of contents](README.md#table-of-contents)

The two main challanges of this task is maintaining the Twitter graph with the sliding window and effectively calculating the vertex degree for each incoming tweet.


## Testing
[Back to Table of contents](README.md#table-of-contents)


