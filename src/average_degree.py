##################################################
#                                                #  
# Coding Challenge for Insight Data Engineering  #
# Judit Lantos, 04/04/16                         #
#                                                # 
##################################################


# Import libraries
import sys
import json
import pandas as pd



def build_edges(data):
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
        # to existing node 
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
  # Calc average degree from number of edges (taking into account duplicate
  # representation) and number of nodes (with edges)
  # (Handshaking lemma)
  two_times_number_of_edges = sum(len(node) for node in edges.values())
  number_of_nodes = len(edges)
  average_degree = two_times_number_of_edges / float(number_of_nodes)
  
  # Crop float result to 2 decimal points without rounding
  before_dec, after_dec = str(average_degree).split('.')
  return '.'.join((before_dec, after_dec[:2]))


# main()
def main():
  if len(sys.argv) != 3:
    print 'Usage: ./average_degree.py file-to-read output-file-name'
    sys.exit(1)

  data = []
  datalimit = 0
  proper = 0
  linenum = 0

  # Open input file
  tweets_file = open(sys.argv[1], "r")

  # Process input file line by line
  for line in tweets_file:
    tweet = json.loads(line)
    linenum += 1
    try:
      limit = tweet['limit']
      datalimit += 1
      # print limit
    except:
      try:
        time = tweet['created_at']
        hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
        data.append([time, hashtags])
        # print time
        proper += 1
      except:
        print linenum
        continue

  average_degree = calc_average_degree(build_edges(data))

  print average_degree
 
  #print data
  #print len(data), proper, datalimit
  #print data[-10:]




if __name__ == '__main__':
  main()
