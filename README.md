# Insight Data Engineering - Coding Challenge

## Table of contents
1. [Challenge summary](README.md#challenge-summary)
2. [Run the code](README.md#run-the-code) 
3. [About the algorithm](README.md#about-the-algorithm)
4. [Testing](README.md#testing)


## Challenge summary 
[Back to Table of contents](README.md#table-of-contents)

>Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears. You will thus be calculating the average degree over a 60-second sliding window.
To clarify, a Twitter hashtag graph is a graph connecting all the hashtags that have been mentioned together in a single tweet. 

See the [original challenge description](https://github.com/jlantos/coding-challenge) for further details on the hashtag graph and sliding window.

## Run the code
[Back to Table of contents](README.md#table-of-contents)

run.sh located in the root runs src/average&#95;degree.py to calculate the average hashtag graph degrees. average_degree.py requires two arguments: an input and an output file with path. 

Example usage: `python src/average&#95;degree.py tweet&#95;input/tweets.txt tweet&#95;output/output.txt`

average&#95;degree.py uses only the Python Standard Library (datetime, heapq, json, math, sys, time).
The code has been written and tested in Python 2.7.6 on a Linux 3.13.0-37-generic #64-Ubuntu machine.


## About the algorithm
[Back to Table of contents](README.md#table-of-contents)

The two main challenges of this task is maintaining the Twitter graph with the sliding window and calculating the vertex degree for each incoming tweet. Both steps need to be effective to ensure fast enough run time and low memory usage for large data sets.

1. To maintain the tweets in the current time window I've used a min heap to store the (time, hashtag list) attributes for each tweet. This data structure allows quick min look up and pop (O(1)), and relatively fast (O(log(n)) insertion. The max time is stored in a separate variable. When a new tweet arrives its time is compared with the max time to check if it's not outside of the window (more than 1 minute earlier). If max time changes the oldest tweets are checked if their time still fall in the new window and are removed as necessary. 
2. To calculate the average vertex degree I've made use of the Handshaking lemma: the sum of all vertex degrees equals to twice the number of edges of a graph. To store the edges I've used a dictionary where the keys are the graph nodes and the values are the list of the other nodes they are connected to. E.g. if  a graph has 3 nodes, which are connected like this: H2-H1-H3 then the resulting dictionary will be {H1:[H2, H3], H2:[H3], H3:[H2]}. Since all edges are accounted for at both nodes when summing the length of each lists we count twice the number of edges (just what the lemma requires). When a new tweet arrives the edges are updated based on the changes of the Tweet heap described above.
 

## Testing
[Back to Table of contents](README.md#table-of-contents)

The folder insight-testsuite contains test cases I've used for unit and system testing. The following test cases were created to test the corresponding behavior.

test-2-tweets-all-distinct: building Twitter graph, all edges are distinct
test-2-tweets-almostsametagintweet: hashtags are treated as case-sensitive
test-2-tweets-duplicate: duplicate edges are counted only once for degree
test-2-tweets-outoforder-inwindow: less than 1 minute earlier tweet contributes to graph
test-2-tweets-outoforder-outofwindow: more than 1 minute earlier tweet does not contribute to graph
test-2-tweets-sametagintweet: self-loops are ignored
test-3-tweets-windowmoved-linear-duplicateedges: mulitple edges between nodes are upated correctly when window moves
test-3-tweets-windowmoved-linear: old tweets are discarded when window moves
test-3-tweets-windowmoved-outoforder: max time is correct when older (but in window) tweet arrives
test-4-tweets-windowmoved-outoforder: older, once out of order tweet is discarded correctly when window moves



