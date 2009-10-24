#!/usr/bin/python
from flickrapi import FlickrAPI
from xml.dom import minidom
import urllib
from operator import itemgetter
import sets
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-u", "--user", dest="user",help="user to generate report for", metavar="USER")
(options, args) = parser.parse_args()

apikey_flickr = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
apikey_flickrsecret = "yyyyyyyyyyyyyyyyyyyyyy"

#########################################################################################
# make a new FlickrAPI instance
fapi = FlickrAPI(apikey_flickr, apikey_flickrsecret)

def getnsid( username ):
	"""Returns the Flickr NSID for a username"""
	rsp = fapi.people_findByUsername(api_key=apikey_flickr,username=username)
	fapi.testFailure(rsp)
	uid = rsp.user[0]['nsid']
	return uid


#### MAIN
user = options.user
nsid = getnsid(user)

#build the initial contact list
print "<!-- building user contacts list for %s... -->" % (user,)
rsp = fapi.contacts_getPublicList(api_key=apikey_flickr,user_id=nsid)
fapi.testFailure(rsp)
mycontactlist = []
for contact in rsp.contacts[0].contact:
	mycontactlist.append( contact.attrib['nsid'] )
mycontactset = sets.Set(mycontactlist)


#walk the list
neighbor_num_shared = {}
neighbor_sets = {}
neighbor_weighted = {}
for contact_nsid in mycontactlist:
	#print "checking for " + contact_nsid
	rsp = fapi.contacts_getPublicList(api_key=apikey_flickr,user_id=contact_nsid)
	fapi.testFailure(rsp)
	friendcontactlist = []
	try:
		for contact in rsp.contacts[0].contact:
			friendcontactlist.append( contact.attrib['nsid'] )
	except AttributeError: #a user had no contacts (loser!)
		pass
	friendcontactset = sets.Set(friendcontactlist)
	sharedcontactset = mycontactset.intersection(friendcontactset)
	# save the set for later
	neighbor_sets[contact_nsid] = friendcontactset
	neighbor_num_shared[contact_nsid] = len(sharedcontactset)
	neighbor_weighted[contact_nsid] = float(len(sharedcontactset)) / (len(mycontactset) + len(friendcontactset)) 
	print "%s\ttotal: %d shared: %d weighted: %f" % (contact_nsid, len(friendcontactlist), len(sharedcontactset), neighbor_weighted[contact_nsid] )

#nextdoor = sorted(neighbor_num_shared.items(), key=itemgetter(1), reverse=True)
nextdoor = sorted(neighbor_weighted.items(), key=itemgetter(1), reverse=True)
output = []
#(a,b,c) = ( sets.Set(), sets.Set(), sets.Set() )
a = mycontactset
b = neighbor_sets[ nextdoor[0][0] ]
c = neighbor_sets[ nextdoor[1][0] ]
user_a = user
#userb
rsp = fapi.people_getInfo(api_key=apikey_flickr,user_id=nextdoor[0][0])
fapi.testFailure(rsp)
user_b = rsp.person[0].username[0].elementText
#userc
rsp = fapi.people_getInfo(api_key=apikey_flickr,user_id=nextdoor[1][0])
fapi.testFailure(rsp)
user_c = rsp.person[0].username[0].elementText

# Supply one data set where:
#     * The first three values specify the relative sizes of three circles: A, B, and C.
chd = [ len(a), len(b), len(c) ] 
#     * The fourth value specifies the area of A intersecting B.
chd.append( len( a.intersection(b) ) ) 
#     * The fifth value specifies the area of A intersecting C.
chd.append( len ( a.intersection(c) ) )
#     * The sixth value specifies the area of B intersecting C.
chd.append( len ( b.intersection(c) ) )
#     * The seventh value specifies the area of A intersecting B intersecting C.
chd.append( len ( a.intersection(b).intersection(c) ) )

chdl = "|".join( [user_a, user_b, user_c] )
chd_s = ",".join([str(c) for c in  chd])
chtt = "Weighted+contact+intersection+for+" + user_a
print "http://chart.apis.google.com/chart?chs=450x200&cht=v&chdl=%s&chd=t:%s&chtt=%s" % (chdl,chd_s,chtt)
