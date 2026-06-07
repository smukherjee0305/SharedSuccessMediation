import urllib2, requests
from bs4 import BeautifulSoup
import time, glob, re
from time import sleep
from random import randint
import sys
from collections import defaultdict
from datetime import datetime
# from urllib.request import Request, urlopen 



def checkurl(url):
	try:
		f = urllib2.urlopen(urllib2.Request(url))
		deadLinkFound = False
	except:
		deadLinkFound = True
	return deadLinkFound


def download_nba_leagues_advanced_data(destdir) :

	# nfl_stats_list = ['passing','rushing','receiving','scrimmage','defense','kicking','returns','scoring']
	# mlb_stats_list = ['batting','pitching','fielding']
	nhl_stats_list = ['skaters-advanced']
	for years in range(1999, 2020, 1) :
		print years

		# base_url = "https://www.basketball-reference.com/leagues/NBA_"+str(years)+"_advanced.html"
		# base_url = "https://www.basketball-reference.com/leagues/NBA_"+str(years)+"_advanced.html"

		# for nfls in nfl_stats_list :
		# 	base_url = "https://www.pro-football-reference.com/years/"+str(years)+"/"+str(nfls)+".htm" 

		# for mlb in mlb_stats_list :
		# 	base_url = "https://www.baseball-reference.com/leagues/MLB/"+str(years)+"-standard-"+str(mlb)+".shtml"

		for nhl in nhl_stats_list :
			base_url = "https://www.hockey-reference.com/leagues/NHL_"+str(years)+"_"+str(nhl)+".html"


			if checkurl(str(base_url)) == False :
				x = urllib2.urlopen(str(base_url))
				xml_str = x.read()

				# outname = str(years)+'__'+str(mlb)
				# outname = str(years)+'__'+str(nfls)
				# outname = str(years)
				outname = str(years)+'__'+str(nhl)

				filename = destdir+str(outname)+'.html'

				file = open(filename, 'w')
				print >> file, xml_str,  
				file.close()

			sleep(randint(25,30))


def download_nba_leagues_coaches_data(destdir) :

	for years in range(1999, 2020, 1) :
		print years
		
		# base_url = "https://www.basketball-reference.com/leagues/NBA_"+str(years)+"_coaches.html"
		base_url = "https://www.baseball-reference.com/leagues/MLB/"+str(years)+"-managers.shtml"
		# base_url = "https://www.pro-football-reference.com/years/"+str(years)+"/coaches.htm"

		if checkurl(str(base_url)) == False :
				x = urllib2.urlopen(str(base_url))
				xml_str = x.read()

				outname = str(years)

				filename = destdir+str(outname)+'.html'

				file = open(filename, 'w')
				print >> file, xml_str,  
				file.close()

		sleep(randint(15,30))


def download_nba_seasons_months_data(destdir) :

	# monthlist = ['october', 'november', 'december']
	monthlist = ['january', 'february', 'march', 'april', 'may', 'june']

	for years in range(2020, 2024, 1) :
			print years
		for m in monthlist :
			# print m
			base_url = "https://www.basketball-reference.com/leagues/NBA_"+str(years)+'_games-'+str(m)+'.html'
			# base_url = "https://www.pro-football-reference.com/years/"+str(years)+"/games.htm"
			# base_url = "https://www.baseball-reference.com/leagues/MLB/"+str(years)+"-schedule.shtml"
			# base_url = "https://www.hockey-reference.com/leagues/NHL_"+str(years)+"_games.html"
			if checkurl(str(base_url)) == False :
				x = urllib2.urlopen(str(base_url))
				xml_str = x.read()

				# outname = str(years)+'__'+str(m)

				outname = str(years)

				filename = destdir+str(outname)+'.html'

				file = open(filename, 'w')
				print >> file, xml_str,  
				file.close()

			sleep(randint(15,45))



def dowload_player_chronology_nba(destdir) :

	chronolist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

	for c in chronolist[-2:] :
		print c

		base_url = "https://www.basketball-reference.com/players/"+str(c)+'/'

		x = urllib2.urlopen(base_url)
		xml_str = x.read()


		sleep(randint(15,25))

		filename = destdir+str(c)+'.html'

		file = open(filename, 'w')
		print >> file, xml_str,  
		file.close()

def download_player_stats_data(sourcedir, destdir, n1, n2) :

	globlist = glob.glob(sourcedir+'*.html')
	globlist.sort()

	print globlist[int(n1):int(n2)]
	for files in globlist[int(n1):int(n2)] :

		print files
		
		sourcepages = open(files,'r')

		soup = BeautifulSoup(sourcepages, "lxml")	

		playersscope = soup('th',{'scope':'row'})

		for players in playersscope :
				
				print players('a')[0]['href']

				base_url = "https://www.basketball-reference.com"+players('a')[0]['href']

			#if checkurl(str(base_url)) == False :

				x = urllib2.urlopen(str(base_url))
				xml_str = x.read()

				outname = str(players('a')[0].text.lower().replace(' ','_'))+'__'+str(players('a')[0]['href'].split('/')[3])

				filename = destdir+str(outname)

				file = open(filename, 'w')
				print >> file, xml_str,  
				file.close()

				sleep(randint(5,15))


def extract_player_info_boxscores_nba(sourcedir, season) :

	globlist = glob.glob(sourcedir+'*__'+str(season)+'.html')
	globlist.sort()
	print globlist
	
	outfile = open('../Data/BoxScores/matchbymatchinfo/NBA_season_'+str(season)+'_match_by_match_box_score_player_info.txt','w')

	for files in globlist :

		matchid = files.split('/')[-1][:-5].split('__')[0]
		season = files.split('/')[-1][:-5].split('__')[1]
		sourcepages = open(files,'r')

		soup = BeautifulSoup(sourcepages, "lxml")		

		players_team_1 = soup('table',{'class':"sortable stats_table"})[0]('tbody')[0]('tr')
		players_team_2 = soup('table',{'class':"sortable stats_table"})[2]('tbody')[0]('tr')



		team1_info = soup('table',{'class':"sortable stats_table"})[0]('caption')[0].text.encode('ascii', 'ignore').replace(' ','_').split('_(')[0]
		team2_info = soup('table',{'class':"sortable stats_table"})[2]('caption')[0].text.encode('ascii', 'ignore').replace(' ','_').split('_(')[0]


		for k in players_team_1 :
			if len(k('td',{'data-stat':'reason'})) == 0: ### Exclude did not play

				if len(k('th',{'class':'left'})) > 0:
					name_id = k('th',{'class':'left'})[0]('a')[0]['href'].split('/')[-1][:-5]
					name_text = k('th',{'class':'left'})[0]('a')[0].text.encode('ascii', 'ignore').replace(' ','_')


					print >> outfile, '%s|%s|%s|%s|%s' % ( matchid, team1_info, name_id, name_text, season )




		for k in players_team_2 :
			if len(k('td',{'data-stat':'reason'})) == 0: ### Exclude did not play

				if len(k('th',{'class':'left'})) > 0:
					name_id = k('th',{'class':'left'})[0]('a')[0]['href'].split('/')[-1][:-5]
					name_text = k('th',{'class':'left'})[0]('a')[0].text.encode('ascii', 'ignore').replace(' ','_')


					print >> outfile, '%s|%s|%s|%s|%s' % ( matchid, team2_info, name_id, name_text, season )






def extract_match_info_schedule_nhl(sourcedir, destdir, seasonyear):

	filelist = glob.glob(sourcedir+'*'+str(seasonyear)+'*.html')
	filelist.sort()

	outfile = open('../Data/BoxScores/matchbymatchinfo/NHL_season_'+str(seasonyear)+'_match_by_match_score_team_info.txt','w')
	print >> outfile, 'date|seasonyear|boxscoreid|visitor_name|visitor_id|visitor_goals|home_name|home_id|home_goals'


	for filename_1 in filelist:


		f = open(filename_1,'r')
		soup2 = BeautifulSoup(f, 'lxml')

		gameinfo = soup2('tbody')

		lengameinfo = len(gameinfo)

		for games in gameinfo :

			for datainfo in games('tr') :
				if len(datainfo('a')) > 0:

					date = datainfo('a')[0].text
					try :

						visitor_name = datainfo('a')[1].text.replace(' ','_')
						visitor_id = datainfo('a')[1]['href'].split('/')[2]
						visitor_goals = datainfo('td',{'data-stat':'visitor_goals'})[0].text

						home_name = datainfo('a')[2].text.replace(' ','_')
						home_id = datainfo('a')[2]['href'].split('/')[2]
						home_goals = datainfo('td',{'data-stat':'home_goals'})[0].text

						boxscoreidurl = datainfo('a')[0]['href']
						boxscoreid = datainfo('a')[0]['href'].split('/')[2][:-5]

						print >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( date, seasonyear, boxscoreid, visitor_name, visitor_id, visitor_goals, home_name, home_id, home_goals )


					except IndexError,e :
						continue


def extract_match_info_schedule_nfl(sourcedir, destdir, seasonyear):

	filelist = glob.glob(sourcedir+'*'+str(seasonyear)+'*.html')
	filelist.sort()

	outfile = open('../Data/BoxScores/matchbymatchinfo/NFL_season_'+str(seasonyear)+'_match_by_match_score_team_info.txt','w')
	print >> outfile, 'date|seasonyear|boxscoreid|winner_name|winner_id|pts_win|yards_win|to_win|loser_name|loser_id|pts_lose|yards_lose|to_lose'


	for filename_1 in filelist:

		f = open(filename_1,'r')
		soup2 = BeautifulSoup(f, 'lxml')

		gameinfo = soup2('tbody')

		lengameinfo = len(gameinfo)

		for games in gameinfo :
			for datainfo in games('tr') :
				if len(datainfo('a')) > 0:

					date = datainfo('td',{'data-stat':'game_date'})[0].text


					try :

						winner_name = datainfo('td',{'data-stat':'winner'})[0].text.replace(' ','_')
						winner_id = datainfo('td',{'data-stat':'winner'})[0]('a')[0]['href'].split('/')[2]

						pts_win = datainfo('td',{'data-stat':'pts_win'})[0].text
						yards_win = datainfo('td',{'data-stat':'yards_win'})[0].text
						to_win = datainfo('td',{'data-stat':'to_win'})[0].text



						loser_name = datainfo('td',{'data-stat':'loser'})[0].text.replace(' ','_')
						loser_id = datainfo('td',{'data-stat':'loser'})[0]('a')[0]['href'].split('/')[2]

						pts_lose = datainfo('td',{'data-stat':'pts_lose'})[0].text
						yards_lose = datainfo('td',{'data-stat':'yards_lose'})[0].text
						to_lose = datainfo('td',{'data-stat':'to_lose'})[0].text

						boxscoreidurl = datainfo('td',{'data-stat':'boxscore_word'})#[0]['href']
						boxscoreid = datainfo('td',{'data-stat':'boxscore_word'})[0]('a')[0]['href'].split('/')[2][:-4]

						print >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( date, seasonyear, boxscoreid, winner_name, winner_id, pts_win, yards_win, to_win, loser_name, loser_id, pts_lose, yards_lose, to_lose)


					except IndexError,e :
						continue


def extract_coach_pages_info(sourcedir, seasonyear):

	filelist = glob.glob(sourcedir+'*'+str(seasonyear)+'*.html')
	filelist.sort()

	outfile = open('../Data/BoxScores/matchbymatchinfo/NFL_season_'+str(seasonyear)+'_coach_team_info.txt','w')
	print >> outfile, 'coachid|coachname|seasonyear|team_id|team_abbr'



	for filename_1 in filelist:

		f = open(filename_1,'r')
		soup2 = BeautifulSoup(f, 'lxml')

		gameinfo = soup2('tbody')

		lengameinfo = len(gameinfo)

		for games in gameinfo :

			for datainfo in games('tr') :
				if len(datainfo('a')) > 0:

					coachid = datainfo('a')[0]['href'].split('/')[-1][:-5]
					coachname  = datainfo('a')[0].text.encode('ascii', 'ignore').replace(' ','_')
					team_id = datainfo('a')[1]['href'].split('/')[2]
					team_abbr = datainfo('a')[1].text.encode('ascii', 'ignore')
					print >> outfile, '%s|%s|%s|%s|%s' % ( coachid, coachname, seasonyear, team_id, team_abbr )


def extract_manager_pages_mlb_info(sourcedir, seasonyear):

	filename_1 = sourcedir+str(seasonyear)+'.html'

	outfile = open('../Data/BoxScores/matchbymatchinfo/MLB_season_'+str(seasonyear)+'_manager_team_info.txt','w')
	print >> outfile, 'managerid|managername|seasonyear|team_id'

	f = open(filename_1,'r')

	soup2 = BeautifulSoup(f, 'lxml')
	# htmlpage = re.sub('<!--', '', str(soup2))
	# soup1 = BeautifulSoup(htmlpage, "lxml")

	gameinfo = soup2('tbody')

	lengameinfo = len(gameinfo)

	for games in gameinfo :

		for datainfo in games('tr') :
			if len(datainfo('a')) > 0:

				coachid = datainfo('a')[0]['href'].split('/')[-1][:-6]
				coachname  = datainfo('a')[0].text.encode('ascii', 'ignore').replace(' ','_')
				team_id = datainfo('a')[1]['href'].split('/')[2]
				print >> outfile, '%s|%s|%s|%s' % ( coachid, coachname, seasonyear, team_id )


def download_coach_info_multiple_teams(seasonyear, destdir) :



	file1 = open('../Data/BoxScores/matchbymatchinfo/MLB_season_'+str(seasonyear)+'_manager_team_info.txt','r')
	data1 = file1.readlines()[1:]

	dict_coach = defaultdict(list)

	for line in data1 :
		line = line.strip().split('|')

		dict_coach[str(line[3])].append(str(line[0]))


	print dict_coach
	for keys, values in dict_coach.items() :
		if len(values) > 1:
			for v in values :

					# base_url = "https://www.basketball-reference.com/coaches/"+str(v)+'.html'
					base_url = "https://www.baseball-reference.com/managers/"+str(v)+'.shtml'
					print base_url

					if checkurl(str(base_url)) == False :
						x = urllib2.urlopen(str(base_url))
						xml_str = x.read()


						outname = str(v)+'__'+str(keys)+'__'+str(seasonyear)

						filename = destdir+str(outname)+'.html'

						file = open(filename, 'w')
						print >> file, xml_str,  
						file.close()

					sleep(randint(25,30))

def extract_manager_multiple_teams_info(sourcedir) :


	filelist = glob.glob(sourcedir+'*.html')
	# filelist.sort()

	outfile = open('../Data/BoxScores/matchbymatchinfo/MLB_manager_multiple_team_hire_fire_info.txt','w')
	print >> outfile, 'coachinfo|coachid|coachname|dates|seasonyear|team_id|team_name|transactionstext'


# https://en.wikipedia.org/wiki/2015_Major_League_Baseball_season
	for filename_1 in filelist:

		f = open(filename_1,'r')
		soup2 = BeautifulSoup(f, 'lxml')

		coachname = soup2('h1',{'itemprop':'name'})[0].text.replace(' ','_').encode('ascii', 'ignore')
		coachinfo = filename_1[:-5].split('/')[-1]

		coachid = filename_1[:-5].split('__')[0].split('/')[-1]
		team_id = filename_1[:-5].split('__')[1]
		seasonyear = filename_1[:-5].split('__')[2]

		print >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s' % (coachinfo, coachid, coachname, "", seasonyear, team_id, "", "")





def extract_coach_hire_fire_info(sourcedir) :


	filelist = glob.glob(sourcedir+'*.html')
	filelist.sort()

	outfile = open('../Data/BoxScores/matchbymatchinfo/NBA_coach_multiple_team_hire_fire_info.txt','w')
	print >> outfile, 'coachinfo|dates|seasonyear|team_id|team_name|transactionstext'



	for filename_1 in filelist:

		f = open(filename_1,'r')
		soup2 = BeautifulSoup(f, 'lxml')

		transactionsinfo = soup2('table',{'id':'coach-transactions'})


		if len(transactionsinfo) > 0 :
			for transactions in transactionsinfo :

				coachinfo = filename_1.split('/')[-1][:-5]


				for p in transactions("p",{"class":"transaction "}) :
					
					try :
						dates = p('strong')[0].text
						team_id = p('a')[0]['href'].split('/')[-1][:-5]
						seasonyear = p('a')[0]['href'].split('/')[2]
						team_name = p('a')[0].text.replace(' ','_')

						print >> outfile, '%s|%s|%s|%s|%s|%s' % ( coachinfo, dates, seasonyear, team_id, team_name, p.text.encode('ascii', 'ignore'))

					except KeyError,e :
						continue





def extract_player_stats_advanced(sourcedir) :

	filelist = glob.glob(sourcedir+'*.html')
	filelist.sort()

	outfile = open('../Data/BoxScores/matchbymatchinfo/NBA_seasonyear_player_advanced_stats.txt','w')
	print >> outfile, 'easonyear|player_id|player_name|value_over_replacement_player|player_efficient_rating|box_plus_minus|win_shares'

	for filename_1 in filelist:

		f = open(filename_1,'r')
		soup2 = BeautifulSoup(f, 'lxml')

		full_stats_table = soup2('tr',{'class':'full_table'})

		seasonyear = filename_1.split('/')[-1][:-5]

		for s in full_stats_table :

			stats_vorp = s('td',{'data-stat':"vorp"})[0].text
			stats_per = s('td',{'data-stat':"per"})[0].text
			stats_bpm = s('td',{'data-stat':"bpm"})[0].text
			stats_ws = s('td',{'data-stat':"ws"})[0].text
			player_id = s('td',{'data-stat':"player"})[0]('a')[0]['href'].split('/')[-1][:-5]
			player_name = s('td',{'data-stat':"player"})[0]('a')[0].text.encode('ascii', 'ignore').replace(' ','_')

			print  >> outfile, '%s|%s|%s|%s|%s|%s|%s' % (  seasonyear, player_id, player_name, stats_vorp, stats_per, stats_bpm, stats_ws )



def merge_nba_coach_players_data_matchid(seasonyear) :

	date_format = "%B %d, %Y" ## coach info 
	date_format1 = "%a, %b %d, %Y" ## for match info data

	outfile = open('../Data/BoxScores/matchbymatchinfo/NBA_season_'+str(seasonyear)+'_match_by_match_score_team_coaches_info.txt','w')
	print >> outfile, 'date|seasonyear|boxscoreid|visitor_name|visitor_id|visitor_coach|visitor_pts|home_name|home_id|home_coach|home_pts'

	file0 = open('../Data/BoxScores/matchbymatchinfo/NBA_coach_multiple_team_hire_fire_info.txt','r')
	data0 = file0.readlines()[1:]

	dict_coach_team_hire_info = defaultdict(list)
	dict_coach_team_fire_info = defaultdict(list)

	for line in data0 :
		line = line.strip().split('|')
		if "Hire" in str(line[5]) :
			dict_coach_team_hire_info[str(line[3])+'|'+str(line[2])] = str(line[1])+'|'+str(line[0].split('__')[0])

		if "Appoint" in str(line[5]) :
			dict_coach_team_hire_info[str(line[3])+'|'+str(line[2])] = str(line[1])+'|'+str(line[0].split('__')[0])

		if "Reassign" in str(line[5]) :
			dict_coach_team_hire_info[str(line[3])+'|'+str(line[2])] = str(line[1])+'|'+str(line[0].split('__')[0])


		if "Fire" in str(line[5]) :
			dict_coach_team_fire_info[str(line[3])+'|'+str(line[2])] = str(line[1])+'|'+str(line[0].split('__')[0])

		if "Resign" in str(line[5]) :
			dict_coach_team_fire_info[str(line[3])+'|'+str(line[2])] = str(line[1])+'|'+str(line[0].split('__')[0])

		if "Trade" in str(line[5]) :
			dict_coach_team_fire_info[str(line[3])+'|'+str(line[2])] = str(line[1])+'|'+str(line[0].split('__')[0])




	file1 = open('../Data/BoxScores/matchbymatchinfo/NBA_season_'+str(seasonyear)+'_coach_team_info.txt','r')
	data1 = file1.readlines()[1:]

	dict_coach = defaultdict(list)

	for line in data1 :
		line = line.strip().split('|')

		dict_coach[str(line[3])].append(str(line[0]))

	dict_coach_team = defaultdict(list)
	for keys, values in dict_coach.items() :
		if len(values) == 1:
			dict_coach_team[str(keys)] = values[0] 



	file3 = open('../Data/BoxScores/matchbymatchinfo/NBA_season_'+str(seasonyear)+'_match_by_match_score_team_info.txt','r')
	data3 = file3.readlines()[1:]

	for line in data3 :
		line = line.strip().split('|')
		print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8] #
		# print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8] )

		if len(dict_coach_team[str(line[4])]) > 0 and  len(dict_coach_team[str(line[7])]) > 0:
			print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8] )


		if len(dict_coach_team[str(line[4])]) > 0 and  len(dict_coach_team[str(line[7])]) == 0:

			try :
				if datetime.strptime(str(line[0]), date_format1) >= datetime.strptime(str(dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])].split('|')[0]), date_format) :
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team_hire_info[str(line[1])+'|'+str(line[7])].split('|')[1], line[8] )
			except AttributeError,e :
				# 	print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team_hire_info[str(line[1])+'|'+str(line[7])].split('|')[1], line[8] )
				# 	print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team_hire_info[str(line[1])+'|'+str(line[7])], line[8]
				continue

			try :

				if datetime.strptime(str(line[0]), date_format1) < datetime.strptime(str(dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])].split('|')[0]), date_format) :
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])].split('|')[1], line[8] )

			except AttributeError,e :
					# print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])].split('|')[1], line[8] )
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])], line[8]
				continue


		if len(dict_coach_team[str(line[4])]) == 0 and  len(dict_coach_team[str(line[7])]) > 0:

			
			try :


				if datetime.strptime(str(line[0]), date_format1) >= datetime.strptime(str(dict_coach_team_fire_info[str(line[1])+'|'+str(line[4])].split('|')[0]), date_format) :
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4], dict_coach_team_hire_info[str(line[1])+'|'+str(line[4])].split('|')[1], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8] )
			except AttributeError,e :
					# print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4], dict_coach_team_hire_info[str(line[1])+'|'+str(line[4])].split('|')[1], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8] )
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8]
					continue

			try :

				if datetime.strptime(str(line[0]), date_format1) < datetime.strptime(str(dict_coach_team_fire_info[str(line[1])+'|'+str(line[4])].split('|')[0]), date_format) :
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4], dict_coach_team_fire_info[str(line[1])+'|'+str(line[4])].split('|')[1], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8] )

			except AttributeError,e :
				continue
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], dict_coach_team_fire_info[str(line[1])+'|'+str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8]


		if len(dict_coach_team[str(line[4])]) == 0 and  len(dict_coach_team[str(line[7])]) == 0:
			
			try :
				if datetime.strptime(str(line[0]), date_format1) >= datetime.strptime(str(dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])].split('|')[0]), date_format) and datetime.strptime(str(line[0]), date_format1) >= datetime.strptime(str(dict_coach_team_fire_info[str(line[1])+'|'+str(line[4])].split('|')[0]), date_format):
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4],  dict_coach_team_hire_info[str(line[1])+'|'+str(line[4])].split('|')[1], line[5], line[6], line[7],  dict_coach_team_hire_info[str(line[1])+'|'+str(line[7])].split('|')[1], line[8] )
			except AttributeError,e :
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8]

				continue

			try :
				if datetime.strptime(str(line[0]), date_format1) < datetime.strptime(str(dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])].split('|')[0]), date_format) and datetime.strptime(str(line[0]), date_format1) < datetime.strptime(str(dict_coach_team_fire_info[str(line[1])+'|'+str(line[4])].split('|')[0]), date_format):
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4],  dict_coach_team_fire_info[str(line[1])+'|'+str(line[4])].split('|')[1], line[5], line[6], line[7],  dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])].split('|')[1], line[8] )
			except AttributeError,e :
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8]

				continue

			try :
				if datetime.strptime(str(line[0]), date_format1) >= datetime.strptime(str(dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])].split('|')[0]), date_format) and datetime.strptime(str(line[0]), date_format1) < datetime.strptime(str(dict_coach_team_fire_info[str(line[1])+'|'+str(line[4])].split('|')[0]), date_format):
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4],  dict_coach_team_fire_info[str(line[1])+'|'+str(line[4])].split('|')[1], line[5], line[6], line[7],  dict_coach_team_hire_info[str(line[1])+'|'+str(line[7])].split('|')[1], line[8] )
			except AttributeError,e :
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8]

				continue

			try :
				if datetime.strptime(str(line[0]), date_format1) < datetime.strptime(str(dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])].split('|')[0]), date_format) and datetime.strptime(str(line[0]), date_format1) >= datetime.strptime(str(dict_coach_team_fire_info[str(line[1])+'|'+str(line[4])].split('|')[0]), date_format):
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4],  dict_coach_team_hire_info[str(line[1])+'|'+str(line[4])].split('|')[1], line[5], line[6], line[7],  dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])].split('|')[1], line[8] )
			except AttributeError,e :
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8]

				continue





def extract_nfl_boxscore_page_coach_match_info(sourcedir, seasonyear) :


	filelist = glob.glob(sourcedir+'*__'+str(seasonyear)+'.html')
	
	outfile = open('../Data/BoxScores/matchbymatchinfo/NFL_season_'+str(seasonyear)+'_match_by_match_score_team_coaches_info.txt','w')
	print >> outfile, 'boxscoreid|home_name|home_id|home_pts|home_coach|visitor_name|visitor_id|visitor_pts|visitor_coach'

	for file in filelist :
		
		boxscoreid = file.split('/')[-1].split('__')[0]

		f = open(file,'r')
		soup2 = BeautifulSoup(f, 'lxml')

		htmlpage = re.sub('<!--', '', str(soup2))

		soup1 = BeautifulSoup(htmlpage, "lxml")

		for d in  soup1('div',{'class':"scorebox"}) :
			
			# print d('a')

			if not "Next_Game" in d('a')[8].text.encode('ascii', 'ignore').replace(' ','_') :

				if not "Prev_Game" in d('a')[8].text.encode('ascii', 'ignore').replace(' ','_') :
					team_home_name = d('a')[2].text.encode('ascii', 'ignore').replace(' ','_')
					team_home_id = d('a')[2]['href']
					team_home_score = d('div',{'class':'score'})[0].text
					coach_home = d('a')[5]['href']

					team_away_name = d('a')[8].text.encode('ascii', 'ignore').replace(' ','_')
					team_away_id = d('a')[8]['href']
					team_away_score = d('div',{'class':'score'})[1].text
					coach_away = d('a')[11]['href']


				if  "Prev_Game" in d('a')[8].text.encode('ascii', 'ignore').replace(' ','_') :
					team_home_name = d('a')[2].text.encode('ascii', 'ignore').replace(' ','_')
					team_home_id = d('a')[2]['href']
					team_home_score = d('div',{'class':'score'})[0].text
					coach_home = d('a')[4]['href']

					team_away_name = d('a')[7].text.encode('ascii', 'ignore').replace(' ','_')
					team_away_id = d('a')[7]['href']
					team_away_score = d('div',{'class':'score'})[1].text
					coach_away = d('a')[9]['href']





			if "Next_Game" in d('a')[8].text.encode('ascii', 'ignore').replace(' ','_') :


				team_home_name = d('a')[2].text.encode('ascii', 'ignore').replace(' ','_')
				team_home_id = d('a')[2]['href']
				team_home_score = d('div',{'class':'score'})[0].text
				coach_home = d('a')[4]['href']

				team_away_name = d('a')[7].text.encode('ascii', 'ignore').replace(' ','_')
				team_away_id = d('a')[7]['href']
				team_away_score = d('div',{'class':'score'})[1].text
				coach_away = d('a')[9]['href']





			# print  boxscoreid, team_home_name, team_home_id, team_home_score, coach_home, team_away_name, team_away_id, team_away_score, coach_away

			print >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s' % (   boxscoreid, team_home_name, team_home_id, team_home_score, coach_home, team_away_name, team_away_id, team_away_score, coach_away )









def extract_nfl_boxscore_players_snap_counts_team_match(sourcedir, seasonyear) :


	filelist = glob.glob(sourcedir+'*__'+str(seasonyear)+'.html')
	
	outfile = open('../Data/BoxScores/matchbymatchinfo/NFL_season_'+str(seasonyear)+'_match_by_match_box_score_player_info.txt','w')
	print >> outfile, 'boxscoreid|team_name_snapc|player_id|player_name|player_pos|player_offence|player_off_pct|player_defense|player_def_pct|seasonyear'
	
	erroroutfile = open('../Data/BoxScores/matchbymatchinfo/Error_NFL_season_'+str(seasonyear)+'_match_by_match_box_score_player_info.txt','w')

	for file in filelist :
		
		boxscoreid = file.split('/')[-1].split('__')[0]

		f = open(file,'r')
		soup2 = BeautifulSoup(f, 'lxml')

		htmlpage = re.sub('<!--', '', str(soup2))

		soup1 = BeautifulSoup(htmlpage, "lxml")

		try: 
			home_team_name = soup1('div',{'id':'all_home_snap_counts'})[0]('h2')[0].text


			for k in soup1('div',{'id':'all_home_snap_counts'})[0]('tbody') :
				for t in k('tr') :

					player_id = t('th')[0]('a')[0]['href'].split('/')[-1][:-4]
					player_name = t('th')[0].text.encode('ascii', 'ignore').replace(' ','_')
					player_pos = t('td')[0].text

					player_offence = t('td')[1].text
					player_off_pct = t('td')[2].text
					player_defense = t('td')[3].text
					player_def_pct = t('td')[4].text


					print >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (boxscoreid, home_team_name, player_id, player_name, player_pos, player_offence, player_off_pct, player_defense, player_def_pct, seasonyear)



			vis_team_name = soup1('div',{'id':'all_vis_snap_counts'})[0]('h2')[0].text


			for k in soup1('div',{'id':'all_vis_snap_counts'})[0]('tbody') :
				for t in k('tr') :

					player_id = t('th')[0]('a')[0]['href'].split('/')[-1][:-4]
					player_name = t('th')[0].text.encode('ascii', 'ignore').replace(' ','_')
					player_pos = t('td')[0].text

					player_offence = t('td')[1].text
					player_off_pct = t('td')[2].text
					player_defense = t('td')[3].text
					player_def_pct = t('td')[4].text


					print >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (boxscoreid, vis_team_name, player_id, player_name, player_pos, player_offence, player_off_pct, player_defense, player_def_pct, seasonyear)


		except IndexError,e :
			print >> erroroutfile, boxscoreid 







def extract_mlb_player_statistics_batting_season(sourcedir, seasonyear) :


	file1 = sourcedir+str(seasonyear)+'__batting.html'
	
	outfile = open('../Data/BoxScores/matchbymatchinfo/MLB_season_'+str(seasonyear)+'_match_by_match_box_score_player_batting_info.txt','w')
	print >> outfile, 'seasonyear|name_id|name_text|team_text|team_id|age|gamesplayed|at_bats|runs_scored|hits|home_runs_hit|slugging_perc|onbase_plus_slugging|onbase_plus_slugging_plus'
	
	# erroroutfile = open('../Data/BoxScores/matchbymatchinfo/Error_NFL_season_'+str(seasonyear)+'_match_by_match_box_score_player_info.txt','w')


	f1 = open(file1,'r')
	soup1 = BeautifulSoup(f1, 'lxml')

	htmlpage1 = re.sub('<!--', '', str(soup1))

	soup1a = BeautifulSoup(htmlpage1, "lxml")


	for k in  soup1a('div',{'id':'div_players_standard_batting'}) :
		for q in k('tr',{'class':'non_qual'}) :

			if len(q('a')) > 1 :
				name_text = q('td',{'data-stat':'player'})[0].text.encode('ascii', 'ignore').replace(' ','_').replace('*','').replace('#','')
				name_id =  q('td',{'data-stat':'player'})[0]('a')[0]['href'].split('/')[-1][:-6]

				team_text = q('td',{'data-stat':'team_ID'})[0]('a')[0]['title'].encode('ascii', 'ignore').replace(' ','_')
				team_id = q('td',{'data-stat':'team_ID'})[0]('a')[0]['href'].split('/')[2]

				age = q('td',{'data-stat':'age'})[0].text

				gamesplayed = q('td',{'data-stat':'G'})[0].text
				at_bats = q('td',{'data-stat':'AB'})[0].text
				runs_scored = q('td',{'data-stat':'R'})[0].text
				hits = q('td',{'data-stat':'H'})[0].text
				home_runs_hit = q('td',{'data-stat':'HR'})[0].text
				slugging_perc = q('td',{'data-stat':'slugging_perc'})[0].text
				onbase_plus_slugging = q('td',{'data-stat':'onbase_plus_slugging'})[0].text
				onbase_plus_slugging_plus = q('td',{'data-stat':'onbase_plus_slugging_plus'})[0].text



				print >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (seasonyear, name_id, name_text, team_text, team_id, age, gamesplayed, at_bats, runs_scored, hits, home_runs_hit, slugging_perc, onbase_plus_slugging, onbase_plus_slugging_plus)




def extract_mlb_player_statistics_pitching_season(sourcedir, seasonyear) :


	file1 = sourcedir+str(seasonyear)+'__pitching.html'
	
	outfile = open('../Data/BoxScores/matchbymatchinfo/MLB_season_'+str(seasonyear)+'_match_by_match_box_score_player_pitching_info.txt','w')
	print >> outfile, 'seasonyear|name_id|name_text|team_text|team_id|age|gamesplayed|earned_run_avg|fip|whip|HBP|hits_per_nine|strikeouts_per_nine|strikeouts_per_base_on_balls'
	
	# erroroutfile = open('../Data/BoxScores/matchbymatchinfo/Error_NFL_season_'+str(seasonyear)+'_match_by_match_box_score_player_info.txt','w')


	f1 = open(file1,'r')
	soup1 = BeautifulSoup(f1, 'lxml')

	htmlpage1 = re.sub('<!--', '', str(soup1))

	soup1a = BeautifulSoup(htmlpage1, "lxml")


	for k in  soup1a('div',{'id':'div_players_standard_pitching'}) :

		for q in k('tr',{'class':'non_qual'}) :

			if len(q('a')) > 1 :


				name_text = q('td',{'data-stat':'player'})[0].text.encode('ascii', 'ignore').replace(' ','_').replace('*','').replace('#','')
				name_id =  q('td',{'data-stat':'player'})[0]('a')[0]['href'].split('/')[-1][:-6]

				team_text = q('td',{'data-stat':'team_ID'})[0]('a')[0]['title'].encode('ascii', 'ignore').replace(' ','_')
				team_id = q('td',{'data-stat':'team_ID'})[0]('a')[0]['href'].split('/')[2]

				age = q('td',{'data-stat':'age'})[0].text


				gamesplayed = q('td',{'data-stat':'G'})[0].text
				earned_run_avg = q('td',{'data-stat':'earned_run_avg'})[0].text
				fip = q('td',{'data-stat':'fip'})[0].text
				whip = q('td',{'data-stat':'whip'})[0].text
				HBP = q('td',{'data-stat':'HBP'})[0].text
				hits_per_nine = q('td',{'data-stat':'hits_per_nine'})[0].text
				strikeouts_per_nine = q('td',{'data-stat':'strikeouts_per_nine'})[0].text
				strikeouts_per_base_on_balls = q('td',{'data-stat':'strikeouts_per_base_on_balls'})[0].text



				print >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (seasonyear, name_id, name_text, team_text, team_id, age, gamesplayed, earned_run_avg, fip, whip, HBP, hits_per_nine, strikeouts_per_nine, strikeouts_per_base_on_balls)



def extract_nfl_boxscore_players_offense_defense_team_match(sourcedir, seasonyear):

	filelist = glob.glob(sourcedir+'*__'+str(seasonyear)+'.html')
	
	outfile1 = open('../Data/BoxScores/matchbymatchinfo/NFL_season_'+str(seasonyear)+'_match_by_match_box_score_offense_player_info.txt','w')
	print >> outfile1, 'boxscoreid|player_id|player_name|team_id|pass_cmp|pass_att|pass_yds|rush_att|rush_yds|rec_yds|seasonyear'

	outfile2 = open('../Data/BoxScores/matchbymatchinfo/NFL_season_'+str(seasonyear)+'_match_by_match_box_score_defense_player_info.txt','w')
	print >> outfile2, 'boxscoreid|player_id|player_name|team_id|def_int|def_int_yds|tackles_combined|tackles_loss|seasonyear'

	
	# erroroutfile = open('../Data/BoxScores/matchbymatchinfo/Error_NFL_season_'+str(seasonyear)+'_match_by_match_box_score_player_info.txt','w')

	for file in filelist :
		
		boxscoreid = file.split('/')[-1].split('__')[0]

		f = open(file,'r')
		soup2 = BeautifulSoup(f, 'lxml')

		htmlpage = re.sub('<!--', '', str(soup2))

		soup1 = BeautifulSoup(htmlpage, "lxml")

		# print boxscoreid
		for k in soup1('div',{'id':'all_player_offense'})[0]('tbody') :

			for t in k('tr') :
				try :
					player_id = t('th')[0]('a')[0]['href'].split('/')[-1][:-4]
					player_name = t('th')[0].text.encode('ascii', 'ignore').replace(' ','_')
					team_id = t('td',{'data-stat':'team'})[0].text.encode('ascii', 'ignore')
					pass_cmp = t('td',{'data-stat':'pass_cmp'})[0].text.encode('ascii', 'ignore')
					pass_att =  t('td',{'data-stat':'pass_att'})[0].text.encode('ascii', 'ignore')
					pass_yds = t('td',{'data-stat':'pass_yds'})[0].text.encode('ascii', 'ignore')
					rush_att = t('td',{'data-stat':'rush_att'})[0].text.encode('ascii', 'ignore')
					rush_yds = t('td',{'data-stat':'rush_yds'})[0].text.encode('ascii', 'ignore')
					rec_yds =  t('td',{'data-stat':'rec_yds'})[0].text.encode('ascii', 'ignore')

					print >> outfile1, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (boxscoreid, player_id, player_name, team_id, pass_cmp, pass_att, pass_yds, rush_att, rush_yds, rec_yds, seasonyear)

				except IndexError,e :
					continue



		for k in soup1('div',{'id':'all_player_defense'})[0]('tbody') :

			for t in k('tr') :
				try :
					player_id = t('th')[0]('a')[0]['href'].split('/')[-1][:-4]
					player_name = t('th')[0].text.encode('ascii', 'ignore').replace(' ','_')
					team_id = t('td',{'data-stat':'team'})[0].text.encode('ascii', 'ignore')
					def_int = t('td',{'data-stat':'def_int'})[0].text.encode('ascii', 'ignore')
					def_int_yds =  t('td',{'data-stat':'def_int_yds'})[0].text.encode('ascii', 'ignore')
					tackles_combined = t('td',{'data-stat':'tackles_combined'})[0].text.encode('ascii', 'ignore')
					tackles_loss = t('td',{'data-stat':'tackles_loss'})[0].text.encode('ascii', 'ignore')

					print >> outfile2, '%s|%s|%s|%s|%s|%s|%s|%s|%s' % (boxscoreid, player_id, player_name, team_id, def_int, def_int_yds, tackles_combined, tackles_loss, seasonyear)

				except IndexError,e :
					continue



def extract_nfl_player_stats_seasonwise(sourcedir, seasonyear) :

	"""
	scrimmage, scoring as player stats
	"""

	file1 = sourcedir+str(seasonyear)+'__scoring'+'.html'
	
	outfile1 = open('../Data/BoxScores/matchbymatchinfo/NFL_season_'+str(seasonyear)+'_playerstats_scoring.txt','w')
	print >> outfile1, 'player_id|player_name|team_id|team_name|age|gamesplayed|xpm|xpa|fgm|fga|scoring|seasonyear'

	file2 = sourcedir+str(seasonyear)+'__scrimmage'+'.html'


	outfile2 = open('../Data/BoxScores/matchbymatchinfo/NFL_season_'+str(seasonyear)+'_playerstats_scrimmage.txt','w')
	print >> outfile2, 'player_id|player_name|team_id|team_name|age|gamesplayed|touches|yds_from_scrimmage|rush_receive_td|seasonyear'

	
	# erroroutfile = open('../Data/BoxScores/matchbymatchinfo/Error_NFL_season_'+str(seasonyear)+'_match_by_match_box_score_player_info.txt','w')

	
	f1 = open(file1,'r')
	soup1 = BeautifulSoup(f1, 'lxml')

	f2 = open(file2,'r')
	soup2 = BeautifulSoup(f2, 'lxml')

	for k in soup1('div',{'id':'all_scoring'})[0]('tbody') :
		for t in k('tr') :
			try :

				player_id = t('td',{'data-stat':'player'})[0]('a')[0]['href'].split('/')[-1][:-4]
				player_name = t('td',{'data-stat':'player'})[0]('a')[0].text.encode('ascii', 'ignore').replace(' ','_')

				team_id = t('td',{'data-stat':'team'})[0]('a')[0]['href'].split('/')[2]
				team_text = t('td',{'data-stat':'team'})[0]('a')[0]['title'].replace(' ','_')

				age = t('td',{'data-stat':'age'})[0].text
				gamesplayed = t('td',{'data-stat':'g'})[0].text

				xpm = t('td',{'data-stat':'xpm'})[0].text
				xpa = t('td',{'data-stat':'xpa'})[0].text
				fgm = t('td',{'data-stat':'fgm'})[0].text
				fga = t('td',{'data-stat':'fga'})[0].text
				scoring = t('td',{'data-stat':'scoring'})[0].text


				print >> outfile1, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (player_id, player_name, team_id, team_text, age, gamesplayed, xpm, xpa, fgm, fga, scoring, seasonyear)



			except IndexError,e :
				continue

	for k in soup2('div',{'id':'all_receiving_and_rushing'})[0]('tbody') :
		for t in k('tr') :
			try :

				player_id = t('td',{'data-stat':'player'})[0]('a')[0]['href'].split('/')[-1][:-4]
				player_name = t('td',{'data-stat':'player'})[0]('a')[0].text.encode('ascii', 'ignore').replace(' ','_')

				team_id = t('td',{'data-stat':'team'})[0]('a')[0]['href'].split('/')[2]
				team_text = t('td',{'data-stat':'team'})[0]('a')[0]['title'].replace(' ','_')

				age = t('td',{'data-stat':'age'})[0].text
				gamesplayed = t('td',{'data-stat':'g'})[0].text

				touches = t('td',{'data-stat':'touches'})[0].text
				yds_from_scrimmage = t('td',{'data-stat':'yds_from_scrimmage'})[0].text
				rush_receive_td = t('td',{'data-stat':'rush_receive_td'})[0].text

				print >> outfile2, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (player_id, player_name, team_id, team_text, age, gamesplayed, touches, yds_from_scrimmage, rush_receive_td, seasonyear)



			except IndexError,e :
				continue






def extract_mlb_boxscore_players_team_match_stats(sourcedir, seasonyear):

	filelist = glob.glob(sourcedir+'DET201210060__'+str(seasonyear)+'.html')
	
	# outfile1 = open('../Data/BoxScores/matchbymatchinfo/MLB_season_'+str(seasonyear)+'_match_by_match_box_score_player_info.txt','w')
	# print >> outfile1, 'boxscoreid|player_id|player_name|team_name|at_bats|runs_scored|hits|onbase_perc|slugging_perc|leverage_index_avg|seasonyear'

	
	# erroroutfile = open('../Data/BoxScores/matchbymatchinfo/Error_NFL_season_'+str(seasonyear)+'_match_by_match_box_score_player_info.txt','w')

	for file in filelist :
		
		boxscoreid = file.split('/')[-1].split('__')[0]

		f = open(file,'r')
		soup2 = BeautifulSoup(f, 'lxml')

		htmlpage = re.sub('<!--', '', str(soup2))

		soup1 = BeautifulSoup(htmlpage, "lxml")

		team1 = soup1('div',{'class':'table_wrapper'})[0]('h2')[0].text.encode('ascii', 'ignore').replace(' ','_')


		for k in soup1('div',{'class':'table_wrapper'})[0]('tbody') :

			for t in k('tr') :
				try :
					player_id = t('th')[0]('a')[0]['href'].split('/')[-1][:-6]
					player_name = t('th')[0]('a')[0].text.encode('ascii', 'ignore').replace(' ','_')

					at_bats = t('td',{'data-stat':'AB'})[0].text.encode('ascii', 'ignore')
					runs_scored =  t('td',{'data-stat':'R'})[0].text.encode('ascii', 'ignore')
					hits = t('td',{'data-stat':'H'})[0].text.encode('ascii', 'ignore')
					onbase_perc = t('td',{'data-stat':'onbase_perc'})[0].text.encode('ascii', 'ignore')
					slugging_perc = t('td',{'data-stat':'slugging_perc'})[0].text.encode('ascii', 'ignore')
					leverage_index_avg =  t('td',{'data-stat':'leverage_index_avg'})[0].text.encode('ascii', 'ignore')

					# print >> outfile1, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (boxscoreid, player_id, player_name, team1, at_bats, runs_scored, hits, onbase_perc, slugging_perc, leverage_index_avg, seasonyear)
					print boxscoreid, player_id, player_name, team1, at_bats, runs_scored, hits, onbase_perc, slugging_perc, leverage_index_avg, seasonyear

				except IndexError,e :
					continue


		team2 = soup1('div',{'class':'table_wrapper'})[1]('h2')[0].text.encode('ascii', 'ignore').replace(' ','_')


		for k in soup1('div',{'class':'table_wrapper'})[1]('tbody') :

			for t in k('tr') :
				try :
					player_id = t('th')[0]('a')[0]['href'].split('/')[-1][:-6]
					player_name = t('th')[0]('a')[0].text.encode('ascii', 'ignore').replace(' ','_')

					at_bats = t('td',{'data-stat':'AB'})[0].text.encode('ascii', 'ignore')
					runs_scored =  t('td',{'data-stat':'R'})[0].text.encode('ascii', 'ignore')
					hits = t('td',{'data-stat':'H'})[0].text.encode('ascii', 'ignore')
					onbase_perc = t('td',{'data-stat':'onbase_perc'})[0].text.encode('ascii', 'ignore')
					slugging_perc = t('td',{'data-stat':'slugging_perc'})[0].text.encode('ascii', 'ignore')
					leverage_index_avg =  t('td',{'data-stat':'leverage_index_avg'})[0].text.encode('ascii', 'ignore')

					# print >> outfile1, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (boxscoreid, player_id, player_name, team1, at_bats, runs_scored, hits, onbase_perc, slugging_perc, leverage_index_avg, seasonyear)
					print boxscoreid, player_id, player_name, team2, at_bats, runs_scored, hits, onbase_perc, slugging_perc, leverage_index_avg, seasonyear

				except IndexError,e :
					continue





def merge_mlb_manager_players_data_matchid(seasonyear) :

	date_format = "%B %d, %Y" ## coach info 


	date_format1 = "%Y%m%d" ## for match info data

	outfile = open('../Data/BoxScores/MLB/textfiles/MLB_season_'+str(seasonyear)+'_match_by_match_score_team_managers_info.txt','w')
	print >> outfile, 'seasonyear|boxscoreid|visitor_name|visitor_id|visitor_manager|visitor_pts|home_name|home_id|home_manager|home_pts'

	file0 = open('../Data/BoxScores/matchbymatchinfo/MLB_manager_multiple_team_hire_fire_info.txt','r')
	data0 = file0.readlines()[1:]

	dict_coach_team_hire_info = defaultdict(list)
	dict_coach_team_fire_info = defaultdict(list)

	for line in data0 :
		line = line.strip().split('|')

		if "hired" in str(line[-1]) :
			dict_coach_team_hire_info[str(line[4])+'|'+str(line[5])] = str(line[3])+'|'+str(line[0].split('__')[0])




		if "fired" in str(line[-1]) :
			dict_coach_team_fire_info[str(line[4])+'|'+str(line[5])] = str(line[3])+'|'+str(line[0].split('__')[0])

		if "resigned" in str(line[-1]) :
			dict_coach_team_fire_info[str(line[4])+'|'+str(line[5])] = str(line[3])+'|'+str(line[0].split('__')[0])

		if "released" in str(line[-1]) :
			dict_coach_team_fire_info[str(line[4])+'|'+str(line[5])] = str(line[3])+'|'+str(line[0].split('__')[0])




	file1 = open('../Data/BoxScores/matchbymatchinfo/MLB_season_'+str(seasonyear)+'_manager_team_info.txt','r')
	data1 = file1.readlines()[1:]

	dict_coach = defaultdict(list)

	for line in data1 :
		line = line.strip().split('|')

		dict_coach[str(line[3])].append(str(line[0]))

	dict_coach_team = defaultdict(list)
	for keys, values in dict_coach.items() :
		if len(values) == 1:
			dict_coach_team[str(keys)] = values[0] 



	file3 = open('../Data/BoxScores/MLB/textfiles/MLB_season_'+str(seasonyear)+'_match_by_match_score_team_info.txt','r')
	data3 = file3.readlines()[1:]

	for line in data3 :
		line = line.strip().split('|')
		boxscoreid = line[1]
		datesmlb = boxscoreid[3:-1]

		print line[0], line[1], line[2], line[3], dict_coach_team[str(line[3])], line[4], line[5], line[6], dict_coach_team[str(line[6])], line[7] #
		# print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8] )




		if len(dict_coach_team[str(line[3])]) > 0 and  len(dict_coach_team[str(line[6])]) > 0:
			print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], dict_coach_team[str(line[3])], line[4], line[5], line[6], dict_coach_team[str(line[6])], line[7] )


		if len(dict_coach_team[str(line[3])]) > 0 and  len(dict_coach_team[str(line[6])]) == 0:

			try :
				if datetime.strptime(str(datesmlb), date_format1) >= datetime.strptime(str(dict_coach_team_fire_info[str(line[0])+'|'+str(line[6])].split('|')[0]), date_format) :
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], dict_coach_team[str(line[3])], line[4], line[5], line[6], dict_coach_team_hire_info[str(line[0])+'|'+str(line[6])].split('|')[1], line[7] )
			except AttributeError,e :
				# 	print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team_hire_info[str(line[1])+'|'+str(line[7])].split('|')[1], line[8] )
				# 	print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team_hire_info[str(line[1])+'|'+str(line[7])], line[8]
				continue

			try :

				if datetime.strptime(str(datesmlb), date_format1) < datetime.strptime(str(dict_coach_team_fire_info[str(line[0])+'|'+str(line[6])].split('|')[0]), date_format) :
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], dict_coach_team[str(line[3])], line[4], line[5], line[6], dict_coach_team_fire_info[str(line[0])+'|'+str(line[6])].split('|')[1], line[7] )

			except AttributeError,e :
					# print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])].split('|')[1], line[8] )
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team_fire_info[str(line[1])+'|'+str(line[7])], line[8]
				continue


		if len(dict_coach_team[str(line[3])]) == 0 and  len(dict_coach_team[str(line[6])]) > 0:

			
			try :


				if datetime.strptime(str(datesmlb), date_format1) >= datetime.strptime(str(dict_coach_team_fire_info[str(line[0])+'|'+str(line[3])].split('|')[0]), date_format) :
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], dict_coach_team_hire_info[str(line[0])+'|'+str(line[3])].split('|')[1], line[4], line[5], line[6], dict_coach_team[str(line[6])], line[7] )
			except AttributeError,e :
					# print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], line[4], dict_coach_team_hire_info[str(line[1])+'|'+str(line[4])].split('|')[1], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8] )
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8]
					continue

			try :

				if datetime.strptime(str(datesmlb), date_format1) < datetime.strptime(str(dict_coach_team_fire_info[str(line[0])+'|'+str(line[3])].split('|')[0]), date_format) :
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], dict_coach_team_fire_info[str(line[0])+'|'+str(line[3])].split('|')[1], line[4], line[5], line[6], dict_coach_team[str(line[6])], line[7] )

			except AttributeError,e :
				continue
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], dict_coach_team_fire_info[str(line[1])+'|'+str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8]


		if len(dict_coach_team[str(line[3])]) == 0 and  len(dict_coach_team[str(line[6])]) == 0:
			
			try :
				if datetime.strptime(str(datesmlb), date_format1) >= datetime.strptime(str(dict_coach_team_fire_info[str(line[0])+'|'+str(line[6])].split('|')[0]), date_format) and datetime.strptime(str(datesmlb), date_format1) >= datetime.strptime(str(dict_coach_team_fire_info[str(line[0])+'|'+str(line[3])].split('|')[0]), date_format):
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], dict_coach_team_hire_info[str(line[0])+'|'+str(line[3])].split('|')[1], line[4], line[5], line[6],  dict_coach_team_hire_info[str(line[0])+'|'+str(line[6])].split('|')[1], line[7] )
			except AttributeError,e :
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8]

				continue

			try :
				if datetime.strptime(str(datesmlb), date_format1) < datetime.strptime(str(dict_coach_team_fire_info[str(line[0])+'|'+str(line[6])].split('|')[0]), date_format) and datetime.strptime(str(datesmlb), date_format1) < datetime.strptime(str(dict_coach_team_fire_info[str(line[0])+'|'+str(line[3])].split('|')[0]), date_format):
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], dict_coach_team_fire_info[str(line[0])+'|'+str(line[3])].split('|')[1], line[4], line[5], line[6],  dict_coach_team_fire_info[str(line[0])+'|'+str(line[6])].split('|')[1], line[7] )
			except AttributeError,e :
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8]

				continue

			try :
				if datetime.strptime(str(datesmlb), date_format1) >= datetime.strptime(str(dict_coach_team_fire_info[str(line[0])+'|'+str(line[6])].split('|')[0]), date_format) and datetime.strptime(str(datesmlb), date_format1) < datetime.strptime(str(dict_coach_team_fire_info[str(line[0])+'|'+str(line[3])].split('|')[0]), date_format):
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], dict_coach_team_fire_info[str(line[0])+'|'+str(line[3])].split('|')[1], line[4], line[5], line[6],  dict_coach_team_hire_info[str(line[0])+'|'+str(line[6])].split('|')[1], line[7] )
			except AttributeError,e :
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8]

				continue

			try :
				if datetime.strptime(str(datesmlb), date_format1) < datetime.strptime(str(dict_coach_team_fire_info[str(line[0])+'|'+str(line[6])].split('|')[0]), date_format) and datetime.strptime(str(datesmlb), date_format1) >= datetime.strptime(str(dict_coach_team_fire_info[str(line[0])+'|'+str(line[3])].split('|')[0]), date_format):
					print  >> outfile, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (  line[0], line[1], line[2], line[3], dict_coach_team_hire_info[str(line[0])+'|'+str(line[3])].split('|')[1], line[4], line[5], line[6],  dict_coach_team_fire_info[str(line[0])+'|'+str(line[6])].split('|')[1], line[7] )
			except AttributeError,e :
					# print line[0], line[1], line[2], line[3], line[4], dict_coach_team[str(line[4])], line[5], line[6], line[7], dict_coach_team[str(line[7])], line[8]

				continue




def code_extract_coach_NBA_main_page(htmlpage) :

	f = open(str(htmlpage),'r')
	soup2 = BeautifulSoup(f, 'lxml')


	tbody = soup2('tbody')

	for t in tbody :
		for k in t('tr') :
			if len(k('th',{"data-stat":"coach"})) > 0:
				if len(k('th',{"data-stat":"coach"})[0]('a')) > 0:
					print k('th',{"data-stat":"coach"})[0]('a')[0]['href']



def code_extract_coach_MLB_main_page(htmlpage) :

	f = open(str(htmlpage),'r')
	soup2 = BeautifulSoup(f, 'lxml')


	tbody = soup2('tbody')

	for t in tbody :

		for k in t('td',{"data-stat":"manager"}) :

					print k('a')[0]['href']



def code_extract_coach_NFL_main_page(htmlpage) :

	f = open(str(htmlpage),'r')
	soup2 = BeautifulSoup(f, 'lxml')


	tbody = soup2('tbody')

	for t in tbody :

		for k in t('td',{"data-stat":"coach"}) :

					print k('a')[0]['href']


def download_coach_manager_pages(destdir, base_url, f1) :


	file1 = open(str(f1), 'r'); data1 = file1.readlines()
	i = 0
	for line in data1 :
		line = line.strip().split()

		base_url2 = str(base_url)+str(line[0])

		print i, base_url2

		if checkurl(str(base_url2)) == False :
			x = urllib2.urlopen(str(base_url2))
			xml_str = x.read()

			outname = str(line[0].split('/')[-1])

			filename = destdir+str(outname)

			file = open(filename, 'w')
			print >> file, xml_str,  
			file.close()

		sleep(randint(25,30))

		i+=1

def extract_birth_info_NHL_managers(fhtml, f2) :

	f = open(str(fhtml),'r')
	soup2 = BeautifulSoup(f, 'lxml')
	
	outfile = open(str(f2),'w')
	print >> outfile, 'managerid|manager_name|date_of_birth|year_birth'

	tbody = soup2('tbody')

	for t in tbody :

		for k in t('tr',{'class':'nhl'}) :
			

			managerid = k('th',{"data-stat":"coach"})[0]('a')[0]['href'].split('/')[-1].split('.')[0]
			manager_name = k('th',{"data-stat":"coach"})[0]('a')[0].text.encode('ascii', 'ignore').replace(' ','_')
			birthdate = k('td',{"data-stat":"birth_date"})[0].text.encode('ascii', 'ignore').replace(' ','_')
			birthyear = birthdate.split(',_')[-1]
			print >> outfile, '%s|%s|%s|%s' % (managerid, manager_name, birthdate, birthyear)


"""
Football-Soccer Database
"""
def download_soccer_pages_seasons(destdir, season1, season2) :
	user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'#'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }

	for s1 in range(int(season1), 1+int(season2)) :
		print s1

		# base_url = "https://www.transfermarkt.com/premier-league/gesamtspielplan/wettbewerb/GB1?saison_id="+str(s1)+"&spieltagVon=1&spieltagBis=38"
		# base_url = "https://www.transfermarkt.com/major-league-soccer/gesamtspielplan/wettbewerb/MLS1?saison_id="+str(s1)+"&spieltagVon=1&spieltagBis=15"
		# base_url = "https://www.transfermarkt.com/ligue-1/gesamtspielplan/wettbewerb/FR1?saison_id="+str(s1)+"&spieltagVon=1&spieltagBis=38"

		base_url = "https://www.transfermarkt.com/bundesliga/gesamtspielplan/wettbewerb/L1?saison_id="+str(s1)+"&spieltagVon=1&spieltagBis=34"

		r = urllib2.Request(base_url, headers=headers)
		x = urllib2.urlopen(r)
		xml_str = x.read()

		outname = str(s1)

		filename = destdir+str(outname)

		file = open(filename, 'w')
		print >> file, xml_str,  
		file.close()

		sleep(randint(5,15))

def extract_match_pages_soccer(sourcedir, n1, n2) :

	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }

	pagesfiles = glob.glob(sourcedir+'*')
	pagesfiles.sort()
	for pages in pagesfiles[int(n1):int(n2)] :
		# print pages

		f = open(pages,'r')
		soup1 = BeautifulSoup(f, 'lxml')

		numboxes = len(soup1("div",{"class":"large-6 columns"}))
		# print numboxes

		for k in range(0, numboxes) :
			if len(soup1("div",{"class":"large-6 columns"})[int(k)]('tbody')) > 0:
				# print soup1("div",{"class":"large-6 columns"})[int(k)]('tbody')[0]
				matchesperbox = len(soup1("div",{"class":"large-6 columns"})[int(k)]('tbody')[0]("td",{"class":"zentriert hauptlink"}))
				# print matchesperbox

				for j in range(0, matchesperbox) :
					href = soup1("div",{"class":"large-6 columns"})[int(k)]('tbody')[0]("td",{"class":"zentriert hauptlink"})[int(j)]('a')[0]['href']
					base_url = "https://www.transfermarkt.com"+str(href)

					print pages, base_url




def download_match_pages_soccer(f1, destdir, n1, n2) :

	user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'#'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }

	file1 = open(str(f1),'r'); data1 = file1.readlines()[int(n1):int(n2)]
	i = 0
	for line in data1 :
		print i
		line = line.split()
		base_url = str(line[-1])

		r = urllib2.Request(base_url, headers=headers)
		x = urllib2.urlopen(r)
		xml_str = x.read()

		outname = str(base_url.split('/')[-1])

		filename = destdir+str(outname)

		file = open(filename, 'w')
		print >> file, xml_str,  
		file.close()

		sleep(randint(30,45))
		i+= 1

def extract_match_info_teams_players_managers(sourcedir, destdir, fres, flineups, fsubs) :

	matchfiles = glob.glob(sourcedir+'*')
	matchfiles.sort()

	outfile_result = open(str(destdir)+str(fres),'w')
	print >> outfile_result, 'matchid|team_home|manager_home|team_away|manager_away|result'
	
	erroroutfile = open(str(destdir)+'error_'+str(fres),'w')

	outfile_lineups = open(str(destdir)+str(flineups),'w')
	print >> outfile_lineups, 'matchid|player|team'

	outfile_fsubs = open(str(destdir)+str(fsubs),'w')
	print >> outfile_fsubs, 'matchid|player|team'
	"""
	EPL
			# manager_home = lineups("table", {"class":"ersatzbank"})[0]('a')[-1]['href']
			# manager_away = lineups("table", {"class":"ersatzbank"})[1]('a')[-1]['href']

			# players_home = lineups("div", {"class":"large-7 columns small-12 aufstellung-vereinsseite"})[0]("span",{"class":"aufstellung-rueckennummer-name spielprofil_tooltip"})
			# players_away = lineups("div", {"class":"large-7 columns small-12 aufstellung-vereinsseite"})[1]("span",{"class":"aufstellung-rueckennummer-name spielprofil_tooltip"})

			# subs_home = lineups("table", {"class":"ersatzbank"})[0]('a')[:-1]
			# subs_away = lineups("table", {"class":"ersatzbank"})[1]('a')[:-1]

			for pl in players_home :
				print >> outfile_lineups, '%s|%s|%s' % (matchid, pl('a')[0]['href'], team_home )

			for pl in players_away :
				print >> outfile_lineups, '%s|%s|%s' % (matchid, pl('a')[0]['href'], team_away )

			# for p in subs_home :
			# 	print >> outfile_fsubs, '%s|%s|%s' % (matchid, p['href'], team_home)

			# for p in subs_away :
			# 	print >> outfile_fsubs, '%s|%s|%s' % (matchid, p['href'], team_away)


	"""

	for match in matchfiles :
		try :
			print match
			f = open(match,'r')
			soup1 = BeautifulSoup(f, 'lxml')
			box_content = soup1("div",{"class":"box-content"})


			team_home = box_content[0]("div",{"class":"sb-team sb-heim"})[0]('a')[1]['href']
			team_away = box_content[0]("div",{"class":"sb-team sb-gast"})[0]('a')[1]['href']

			result = box_content[0]("div",{"class":"sb-ergebnis"})[0]("div",{"class":"sb-endstand"})[0].text.split("\n")[1].split('\t')[-1]

			lineups = soup1("div", {"class":"box"})[2]
			

			# manager_home = lineups("table", {"class":"aufstellung-spielerliste-table"})[0]('a')[-1]['href']
			# manager_away = lineups("table", {"class":"aufstellung-spielerliste-table"})[1]('a')[-1]['href']

			# players_home = lineups("table", {"class":"aufstellung-spielerliste-table"})[0]('a')[:-1]
			# players_away = lineups("table", {"class":"aufstellung-spielerliste-table"})[1]('a')[:-1]

			matchid = match.split('/')[-1]

			# print matchid, team_home, manager_home, team_away, manager_away, result

			# print soup1("div", {"class":"box"})[4]('div')

			manager_home = lineups("table", {"class":"ersatzbank"})[0]('a')[-1]['href']
			manager_away = lineups("table", {"class":"ersatzbank"})[1]('a')[-1]['href']

			players_home = lineups("div", {"class":"large-7 columns small-12 aufstellung-vereinsseite"})[0]("span",{"class":"aufstellung-rueckennummer-name spielprofil_tooltip"})
			players_away = lineups("div", {"class":"large-7 columns small-12 aufstellung-vereinsseite"})[1]("span",{"class":"aufstellung-rueckennummer-name spielprofil_tooltip"})

			subs_home = lineups("table", {"class":"ersatzbank"})[0]('a')[:-1]
			subs_away = lineups("table", {"class":"ersatzbank"})[1]('a')[:-1]

			print >> outfile_result, '%s|%s|%s|%s|%s|%s' % (matchid, team_home, manager_home, team_away, manager_away, result )

			for pl in players_home :
				print >> outfile_lineups, '%s|%s|%s' % (matchid, pl('a')[0]['href'], team_home )

			for pl in players_away :
				print >> outfile_lineups, '%s|%s|%s' % (matchid, pl('a')[0]['href'], team_away )

			for p in subs_home :
				print >> outfile_fsubs, '%s|%s|%s' % (matchid, p['href'], team_home)

			for p in subs_away :
				print >> outfile_fsubs, '%s|%s|%s' % (matchid, p['href'], team_away)

			# for pl in players_home :
			# 	print >> outfile_lineups, '%s|%s|%s' % (matchid, pl['href'], team_home )

			# for pl in players_away :
			# 	print >> outfile_lineups, '%s|%s|%s' % (matchid, pl['href'], team_away )


			# for p2 in soup1("div", {"class":"box"})[4]('div'):

			# 	if len(p2("div", {"class":"sb-aktion-wappen"})) == 1 and len(p2("span", {"class":"sb-aktion-wechsel-ein"})) == 1:
			# 		player = p2("span", {"class":"sb-aktion-wechsel-ein"})[0]('a')[0]['href'].split('/saison/')[0]
			# 		team = p2("div", {"class":"sb-aktion-wappen"})[0]('a')[0]['href']

			# 		print >> outfile_fsubs, '%s|%s|%s' % (matchid, player, team)


		except IndexError,e :
			print >> erroroutfile, match, e


def extract_match_info_teams_players_managers2(sourcedir, destdir, ferror1, fres, flineups, fsubs) :

	matchfiles = glob.glob(sourcedir+'*')
	matchfiles.sort()

	list_err = []
	data_err = open(str(ferror1),'r').readlines()
	for line in data_err :
		line = line.strip().split()
		print line[1]
		list_err.append(str(line[1].split('/')[-1]))
	print list_err

	outfile_result = open(str(destdir)+str(fres),'w')
	print >> outfile_result, 'matchid|team_home|manager_home|team_away|manager_away|result'
	
	erroroutfile = open(str(destdir)+'error_'+str(fres),'w')

	outfile_lineups = open(str(destdir)+str(flineups),'w')
	print >> outfile_lineups, 'matchid|player|team'

	outfile_fsubs = open(str(destdir)+str(fsubs),'w')
	print >> outfile_fsubs, 'matchid|player|team'


	for match in matchfiles :
		try :
			
			matchid = match.split('/')[-1]
			if str(matchid) in list_err :
				print matchid

				f = open(match,'r')
				soup1 = BeautifulSoup(f, 'lxml')
				box_content = soup1("div",{"class":"box-content"})

				team_home = box_content[0]("div",{"class":"sb-team sb-heim"})[0]('a')[1]['href']
				team_away = box_content[0]("div",{"class":"sb-team sb-gast"})[0]('a')[1]['href']

				result = box_content[0]("div",{"class":"sb-ergebnis"})[0]("div",{"class":"sb-endstand"})[0].text.split("\n")[1].split('\t')[-1]
				lineups = soup1("div", {"class":"box"})[2]

				manager_home = lineups("table")[0]('a')[-1]['href']
				manager_away = lineups("table")[1]('a')[-1]['href']

				players_home = lineups("table")[0]('a')[:-1]
				players_away = lineups("table")[1]('a')[:-1]

				print >> outfile_result, '%s|%s|%s|%s|%s|%s' % (matchid, team_home, manager_home, team_away, manager_away, result )

				for pl in players_home :
					print >> outfile_lineups, '%s|%s|%s' % (matchid, pl['href'], team_home )

				for pl in players_away :
					print >> outfile_lineups, '%s|%s|%s' % (matchid, pl['href'], team_away )


				for p2 in soup1("div", {"class":"box"})[4]('div'):

					if len(p2("div", {"class":"sb-aktion-wappen"})) == 1 and len(p2("span", {"class":"sb-aktion-wechsel-ein"})) == 1:
						player = p2("span", {"class":"sb-aktion-wechsel-ein"})[0]('a')[0]['href'].split('/saison/')[0]
						team = p2("div", {"class":"sb-aktion-wappen"})[0]('a')[0]['href']

						print >> outfile_fsubs, '%s|%s|%s' % (matchid, player, team)

		except IndexError,e :
			print >> erroroutfile, match, e




def download_players_stats_pages_soccer(f1, destdir, n1, n2) :

	user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'#'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }

	file1 = open(str(f1),'r'); data1 = file1.readlines()[int(n1):int(n2)]
	i = 0
	for line in data1 :
		print i
		line = line.strip().split('|')
		playername = str(line[0])
		player_id = str(line[1])
		base_url = "https://www.transfermarkt.com/"+playername+"/detaillierteleistungsdaten/spieler/"+player_id+"/plus/1"

		r = urllib2.Request(base_url, headers=headers)
		x = urllib2.urlopen(r)
		xml_str = x.read()

		outname = player_id

		filename = destdir+str(outname)

		file = open(filename+".html", 'w')
		print >> file, xml_str,  
		file.close()

		sleep(randint(30,45))
		i+= 1

def download_managers_stats_pages_soccer(f1, destdir, n1, n2) :

	user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'#'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }

	file1 = open(str(f1),'r'); data1 = file1.readlines()[int(n1):int(n2)]
	i = 0
	for line in data1 :
		print i
		line = line.strip().split('/')
		managername = str(line[1])
		manager_id = str(line[-1])
		base_url = "https://www.transfermarkt.com/"+managername+"/stationen/trainer/"+manager_id+"/plus/1"

		r = urllib2.Request(base_url, headers=headers)
		x = urllib2.urlopen(r)
		xml_str = x.read()

		outname = manager_id

		filename = destdir+str(outname)

		file = open(filename+".html", 'w')
		print >> file, xml_str,  
		file.close()

		sleep(randint(30,45))
		i+= 1

def extract_managers_pages_career(sourcedir, destdir, fres) :
	files = glob.glob(sourcedir+'*.html')
	files.sort()	

	outfile_result = open(str(destdir)+str(fres),'w')
	print >> outfile_result, 'managerid|club|appointed|chargetill|daysincharge|position|players_used'
	
	erroroutfile = open(str(destdir)+'error_'+str(fres),'w')


	for f in files :
		managerid = f.split('/')[-1][:-5]
		data1 = open(f, 'r')
		soup1 = BeautifulSoup(data1, 'lxml')
		print managerid
		tables = soup1("table",{"class":"items"}) 
		try :
			for k in tables[0]('tr')[1:] :
				try :
					players_used = k("td",{"class":"zentriert"})[7].text.encode('ascii', 'ignore')
					club = k('a')[0]['href']
					appointed = k("td",{"class":"zentriert"})[1].text.encode('ascii', 'ignore')
					chargetill = k("td",{"class":"zentriert"})[2].text.encode('ascii', 'ignore')
					daysincharge = k('td',{"class":"rechts"})[0].text.encode('ascii', 'ignore')
					position = k('td',{"class":"rechts"})[1].text.encode('ascii', 'ignore')
					
					print >> outfile_result, '%s|%s|%s|%s|%s|%s|%s' % (managerid, club, appointed, chargetill, daysincharge, position, players_used)

				except IndexError, e:
					print >> erroroutfile, managerid, e

		except IndexError, e:
			print >> erroroutfile, managerid, e

def extract_managers_pages_bio(sourcedir, destdir, fres) :
	files = glob.glob(sourcedir+'*.html')
	files.sort()	

	outfile_result = open(str(destdir)+str(fres),'w')
	print >> outfile_result, 'managerid|birthDate|birthPlace|nationality'
	
	erroroutfile = open(str(destdir)+'error_'+str(fres),'w')


	for f in files :
		managerid = f.split('/')[-1][:-5]
		data1 = open(f, 'r')
		soup1 = BeautifulSoup(data1, 'lxml')
		# print managerid
		try :
			datacontent = soup1("div",{"class":"dataContent"})

			birthDate = datacontent[0]('span',{'itemprop':'birthDate'})[0].text.split('\n')[1].split('\t')[0].replace(' ','')

			birthPlace = datacontent[0]('span',{'itemprop':'birthPlace'})[0].text.encode('ascii', 'ignore')
			nationality = datacontent[0]('span',{'itemprop':'nationality'})[0].text.encode('ascii', 'ignore')

			# preferred_formation = datacontent[0]("span",{"class":"dataValue"})[-1].text.replace('-','_').encode('ascii', 'ignore')
			# Avg_term = datacontent[0]("span",{"class":"dataValue"})[-2].text.encode('ascii', 'ignore').replace(' ','')

			print >> outfile_result, '%s|%s|%s|%s' % ( managerid, birthDate, birthPlace, nationality)

		except IndexError,e :
			print >> erroroutfile, managerid, e

def extract_managers_as_players_bio(sourcedir, destdir, fres) :
	files = glob.glob(sourcedir+'*.html')
	files.sort()	

	outfile_result = open(str(destdir)+str(fres),'w')
	print >> outfile_result, 'managerid|FormerPlayer|LastClubasPlayer|MostgamesasPlayer|RetireasPlayer'
	
	erroroutfile = open(str(destdir)+'error_'+str(fres),'w')


	for f in files :
		managerid = f.split('/')[-1][:-5]
		data1 = open(f, 'r')
		soup1 = BeautifulSoup(data1, 'lxml')
		print managerid

		dataProfile = soup1("div",{"class":"dataProfile"})
		try :

			LastClubasPlayer = dataProfile[0]("span",{"class":"dataValue"})[0].text.encode('ascii', 'ignore')#.replace(' ','_')
			MostgamesasPlayer = dataProfile[0]("span",{"class":"dataValue"})[1].text.encode('ascii', 'ignore').split('\n')[1].replace('\t','')
			RetireasPlayer = dataProfile[0]("span",{"class":"dataValue"})[2].text.encode('ascii', 'ignore').split('\n')[1].replace('\t','')
			FormerPlayer = "Played"
		except IndexError,e :

			LastClubasPlayer = "None"
			MostgamesasPlayer = "None"
			RetireasPlayer = "None"
			FormerPlayer = "Never_Played"


		print >> outfile_result, '%s|%s|%s|%s|%s' % ( managerid, FormerPlayer, LastClubasPlayer, MostgamesasPlayer, RetireasPlayer)


def extract_players_pages_career(sourcedir, destdir, fres) :
	files = glob.glob(sourcedir+'*.html')
	files.sort()	

	outfile_result = open(str(destdir)+str(fres),'w')
	print >> outfile_result, 'playerid|season|appearances|goals|assists|competition'
	
	# erroroutfile = open(str(destdir)+'error_'+str(fres),'w')


	for f in files :
		playerid = f.split('/')[-1][:-5]
		data1 = open(f, 'r')
		soup1 = BeautifulSoup(data1, 'lxml')
		print playerid

		tables = soup1("div",{"class":"box"}) 

		for leagues in tables[1:] :

			for b in leagues('tbody') :

				b2 = b("td", {"class":"zentriert"})

				season = [b2[i::12] for i in range(12)][0]
				appearances = [b2[i::12] for i in range(12)][2]
				goals = [b2[i::12] for i in range(12)][3]
				assists = [b2[i::12] for i in range(12)][4]
				
				b3 = b("td", {"class":"hauptlink"})
				competition = [b3[i::3] for i in range(3)][1]

				seasonval = [str(x.text.encode('ascii', 'ignore')) for x in season]
				appearancesval = [str(x.text.encode('ascii', 'ignore')) for x in appearances]
				goalsval = [str(x.text.encode('ascii', 'ignore')) for x in goals]
				assistsval = [str(x.text.encode('ascii', 'ignore')) for x in assists]
				competitionval = [str(x.text.encode('ascii', 'ignore')) for x in competition]

				zippedvals = zip(seasonval, appearancesval, goalsval, assistsval, competitionval)	

				for z1, z2, z3, z4, z5 in zippedvals :
					print >> outfile_result, '%s|%s|%s|%s|%s|%s' % ( playerid, z1, z2, z3, z4, z5)




def extract_match_info_substitutions(sourcedir, destdir, fsubs) :

	matchfiles = glob.glob(sourcedir+'*')
	matchfiles.sort()

	outfile_fsubs = open(str(destdir)+str(fsubs),'w')
	print >> outfile_fsubs, 'matchid|subs_in|subs_out'
	erroroutfile = open(str(destdir)+'error_'+str(fsubs),'w')

	"""
	EPL

			# subs_home = lineups("table", {"class":"ersatzbank"})[0]('a')[:-1]
			# subs_away = lineups("table", {"class":"ersatzbank"})[1]('a')[:-1]

			# for p in subs_home :
			# 	print >> outfile_fsubs, '%s|%s|%s' % (matchid, p['href'], team_home)

			# for p in subs_away :
			# 	print >> outfile_fsubs, '%s|%s|%s' % (matchid, p['href'], team_away)


	"""

	for match in matchfiles :
		try :
			print match
			f = open(match,'r')
			soup1 = BeautifulSoup(f, 'lxml')
			box_content = soup1("div",{"class":"box-content"})
			team_home = box_content[0]("div",{"class":"sb-team sb-heim"})[0]('a')[1]['href']
			team_away = box_content[0]("div",{"class":"sb-team sb-gast"})[0]('a')[1]['href']

			lineups = soup1("div", {"class":"box"})[2]
			substitutions = soup1("div", {"class":"box"})[4]

			matchid = match.split('/')[-1]

			for s in substitutions("div",{"class":"sb-aktion-aktion"}) :
				subs_in_data = s("span", {"class":"sb-aktion-wechsel-ein"})
				subs_out_data = s("span", {"class":"sb-aktion-wechsel-aus"})

				print >> outfile_fsubs, '%s|%s|%s' % (matchid, subs_in_data[0]('a')[0]['href'], subs_out_data[0]('a')[0]['href'])


		except IndexError,e :
			# continue
			print >> erroroutfile, match, e





if __name__ == "__main__" :

	f1 = sys.argv[1]; f2 = sys.argv[2]; f3 = sys.argv[3]; #f4 = sys.argv[4]; #f5 = sys.argv[5]; f6 = sys.argv[6]
	#dowload_player_chronology_nba(f1)
	#download_player_stats_data(f1, f2, f3, f4)
	#download_nba_seasons_months_data(f1)
	# download_nba_leagues_advanced_data(f1)
	#download_nba_leagues_coaches_data(f1)
	# # download_nba_seasons_months_data(f1)
	# extract_player_info_boxscores_nba(f1, f2)
	# extract_match_info_schedule_nhl(f1, f2, f3)
	# extract_match_info_schedule_nfl(f1, f2, f3)
	# extract_coach_pages_info(f1, f2)

	# download_coach_info_multiple_teams(f1, f2)
	# extract_coach_hire_fire_info(f1)
	# extract_player_stats_advanced(f1)
	# merge_nba_coach_players_data_matchid(f1)


	# extract_nfl_boxscore_page_coach_match_info(f1, f2)

	# extract_nfl_boxscore_players_snap_counts_team_match(f1, f2)

	# extract_mlb_player_statistics_batting_season(f1, f2) 

	# extract_mlb_player_statistics_pitching_season(f1, f2)

	# extract_nfl_boxscore_players_offense_defense_team_match(f1, f2)
	# extract_nfl_player_stats_seasonwise(f1, f2)
	# extract_mlb_boxscore_players_team_match_stats(f1, f2) 
	# extract_manager_pages_mlb_info(f1, f2)
	# extract_manager_multiple_teams_info(f1)
	# merge_mlb_manager_players_data_matchid(f1)
	
	# code_extract_coach_NBA_main_page(f1)
	# code_extract_coach_MLB_main_page(f1)
	# code_extract_coach_NFL_main_page(f1)

	# download_coach_manager_pages(f1, f2, f3)
	# extract_birth_info_NHL_managers(f1, f2)
	# download_soccer_pages_seasons(f1, f2, f3)
	# extract_match_pages_soccer(f1, f2, f3)
	# download_match_pages_soccer(f1, f2, f3, f4)

	# extract_match_info_teams_players_managers(f1, f2, f3, f4, f5)
	# extract_match_info_teams_players_managers2(f1, f2, f3, f4, f5, f6)

	# download_players_stats_pages_soccer(f1, f2, f3, f4)

	# download_managers_stats_pages_soccer(f1, f2, f3, f4)
	# extract_managers_pages_career(f1, f2, f3)
	# extract_managers_pages_bio(f1, f2, f3)
	# extract_players_pages_career(f1, f2, f3)


	# extract_match_info_substitutions(f1, f2, f3)
	extract_managers_as_players_bio(f1, f2, f3)







