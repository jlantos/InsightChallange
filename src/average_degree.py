##################################################
#                                                #  
# Coding Challenge for Insight Data Engineering  #
# Judit Lantos, 04/04/16                         #
#                                                # 
##################################################


# Import libraries
import sys
import json
from math import floor
from datetime import datetime
import heapq
import time


def extract_fields(tweet):
  """Extract created_at and hashtag fields from a tweet, convert time to 
     datetime format and keep only unique hashtags in a list"""
  time = tweet["created_at"]
  time = convert_time(time)
  hashtags = [hashtag["text"] for hashtag in tweet["entities"]["hashtags"]]
  hashtags = list(set(hashtags))

  return time, hashtags


def convert_time(time_string):
  """Convert created_at string time to datetime"""
  return datetime.strptime(time_string, "%a %b %d %H:%M:%S +0000 %Y")


def process_tweet(time, hashtags, line_num):
  """Check if the new tweet falls into current time window, handle moving window, 
     update Twitter graph, and calculate average vertex degree"""
  graph_changed = False

  # First tweet goes to tweet heap and defines max time, 
  # add its edges to edges dict
  if line_num == 1:
    heapq.heappush(process_tweet.tweet_heap, (time, hashtags))
    process_tweet.max_time = time
    process_tweet.edges, graph_changed = add_edges(process_tweet.edges, hashtags)

  else: 
    # Check if new tweet arrived less than 1 min earlier than max time
    if (process_tweet.max_time - time).total_seconds() < 60:
      # Add tweet to tweet heap and add its edges to edges dict
      heapq.heappush(process_tweet.tweet_heap, (time, hashtags))
      process_tweet.edges, graph_changed = add_edges(process_tweet.edges, hashtags)

      # Update max_time and remove older tweets from heap
      if time > process_tweet.max_time:
        process_tweet.max_time = time
        
        # Check if current min time tweet is still in window, if not remove its edges 
        while (process_tweet.max_time - process_tweet.tweet_heap[0][0]).total_seconds() >= 60:
          process_tweet.edges, graph_changed = remove_edges(process_tweet.edges, process_tweet.tweet_heap[0][1])
          heapq.heappop(process_tweet.tweet_heap)


  # Recalculate degree if tweet graph changed or return previous value
  if graph_changed:
    average_degree = calc_average_degree(process_tweet.edges)
  else:
    average_degree = process_tweet.average_degree_prev

  # Update previous degree value 
  process_tweet.average_degree_prev = average_degree
  
  return average_degree


# Initialize static variables
process_tweet.tweet_heap = []
process_tweet.average_degree_prev = 0
process_tweet.max_time = datetime(1970, 1, 1, 0, 0, 0)
process_tweet.edges = {}


def add_edges(edges, tags):
  """Add edges of a tweet to the edges dict"""
  graph_changed = False

  # Add edges to edges dict if there are at least 2 tags
  if len(tags) > 1: 
    for first_tag in tags:
      # To consider all combinations create a list containing the tags on
      # the right (k+1:n) of the current one (k)
      current_index = tags.index(first_tag)
      new_list = tags[current_index + 1 : ]
       
      # Add the edge to both nodes of the hashtag pair
      for second_tag in new_list:
        edges = insert_to_dict(edges, first_tag, second_tag)
        edges = insert_to_dict(edges, second_tag, first_tag)
    
    graph_changed = True

  return edges, graph_changed  


def insert_to_dict(edges, first_tag, second_tag):
  """Insert first_tag:second_tag to edges dict by either adding
     a new key, or adding second_tag to first_tag's value list"""
  if first_tag in edges:
    edges[first_tag].append(second_tag)
  else:
    edges[first_tag] = [second_tag]

  return edges


def remove_edges(edges, tags):
  """Remove edges of a tweet from the edges dict"""
  graph_changed = False

  # Remove edges from edges dict if there are at least 2 tags
  if len(tags) > 1: 
    for first_tag in tags:
      # To consider all combinations create a list containing the tags on
      # the right (k+1:n) of the current one (k)
      current_index = tags.index(first_tag)
      new_list = tags[current_index + 1 : ]
       
      # Remove edge from both nodes of the hashtag pair
      for second_tag in new_list:
        edges[first_tag].remove(second_tag)
        edges[second_tag].remove(first_tag)
    
    # Delete nodes (hashtags) with no edges left
    edges = {key: value for key, value in edges.items() if len(value)}
    
    graph_changed = True

  return edges, graph_changed  


def calc_average_degree(edges):
  """ Calc average graph degree from number of edges (taking into account 
      duplicate representation) and number of nodes (with at least 1 edge)
      (Handshaking lemma) """
  number_of_nodes = len(edges)
  if number_of_nodes > 0:
    two_times_number_of_edges = sum(len(set(node)) for node in edges.values())
    average_degree = two_times_number_of_edges / float(number_of_nodes)
  else:
    average_degree = 0.0

  return floor(100*average_degree)/100


def main():
  """Reads input tweet file, and outputs average graph degree for each line.
     Only tweets within the last 60 seconds contribute to the graph."""
  if len(sys.argv) != 3:
    print "Usage: ./average_degree.py file-to-read output-file-name"
    sys.exit(1)

  line_num = 0

  # Open input and output files
  tweets_file = open(sys.argv[1], "r")
  output_file = open(sys.argv[2], "w")

  # Process input file line by line
  for line in tweets_file:
    tweet = json.loads(line)

    # Check if tweet is non-empty "useful" tweet
    try:
      # Get created_at and hashtag fields
      time, hashtags = extract_fields(tweet)
      line_num += 1
    except KeyError:
      continue

    # Calculate average vertex degree and print it to file
    average_degree = process_tweet(time, hashtags, line_num)
    output_file.write("%.2f" % average_degree + "\n")
    print "%.2f" % average_degree
     
  # Print farewell message
  print("--- Processed %d valid tweets ---" % line_num)

  # Close files
  tweets_file.close()
  output_file.close()


# Timing run
start_time = time.time()

if __name__ == "__main__":
  main()

print("--- Running time: %s seconds ---" % (time.time() - start_time))
