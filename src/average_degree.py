##################################################
#                                                #  
# Coding Challenge for Insight Data Engineering  #
# Judit Lantos, 04/04/16                         #
#                                                # 
##################################################


# Import libraries
import sys
import json
import numpy as np
from datetime import datetime
import heapq
import time



def extract_fields(tweet):
  """Extract created_at and hashtag fields from a tweet"""
  time = tweet["created_at"]
  time = convert_time(time)
  hashtags = [hashtag["text"] for hashtag in tweet["entities"]["hashtags"]]

  return time, hashtags


def build_edges(data):
  """Take a list of hashtag lists and build the dict of graph edges"""
  # Dict for edges, all edges are listed for both nodes
  edges = {}
  for tweet in data:
    tags = tweet[1]
    print tags 
    # Create edge if there are at least 2 tags
    if len(tags) > 1: 
      for tag in tags:
        current_index = tags.index(tag)
        new_list = tags[current_index + 1 : ]
       
        # Iterate through the rest of the tags and either add the edge 
        # to existing node or create new node
        for item in new_list:
          if tag in edges:
            edges[tag].append(item)
          else:
            edges[tag] = [item]
          if item in edges:
            edges[item].append(tag)
          else:
            edges[item] = [tag]

  return edges


def calc_average_degree(edges):
  """ Calc average graph degree from number of edges (taking into account 
      duplicate representation) and number of nodes (with at least 1 edge)
      (Handshaking lemma) """
  two_times_number_of_edges = sum(len(set(node)) for node in edges.values())
  number_of_nodes = len(edges)
  average_degree = two_times_number_of_edges / float(number_of_nodes)

  return np.floor(100*average_degree)/100


def convert_time(time_string):
  """Convert created_at string time to datetime"""
  return datetime.strptime(time_string, "%a %b %d %H:%M:%S +0000 %Y")


def main():
  """Reads input tweet file, and outputs average graph degree for each line.
     Only tweets within the last 60 seconds contribute to the graph"""
  if len(sys.argv) != 3:
    print "Usage: ./average_degree.py file-to-read output-file-name"
    sys.exit(1)

  data = []
  line_num = 0
  average_degree = 0
  average_degree_prev = 0

  # Open input amd output files
  tweets_file = open(sys.argv[1], "r")
  output_file = open(sys.argv[2], "w")


  # Process input file line by line
  for line in tweets_file:
    tweet = json.loads(line)


#    # Check if tweet is data limit
#    try:
#      limit = tweet["limit"]
#
    # Check if tweet is non-empty "useful" tweet
#    except:
    try:
      time, hashtags = extract_fields(tweet)

      line_num += 1

      # First tweet goes to heap and defines max time
      if line_num == 1:
        heapq.heappush(data, (time, hashtags))
        print data
        max_time = time
        print "max time " + str(max_time)
        average_degree = calc_average_degree(build_edges(data))
      else:
        time_diff = max_time - time
        print time_diff.total_seconds()
         
        # Check if new tweet arrived less than 1 min earlier
        if time_diff.total_seconds() < 60:
          # Add tweet to heap
          heapq.heappush(data, (time, hashtags))
          # Update max_time and remove older tweets from heap
          if time > max_time:
            max_time = time
            print "max time " + str(max_time)
            while (max_time-data[0][0]).total_seconds() >= 60:
              heapq.heappop(data) 
              print data
     
            average_degree = calc_average_degree(build_edges(data))

          else:
            average_degree = average_degree_prev

      average_degree_prev = average_degree
    
      output_file.write("%.2f" % average_degree + "\n")
      print "%.2f" % average_degree
     
    except:
      continue

  # Print farewall message
  print("--- Processed %d valid tweets ---" % line_num)

  # Close files
  tweets_file.close()
  output_file.close()


# Timing run
start_time = time.time()

if __name__ == "__main__":
  main()

print("--- Running time: %s seconds ---" % (time.time() - start_time))

