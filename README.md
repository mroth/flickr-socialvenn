== Flickr Social Venn Diagram -- Weighted Contact Intersection

A quick hack to generate a weighted contact intersection venn diagram for a Flickr user and their closest neighbors.  It was used for research purposes to see how socially interconnected a specific Flickr members is (e.g. do they have any marked contacts with whom they have high social network overlap).  Warning: this can be REALLY SLOW to run for highly-connected Flickr members.

Usage:
python flickrsocialvenn.py -u username

The last thing it dumps to STDOUT will be a URL to your graph (via Google Charts)

![example1](http://chart.apis.google.com/chart?chs=450x200&cht=v&chdl=flickrjo|cburg|ginormous&chd=t:163,124,45,36,26,29,24&chtt=Weighted+contact+intersection+for+flickrjo)