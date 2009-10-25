## Flickr Social Venn Diagram -- Weighted Contact Intersection

A quick hack to generate a weighted contact intersection venn diagram for a Flickr user and their closest neighbors.  It was used for research purposes to see how socially interconnected a specific Flickr members is (e.g. do they have any marked contacts with whom they have high social network overlap).  Warning: this can be REALLY SLOW to run for highly-connected Flickr members.

You will need to put your own API key/secret into the variables of the file.

Usage:
`python flickrsocialvenn.py -u username`

The last thing it dumps to STDOUT will be a URL to your graph (via Google Charts)

## Examples

![example1](http://chart.apis.google.com/chart?chs=450x200&cht=v&chdl=PablitoR|wendy%20marie|steponnopets&chd=t:7,4,5,3,3,3,2&chtt=Weighted+contact+intersection+for+PablitoR)
![example2](http://chart.apis.google.com/chart?chs=450x200&cht=v&chdl=jonathan_katzman|rtsai|pgriess&chd=t:47,12,21,2,2,2,1&chtt=Weighted+contact+intersection+for+jonathan_katzman)