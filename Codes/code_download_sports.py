import urllib.request
from bs4 import BeautifulSoup
import time, glob, re
from time import sleep
from random import randint
import sys, random, copy
from collections import defaultdict, Counter
import json, difflib
from itertools import combinations, product, permutations


user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
headers = { 'User-Agent' : user_agent }

def checkurl(url):
	try:
		f = urllib.request.urlopen(urllib.request.Request(url, headers=headers))
		deadLinkFound = False
	except:
		deadLinkFound = True
	return deadLinkFound


def download_nba_seasons_months_data(destdir) :

	# monthlist = ['october', 'november', 'december']
	# monthlist = ['january', 'february', 'march', 'april', 'may', 'june', 'july']

	for years in range(2020, 2024, 1) :
			print(years)
		# for m in monthlist :
			# print(m)
			# urllink = "https://www.basketball-reference.com/leagues/NBA_"+str(years)+'_games-'+str(m)+'.html'
			# base_url = "https://www.pro-football-reference.com/years/"+str(years)+"/games.htm"
			urllink = "https://www.baseball-reference.com/leagues/MLB/"+str(years)+"-schedule.shtml"
			# base_url = "https://www.hockey-reference.com/leagues/NHL_"+str(years)+"_games.html"

			if checkurl(str(urllink)) == False :
				base_url = urllib.request.Request(urllink, headers=headers)
				urlopen = urllib.request.urlopen(base_url)

				# outputhtml = str(years)+'__'+str(m)+'.html'
				outputhtml = str(years)
				wext = open(destdir+str(outputhtml),'wb')
				wext.write(urlopen.read())
				
				wext.close()
				sleep(randint(20,30))


 
def download_nba_leagues_coaches_data(destdir) :

	for years in range(2020, 2025, 1) :
		print(years)
		
		# urllink = "https://www.basketball-reference.com/leagues/NBA_"+str(years)+"_coaches.html"
		urllink = "https://www.baseball-reference.com/leagues/MLB/"+str(years)+"-managers.shtml"
		# base_url = "https://www.pro-football-reference.com/years/"+str(years)+"/coaches.htm"

		if checkurl(str(urllink)) == False :
			base_url = urllib.request.Request(urllink, headers=headers)
			urlopen = urllib.request.urlopen(base_url)

			# outputhtml = str(years)+'__'+str(m)+'.html'
			outputhtml = str(years)+'.html'
			wext = open(destdir+str(outputhtml),'wb')
			wext.write(urlopen.read())
			
			wext.close()
			sleep(randint(20,30))



def extract_match_by_match_nba(sourcedir, destdir, seasonyear):

	filelist = glob.glob(sourcedir+'*'+str(seasonyear)+'*.html')
	filelist.sort()


	fout01 = open(destdir+'NBA_season_'+str(seasonyear)+'_match_by_match_score_team_info.txt', 'w')
	print('date|seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|home_name|home_id|home_pts',file=fout01)


	i = 0
	for filename_1 in filelist:
		print(i, filename_1)

		f = open(filename_1,'r', encoding='utf-8')
		soup2 = BeautifulSoup(f, "lxml")

		gameinfo = soup2('tbody')

		lengameinfo = len(gameinfo)
		j = 0
		for games in gameinfo :
			print(j)
			for datainfo in games('tr') :
				if len(datainfo('a')) > 0:
					# print(datainfo)
					date = datainfo('a')[0].text

					visitor_name = datainfo('a')[1].text.replace(' ','_')
					visitor_id = datainfo('a')[1]['href'].split('/')[2]
					visitor_pts = datainfo('td',{'data-stat':'visitor_pts'})[0].text

					home_name = datainfo('a')[2].text.replace(' ','_')
					home_id = datainfo('a')[2]['href'].split('/')[2]
					home_pts = datainfo('td',{'data-stat':'home_pts'})[0].text

					boxscoreidurl = datainfo('a')[3]['href']
					boxscoreid = datainfo('a')[3]['href'].split('/')[2][:-5]

					print('%s|%s|%s|%s|%s|%s|%s|%s|%s' % (date, seasonyear, boxscoreid, visitor_name, visitor_id, visitor_pts, home_name, home_id, home_pts),file=fout01)




def download_boxscore_matchbymatch_nba(sourcedir, destdir, seasonyear, n1, n2):

	infile = open(str(sourcedir)+'NBA_season_'+str(seasonyear)+'_match_by_match_score_team_info.txt','r')
	datain = infile.readlines()

	j = 0
	for line in datain[int(n1):1+int(n2)]:

		line = line.strip().split('|')
		boxscoreidurl = "/boxscores/"+str(line[2])+'.html'

		urllink = "https://www.basketball-reference.com"+str(boxscoreidurl)
		print(j, urllink)

		if checkurl(str(urllink)) == False :
			base_url = urllib.request.Request(urllink, headers=headers)
			urlopen = urllib.request.urlopen(base_url)

			outname = str(boxscoreidurl.split('/')[2][:-5])+'__'+str(seasonyear)

			filename = str(outname)+'.html'

			wext = open(destdir+str(filename),'wb')
			wext.write(urlopen.read())
			
			wext.close()
			sleep(randint(20,30))
			j+=1






if __name__ == "__main__" :
	f1 = sys.argv[1]; f2 = sys.argv[2]; f3 = sys.argv[3]; f4 = sys.argv[4]; f5 = sys.argv[5]

	# download_nba_seasons_months_data(f1)
	# download_nba_leagues_coaches_data(f1)
	# extract_match_by_match_nba(f1, f2, f3)
	download_boxscore_matchbymatch_nba(f1, f2, f3, f4, f5)