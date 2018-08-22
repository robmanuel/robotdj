# -*- coding: utf-8 -*-

# Robot DJ
# 
# Plays songs from UK charts from @robmnauel

# Made because I want Spotify to have a Random button
# but not too random - figured chart data would serve
# ... then made it work via speech simply because it's
# funnier. Far less reliable. But funnier.

# Requires:

# * OS X computer attached to speakers loud enough for Alexa to hear
# * Alexa
# * A Spotify account connected to Alexa

# you could probably change this "OK Google" etc - but I 
# don't have one to test - I found "ah-lex-uh" worked better
# than "alexa" but your mileage may vary.

vassistant="ah-lex-uh" 

# requires chart data available at
# https://github.com/yatace/UKSingleCharts/blob/master/all.json?raw=true

remotecharts="https://github.com/yatace/UKSingleCharts/blob/master/all.json?raw=true"

# THINGS TO DO

# write a shitty blog post about it
# filter data so tracks are just once rather than every time they chart

# DONE

# help key DONE lol
# youtube search DONE
# remove songs/song2 DONE
# remove after FT. or Featuring. DONE
# make the play command lowercase? DONE
# Limit year function DONE SORTA
# remove brackets [({ DONE
# make it download file... YES
# Make it loop? YES
# MAKE limit less buggy DONE
# uploade to github DONE


import json, random, webbrowser, re
from os import system
from random import shuffle
import os.path


def getCharts(remotecharts):
	charts="all.json"
	if os.path.isfile(charts): 
		print "Chart data already downloaded"
	else:
		print "Best download some chart data then"
		system ("wget -O %s %s" % (charts,remotecharts))
	print "Reading file: %s" % charts
	with open(charts, "r") as read_file:
		data = json.load(read_file)
	print "%d hits in system. Woo." % len (data)
	return data

def expandfeaturing(str):
	return str.replace (" FT ", " FEATURING ")

def killbrackets(str):
	return re.sub(r'[\{\(\[].*[\)\}\]]', '', str)

def killslashes(str):
	# return "CAKE" if sent "CAKE/MONKEY" coz double A sides
	
	if "/" in str:
		str=str.split("/")[0]
	return str

def trackInfo(track):
	ret={}
	ret["title"]=killslashes(killbrackets(track["title"]))
	ret["artist"]=expandfeaturing(killslashes(track["artist"][0]))

	ret["position"]=track["position"]

	if track["cover"].count("=") > 0:
		ret["cover"]=track["cover"].split("=")[1]
	else:
		ret["cover"]=None

	ret["peak"]=int(track["peak"])
	ret["year"]=int(track["chartId"].split("-")[1][0:4])
	ret["month"]=int(track["chartId"].split("-")[1][4:6])
	ret["day"]=int(track["chartId"].split("-")[1][6:8])

	return ret

def printTrack (trackdata):
	print "%s by %s" %  (trackdata["title"], trackdata["artist"]),
	if limit==None:
		print "\n"
	else:
		print "-- Search: '%s'" % limit
	print "No %s in %s/%s/%s (current peak: %s)" % (trackdata["position"],trackdata["day"],trackdata["month"],trackdata["year"],trackdata["peak"]) 


superloop=True
print "-"*60
print "Welcome to ROBOT DJ by @robmanuel\n"*10

data=getCharts(remotecharts)

limit=None

while superloop==True:

	shuffle (data)
	

	for track in data:
		trackdata=trackInfo (track)
		if limit != None:
			if (limit.lower() in trackdata["artist"].lower()) or (limit.lower() in trackdata["title"].lower()) or (limit in str(trackdata["year"])):
				loop=True
			else:
				loop=False
				#printTrack(trackdata)
		else:
			loop= True

		while loop==True:
			print "-"*60
			printTrack(trackdata)
			next=raw_input("Press [ENTER] for next, [p] to play, type any word to search, and [h] for help: ")
			if next=="p":
				# p = use say command to trigger Alexa
				cmd=u"say \"%s. Play the song %s. By %s\"" % (vassistant,trackdata["title"].title(), trackdata["artist"].title())
				print "playing...%s" %cmd
				system (cmd)
			elif next=="y":
				# y = google for youtube link
				url="http://www.google.com/search?q=youtube+%s+%s&btnI" % (trackdata["artist"],trackdata["title"])
				webbrowser.open(url)
			elif next=="r":
				print "Deleting search: %s" % limit
				limit=None
			elif next=="t":
				# t = dump track info (debugging really)
				print track
			elif next=="c":
				# c = show cover
				print "Cover: %s" % trackdata["cover"]
				webbrowser.open(trackdata["cover"])
			elif next=="m":
				# use say command to find more music by same artist
				cmd=u"say \"%s. Play %s\"" % (vassistant,trackdata["artist"].title())
				system (cmd)
			elif next=="w":
				# w = look up track on wikipedia
				url="https://en.wikipedia.org/w/index.php?search=%s %s" % (trackdata["artist"],trackdata["title"])
				webbrowser.open(url)
			elif next=="e" or next=="q" :
				# e = quit to command prompt
				system ("say \"%s. Stop.\"" % vassistant)			
				print "bye bye you old sausage"
				exit()
			elif next=="h":
				# h = help command
				print "-"*60
				print "ROBOT DJ by @robmanuel\n\nKeys\n\n[ENTER]: Suggest next track\np: play track (Alexa)\ntype a word: search for something i.e. duran duran or limit to songs from 1980s by '198'\nr: reset search\nm: more tracks by same artist (Alexa)\ny: Youtube play\nw: Wikipedia lookup\nc: cover - show it!\ne: exit\nh: help\n\n"
			elif len(next)>0:
				# let's assume it's a limit
				print "Limiting to: %s" % limit
				limit=next
				loop=False
			else:
				# goto next track
				loop=False
	
	if limit==None:
		print "We've bust through to end of chart data..."
	else:
		q=raw_input("Reached end of chart data. Shall we reset the search? (y/n)")
		if q=="n":
			print "Keeping search: %s" % limit 
		else:
			limit=None