# MakingAllRoadsSafe

This analysis was done as a part of a broader evaluation exploring the economic impact of traffic congestion in Nairobi, Kenya and the potential cost-savings that autonomous vehicle technology (AVT) might bring if implemented in a limited capacity throughout Nairobi. 

Data was collected from Uber Movement and Open Street Map (OSM).

The OSM API has a limit for how many requests can be made by an individual user. When I set out to pull this data, I first gathered all unique 'osm_way_ids' from the Uber Movement, Nairobi dataset so I was only hitting the API once for each road. However, I didn't anticipate getting kicked out of the API after only 300 hits (#RTFM).¶

My next step was to evaluate the street ID's that I'd collected. Since they weren't collected in any order, I was curious how many of these ID's happened to belong to the top 100 most traversed roads in Nairobi. Luckily, 53 of the top 100 most popular roads were included in this group. I created a new list of the remaining 47 'osm_way_ids' and refactored my code to hit the OSM API at irregular intervals. I then resumed my API calls with the narrowed list and, luckily, was not kicked out. I was then able to map the information collected on each of these most traveled roads (such as name of road, type of road, surface, etc.) to the 'osm_way_ids' in the dataset containing all trips on this set of most traveled roads. This became the basis for my analysis and visualization, which can be found in bar_plots_viz.ipynb.

I later conducted a two-sample t test on roadways during morning and evening commuting hours to determine if the average speeds during congested periods varied significantly from average speeds during non-congested periods (referred to as 'free flow rate'). 
