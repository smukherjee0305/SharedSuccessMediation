import sys
import os
import networkx as nx
from collections import defaultdict
import glob
import numpy as np
np.set_printoptions(legacy='1.25')

# sys.path.insert(0, '/Users/satyammukherjee/OneDrive - Shiv Nadar University/ProjectResearch/ComputationalLegalStudies/Codes/')

# import old_gml as nx_old


def create_edgelist_network_sports(f1, gmlw) :

	data1 = open(f1, 'r')
	G = nx.DiGraph()

	edgelist_win_loss = [];edgelist_diff_score = [];
	edgelist_pl_coach = []; edgelist_pl_pl = []; 

	edgelist_skill1_bin1 = []; edgelist_skill2_bin1 = []
	edgelist_skill1_bin3 = []; edgelist_skill2_bin3 = []
	edgelist_skill1_bin5 = []; edgelist_skill2_bin5 = []

	for line in data1.readlines()[1:] :
		line = line.strip().split('|')

		try :
			matchid = str(line[1])

			team1 = str(line[2]); score1 = int(line[3])
			team2 = str(line[4]); score2 = int(line[5])

			skill1_bin1 = float(line[6])
			skill1_bin3 = float(line[7])
			skill1_bin5 = float(line[8])

			skill2_bin1 = float(line[9])
			skill2_bin3 = float(line[10])
			skill2_bin5 = float(line[11])

			plcoach = float(line[12])
			plpl = float(line[13])

			node1 = team1+'__'+matchid
			node2 = team2+'__'+matchid

			if score2 > score1:
				diffscore = score2 - score1

				edgelist_diff_score.append((node1, node2, diffscore))
				edgelist_pl_coach.append((node1, node2, plcoach))
				edgelist_pl_pl.append((node1, node2, plpl))

				edgelist_skill1_bin1.append((node1, node2, skill1_bin1))
				edgelist_skill1_bin3.append((node1, node2, skill1_bin3))
				edgelist_skill1_bin5.append((node1, node2, skill1_bin5))

				edgelist_skill2_bin1.append((node1, node2, skill2_bin1))
				edgelist_skill2_bin3.append((node1, node2, skill2_bin3))
				edgelist_skill2_bin5.append((node1, node2, skill2_bin5))


			if score1 > score2:
				diffscore = score1 - score2

				edgelist_diff_score.append((node2, node1, diffscore))
				edgelist_pl_coach.append((node2, node1, plcoach))
				edgelist_pl_pl.append((node2, node1, plpl))

				edgelist_skill1_bin1.append((node2, node1, skill1_bin1))
				edgelist_skill1_bin3.append((node2, node1, skill1_bin3))
				edgelist_skill1_bin5.append((node2, node1, skill1_bin5))

				edgelist_skill2_bin1.append((node2, node1, skill2_bin1))
				edgelist_skill2_bin3.append((node2, node1, skill2_bin3))
				edgelist_skill2_bin5.append((node2, node1, skill2_bin5))


		except ValueError:
			continue

	G.add_weighted_edges_from(edgelist_diff_score,weight="diffscore")
	G.add_weighted_edges_from(edgelist_pl_coach,weight="diff_pl_coach")
	G.add_weighted_edges_from(edgelist_pl_pl,weight="diff_pl_pl")

	G.add_weighted_edges_from(edgelist_skill1_bin1,weight="diff_sk1_bin1")
	G.add_weighted_edges_from(edgelist_skill1_bin3,weight="diff_sk1_bin3")
	G.add_weighted_edges_from(edgelist_skill1_bin5,weight="diff_sk1_bin5")

	G.add_weighted_edges_from(edgelist_skill2_bin1,weight="diff_sk2_bin1")
	G.add_weighted_edges_from(edgelist_skill2_bin3,weight="diff_sk2_bin3")
	G.add_weighted_edges_from(edgelist_skill2_bin5,weight="diff_sk2_bin5")


	# print G.edges(data=True)
	G = nx_old.write_gml(G, str(gmlw))

def create_edgelist_network_sports_agg(f1, gmlw) :

	data1 = open(f1, 'r')
	G = nx.DiGraph()

	edgelist_win_loss = defaultdict(list);edgelist_diff_score = defaultdict(list);
	edgelist_pl_coach = defaultdict(list); edgelist_pl_pl = defaultdict(list); 

	edgelist_skill1_bin1 = defaultdict(list); edgelist_skill2_bin1 = defaultdict(list)
	edgelist_skill1_bin3 = defaultdict(list); edgelist_skill2_bin3 = defaultdict(list)
	edgelist_skill1_bin5 = defaultdict(list); edgelist_skill2_bin5 = defaultdict(list)

	for line in data1.readlines()[1:] :
		line = line.strip().split('|')

		try :
			seasonyear = str(line[0])
			matchid = str(line[2])

			team1 = str(line[3]); score1 = int(line[4])
			team2 = str(line[5]); score2 = int(line[6])

			skill1_bin1 = float(line[7])
			skill1_bin3 = float(line[8])
			skill1_bin5 = float(line[9])

			skill2_bin1 = float(line[10])
			skill2_bin3 = float(line[11])
			skill2_bin5 = float(line[12])

			plcoach = float(line[13])
			plpl = float(line[14])

			node1 = team1
			node2 = team2
			# print seasonyear, season
			node1 = team1+'__'+seasonyear
			node2 = team2+'__'+seasonyear
			# if int(seasonyear) == int(season) :

			if score2 > score1:
					diffscore = score2 - score1

					edgelist_diff_score[(node1, node2)].append(diffscore)
					edgelist_pl_coach[(node1, node2)].append(plcoach)
					edgelist_pl_pl[(node1, node2)].append( plpl)

					edgelist_skill1_bin1[(node1, node2)].append(skill1_bin1)
					edgelist_skill1_bin3[(node1, node2)].append(skill1_bin3)
					edgelist_skill1_bin5[(node1, node2)].append(skill1_bin5)

					edgelist_skill2_bin1[(node1, node2)].append(skill2_bin1)
					edgelist_skill2_bin3[(node1, node2)].append(skill2_bin3)
					edgelist_skill2_bin5[(node1, node2)].append(skill2_bin5)


			if score1 > score2:
					diffscore = score1 - score2

					edgelist_diff_score[(node2, node1)].append(diffscore)
					edgelist_pl_coach[(node2, node1)].append(plcoach)
					edgelist_pl_pl[(node2, node1)].append(plpl)

					edgelist_skill1_bin1[(node2, node1)].append(skill1_bin1)
					edgelist_skill1_bin3[(node2, node1)].append(skill1_bin3)
					edgelist_skill1_bin5[(node2, node1)].append(skill1_bin5)

					edgelist_skill2_bin1[(node2, node1)].append(skill2_bin1)
					edgelist_skill2_bin3[(node2, node1)].append(skill2_bin3)
					edgelist_skill2_bin5[(node2, node1)].append(skill2_bin5)


		except ValueError:
			continue


	mu_edges_score = []; mu_edges_pl_coach = []; mu_edges_pl_pl = []; 
	sum_edges_score = []; sum_edges_pl_coach = []; sum_edges_pl_pl = []; 

	for keys in sorted(edgelist_diff_score.iterkeys()) :
			mu_edges_score.append((keys[0], keys[1], np.mean(edgelist_diff_score[keys])))
			sum_edges_score.append((keys[0], keys[1], np.sum(edgelist_diff_score[keys]))) 

	for keys in sorted(edgelist_pl_coach.iterkeys()) :
			mu_edges_pl_coach.append((keys[0], keys[1], np.mean(edgelist_pl_coach[keys])))
			sum_edges_pl_coach.append((keys[0], keys[1], np.sum(edgelist_pl_coach[keys])))

	for keys in sorted(edgelist_pl_pl.iterkeys()) :
			mu_edges_pl_pl.append((keys[0], keys[1], np.mean(edgelist_pl_pl[keys]))) 
			sum_edges_pl_pl.append((keys[0], keys[1], np.sum(edgelist_pl_pl[keys]))) 

	mu_edges_skill1_bin1 = []; mu_edges_skill1_bin3 = []; mu_edges_skill1_bin5 = []; 
	sum_edges_skill1_bin1 = []; sum_edges_skill1_bin3 = []; sum_edges_skill1_bin5 = []; 

	for keys in sorted(edgelist_skill1_bin1.iterkeys()) :
			mu_edges_skill1_bin1.append((keys[0], keys[1], np.mean(edgelist_skill1_bin1[keys])))
			sum_edges_skill1_bin1.append((keys[0], keys[1], np.sum(edgelist_skill1_bin1[keys]))) 

	for keys in sorted(edgelist_skill1_bin3.iterkeys()) :
			mu_edges_skill1_bin3.append((keys[0], keys[1], np.mean(edgelist_skill1_bin3[keys])))
			sum_edges_skill1_bin3.append((keys[0], keys[1], np.sum(edgelist_skill1_bin3[keys])))

	for keys in sorted(edgelist_skill1_bin5.iterkeys()) :
			mu_edges_skill1_bin5.append((keys[0], keys[1], np.mean(edgelist_skill1_bin5[keys]))) 
			sum_edges_skill1_bin5.append((keys[0], keys[1], np.sum(edgelist_skill1_bin5[keys]))) 


	mu_edges_skill2_bin1 = []; mu_edges_skill2_bin3 = []; mu_edges_skill2_bin5 = []; 
	sum_edges_skill2_bin1 = []; sum_edges_skill2_bin3 = []; sum_edges_skill2_bin5 = []; 

	for keys in sorted(edgelist_skill2_bin1.iterkeys()) :
			mu_edges_skill2_bin1.append((keys[0], keys[1], np.mean(edgelist_skill2_bin1[keys])))
			sum_edges_skill2_bin1.append((keys[0], keys[1], np.sum(edgelist_skill2_bin1[keys]))) 

	for keys in sorted(edgelist_skill2_bin3.iterkeys()) :
			mu_edges_skill2_bin3.append((keys[0], keys[1], np.mean(edgelist_skill2_bin3[keys])))
			sum_edges_skill2_bin3.append((keys[0], keys[1], np.sum(edgelist_skill2_bin3[keys])))

	for keys in sorted(edgelist_skill2_bin5.iterkeys()) :
			mu_edges_skill2_bin5.append((keys[0], keys[1], np.mean(edgelist_skill2_bin5[keys]))) 
			sum_edges_skill2_bin5.append((keys[0], keys[1], np.sum(edgelist_skill2_bin5[keys]))) 


	G.add_weighted_edges_from(mu_edges_score,weight="diff_score_mu")
	G.add_weighted_edges_from(mu_edges_pl_coach,weight="pl_coach_mu")
	G.add_weighted_edges_from(mu_edges_pl_pl,weight="pl_pl_mu")

	G.add_weighted_edges_from(mu_edges_skill1_bin1,weight="skill1_bin1_mu")
	G.add_weighted_edges_from(mu_edges_skill1_bin3,weight="skill1_bin3_mu")
	G.add_weighted_edges_from(mu_edges_skill1_bin5,weight="skill1_bin5_mu")

	G.add_weighted_edges_from(mu_edges_skill2_bin1,weight="skill2_bin1_mu")
	G.add_weighted_edges_from(mu_edges_skill2_bin3,weight="skill2_bin3_mu")
	G.add_weighted_edges_from(mu_edges_skill2_bin5,weight="skill2_bin5_mu")


	G.add_weighted_edges_from(sum_edges_score,weight="diff_score_sum")
	G.add_weighted_edges_from(sum_edges_pl_coach,weight="pl_coach_sum")
	G.add_weighted_edges_from(sum_edges_pl_pl,weight="pl_pl_sum")

	G.add_weighted_edges_from(sum_edges_skill1_bin1,weight="skill1_bin1_sum")
	G.add_weighted_edges_from(sum_edges_skill1_bin3,weight="skill1_bin3_sum")
	G.add_weighted_edges_from(sum_edges_skill1_bin5,weight="skill1_bin5_sum")

	G.add_weighted_edges_from(sum_edges_skill2_bin1,weight="skill2_bin1_sum")
	G.add_weighted_edges_from(sum_edges_skill2_bin3,weight="skill2_bin3_sum")
	G.add_weighted_edges_from(sum_edges_skill2_bin5,weight="skill2_bin5_sum")

	
	# print G.edges(data=True)

	G = nx_old.write_gml(G, str(gmlw))



def create_team_vs_team_sports(f1) :

	data1 = open(f1, 'r')
	
	dict_1= defaultdict(list); list1 = []
	G = nx.DiGraph()
	for line in data1.readlines()[1:] :
		line = line.strip().split('|')

		try :
			year = str(line[0])
			matchid = str(line[1])

			team1 = str(line[2]); 
			team2 = str(line[4]); 	

			dict_1[year+'__'+matchid] = team1+'|'+team2+'|'+year+'|'+matchid
			list1.append((team1, team2))

		except ValueError:
			continue
	G.add_edges_from(list1)
	G2 = G.to_undirected()

	# print len(G.edges()), len(G2.edges())

	# for u,v, in G2.edges() :
	# 	print u, v, 


def get_nodecov_network(gmlw) :

	G = nx_old.read_gml(str(gmlw))

	##indegree
	indegree_centrality = G.in_degree()
	for node, deg in indegree_centrality.items() :
		G.node[node]['indegree'] = float(deg)

	for u,v,d in G.edges(data=True):
		num_matches_won = int((d['diff_score_sum']*1.0/d['diff_score_mu']))
		G[u][v]['num_matches_won'] = num_matches_won


	instr_centrality = G.in_degree(weight='num_matches_won')
	for node, deg in instr_centrality.items() :
		G.node[node]['instrength_matches'] = float(deg)

	# print G.nodes(data=True)
	G = nx_old.write_gml(G, str(gmlw))


def create_edgelist_network_sports_agg_yearly(gmlr, destdir) :

	G = nx_old.read_gml(gmlr)

	for gmlw in nx.strongly_connected_components(G):

		listgml = list(gmlw)

		nodelabels = [str(G.node[n]['label']) for n in listgml]
		season = nodelabels[0].split('__')[1]

		G2 = nx.DiGraph()
		G2.add_weighted_edges_from([ (u,v, d['num_matches_won']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='num_matches_won')
		G2.add_weighted_edges_from([ (u,v, d['skill2_bin1_mu']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='skill2_bin1_mu')
		G2.add_weighted_edges_from([ (u,v, d['skill1_bin5_mu']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='skill1_bin5_mu')
		G2.add_weighted_edges_from([ (u,v, d['pl_coach_mu']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='pl_coach_mu')
		G2.add_weighted_edges_from([ (u,v, d['skill1_bin3_mu']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='skill1_bin3_mu')
		G2.add_weighted_edges_from([ (u,v, d['pl_pl_mu']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='pl_pl_mu')
		G2.add_weighted_edges_from([ (u,v, d['skill1_bin3_sum']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='skill1_bin3_sum')
		G2.add_weighted_edges_from([ (u,v, d['diff_score_mu']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='diff_score_mu')
		G2.add_weighted_edges_from([ (u,v, d['skill2_bin3_sum']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='skill2_bin3_sum')
		G2.add_weighted_edges_from([ (u,v, d['diff_score_sum']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='diff_score_sum')
		G2.add_weighted_edges_from([ (u,v, d['skill2_bin5_mu']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='skill2_bin5_mu')
		G2.add_weighted_edges_from([ (u,v, d['skill1_bin1_sum']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='skill1_bin1_sum')
		G2.add_weighted_edges_from([ (u,v, d['skill2_bin3_mu']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='skill2_bin3_mu')
		G2.add_weighted_edges_from([ (u,v, d['skill1_bin5_sum']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='skill1_bin5_sum')
		G2.add_weighted_edges_from([ (u,v, d['pl_coach_sum']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='pl_coach_sum')
		G2.add_weighted_edges_from([ (u,v, d['skill2_bin1_sum']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='skill2_bin1_sum')
		G2.add_weighted_edges_from([ (u,v, d['skill2_bin5_sum']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='skill2_bin5_sum')
		G2.add_weighted_edges_from([ (u,v, d['pl_pl_sum']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='pl_pl_sum')
		G2.add_weighted_edges_from([ (u,v, d['skill1_bin1_mu']) for u,v, d in G.edges(nbunch=listgml,data=True)],weight='skill1_bin1_mu')


		for n in listgml :
			G2.node[n]['label'] = str(G.node[n]['label'])
			G2.node[n]['indegree'] = float(G.node[n]['indegree'])
			G2.node[n]['instrength_matches'] = float(G.node[n]['instrength_matches'])

		outgml = 'agg_networks_'+str(season)+'.gml'

		G2 = nx_old.write_gml(G2, destdir+str(outgml))



def create_neutral_edgelist_network_sports_agg(f1, gmlr, gmlw) :

	data1 = open(f1, 'r')

	# G = nx.DiGraph()
	G = nx.read_gml(gmlr)

	edgelist_pl_coach = defaultdict(list); edgelist_pl_pl = defaultdict(list); 


	for line in data1.readlines()[1:] :
		line = line.strip().split('|')

		try :
			seasonyear = str(line[0])
			matchid = str(line[1])

			team1 = str(line[2]); score1 = int(line[3])
			team2 = str(line[4]); score2 = int(line[5])

			plcoach = float(line[6])
			plpl = float(line[7])

			node1 = team1+'__'+seasonyear
			node2 = team2+'__'+seasonyear
			# if int(seasonyear) == int(season) :

			if score2 > score1:

					edgelist_pl_coach[(node1, node2)].append(plcoach)
					edgelist_pl_pl[(node1, node2)].append( plpl)

			if score1 > score2:

					edgelist_pl_coach[(node2, node1)].append(plcoach)
					edgelist_pl_pl[(node2, node1)].append(plpl)


		except ValueError:
			continue
	print(edgelist_pl_pl)

	mu_edges_pl_coach = []; mu_edges_pl_pl = []; 
	sum_edges_pl_coach = []; sum_edges_pl_pl = []; 


	for keys in sorted(edgelist_pl_coach.keys()) :
			mu_edges_pl_coach.append((keys[0], keys[1], np.mean(edgelist_pl_coach[keys])))
			sum_edges_pl_coach.append((keys[0], keys[1], np.sum(edgelist_pl_coach[keys])))

	for keys in sorted(edgelist_pl_pl.keys()) :
			mu_edges_pl_pl.append((keys[0], keys[1], np.mean(edgelist_pl_pl[keys]))) 
			sum_edges_pl_pl.append((keys[0], keys[1], np.sum(edgelist_pl_pl[keys]))) 


	G.add_weighted_edges_from(mu_edges_pl_coach,weight="pl_coach_mu_all")
	G.add_weighted_edges_from(mu_edges_pl_pl,weight="pl_pl_mu_all")

	G.add_weighted_edges_from(sum_edges_pl_coach,weight="pl_coach_sum_all")
	G.add_weighted_edges_from(sum_edges_pl_pl,weight="pl_pl_sum_all")

	G.remove_node("LAA__2016")
	edges_to_remove = [(u, v) for u, v, data in G.edges(data=True) if data.get("num_matches_won") is None]
	G.remove_edges_from(edges_to_remove)
	
	G = nx.write_gml(G, str(gmlw))



if __name__ == "__main__" :

	f1 = sys.argv[1]; f2 = sys.argv[2]; f3 = sys.argv[3]

	# create_edgelist_network_sports(f1, f2)
	# create_team_vs_team_sports(f1)
	# create_edgelist_network_sports_agg(f1, f2)

	# get_nodecov_network(f1)
	# create_edgelist_network_sports_agg_yearly(f1, f2)
	create_neutral_edgelist_network_sports_agg(f1, f2, f3)

