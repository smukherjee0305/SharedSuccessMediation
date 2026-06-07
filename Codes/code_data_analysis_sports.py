import sys
import os
import networkx as nx
from collections import defaultdict
import glob
import fileinput
import numpy as np
from scipy import stats
from sets import Set
from itertools import combinations
from datetime import datetime

def countDuplicatesInList(dupedList):
	 uniqueSet = Set(item for item in dupedList)
	 return [(item, dupedList.count(item)) for item in uniqueSet]

def c2str(data):
	if len(str(data))==1:
		ret='0'+str(data)
	else:
		ret = str(data)
	return ret

###Code for compositional relationship!
####
####


def gen_compositional_mlb_variables(destdir, start_yr, bin1) :

	## read the datascores for MLB containing matchid and scores ##
	## read MLB batting data ###

	filelist1 = glob.glob('../Data/BoxScores/matchbymatchinfo/MLB_season_*_match_by_match_box_score_player_batting_info.txt'); filelist1.sort()

	team_runs_scored = defaultdict(list); team_slugging_perc = defaultdict(list); team_onbase_plus_slugging = defaultdict(list); 

	for f1 in filelist1 :
		file1 = open(str(f1),'r')
		data1 = file1.readlines()[1:]

		for line in data1 :  
			line = line.strip().split('|')
			yearnew = line[0]
			if int(yearnew) >= int(start_yr) - int(bin1) and int(yearnew) < int(start_yr) :

			# if int(yearnew) < int(start_yr):
				try: 

					team_runs_scored[str(line[1])].append(float(line[8])) 
					team_slugging_perc[str(line[1])].append(float(line[11])) 
					team_onbase_plus_slugging[str(line[1])].append(float(line[12])) 

				except ValueError :

					team_runs_scored[str(line[1])].append(0.0) 
					team_slugging_perc[str(line[1])].append(0.0) 
					team_onbase_plus_slugging[str(line[1])].append(0.0) 


	## read MLB pitching data ###

	filelist2 = glob.glob('../Data/BoxScores/matchbymatchinfo/MLB_season_*_match_by_match_box_score_player_pitching_info.txt'); filelist2.sort()

	team_earned_run_avg = defaultdict(list); team_fip = defaultdict(list); team_whip = defaultdict(list); team_HBP = defaultdict(list);

	for f2 in filelist2 :
		file2 = open(str(f2),'r')
		data2 = file2.readlines()[1:]

		for line in data2 :  
			line = line.strip().split('|')
			yearnew = line[0]
			if int(yearnew) >= int(start_yr) - int(bin1) and int(yearnew) < int(start_yr) :
			# if int(yearnew) < int(start_yr):
				try: 

					team_earned_run_avg[str(line[1])].append(float(line[7])) 
					team_fip[str(line[1])].append(float(line[8])) 
					team_whip[str(line[1])].append(float(line[9])) 
					team_HBP[str(line[1])].append(float(line[10])) 

				except ValueError :

					team_earned_run_avg[str(line[1])].append(0.0) 
					team_fip[str(line[1])].append(0.0) 
					team_whip[str(line[1])].append(0.0) 
					team_HBP[str(line[1])].append(0.0) 


	file3a = open('../Data/BoxScores/matchbymatchinfo/MLB_season_'+str(start_yr)+'_match_by_match_box_score_player_info.txt','r') 
	data3a = file3a.readlines()
	file3a.close()

	team_mean_runs_scored = defaultdict(list); team_mean_slugging_perc = defaultdict(list); team_mean_onbase_plus_slugging = defaultdict(list); 
	team_mean_earned_run_avg = defaultdict(list); team_mean_fip = defaultdict(list); team_mean_whip = defaultdict(list); team_mean_HBP = defaultdict(list);

	for line in data3a :
		line = line.strip().split('|')

		if str(line[1]) in team_runs_scored :
					team_mean_runs_scored[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_runs_scored[str(line[1])]))

		if str(line[1]) in team_slugging_perc :
					team_mean_slugging_perc[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_slugging_perc[str(line[1])]))

		if str(line[1]) in team_onbase_plus_slugging :
					team_mean_onbase_plus_slugging[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_onbase_plus_slugging[str(line[1])]))



		if str(line[1]) in team_earned_run_avg :
					team_mean_earned_run_avg[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_earned_run_avg[str(line[1])]))

		if str(line[1]) in team_fip :
					team_mean_fip[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_fip[str(line[1])]))

		if str(line[1]) in team_whip :
					team_mean_whip[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_whip[str(line[1])]))

		if str(line[1]) in team_HBP :
					team_mean_HBP[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_HBP[str(line[1])]))




	file3b = open('../Data/BoxScores/matchbymatchinfo/MLB_season_'+str(start_yr)+'_match_by_match_box_score_player_info2.txt','r') 
	data3b = file3b.readlines()
	file3b.close()


	for line in data3b :
		line = line.strip().split('|')

		if str(line[1]) in team_runs_scored :
					team_mean_runs_scored[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_runs_scored[str(line[1])]))

		if str(line[1]) in team_slugging_perc :
					team_mean_slugging_perc[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_slugging_perc[str(line[1])]))

		if str(line[1]) in team_onbase_plus_slugging :
					team_mean_onbase_plus_slugging[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_onbase_plus_slugging[str(line[1])]))



		if str(line[1]) in team_earned_run_avg :
					team_mean_earned_run_avg[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_earned_run_avg[str(line[1])]))

		if str(line[1]) in team_fip :
					team_mean_fip[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_fip[str(line[1])]))

		if str(line[1]) in team_whip :
					team_mean_whip[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_whip[str(line[1])]))

		if str(line[1]) in team_HBP :
					team_mean_HBP[str(line[3])+'|'+str(line[0])].append(np.nanmean(team_HBP[str(line[1])]))




	file4 = open('../Data/BoxScores/MLB/textfiles/MLB_season_'+str(start_yr)+'_match_by_match_score_team_info.txt','r') 
	data4 = file4.readlines()[1:]
	file4.close()

	# print team_mean_HBP['Detroit_Tigers|DET201210060'], team_mean_HBP['Oakland_Athletics|DET201210060']

	fh6 = open(destdir+'MLB_compositional_batting_pitching_bin_'+str(bin1)+'_'+str(start_yr)+'.txt' , 'w')
	print >> fh6, 'seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mean_runs_t1_bin_'+str(bin1)+'|mean_slugperc_t1_bin_'+str(bin1)+'|mean_OPS_t1_bin_'+str(bin1)+'|mean_ERA_t1_bin_'+str(bin1)+'|mean_WHIP_t1_bin_'+str(bin1)+'|mean_fip_t1_bin_'+str(bin1)+'|mean_hbp_t1_bin_'+str(bin1)+'|home_name|home_id|home_pts|mean_runs_t2_bin_'+str(bin1)+'|mean_slugperc_t2_bin_'+str(bin1)+'|mean_OPS_t2_bin_'+str(bin1)+'|mean_ERA_t2_bin_'+str(bin1)+'|mean_WHIP_t2_bin_'+str(bin1)+'|mean_fip_t2_bin_'+str(bin1)+'|mean_hbp_t2_bin_'+str(bin1)

	# fh6 = open(destdir+'MLB_compositional_batting_pitching'+'_'+str(start_yr)+'.txt' , 'w')
	# print >> fh6, 'seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mean_runs_t1|mean_slugperc_t1|mean_OPS_t1|mean_ERA_t1|mean_WHIP_t1|mean_fip_t1|mean_hbp_t1|home_name|home_id|home_pts|mean_runs_t2|mean_slugperc_t2|mean_OPS_t2|mean_ERA_t2|mean_WHIP_t2|mean_fip_t2|mean_hbp_t2'

	for line in data4 :
		line = line.strip()
		line = line.split('|')
		if int(line[0]) == int(start_yr) :

			team1 = line[2]
			team2 = line[5]

			keys1 = str(team1)+'|'+str(line[1]); keys2 = str(team2)+'|'+str(line[1])

			# print keys1, team_mean_HBP[str(keys1)]

			## Average batting statistics
			mean_runs_t1 = float(np.nanmean(team_mean_runs_scored[keys1])); 		mean_runs_t2 = float(np.nanmean(team_mean_runs_scored[keys2])); 
			mean_slugperc_t1 = float(np.nanmean(team_mean_slugging_perc[keys1]));	mean_slugperc_t2 = float(np.nanmean(team_mean_slugging_perc[keys2]));
			mean_OPS_t1 = float(np.nanmean(team_mean_onbase_plus_slugging[keys1]));	mean_OPS_t2 = float(np.nanmean(team_mean_onbase_plus_slugging[keys2]));

			## Average pitching statistics
			mean_ERA_t1 = float(np.nanmean(team_mean_earned_run_avg[keys1])); 	mean_ERA_t2 = float(np.nanmean(team_mean_earned_run_avg[keys2])); 
			mean_WHIP_t1 = float(np.nanmean(team_mean_whip[keys1]));	mean_WHIP_t2 = float(np.nanmean(team_mean_whip[keys2]));
			mean_pitch_fip_t1 = float(np.nanmean(team_mean_fip[keys1])); mean_pitch_fip_t2 = float(np.nanmean(team_mean_fip[keys2]));
			mean_pitch_hbp_t1 = float(np.nanmean(team_mean_HBP[keys1])); mean_pitch_hbp_t2 = float(np.nanmean(team_mean_HBP[keys2]));


			print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], line[4], mean_runs_t1, mean_slugperc_t1, mean_OPS_t1, mean_ERA_t1, mean_WHIP_t1, mean_pitch_fip_t1, mean_pitch_hbp_t1, line[5], line[6], line[7], mean_runs_t2, mean_slugperc_t2, mean_OPS_t2, mean_ERA_t2, mean_WHIP_t2, mean_pitch_fip_t2, mean_pitch_hbp_t2 )


def gen_compositional_NFL_variables(destdir, start_yr) :

	#file1 = open('../Data/Researchdata/data_for_analysis/FIFA_world_cup_matchid_year_teamscores.txt','r') 

	filelist1 = glob.glob('../Data/BoxScores/matchbymatchinfo/NFL_season_*_playerstats_scrimmage.txt'); filelist1.sort()

	team_touches = defaultdict(list); team_yds_from_scrimmage = defaultdict(list); team_rush_receive_td = defaultdict(list); 

	for f1 in filelist1 :
		file1 = open(str(f1),'r')
		data1 = file1.readlines()[1:]

		for line in data1 :  
			line = line.strip().split('|')
			yearnew = line[-1]
			# if int(yearnew) >= int(start_yr) - int(bin1) and int(yearnew) < int(start_yr) :
				# print line[0], line[6], line[7], line[8]
			if int(yearnew) < int(start_yr):
				try: 

					team_touches[str(line[0])].append(float(line[6])) 
					team_yds_from_scrimmage[str(line[0])].append(float(line[7])) 
					team_rush_receive_td[str(line[0])].append(float(line[8])) 

				except ValueError :

					team_touches[str(line[0])].append(0.0) 
					team_yds_from_scrimmage[str(line[0])].append(0.0) 
					team_rush_receive_td[str(line[0])].append(0.0) 



	filelist2 = glob.glob('../Data/BoxScores/matchbymatchinfo/NFL_season_*_playerstats_scoring.txt'); filelist1.sort()

	team_xpm = defaultdict(list); team_xpa = defaultdict(list); team_fgm = defaultdict(list); team_scoring = defaultdict(list);

	for f2 in filelist2 :
		file2 = open(str(f2),'r')
		data2 = file2.readlines()[1:]

		for line in data2 :  
			line = line.strip().split('|')
			yearnew = line[-1]
			# if int(yearnew) >= int(start_yr) - int(bin1) and int(yearnew) < int(start_yr) :
			if int(yearnew) < int(start_yr):
				try: 

					team_xpm[str(line[0])].append(float(line[6])) 
					team_xpa[str(line[0])].append(float(line[7])) 
					team_fgm[str(line[0])].append(float(line[8])) 
					team_scoring[str(line[0])].append(float(line[10])) 

				except ValueError :

					team_xpm[str(line[0])].append(0.0) 
					team_xpa[str(line[0])].append(0.0) 
					team_fgm[str(line[0])].append(0.0) 
					team_scoring[str(line[0])].append(0.0) 

	# print team_xpm

	file3 = open('../Data/BoxScores/matchbymatchinfo/NFL_season_'+str(start_yr)+'_match_by_match_box_score_player_info.txt','r') 
	data3 = file3.readlines()
	file3.close()

	team_mean_touches = defaultdict(list); team_mean_scrimmage = defaultdict(list); team_mean_rush = defaultdict(list); 
	team_mean_xpm = defaultdict(list); team_mean_xpa = defaultdict(list); team_mean_fgm = defaultdict(list); team_mean_scoring = defaultdict(list);

	for line in data3 :
		line = line.strip().split('|')

		if str(line[2]) in team_touches :
					team_mean_touches[str(line[1].split(' Snap Counts')[0])+'|'+str(line[0])].append(np.nanmean(team_touches[str(line[2])]))

		if str(line[2]) in team_yds_from_scrimmage :
					team_mean_scrimmage[str(line[1].split(' Snap Counts')[0])+'|'+str(line[0])].append(np.nanmean(team_yds_from_scrimmage[str(line[2])]))

		if str(line[2]) in team_rush_receive_td :
					team_mean_rush[str(line[1].split(' Snap Counts')[0])+'|'+str(line[0])].append(np.nanmean(team_rush_receive_td[str(line[2])]))



		if str(line[2]) in team_xpm :
					team_mean_xpm[str(line[1].split(' Snap Counts')[0])+'|'+str(line[0])].append(np.nanmean(team_xpm[str(line[2])]))

		if str(line[2]) in team_xpa :
					team_mean_xpa[str(line[1].split(' Snap Counts')[0])+'|'+str(line[0])].append(np.nanmean(team_xpa[str(line[2])]))

		if str(line[2]) in team_fgm :
					team_mean_fgm[str(line[1].split(' Snap Counts')[0])+'|'+str(line[0])].append(np.nanmean(team_fgm[str(line[2])]))

		if str(line[2]) in team_scoring :
					team_mean_scoring[str(line[1].split(' Snap Counts')[0])+'|'+str(line[0])].append(np.nanmean(team_scoring[str(line[2])]))



	# print team_mean_xpm

	file4 = open('../Data/BoxScores/matchbymatchinfo/NFL_season_'+str(start_yr)+'_match_by_match_score_team_info.txt','r') 
	data4 = file4.readlines()[1:]
	file4.close()

	fh6 = open(destdir+'NFL_compositional_per_year'+'_'+str(start_yr)+'.txt' , 'w')
	print >> fh6, 'date|seasonyear|boxscoreid|winner_name|winner_id|pts_win|yards_win|to_win|mean_touches_t1|mean_scrimage_t1|mean_rush_receive_t1|mean_xpm_t1|mean_xpa_t1|mean_fgm_t1|mean_scoring_t1|loser_name|loser_id|pts_lose|yards_lose|to_lose|mean_touches_t2|mean_scrimage_t2|mean_rush_receive_t2|mean_xpm_t2|mean_xpa_t2|mean_fgm_t2|mean_scoring_t2'

	# fh6 = open(destdir+'NFL_compositional_per_year_bin_'+str(bin1)+'_'+str(start_yr)+'.txt' , 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|winner_name|winner_id|pts_win|yards_win|to_win|mean_touches_t1_bin_'+str(bin1)+'|mean_scrimage_t1_bin_'+str(bin1)+'|mean_rush_receive_t1_bin_'+str(bin1)+'|mean_xpm_t1_bin_'+str(bin1)+'|mean_xpa_t1_bin_'+str(bin1)+'|mean_fgm_t1_bin_'+str(bin1)+'|mean_scoring_t1_bin_'+str(bin1)+'|loser_name|loser_id|pts_lose|yards_lose|to_lose|mean_touches_t2_bin_'+str(bin1)+'|mean_scrimage_t2_bin_'+str(bin1)+'|mean_rush_receive_t2_bin_'+str(bin1)+'|mean_xpm_t2_bin_'+str(bin1)+'|mean_xpa_t2_bin_'+str(bin1)+'|mean_fgm_t2_bin_'+str(bin1)+'|mean_scoring_t2_bin_'+str(bin1)

	for line in data4 :
			line = line.strip().split('|')


			team1 = line[3]; team2 = line[8]

			keys1 = str(team1.split('_')[-1])+'|'+str(line[2]); keys2 = str(team2.split('_')[-1])+'|'+str(line[2])

			## Average NFL reference
			mean_touches_t1 = float(np.nanmean(team_mean_touches[keys1])); mean_touches_t2 = float(np.nanmean(team_mean_touches[keys2]))
			mean_scrimage_t1 = float(np.nanmean(team_mean_scrimmage[keys1])); 	 mean_scrimage_t2 = float(np.nanmean(team_mean_scrimmage[keys2]))
			mean_rush_receive_t1 = float(np.nanmean(team_mean_rush[keys1]));   mean_rush_receive_t2 = float(np.nanmean(team_mean_rush[keys2]))
			mean_xpm_t1 = float(np.nanmean(team_mean_xpm[keys1]));     mean_xpm_t2 = float(np.nanmean(team_mean_xpm[keys2]))
			mean_xpa_t1 = float(np.nanmean(team_mean_xpa[keys1]));     mean_xpa_t2 = float(np.nanmean(team_mean_xpa[keys2]))
			mean_fgm_t1 = float(np.nanmean(team_mean_fgm[keys1]));     mean_fgm_t2 = float(np.nanmean(team_mean_fgm[keys2]))
			mean_scoring_t1 = float(np.nanmean(team_mean_scoring[keys1]));     mean_scoring_t2 = float(np.nanmean(team_mean_scoring[keys2]))



			print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], mean_touches_t1, mean_scrimage_t1, mean_rush_receive_t1, mean_xpm_t1, mean_xpa_t1, mean_fgm_t1, mean_scoring_t1, line[8], line[9], line[10], line[11], line[12], mean_touches_t2, mean_scrimage_t2, mean_rush_receive_t2, mean_xpm_t2, mean_xpa_t2, mean_fgm_t2, mean_scoring_t2)



def gen_compositional_NBA_variables(destdir, start_yr, bin1) :
	## read the datascores for NBA containing matchid and scores ##

	file1 = open('../Data/BoxScores/matchbymatchinfo/NBA_seasonyear_player_advanced_stats.txt','r') 
	data1 = file1.readlines()[1:]
	file1.close()


	team_vorp = defaultdict(list); team_per = defaultdict(list); team_bpm = defaultdict(list); team_ws = defaultdict(list);

	for line in data1 :  
		line = line.strip().split('|')
		yearnew = line[0]
		if int(yearnew) >= int(start_yr) - int(bin1) and int(yearnew) < int(start_yr) :

			try: 
				team_vorp[str(line[1])].append(float(line[3])) 
				team_per[str(line[1])].append(float(line[4])) 
				team_bpm[str(line[1])].append(float(line[5])) 
				team_ws[str(line[1])].append(float(line[6])) 
			except ValueError :
				team_per[str(line[1])].append(0.0)


	file4 = open('../Data/BoxScores/matchbymatchinfo/NBA_season_'+str(start_yr)+'_match_by_match_box_score_player_info.txt','r') 
	data4 = file4.readlines()
	file4.close()

	team_mean_vorp = defaultdict(list); team_mean_per = defaultdict(list); team_mean_bpm = defaultdict(list); team_mean_ws = defaultdict(list);

	for line in data4 :
		line = line.strip().split('|')

		if str(line[2]) in team_vorp :
					team_mean_vorp[str(line[1])+'|'+str(line[0])].append(np.nanmean(team_vorp[str(line[2])]))

		if str(line[2]) in team_per :
					team_mean_per[str(line[1])+'|'+str(line[0])].append(np.nanmean(team_per[str(line[2])]))

		if str(line[2]) in team_bpm :
					team_mean_bpm[str(line[1])+'|'+str(line[0])].append(np.nanmean(team_bpm[str(line[2])]))

		if str(line[2]) in team_ws :
					team_mean_ws[str(line[1])+'|'+str(line[0])].append(np.nanmean(team_ws[str(line[2])]))





	file2 = open('../Data/BoxScores/matchbymatchinfo/NBA_season_'+str(start_yr)+'_match_by_match_score_team_info.txt','r') 
	data2 = file2.readlines()[1:]
	file2.close()

	#fh6 = open(destdir+'NBA_compositional_per_year'+'_'+str(start_yr)+'.txt' , 'w')
	#print >> fh6, 'MatchID|Team1|mean_PTS_t1|mean_STL_t1|mean_AST_t1|mean_DBPM_t1|mean_BPM_t1|mean_VORP_t1|HAteam01|Team2|mean_PTS_t2|mean_STL_t2|mean_AST_t2|mean_DBPM_t2|mean_BPM_t2|mean_VORP_t2|HAteam02'


	fh6 = open(destdir+'NBA_compositional_per_year_bin_'+str(bin1)+'_'+str(start_yr)+'.txt' , 'w')
	print >> fh6, 'date|seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mean_vorp_t1_bin_'+str(bin1)+'|mean_per_t1_bin_'+str(bin1)+'|mean_bpm_t1_bin_'+str(bin1)+'|mean_ws_t1_bin_'+str(bin1)+'|home_name|home_id|home_pts|mean_vorp_t2_bin_'+str(bin1)+'|mean_per_t2_bin_'+str(bin1)+'|mean_bpm_t2_bin_'+str(bin1)+'|mean_ws_t2_bin_'+str(bin1)

	for line in data2 :
			line = line.strip().split('|')


			team1 = line[3]; team2 = line[6]

			keys1 = str(team1)+'|'+str(line[2]); keys2 = str(team2)+'|'+str(line[2])

			## Average Basketball reference
			mean_vorp_t1 = float(np.nanmean(team_mean_vorp[keys1])); mean_vorp_t2 = float(np.nanmean(team_mean_vorp[keys2]))
			mean_per_t1 = float(np.nanmean(team_mean_per[keys1])); 	 mean_per_t2 = float(np.nanmean(team_mean_per[keys2]))
			mean_bpm_t1 = float(np.nanmean(team_mean_bpm[keys1]));   mean_bpm_t2 = float(np.nanmean(team_mean_bpm[keys2]))
			mean_ws_t1 = float(np.nanmean(team_mean_ws[keys1]));     mean_ws_t2 = float(np.nanmean(team_mean_ws[keys2]))



			print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], line[4], line[5], mean_vorp_t1, mean_per_t1, mean_bpm_t1, mean_ws_t1, line[6], line[7], line[8], mean_vorp_t2, mean_per_t2, mean_bpm_t2, mean_ws_t2)





def gen_compositional_soccer_variables(sourcedir, destdir, start_yr, bin1) :
	## read the datascores for soccer containing matchid and scores ##

	file1 = open('../Data/data_for_analysis/transfrmarket/'+str(sourcedir)+'/players_career_stats_history.txt','r') 
	data1 = file1.readlines()[1:]
	file1.close()


	team_goals = defaultdict(list); team_assists = defaultdict(list); 

	for line in data1 :  
		line = line.strip().split('|')

		if "/" in str(line[1]) :
			y1 = str(line[1].split('/')[0])
			y2 = str(line[1].split('/')[1])
			if int(y1) <= 21:
				yearnew = '20'+str(y1)

			if int(y1) > 21:
				yearnew = '19'+str(y1)

		if not "/" in str(line[1]) :
			yearnew = int(line[1])

		# if int(yearnew) < int(start_yr) :
		if int(yearnew) >= int(start_yr) - int(bin1) and int(yearnew) < int(start_yr) :

			try: 
				team_goals[str(line[0])].append(float(line[3])) 
				team_assists[str(line[0])].append(float(line[4])) 

			except ValueError :
				team_goals[str(line[0])].append(0.0)				
				team_assists[str(line[0])].append(0.0)

	# print team_goals

	filelist = glob.glob('../Data/data_for_analysis/transfrmarket/'+str(sourcedir)+'/'+'Bundelisga_players_*.txt'); filelist.sort()
	
	team_mean_goals = defaultdict(list); team_mean_assists = defaultdict(list); 
	for f2 in filelist :

		file2 = open(f2,'r') ## form relationship  !!!
		data2 = file2.readlines()[1:]

		for line in data2 :
			line = line.strip().split('|')
			matcid = line[0]
			playerid = line[1].split('/')[-1]
			team_id = line[2].split('/')[4]
			year = line[2].split('/')[-1]

			if str(playerid) in team_goals :
						team_mean_goals[str(team_id)+'|'+str(matcid)].append(np.nanmean(team_goals[str(playerid)]))

			if str(playerid) in team_assists :
						team_mean_assists[str(team_id)+'|'+str(matcid)].append(np.nanmean(team_assists[str(playerid)]))


	# fh6 = open(destdir+'Bundelisga_compositional_per_year'+'_'+str(start_yr)+'.txt' , 'w')
	# print >> fh6, 'MatchID|seasonyear|team_home|team_home_id|score_home|mean_goals_t1|mean_assists_t1|team_away|team_away_id|score_away|mean_goals_t2|mean_assists_t2'

	fh6 = open(destdir+'Bundelisga_compositional_per_year_bin_'+str(bin1)+'_'+str(start_yr)+'.txt' , 'w')
	print >> fh6, 'MatchID|seasonyear|team_home|team_home_id|score_home|mean_goals_t1_bin_'+str(bin1)+'|mean_assists_t1_bin_'+str(bin1)+'|team_away|team_away_id|score_away|mean_goals_t2_bin_'+str(bin1)+'|mean_assists_t2_bin_'+str(bin1)

	filelist2 = glob.glob('../Data/data_for_analysis/transfrmarket/'+str(sourcedir)+'/'+'Bundelisga_result*.txt'); filelist2.sort()

	for f2 in filelist2 :
		file2 = open(str(f2),'r')
		data = file2.readlines()[1:]


		for line in data :  
			line = line.strip().split('|')
			matcid = line[0]

			team_home = line[1].split('/')[1]
			team_away = line[3].split('/')[1]
	  
			team_home_id = line[1].split('/')[4]
			team_away_id = line[3].split('/')[4]

			score_home = line[-1].split('(')[0].split(":")[0]
			score_away = line[-1].split('(')[0].split(":")[1]

			keys1 = str(team_home_id)+'|'+str(matcid); 
			keys2 = str(team_away_id)+'|'+str(matcid)

			year = line[1].split('/')[-1]

			if int(year) == int(start_yr) :

				## Average Soccer
				mean_goals_t1 = float(np.nanmean(team_mean_goals[keys1])); 		mean_goals_t2 = float(np.nanmean(team_mean_goals[keys2]))
				mean_assists_t1 = float(np.nanmean(team_mean_assists[keys1])); 	mean_assists_t2 = float(np.nanmean(team_mean_assists[keys2]))


				print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( matcid, year, team_home, team_home_id, score_home, mean_goals_t1, mean_assists_t1, team_away, team_away_id, score_away, mean_goals_t2, mean_assists_t2 )



#####	@@@@@@@		#### %%%%%% &&&&& 								
#####	Code for player relationship!
#### 	*********** #### ******* ******

def create_relational_variable_NBA(destdir, start_yr, bin1) :

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	filelist1 = glob.glob('../Data/BoxScores/matchbymatchinfo/NBA_season_*_match_by_match_score_team_info.txt'); filelist1.sort()

	for f1 in filelist1 :
		file1 = open(str(f1),'r')
		data = file1.readlines()[1:]


		for line in data :  
			line = line.strip().split('|')
			matcid = line[2]
	  
			if int(line[5]) > int(line[8]) :
				matcid_team_result[str(line[3])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[6])+'|'+str(matcid)] = "L"

			if int(line[5]) == int(line[8]) :
				matcid_team_result[str(line[3])+'|'+str(matcid)] = "D"
				matcid_team_result[str(line[6])+'|'+str(matcid)] = "D"
	 
			if int(line[5]) < int(line[8]) :
				matcid_team_result[str(line[6])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[3])+'|'+str(matcid)] = "L"


	# print matcid_team_result

	filelist = glob.glob('../Data/BoxScores/matchbymatchinfo/NBA_season_*_match_by_match_box_score_player_info.txt'); filelist.sort()
	 ## form relationship  !!!
	
	team_nodes = defaultdict(list);	team_combos = []; 	team_nodes_past = defaultdict(list)

	for f2 in filelist :

		file2 = open(f2,'r') ## form relationship  !!!
		data2 = file2.readlines()[1:]

		for line in data2 :
			line = line.strip().split('|')
			year = line[4]

			if int(year) == int(start_yr) :
				team_nodes[str(line[1])+'|'+str(line[0])].append(str(line[2]))


			# if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :
				# if matcid_team_result[str(line[1])+'|'+str(line[0])] == "W" : 
					team_nodes_past[str(line[1])+'|'+str(line[0])].append(str(line[2])) 

	# print team_nodes_past
	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))
		edges = combinations(nodes,2)

		G = nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


 ## now look back and see how many times players played with each other earlier !

	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = combinations(nodes2, 2)
		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])


	# fh6 = open(destdir+'NBA_relational_succesful_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mu_rel_suc_t1_bin_'+str(bin1)+'|std_rel_suc_t1_bin_'+str(bin1)+'|med_rel_suc_t1_bin_'+str(bin1)+'|home_name|home_id|home_pts|mu_rel_suc_t2_bin_'+str(bin1)+'|std_rel_suc_t2_bin_'+str(bin1)+'|med_rel_suc_t2_bin_'+str(bin1)
	
	fh6 = open(destdir+'NBA_relational_all_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'date|seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mu_rel_all_t1_bin_'+str(bin1)+'|std_rel_all_t1_bin_'+str(bin1)+'|med_rel_all_t1_bin_'+str(bin1)+'|home_name|home_id|home_pts|mu_rel_all_t2_bin_'+str(bin1)+'|std_rel_all_t2_bin_'+str(bin1)+'|med_rel_all_t2_bin_'+str(bin1)


	# fh6 = open(destdir+'NBA_relational_succesful_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mu_rel_suc_t1|std_rel_suc_t1|med_rel_suc_t1|home_name|home_id|home_pts|mu_rel_suc_t2|std_rel_suc_t2|med_rel_suc_t2'
	
	# fh6 = open(destdir+'NBA_relational_all_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mu_rel_all_t1|std_rel_all_t1|med_rel_all_t1|home_name|home_id|home_pts|mu_rel_all_t2|std_rel_all_t2|med_rel_all_t2'


	file3 = open('../Data/BoxScores/matchbymatchinfo/NBA_season_'+str(start_yr)+'_match_by_match_score_team_info.txt','r') 
	data3 = file3.readlines()[1:]

	for line in data3 :

			line = line.strip().split('|')

			team1 = line[3]; team2 = line[6]

			keys1 = str(team1)+'|'+str(line[2]); keys2 = str(team2)+'|'+str(line[2])


			## Average relational
			mean_rel_t1 = float(np.nanmean(teams_id[keys1])); 		mean_rel_t2 = float(np.nanmean(teams_id[keys2]))
			median_rel_t1 = float(np.nanmedian(teams_id[keys1])); 	median_rel_t2 = float(np.nanmedian(teams_id[keys2]))
			std_rel_t1 = float(np.std(teams_id[keys1]));   			std_rel_t2 = float(np.std(teams_id[keys2]))



			print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], line[4], line[5], mean_rel_t1, std_rel_t1, median_rel_t1, line[6], line[7], line[8], mean_rel_t2, std_rel_t2, median_rel_t2)





def create_relational_variable_NFL(destdir, start_yr, bin1) :

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	filelist1 = glob.glob('../Data/BoxScores/matchbymatchinfo/NFL_season_*_match_by_match_score_team_info.txt'); filelist1.sort()

	dict_short_form = defaultdict(list)


	for f1 in filelist1 :
		file1 = open(str(f1),'r')
		data = file1.readlines()[1:]


		for line in data :  
			line = line.strip().split('|')
			matcid = line[2]
	  
			matcid_team_result[str(line[3].split('_')[-1])+'|'+str(matcid)] = "W"
			matcid_team_result[str(line[8].split('_')[-1])+'|'+str(matcid)] = "L"

			dict_short_form[str(line[4])] = str(line[3].split('_')[-1])
			dict_short_form[str(line[9])] = str(line[9].split('_')[-1])


	# print matcid_team_result

	filelist = glob.glob('../Data/BoxScores/matchbymatchinfo/NFL_season_*_match_by_match_box_score_player_info.txt'); filelist.sort()
	 ## form relationship  !!!
	
	team_nodes = defaultdict(list);	team_combos = []; 	team_nodes_past = defaultdict(list)

	for f2 in filelist :

		file2 = open(f2,'r') ## form relationship  !!!
		data2 = file2.readlines()[1:]

		for line in data2 :
			line = line.strip().split('|')
			year = line[-1]

			if int(year) == int(start_yr) :
				team_nodes[str(line[1].split(' Snap Counts')[0])+'|'+str(line[0])].append(str(line[2]))


			# if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :
				# if matcid_team_result[str(line[1])+'|'+str(line[0])] == "W" : 
					team_nodes_past[str(line[1].split(' Snap Counts')[0])+'|'+str(line[0])].append(str(line[2])) 


# defense 

	filelist2 = glob.glob('../Data/BoxScores/matchbymatchinfo/NFL_season_*_match_by_match_box_score_defense_player_info.txt'); filelist2.sort()
	 ## form relationship  !!!
	
	for f3 in filelist2 :

		file3 = open(f3,'r') ## form relationship  !!!
		data3 = file3.readlines()[1:]

		for line in data3 :
			line = line.strip().split('|')
			year = line[-1]

			if int(year) == int(start_yr) :
				team_nodes[str(dict_short_form[str(line[3].lower())])+'|'+str(line[0])].append(str(line[1]))


			# if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :
				# if matcid_team_result[str(line[1])+'|'+str(line[0])] == "W" : 
					team_nodes_past[str(dict_short_form[str(line[3].lower())])+'|'+str(line[0])].append(str(line[1])) 



# offense

	filelist3 = glob.glob('../Data/BoxScores/matchbymatchinfo/NFL_season_*_match_by_match_box_score_offense_player_info.txt'); filelist3.sort()
	 ## form relationship  !!!
	
	for f4 in filelist3 :

		file4 = open(f4,'r') ## form relationship  !!!
		data4 = file4.readlines()[1:]

		for line in data4 :
			line = line.strip().split('|')
			year = line[-1]

			if int(year) == int(start_yr) :
				team_nodes[str(dict_short_form[str(line[3].lower())])+'|'+str(line[0])].append(str(line[1]))


			# if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :
				# if matcid_team_result[str(line[1])+'|'+str(line[0])] == "W" : 
					team_nodes_past[str(dict_short_form[str(line[3].lower())])+'|'+str(line[0])].append(str(line[1])) 






	# print team_nodes_past
	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))
		edges = combinations(nodes,2)

		G = nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


 ## now look back and see how many times players played with each other earlier !

	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = combinations(nodes2, 2)
		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])


	# fh6 = open(destdir+'NFL_relational_succesful_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|winner_name|winner_id|pts_win|yards_win|to_win|mu_rel_suc_t1_bin_'+str(bin1)+'|std_rel_suc_t1_bin_'+str(bin1)+'|med_rel_suc_t1_bin_'+str(bin1)+'|loser_name|loser_id|pts_lose|yards_lose|to_lose|mu_rel_suc_t2_bin_'+str(bin1)+'|std_rel_suc_t2_bin_'+str(bin1)+'|med_rel_suc_t2_bin_'+str(bin1)
	
	fh6 = open(destdir+'NFL_relational_all_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'date|seasonyear|boxscoreid|winner_name|winner_id|pts_win|yards_win|to_win|mu_rel_all_t1_bin_'+str(bin1)+'|std_rel_all_t1_bin_'+str(bin1)+'|med_rel_all_t1_bin_'+str(bin1)+'|loser_name|loser_id|pts_lose|yards_lose|to_lose|home_pts|mu_rel_all_t2_bin_'+str(bin1)+'|std_rel_all_t2_bin_'+str(bin1)+'|med_rel_all_t2_bin_'+str(bin1)


	# fh6 = open(destdir+'NFL_relational_succesful_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|winner_name|winner_id|pts_win|yards_win|to_win|mu_rel_suc_t1|std_rel_suc_t1|med_rel_suc_t1|loser_name|loser_id|pts_lose|yards_lose|to_lose|mu_rel_suc_t2|std_rel_suc_t2|med_rel_suc_t2'
	
	# fh6 = open(destdir+'NFL_relational_all_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|winner_name|winner_id|pts_win|yards_win|to_win|mu_rel_all_t1|std_rel_all_t1|med_rel_all_t1|loser_name|loser_id|pts_lose|yards_lose|to_lose|mu_rel_all_t2|std_rel_all_t2|med_rel_all_t2'


	file3 = open('../Data/BoxScores/matchbymatchinfo/NFL_season_'+str(start_yr)+'_match_by_match_score_team_info.txt','r') 
	data3 = file3.readlines()[1:]

	for line in data3 :

			line = line.strip().split('|')

			team1 = line[3]; team2 = line[8]

			keys1 = str(team1.split('_')[-1])+'|'+str(line[2]); keys2 = str(team2.split('_')[-1])+'|'+str(line[2])


			## Average relational
			mean_rel_t1 = float(np.nanmean(teams_id[keys1])); 		mean_rel_t2 = float(np.nanmean(teams_id[keys2]))
			median_rel_t1 = float(np.nanmedian(teams_id[keys1])); 	median_rel_t2 = float(np.nanmedian(teams_id[keys2]))
			std_rel_t1 = float(np.std(teams_id[keys1]));   			std_rel_t2 = float(np.std(teams_id[keys2]))



			print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], line[4], line[5],  line[6], line[7], mean_rel_t1, std_rel_t1, median_rel_t1, line[8], line[9], line[10], line[11], line[12], mean_rel_t2, std_rel_t2, median_rel_t2)





def create_relational_variable_MLB(destdir, string_type, start_yr, bin1) :

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	filelist1 = glob.glob('../Data/BoxScores/MLB/textfiles/MLB_season_*_match_by_match_score_team_info.txt'); filelist1.sort()

	for f1 in filelist1 :
		file1 = open(str(f1),'r')
		data = file1.readlines()[1:]


		for line in data :  
			line = line.strip().split('|')
			matcid = line[1]
	  
			if int(line[4]) > int(line[7]) :
				matcid_team_result[str(line[2])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[5])+'|'+str(matcid)] = "L"

			if int(line[4]) == int(line[7]) :
				matcid_team_result[str(line[2])+'|'+str(matcid)] = "D"
				matcid_team_result[str(line[5])+'|'+str(matcid)] = "D"
	 
			if int(line[4]) < int(line[7]) :
				matcid_team_result[str(line[5])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[2])+'|'+str(matcid)] = "L"


	# print matcid_team_result

	filelist = glob.glob('../Data/BoxScores/matchbymatchinfo/MLB_season_*_match_by_match_box_score_player_info*.txt'); filelist.sort()
	 ## form relationship  !!!
	
	team_nodes = defaultdict(list);	team_combos = []; 	team_nodes_past = defaultdict(list)

	for f2 in filelist :

		file2 = open(f2,'r') ## form relationship  !!!
		data2 = file2.readlines()[1:]

		for line in data2 :
			line = line.strip().split('|')
			year = line[-1]

			if int(year) == int(start_yr) :
				team_nodes[str(line[3])+'|'+str(line[0])].append(str(line[1]))


			# if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :

				if str(string_type) == "suc" :
					if matcid_team_result[str(line[3])+'|'+str(line[0])] == "W" : 
						team_nodes_past[str(line[3])+'|'+str(line[0])].append(str(line[1])) 

				if str(string_type) == "all" :	
						team_nodes_past[str(line[3])+'|'+str(line[0])].append(str(line[1]))	

	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))
		edges = combinations(nodes,2)

		G = nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = combinations(nodes2, 2)
		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])



	fh6 = open(destdir+'MLB_relational_'+str(string_type)+'_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mu_rel_'+str(string_type)+'_t1_bin_'+str(bin1)+'|std_rel_'+str(string_type)+'_t1_bin_'+str(bin1)+'|med_rel_'+str(string_type)+'_t1_bin_'+str(bin1)+'|home_name|home_id|home_pts|mu_rel_'+str(string_type)+'_t2_bin_'+str(bin1)+'|std_rel_'+str(string_type)+'_t2_bin_'+str(bin1)+'|med_rel_'+str(string_type)+'_t2_bin_'+str(bin1)

	#fh6 = open(destdir+'MLB_relational_'+str(string_type)+'_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mu_rel_'+str(string_type)+'_t1|std_rel_'+str(string_type)+'_t1|med_rel_'+str(string_type)+'_t1|home_name|home_id|home_pts|mu_rel_'+str(string_type)+'_t2|std_rel_'+str(string_type)+'_t2|med_rel_'+str(string_type)+'_t2'


	file4 = open('../Data/BoxScores/MLB/textfiles/MLB_season_'+str(start_yr)+'_match_by_match_score_team_info.txt','r') 
	data4 = file4.readlines()[1:]	


	for line in data4 :
		line = line.strip()
		line = line.split('|')

		team1 = line[2]; team2 = line[5]
		keys1 = str(team1)+'|'+str(line[1]); keys2 = str(team2) + '|' + str(line[1])


		## Average relational
		mean_rel_t1 = float(np.nanmean(teams_id[keys1])); 		mean_rel_t2 = float(np.nanmean(teams_id[keys2]))
		median_rel_t1 = float(np.nanmedian(teams_id[keys1])); 	median_rel_t2 = float(np.nanmedian(teams_id[keys2]))
		std_rel_t1 = float(np.std(teams_id[keys1]));   			std_rel_t2 = float(np.std(teams_id[keys2]))



		print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], line[4], mean_rel_t1, std_rel_t1, median_rel_t1, line[5], line[6], line[7], mean_rel_t2, std_rel_t2, median_rel_t2)





def create_relational_variable_soccer(sourcedir, destdir, start_yr, bin1) :

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	filelist1 = glob.glob('../Data/data_for_analysis/transfrmarket/'+str(sourcedir)+'/'+'Bundelisga_result*.txt'); filelist1.sort()

	for f1 in filelist1 :
		file1 = open(str(f1),'r')
		data = file1.readlines()[1:]


		for line in data :  
			line = line.strip().split('|')
			matcid = line[0]
	  
			team_home_id = line[1].split('/')[4]; team_away_id = line[3].split('/')[4]

			score_home = line[-1].split('(')[0].split(":")[0]
			score_away = line[-1].split('(')[0].split(":")[1]

			if int(score_home) > int(score_away) :
				matcid_team_result[str(team_home_id)+'|'+str(matcid)] = "W"
				matcid_team_result[str(team_away_id)+'|'+str(matcid)] = "L"

			if int(score_home) == int(score_away) :
				matcid_team_result[str(team_home_id)+'|'+str(matcid)] = "D"
				matcid_team_result[str(team_away_id)+'|'+str(matcid)] = "D"
	 
			if int(score_home) < int(score_away) :
				matcid_team_result[str(team_away_id)+'|'+str(matcid)] = "W"
				matcid_team_result[str(team_home_id)+'|'+str(matcid)] = "L"


	# print matcid_team_result

	 ## form relationship  !!!
	filelist = glob.glob('../Data/data_for_analysis/transfrmarket/'+str(sourcedir)+'/'+'Bundelisga_players_*.txt'); filelist.sort()
	
	team_nodes = defaultdict(list);	team_combos = []; 	team_nodes_past = defaultdict(list)

	for f2 in filelist :

		file2 = open(f2,'r') ## form relationship  !!!
		data2 = file2.readlines()[1:]

		for line in data2 :
			line = line.strip().split('|')
			matcid = line[0]
			playerid = line[1].split('/')[-1]
			team_id = line[2].split('/')[4]
			year = line[2].split('/')[-1]

			if int(year) == int(start_yr) :
				team_nodes[str(team_id)+'|'+str(matcid)].append(str(playerid))


			# if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :
				# if matcid_team_result[str(team_id)+'|'+str(matcid)] == "W" : 
					team_nodes_past[str(team_id)+'|'+str(matcid)].append(str(playerid)) 

	# print team_nodes_past
	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))
		edges = combinations(nodes,2)

		G = nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


 ## now look back and see how many times players played with each other earlier !

	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = combinations(nodes2, 2)
		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])

		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])


	# fh6 = open(destdir+'Bundelisga_relational_succesful_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'MatchID|team_home|team_home_id|score_home|mu_rel_suc_t1_bin_'+str(bin1)+'|std_rel_suc_t1_bin_'+str(bin1)+'|med_rel_suc_t1_bin_'+str(bin1)+'|team_away|team_away_id|score_away|mu_rel_suc_t2_bin_'+str(bin1)+'|std_rel_suc_t2_bin_'+str(bin1)+'|med_rel_suc_t2_bin_'+str(bin1)
	
	fh6 = open(destdir+'Bundelisga_relational_all_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'MatchID|team_home|team_home_id|score_home|mu_rel_all_t1_bin_'+str(bin1)+'|std_rel_all_t1_bin_'+str(bin1)+'|med_rel_all_t1_bin_'+str(bin1)+'|team_away|team_away_id|score_away|mu_rel_all_t2_bin_'+str(bin1)+'|std_rel_all_t2_bin_'+str(bin1)+'|med_rel_all_t2_bin_'+str(bin1)


	# fh6 = open(destdir+'Bundelisga_relational_succesful_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'MatchID|team_home|team_home_id|score_home|mu_rel_suc_t1|std_rel_suc_t1|med_rel_suc_t1|team_away|team_away_id|score_away|mu_rel_suc_t2|std_rel_suc_t2|med_rel_suc_t2'
	
	# fh6 = open(destdir+'Bundelisga_relational_all_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'MatchID|team_home|team_home_id|score_home|mu_rel_all_t1|std_rel_all_t1|med_rel_all_t1|team_away|team_away_id|score_away|mu_rel_all_t2|std_rel_all_t2|med_rel_all_t2'

	filelist2 = glob.glob('../Data/data_for_analysis/transfrmarket/'+str(sourcedir)+'/'+'Bundelisga_result*.txt'); filelist2.sort()

	for f2 in filelist2 :
		file2 = open(str(f2),'r')
		data = file2.readlines()[1:]


		for line in data :  
			line = line.strip().split('|')
			matcid = line[0]

			team_home = line[1].split('/')[1]
			team_away = line[3].split('/')[1]
	  
			team_home_id = line[1].split('/')[4]
			team_away_id = line[3].split('/')[4]

			score_home = line[-1].split('(')[0].split(":")[0]
			score_away = line[-1].split('(')[0].split(":")[1]

			keys1 = str(team_home_id)+'|'+str(matcid); 
			keys2 = str(team_away_id)+'|'+str(matcid)

			year = line[1].split('/')[-1]

			if int(year) == int(start_yr) :
				## Average relational
				mean_rel_t1 = float(np.nanmean(teams_id[keys1])); 		mean_rel_t2 = float(np.nanmean(teams_id[keys2]))
				median_rel_t1 = float(np.nanmedian(teams_id[keys1])); 	median_rel_t2 = float(np.nanmedian(teams_id[keys2]))
				std_rel_t1 = float(np.std(teams_id[keys1]));   			std_rel_t2 = float(np.std(teams_id[keys2]))

				print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( matcid, team_home, team_home_id, score_home, mean_rel_t1, std_rel_t1, median_rel_t1, team_away, team_away_id, score_away, mean_rel_t2, std_rel_t2, median_rel_t2)






#####	@@@@@@@		#### %%%%%% &&&&& 								
#####	Code for player-coach relationship!
#### 	*********** #### ******* ******

def create_relational_variable_player_coach_NBA(destdir, start_yr, bin1) :

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	filelist1 = glob.glob('../Data/BoxScores/matchbymatchinfo/NBA_season_*_match_by_match_score_team_info.txt'); filelist1.sort()

	for f1 in filelist1 :
		file1 = open(str(f1),'r')
		data = file1.readlines()[1:]


		for line in data :  
			line = line.strip().split('|')
			matcid = line[2]
	  
			if int(line[5]) > int(line[8]) :
				matcid_team_result[str(line[3])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[6])+'|'+str(matcid)] = "L"

			if int(line[5]) == int(line[8]) :
				matcid_team_result[str(line[3])+'|'+str(matcid)] = "D"
				matcid_team_result[str(line[6])+'|'+str(matcid)] = "D"
	 
			if int(line[5]) < int(line[8]) :
				matcid_team_result[str(line[6])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[3])+'|'+str(matcid)] = "L"


	filelist2 = glob.glob('../Data/BoxScores/matchbymatchinfo/NBA_season_*_match_by_match_score_team_coaches_info.txt'); filelist1.sort()

	dict_matchid_coach_team = defaultdict(list)
	for f2 in filelist2 :
		file2 = open(str(f2),'r')
		data2 = file2.readlines()[1:]

		for line in data2 :  
			line = line.strip().split('|')
			matchid = line[2]
			teamv = line[3]
			coachv = line[5]
			teamh = line[7]
			coachh = line[9]

			if not "[]" in coachv :
				dict_matchid_coach_team[str(teamv)+'|'+str(matchid)] = str(coachv)
			
			if not "[]" in coachh :	  			
				dict_matchid_coach_team[str(teamh)+'|'+str(matchid)] = str(coachh)



	# print matcid_team_result

	filelist = glob.glob('../Data/BoxScores/matchbymatchinfo/NBA_season_*_match_by_match_box_score_player_info.txt'); filelist.sort()
	 ## form relationship  !!!
	
	team_nodes = defaultdict(list);	team_combos = []; 	team_nodes_past = defaultdict(list)

	for f2 in filelist :

		file2 = open(f2,'r') ## form relationship  !!!
		data2 = file2.readlines()[1:]

		for line in data2 :
			line = line.strip().split('|')
			year = line[4]

			if int(year) == int(start_yr) :
				team_nodes[str(line[1])+'|'+str(line[0])].append(str(line[2]))


			# if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :
				# if matcid_team_result[str(line[1])+'|'+str(line[0])] == "W" : 
					team_nodes_past[str(line[1])+'|'+str(line[0])].append(str(line[2])) 

	# print team_nodes_past
	players_pair = defaultdict(list)

	for k in team_nodes :
		players = list(set(team_nodes[k]))
		
		edges = []


		if str(k) in dict_matchid_coach_team :
			coach = dict_matchid_coach_team[str(k)]
			for p in players :
				edges.append((coach, p))
		
		G = nx.Graph();  G.add_edges_from(edges) 

		# print k, G.edges()

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


 ## now look back and see how many times players played with each other earlier !

	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = []

		if str(k) in dict_matchid_coach_team :
			coach = dict_matchid_coach_team[str(k)]
			for n in nodes2 :
				edges2.append((coach, n))

		# print k, edges2


		G2 = nx.Graph(); G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])


	# fh6 = open(destdir+'NBA_relational_succesful_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mu_coach_player_suc_t1_bin_'+str(bin1)+'|std_coach_player_suc_t1_bin_'+str(bin1)+'|med_coach_player_suc_t1_bin_'+str(bin1)+'|home_name|home_id|home_pts|mu_coach_player_suc_t2_bin_'+str(bin1)+'|std_coach_player_suc_t2_bin_'+str(bin1)+'|med_coach_player_suc_t2_bin_'+str(bin1)
	
	fh6 = open(destdir+'NBA_coach_player_all_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'date|seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mu_coach_player_all_t1_bin_'+str(bin1)+'|std_coach_player_all_t1_bin_'+str(bin1)+'|med_coach_player_all_t1_bin_'+str(bin1)+'|home_name|home_id|home_pts|mu_coach_player_all_t2_bin_'+str(bin1)+'|std_coach_player_all_t2_bin_'+str(bin1)+'|med_coach_player_all_t2_bin_'+str(bin1)


	# fh6 = open(destdir+'NBA_coach_player_succesful_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mu_coach_player_suc_t1|std_coach_player_suc_t1|med_coach_player_suc_t1|home_name|home_id|home_pts|mu_coach_player_suc_t2|std_coach_player_suc_t2|med_coach_player_suc_t2'
	
	# fh6 = open(destdir+'NBA_coach_player_all_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mu_coach_player_all_t1|std_coach_player_all_t1|med_coach_player_all_t1|home_name|home_id|home_pts|mu_coach_player_all_t2|std_coach_player_all_t2|med_coach_player_all_t2'


	file3 = open('../Data/BoxScores/matchbymatchinfo/NBA_season_'+str(start_yr)+'_match_by_match_score_team_info.txt','r') 
	data3 = file3.readlines()[1:]

	for line in data3 :

			line = line.strip().split('|')

			team1 = line[3]; team2 = line[6]

			keys1 = str(team1)+'|'+str(line[2]); keys2 = str(team2)+'|'+str(line[2])


			## Average relational
			mean_rel_t1 = float(np.nanmean(teams_id[keys1])); 		mean_rel_t2 = float(np.nanmean(teams_id[keys2]))
			median_rel_t1 = float(np.nanmedian(teams_id[keys1])); 	median_rel_t2 = float(np.nanmedian(teams_id[keys2]))
			std_rel_t1 = float(np.std(teams_id[keys1]));   			std_rel_t2 = float(np.std(teams_id[keys2]))



			print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], line[4], line[5], mean_rel_t1, std_rel_t1, median_rel_t1, line[6], line[7], line[8], mean_rel_t2, std_rel_t2, median_rel_t2)




def create_relational_variable_player_coach_NFL(destdir, start_yr, bin1) :

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	filelist1 = glob.glob('../Data/BoxScores/matchbymatchinfo/NFL_season_*_match_by_match_score_team_info.txt'); filelist1.sort()

	dict_short_form = defaultdict(list)


	for f1 in filelist1 :
		file1 = open(str(f1),'r')
		data = file1.readlines()[1:]


		for line in data :  
			line = line.strip().split('|')
			matcid = line[2]
	  
			matcid_team_result[str(line[3].split('_')[-1])+'|'+str(matcid)] = "W"
			matcid_team_result[str(line[8].split('_')[-1])+'|'+str(matcid)] = "L"

			dict_short_form[str(line[4])] = str(line[3].split('_')[-1])
			dict_short_form[str(line[9])] = str(line[9].split('_')[-1])


	filescoach = glob.glob('../Data/BoxScores/matchbymatchinfo/NBA_season_*_match_by_match_score_team_coaches_info.txt'); filelist1.sort()

	dict_matchid_coach_team = defaultdict(list)
	for fc in filescoach :
		filec = open(str(fc),'r')
		datascores = filec.readlines()[1:]

		for line in datascores :  
			line = line.strip().split('|')
			matchid = line[0]
			teamv = line[5].split('_')[-1]
			coachv = line[8].split('/')[-1][:-4]
			teamh = line[1].split('_')[-1]
			coachh = line[4].split('/')[-1][:-4]

			dict_matchid_coach_team[str(teamv)+'|'+str(matchid)] = str(coachv)
			dict_matchid_coach_team[str(teamh)+'|'+str(matchid)] = str(coachh)




	# print matcid_team_result

	filelist = glob.glob('../Data/BoxScores/matchbymatchinfo/NFL_season_*_match_by_match_box_score_player_info.txt'); filelist.sort()
	 ## form relationship  !!!
	
	team_nodes = defaultdict(list);	team_combos = []; 	team_nodes_past = defaultdict(list)

	for f2 in filelist :

		file2 = open(f2,'r') ## form relationship  !!!
		data2 = file2.readlines()[1:]

		for line in data2 :
			line = line.strip().split('|')
			year = line[-1]

			if int(year) == int(start_yr) :
				team_nodes[str(line[1].split(' Snap Counts')[0])+'|'+str(line[0])].append(str(line[2]))


			# if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :
				# if matcid_team_result[str(line[1].split(' Snap Counts')[0])+'|'+str(line[0])] == "W" : 
					team_nodes_past[str(line[1].split(' Snap Counts')[0])+'|'+str(line[0])].append(str(line[2])) 


# defense 

	filelist2 = glob.glob('../Data/BoxScores/matchbymatchinfo/NFL_season_*_match_by_match_box_score_defense_player_info.txt'); filelist2.sort()
	 ## form relationship  !!!
	
	for f3 in filelist2 :

		file3 = open(f3,'r') ## form relationship  !!!
		data3 = file3.readlines()[1:]

		for line in data3 :
			line = line.strip().split('|')
			year = line[-1]

			if int(year) == int(start_yr) :
				team_nodes[str(dict_short_form[str(line[3].lower())])+'|'+str(line[0])].append(str(line[1]))


			# if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :
				# if matcid_team_result[str(line[3].lower())])+'|'+str(line[0])] == "W" : 
					team_nodes_past[str(dict_short_form[str(line[3].lower())])+'|'+str(line[0])].append(str(line[1])) 



# offense

	filelist3 = glob.glob('../Data/BoxScores/matchbymatchinfo/NFL_season_*_match_by_match_box_score_offense_player_info.txt'); filelist3.sort()
	 ## form relationship  !!!
	
	for f4 in filelist3 :

		file4 = open(f4,'r') ## form relationship  !!!
		data4 = file4.readlines()[1:]

		for line in data4 :
			line = line.strip().split('|')
			year = line[-1]

			if int(year) == int(start_yr) :
				team_nodes[str(dict_short_form[str(line[3].lower())])+'|'+str(line[0])].append(str(line[1]))


			# if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :
				# if matcid_team_result[str(dict_short_form[str(line[3].lower())])+'|'+str(line[0])] == "W" : 
					team_nodes_past[str(dict_short_form[str(line[3].lower())])+'|'+str(line[0])].append(str(line[1])) 






	# print team_nodes_past
	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))
		edges = []

		if str(k) in dict_matchid_coach_team :
			coach = dict_matchid_coach_team[str(k)]
			for p in players :
				edges.append((coach, p))

		G = nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


 ## now look back and see how many times players played with each other earlier !

	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = []

		if str(k) in dict_matchid_coach_team :
			coach = dict_matchid_coach_team[str(k)]
			for n in nodes2 :
				edges2.append((coach, n))

		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])


	# fh6 = open(destdir+'NFL_coach_player_succesful_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|winner_name|winner_id|pts_win|yards_win|to_win|mu_coach_player_suc_t1_bin_'+str(bin1)+'|std_coach_player_suc_t1_bin_'+str(bin1)+'|med_coach_player_suc_t1_bin_'+str(bin1)+'|loser_name|loser_id|pts_lose|yards_lose|to_lose|mu_coach_player_suc_t2_bin_'+str(bin1)+'|std_coach_player_suc_t2_bin_'+str(bin1)+'|med_coach_player_suc_t2_bin_'+str(bin1)
	
	fh6 = open(destdir+'NFL_coach_player_all_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'date|seasonyear|boxscoreid|winner_name|winner_id|pts_win|yards_win|to_win|mu_coach_player_all_t1_bin_'+str(bin1)+'|std_coach_player_all_t1_bin_'+str(bin1)+'|med_coach_player_all_t1_bin_'+str(bin1)+'|loser_name|loser_id|pts_lose|yards_lose|to_lose|mu_coach_player_all_t2_bin_'+str(bin1)+'|std_coach_player_all_t2_bin_'+str(bin1)+'|med_coach_player_all_t2_bin_'+str(bin1)


	# fh6 = open(destdir+'NFL_coach_player_succesful_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|winner_name|winner_id|pts_win|yards_win|to_win|mu_coach_player_suc_t1|std_coach_player_suc_t1|med_coach_player_suc_t1|loser_name|loser_id|pts_lose|yards_lose|to_lose|mu_coach_player_suc_t2|std_coach_player_suc_t2|med_coach_player_suc_t2'
	
	# fh6 = open(destdir+'NFL_coach_player_all_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'date|seasonyear|boxscoreid|winner_name|winner_id|pts_win|yards_win|to_win|mu_coach_player_all_t1|std_coach_player_all_t1|med_coach_player_all_t1|loser_name|loser_id|pts_lose|yards_lose|to_lose|mu_coach_player_all_t2|std_coach_player_all_t2|med_coach_player_all_t2'


	file3 = open('../Data/BoxScores/matchbymatchinfo/NFL_season_'+str(start_yr)+'_match_by_match_score_team_info.txt','r') 
	data3 = file3.readlines()[1:]

	for line in data3 :

			line = line.strip().split('|')

			team1 = line[3]; team2 = line[8]

			keys1 = str(team1.split('_')[-1])+'|'+str(line[2]); keys2 = str(team2.split('_')[-1])+'|'+str(line[2])


			## Average relational
			mean_rel_t1 = float(np.nanmean(teams_id[keys1])); 		mean_rel_t2 = float(np.nanmean(teams_id[keys2]))
			median_rel_t1 = float(np.nanmedian(teams_id[keys1])); 	median_rel_t2 = float(np.nanmedian(teams_id[keys2]))
			std_rel_t1 = float(np.std(teams_id[keys1]));   			std_rel_t2 = float(np.std(teams_id[keys2]))



			print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], line[4], line[5],  line[6], line[7], mean_rel_t1, std_rel_t1, median_rel_t1, line[8], line[9], line[10], line[11], line[12], mean_rel_t2, std_rel_t2, median_rel_t2)




def create_relational_variable_coach_player_MLB(destdir, string_type, start_yr, bin1) :

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	filelist1 = glob.glob('../Data/BoxScores/MLB/textfiles/MLB_season_*_match_by_match_score_team_info.txt'); filelist1.sort()

	for f1 in filelist1 :
		file1 = open(str(f1),'r')
		data = file1.readlines()[1:]


		for line in data :  
			line = line.strip().split('|')
			matcid = line[1]
	  
			if int(line[4]) > int(line[7]) :
				matcid_team_result[str(line[2])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[5])+'|'+str(matcid)] = "L"

			if int(line[4]) == int(line[7]) :
				matcid_team_result[str(line[2])+'|'+str(matcid)] = "D"
				matcid_team_result[str(line[5])+'|'+str(matcid)] = "D"
	 
			if int(line[4]) < int(line[7]) :
				matcid_team_result[str(line[5])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[2])+'|'+str(matcid)] = "L"



	filelist2 = glob.glob('../Data/BoxScores/MLB/textfiles/MLB_season_*_match_by_match_score_team_managers_info.txt'); filelist2.sort()

	dict_matchid_coach_team = defaultdict(list)
	for f2 in filelist2 :
		file2 = open(str(f2),'r')
		data2 = file2.readlines()[1:]

		for line in data2 :  
			line = line.strip().split('|')
			matchid = line[1]
			teamv = line[2]
			coachv = line[4]
			teamh = line[6]
			coachh = line[8]

			if not "[]" in coachv :
				dict_matchid_coach_team[str(teamv)+'|'+str(matchid)] = str(coachv)
			
			if not "[]" in coachh :	  			
				dict_matchid_coach_team[str(teamh)+'|'+str(matchid)] = str(coachh)

	# print matcid_team_result

	filelist3 = glob.glob('../Data/BoxScores/matchbymatchinfo/MLB_season_*_match_by_match_box_score_player_info*.txt'); filelist3.sort()
	 ## form relationship  !!!
	
	team_nodes = defaultdict(list);	team_combos = []; 	team_nodes_past = defaultdict(list)

	for f3 in filelist3 :

		file3 = open(f3,'r') ## form relationship  !!!
		data3 = file3.readlines()[1:]

		for line in data3 :
			line = line.strip().split('|')
			year = line[-1]

			if int(year) == int(start_yr) :
				team_nodes[str(line[3])+'|'+str(line[0])].append(str(line[1]))


			# if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :

				if str(string_type) == "suc" :
					if matcid_team_result[str(line[3])+'|'+str(line[0])] == "W" : 
						team_nodes_past[str(line[3])+'|'+str(line[0])].append(str(line[1])) 

				if str(string_type) == "all" :	
						team_nodes_past[str(line[3])+'|'+str(line[0])].append(str(line[1]))	

	players_pair = defaultdict(list)

	for k in team_nodes :
		players = list(set(team_nodes[k]))
		
		edges = []


		if str(k) in dict_matchid_coach_team :
			coach = dict_matchid_coach_team[str(k)]
			for p in players :
				edges.append((coach, p))
		
		G = nx.Graph();  G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = []

		if str(k) in dict_matchid_coach_team :
			coach = dict_matchid_coach_team[str(k)]
			for n in nodes2 :
				edges2.append((coach, n))

		G2 = nx.Graph(); G2.add_edges_from(edges2) 

		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])



	fh6 = open(destdir+'MLB_coach_player_'+str(string_type)+'_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mu_coach_player_'+str(string_type)+'_t1_bin_'+str(bin1)+'|std_coach_player_'+str(string_type)+'_t1_bin_'+str(bin1)+'|med_coach_player_'+str(string_type)+'_t1_bin_'+str(bin1)+'|home_name|home_id|home_pts|mu_coach_player_'+str(string_type)+'_t2_bin_'+str(bin1)+'|std_coach_player_'+str(string_type)+'_t2_bin_'+str(bin1)+'|med_coach_player_'+str(string_type)+'_t2_bin_'+str(bin1)

	#fh6 = open(destdir+'MLB_coach_player_'+str(string_type)+'_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'seasonyear|boxscoreid|visitor_name|visitor_id|visitor_pts|mu_coach_player_'+str(string_type)+'_t1|std_coach_player_'+str(string_type)+'_t1|med_coach_player_'+str(string_type)+'_t1|home_name|home_id|home_pts|mu_coach_player_'+str(string_type)+'_t2|std_coach_player_'+str(string_type)+'_t2|med_coach_player_'+str(string_type)+'_t2'


	file4 = open('../Data/BoxScores/MLB/textfiles/MLB_season_'+str(start_yr)+'_match_by_match_score_team_info.txt','r') 
	data4 = file4.readlines()[1:]	


	for line in data4 :
		line = line.strip()
		line = line.split('|')

		team1 = line[2]; team2 = line[5]
		keys1 = str(team1)+'|'+str(line[1]); keys2 = str(team2) + '|' + str(line[1])


		## Average relational
		mean_rel_t1 = float(np.nanmean(teams_id[keys1])); 		mean_rel_t2 = float(np.nanmean(teams_id[keys2]))
		median_rel_t1 = float(np.nanmedian(teams_id[keys1])); 	median_rel_t2 = float(np.nanmedian(teams_id[keys2]))
		std_rel_t1 = float(np.std(teams_id[keys1]));   			std_rel_t2 = float(np.std(teams_id[keys2]))



		print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( line[0], line[1], line[2], line[3], line[4], mean_rel_t1, std_rel_t1, median_rel_t1, line[5], line[6], line[7], mean_rel_t2, std_rel_t2, median_rel_t2)



def create_relational_variable_player_coach_soccer(sourcedir, destdir, start_yr):#, bin1) :

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)
	dict_matchid_coach_team = defaultdict(list)

	filelist1 = glob.glob('../Data/data_for_analysis/transfrmarket/'+str(sourcedir)+'/'+'Bundelisga_result*.txt'); filelist1.sort()

	for f1 in filelist1 :
		file1 = open(str(f1),'r')
		data = file1.readlines()[1:]


		for line in data :  
			line = line.strip().split('|')
			matcid = line[0]
	  
			team_home_id = line[1].split('/')[4]; team_away_id = line[3].split('/')[4]

			score_home = line[-1].split('(')[0].split(":")[0]
			score_away = line[-1].split('(')[0].split(":")[1]

			coach_home_id = line[2].split('/')[-1]; coach_away_id = line[4].split('/')[-1]

			if int(score_home) > int(score_away) :
				matcid_team_result[str(team_home_id)+'|'+str(matcid)] = "W"
				matcid_team_result[str(team_away_id)+'|'+str(matcid)] = "L"

			if int(score_home) == int(score_away) :
				matcid_team_result[str(team_home_id)+'|'+str(matcid)] = "D"
				matcid_team_result[str(team_away_id)+'|'+str(matcid)] = "D"
	 
			if int(score_home) < int(score_away) :
				matcid_team_result[str(team_away_id)+'|'+str(matcid)] = "W"
				matcid_team_result[str(team_home_id)+'|'+str(matcid)] = "L"

			dict_matchid_coach_team[str(team_home_id)+'|'+str(matcid)] = str(coach_home_id)
			dict_matchid_coach_team[str(team_away_id)+'|'+str(matcid)] = str(coach_away_id)

	# print matcid_team_result

	filelist = glob.glob('../Data/data_for_analysis/transfrmarket/'+str(sourcedir)+'/'+'Bundelisga_players_*.txt'); filelist.sort()
	
	team_nodes = defaultdict(list);	team_combos = []; 	team_nodes_past = defaultdict(list)

	for f2 in filelist :

		file2 = open(f2,'r') ## form relationship  !!!
		data2 = file2.readlines()[1:]

		for line in data2 :
			line = line.strip().split('|')
			matcid = line[0]
			playerid = line[1].split('/')[-1]
			team_id = line[2].split('/')[4]
			year = line[2].split('/')[-1]

			if int(year) == int(start_yr) :
				team_nodes[str(team_id)+'|'+str(matcid)].append(str(playerid))

			if int(year) < int(start_yr) :
			# if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :
				# if matcid_team_result[str(team_id)+'|'+str(matcid)] == "W" : 
					team_nodes_past[str(team_id)+'|'+str(matcid)].append(str(playerid)) 

	# print team_nodes_past
	players_pair = defaultdict(list)

	for k in team_nodes :
		players = list(set(team_nodes[k]))
		edges = []

		if str(k) in dict_matchid_coach_team :
			coach = dict_matchid_coach_team[str(k)]
			for p in players :
				edges.append((coach, p))
		
		G = nx.Graph();  G.add_edges_from(edges) 

		# print k, G.edges()

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


 ## now look back and see how many times players played with each other earlier !

	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = []

		if str(k) in dict_matchid_coach_team :
			coach = dict_matchid_coach_team[str(k)]
			for n in nodes2 :
				edges2.append((coach, n))

		# print k, edges2


		G2 = nx.Graph(); G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])


	# fh6 = open(destdir+'Bundelisga_coach_player_succesful_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'MatchID|team_home|team_home_id|score_home|mu_coach_player_suc_t1_bin_'+str(bin1)+'|std_coach_player_suc_t1_bin_'+str(bin1)+'|med_coach_player_suc_t1_bin_'+str(bin1)+'|team_away|team_away_id|score_away|mu_coach_player_suc_t2_bin_'+str(bin1)+'|std_coach_player_suc_t2_bin_'+str(bin1)+'|med_coach_player_suc_t2_bin_'+str(bin1)
	
	# fh6 = open(destdir+'Bundelisga_coach_player_all_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'MatchID|team_home|team_home_id|score_home|mu_coach_player_all_t1_bin_'+str(bin1)+'|std_coach_player_all_t1_bin_'+str(bin1)+'|med_coach_player_all_t1_bin_'+str(bin1)+'|team_away|team_away_id|score_away|mu_coach_player_all_t2_bin_'+str(bin1)+'|std_coach_player_all_t2_bin_'+str(bin1)+'|med_coach_player_all_t2_bin_'+str(bin1)


	# fh6 = open(destdir+'Bundelisga_coach_player_succesful_'+str(start_yr)+'.txt', 'w')
	# print >> fh6, 'MatchID|team_home|team_home_id|score_home|mu_coach_player_suc_t1|std_coach_player_suc_t1|med_coach_player_suc_t1|team_away|team_away_id|score_away|mu_coach_player_suc_t2|std_coach_player_suc_t2|med_coach_player_suc_t2'
	
	fh6 = open(destdir+'Bundelisga_coach_player_all_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'MatchID|team_home|team_home_id|score_home|mu_coach_player_all_t1|std_coach_player_all_t1|med_coach_player_all_t1|team_away|team_away_id|score_away|mu_coach_player_all_t2|std_coach_player_all_t2|med_coach_player_all_t2'


	filelist2 = glob.glob('../Data/data_for_analysis/transfrmarket/'+str(sourcedir)+'/'+'Bundelisga_result*.txt'); filelist2.sort()

	for f2 in filelist2 :
		file2 = open(str(f2),'r')
		data = file2.readlines()[1:]


		for line in data :  
			line = line.strip().split('|')
			matcid = line[0]

			team_home = line[1].split('/')[1]
			team_away = line[3].split('/')[1]
	  
			team_home_id = line[1].split('/')[4]
			team_away_id = line[3].split('/')[4]

			score_home = line[-1].split('(')[0].split(":")[0]
			score_away = line[-1].split('(')[0].split(":")[1]

			keys1 = str(team_home_id)+'|'+str(matcid); 
			keys2 = str(team_away_id)+'|'+str(matcid)

			year = line[1].split('/')[-1]

			if int(year) == int(start_yr) :
				## Average relational
				mean_rel_t1 = float(np.nanmean(teams_id[keys1])); 		mean_rel_t2 = float(np.nanmean(teams_id[keys2]))
				median_rel_t1 = float(np.nanmedian(teams_id[keys1])); 	median_rel_t2 = float(np.nanmedian(teams_id[keys2]))
				std_rel_t1 = float(np.std(teams_id[keys1]));   			std_rel_t2 = float(np.std(teams_id[keys2]))

				print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % ( matcid, team_home, team_home_id, score_home, mean_rel_t1, std_rel_t1, median_rel_t1, team_away, team_away_id, score_away, mean_rel_t2, std_rel_t2, median_rel_t2)




if __name__ == '__main__':

	f1 = sys.argv[1]; f2 = sys.argv[2]; f3 = sys.argv[3]; #f4 = sys.argv[4]; #f5 = sys.argv[5]; f6 = sys.argv[6]; f7 = sys.argv[7]; #f8 = sys.argv[8]; f9 = sys.argv[9]

	# gen_compositional_mlb_variables(f1, f2, f3)

	# gen_compositional_NBA_variables(f1, f2, f3)
	#gen_compositional_IPL_variables(f1, f2, f3, f4)

	#create_relational_variable_IPL(f1, f2, f3)
	# create_relational_variable_NBA(f1, f2, f3)
	#create_relational_variable_MLB(f1, f2, f3, f4, f5)
	#create_relational_variable_EPL(f1, f2, f3, f4, f5)

	# create_relational_variable_player_coach_NBA(f1, f2, f3)
	# gen_compositional_NFL_variables(f1, f2)#, f3)
	# create_relational_variable_NFL(f1, f2, f3)
	# create_relational_variable_coach_player_MLB(f1, f2, f3, f4)

	# create_relational_variable_soccer(f1, f2, f3, f4)
	create_relational_variable_player_coach_soccer(f1, f2, f3)

	# gen_compositional_soccer_variables(f1, f2, f3, f4)



