
// NBA


 gen diff_score_win_loss = home_pts - visitor_pts if home_pts > visitor_pts 
 replace diff_score_win_loss = visitor_pts - home_pts if visitor_pts > home_pts 


 gen diff_bpm_win_loss_bin_3 = mean_bpm_t1_bin_3 - mean_bpm_t2_bin_3 if visitor_pts > home_pts 
 replace diff_bpm_win_loss_bin_3 = mean_bpm_t2_bin_3 - mean_bpm_t1_bin_3 if home_pts  > visitor_pts  

  gen diff_bpm_win_loss_bin_5 = mean_bpm_t1_bin_5 - mean_bpm_t2_bin_5 if visitor_pts > home_pts 
  replace diff_bpm_win_loss_bin_5 = mean_bpm_t2_bin_5 - mean_bpm_t1_bin_5 if home_pts  > visitor_pts  

  gen diff_bpm_win_loss_bin_1 = mean_bpm_t1_bin_1 - mean_bpm_t2_bin_1 if visitor_pts > home_pts 
  replace diff_bpm_win_loss_bin_1 = mean_bpm_t2_bin_1 - mean_bpm_t1_bin_1 if home_pts  > visitor_pts  
  
  
  
   gen diff_per_win_loss_bin_3 = mean_per_t1_bin_3 - mean_per_t2_bin_3 if visitor_pts > home_pts 
 replace diff_per_win_loss_bin_3 = mean_per_t2_bin_3 - mean_per_t1_bin_3 if home_pts  > visitor_pts  

  gen diff_per_win_loss_bin_5 = mean_per_t1_bin_5 - mean_per_t2_bin_5 if visitor_pts > home_pts 
  replace diff_per_win_loss_bin_5 = mean_per_t2_bin_5 - mean_per_t1_bin_5 if home_pts  > visitor_pts  

  gen diff_per_win_loss_bin_1 = mean_per_t1_bin_1 - mean_per_t2_bin_1 if visitor_pts > home_pts 
  replace diff_per_win_loss_bin_1 = mean_per_t2_bin_1 - mean_per_t1_bin_1 if home_pts  > visitor_pts  
  
 
 gen diff_pl_pl_suc_win_loss = mu_rel_suc_t1 - mu_rel_suc_t2  if visitor_pts > home_pts
 replace diff_pl_pl_suc_win_loss = mu_rel_suc_t2 - mu_rel_suc_t1  if home_pts  > visitor_pts


 gen diff_pl_coach_suc_win_loss = mu_coach_player_suc_t1  - mu_coach_player_suc_t2   if visitor_pts > home_pts
 replace diff_pl_coach_suc_win_loss = mu_coach_player_suc_t2  - mu_coach_player_suc_t1   if home_pts  > visitor_pts


 gen diff_pl_pl_all_win_loss = mu_rel_all_t1  - mu_rel_all_t2  if visitor_pts > home_pts
 replace diff_pl_pl_all_win_loss = mu_rel_all_t2 - mu_rel_all_t1  if home_pts  > visitor_pts

 gen diff_pl_coach_all_win_loss = mu_coach_player_all_t1  - mu_coach_player_all_t2   if visitor_pts > home_pts
 replace diff_pl_coach_all_win_loss = mu_coach_player_all_t2  - mu_coach_player_all_t1   if home_pts  > visitor_pts


 
xi: nbreg diff_score_win_loss diff_bpm_win_loss_bin_3 diff_per_win_loss_bin_3   i.visitor_name i.home_name i.seasonyear, robust
estat ic

xi: nbreg diff_score_win_loss diff_bpm_win_loss_bin_3 diff_per_win_loss_bin_3 diff_pl_pl_suc_win_loss   i.visitor_name i.home_name i.seasonyear, robust
estat ic

xi: nbreg diff_score_win_loss diff_bpm_win_loss_bin_3 diff_per_win_loss_bin_3  diff_pl_coach_suc_win_loss  i.visitor_name i.home_name i.seasonyear, robust
estat ic

xi: nbreg diff_score_win_loss diff_bpm_win_loss_bin_3 diff_per_win_loss_bin_3 diff_pl_pl_suc_win_loss diff_pl_coach_suc_win_loss  i.visitor_name i.home_name i.seasonyear, robust
estat ic
	



xi: nbreg diff_score_win_loss diff_bpm_win_loss_bin_3 diff_per_win_loss_bin_3   i.visitor_name i.home_name i.seasonyear, robust
estat ic

xi: nbreg diff_score_win_loss diff_bpm_win_loss_bin_3 diff_per_win_loss_bin_3 diff_pl_pl_all_win_loss   i.visitor_name i.home_name i.seasonyear, robust
estat ic

xi: nbreg diff_score_win_loss diff_bpm_win_loss_bin_3 diff_per_win_loss_bin_3  diff_pl_coach_all_win_loss  i.visitor_name i.home_name i.seasonyear, robust
estat ic

xi: nbreg diff_score_win_loss diff_bpm_win_loss_bin_3 diff_per_win_loss_bin_3 diff_pl_pl_all_win_loss diff_pl_coach_all_win_loss  i.visitor_name i.home_name i.seasonyear, robust
estat ic
	
 
encode visitor_name , gen(visitor_name_id)
encode home_name  , gen(home_name_id)

sgmediation2 diff_score_win_loss, iv(diff_pl_coach_suc_win_loss) mv(diff_pl_pl_suc_win_loss) cv(diff_bpm_win_loss_bin_3 diff_per_win_loss_bin_3   i.visitor_name_id  i.home_name_id  i.seasonyear)

bootstrap r(ind_eff) r(dir_eff) r(tot_eff), reps(1000): sgmediation2 diff_score_win_loss, iv(diff_pl_coach_suc_win_loss) mv(diff_pl_pl_suc_win_loss) cv(diff_bpm_win_loss_bin_3 diff_per_win_loss_bin_3   i.visitor_name_id  i.home_name_id  i.seasonyear)
estat bootstrap, bc percentile

sgmediation2 diff_score_win_loss, iv(diff_pl_coach_all_win_loss) mv(diff_pl_pl_all_win_loss) cv(diff_bpm_win_loss_bin_3 diff_per_win_loss_bin_3   i.visitor_name_id  i.home_name_id  i.seasonyear)

bootstrap r(ind_eff) r(dir_eff) r(tot_eff), reps(1000): sgmediation2 diff_score_win_loss, iv(diff_pl_coach_all_win_loss) mv(diff_pl_pl_all_win_loss) cv(diff_bpm_win_loss_bin_3 diff_per_win_loss_bin_3   i.visitor_name_id  i.home_name_id  i.seasonyear)
estat bootstrap, bc percentile


// MLB
	
gen diff_win_rel_all = mu_rel_all_t1 - mu_rel_all_t2 if visitor_pts < home_pts 
replace diff_win_rel_all = mu_rel_all_t2 - mu_rel_all_t1 if visitor_pts > home_pts 

gen diff_win_coach_player_all = mu_coach_player_all_t1 - mu_coach_player_all_t2 if visitor_pts < home_pts 
replace diff_win_coach_player_all = mu_coach_player_all_t2 - mu_coach_player_all_t1 if visitor_pts > home_pts 

en mean_era_win_bin_1 = mean_era_t1_bin_1 if visitor_pts > home_pts 
replace mean_era_win_bin_1 = mean_era_t2_bin_1 if visitor_pts < home_pts 

gen mean_era_win_bin_3 = mean_era_t1_bin_3 if visitor_pts > home_pts 
replace mean_era_win_bin_3 = mean_era_t2_bin_3 if visitor_pts < home_pts 

gen mean_era_win_bin_5 = mean_era_t1_bin_5 if visitor_pts > home_pts 
replace mean_era_win_bin_5 = mean_era_t2_bin_5 if visitor_pts < home_pts 


gen mean_ops_win_bin_1 = mean_ops_t1_bin_1 if visitor_pts > home_pts 
replace mean_ops_win_bin_1 = mean_ops_t2_bin_1 if visitor_pts < home_pts 

gen mean_ops_win_bin_3 = mean_ops_t1_bin_3 if visitor_pts > home_pts 
replace mean_ops_win_bin_3 = mean_ops_t2_bin_3 if visitor_pts < home_pts 

gen mean_ops_win_bin_5 = mean_ops_t1_bin_5 if visitor_pts > home_pts 
replace mean_ops_win_bin_5 = mean_ops_t2_bin_5 if visitor_pts < home_pts 



xi: nbreg diff_win_pts diff_era_win_loss_bin_3  diff_ops_win_loss_bin_3 i.visitor_name i.home_name i.seasonyear, robust
estat ic

xi: nbreg diff_win_pts diff_era_win_loss_bin_3  diff_ops_win_loss_bin_3 diff_win_rel_suc  i.visitor_name i.home_name i.seasonyear, robust
estat ic

xi: nbreg diff_win_pts diff_era_win_loss_bin_3  diff_ops_win_loss_bin_3 diff_win_coach_player_suc i.visitor_name i.home_name i.seasonyear, robust
estat ic

xi: nbreg diff_win_pts diff_era_win_loss_bin_3  diff_ops_win_loss_bin_3 diff_win_rel_suc diff_win_coach_player_suc i.visitor_name i.home_name i.seasonyear, robust
estat ic


xi: nbreg diff_win_pts diff_era_win_loss_bin_3  diff_ops_win_loss_bin_3 i.visitor_name i.home_name i.seasonyear, robust
estat ic

xi: nbreg diff_win_pts diff_era_win_loss_bin_3  diff_ops_win_loss_bin_3 diff_win_rel_all  i.visitor_name i.home_name i.seasonyear, robust
estat ic

xi: nbreg diff_win_pts diff_era_win_loss_bin_3  diff_ops_win_loss_bin_3 diff_win_coach_player_all i.visitor_name i.home_name i.seasonyear, robust
estat ic

xi: nbreg diff_win_pts diff_era_win_loss_bin_3  diff_ops_win_loss_bin_3 diff_win_rel_all diff_win_coach_player_all i.visitor_name i.home_name i.seasonyear, robust


encode visitor_name , gen(visitor_name_id)

encode home_name  , gen(home_name_id)

sgmediation2 diff_win_pts, iv(diff_win_coach_player_suc) mv(diff_win_rel_suc) cv(diff_era_win_loss_bin_3  diff_ops_win_loss_bin_3   i.visitor_name_id  i.home_name_id  i.seasonyear)

bootstrap r(ind_eff) r(dir_eff) r(tot_eff), reps(1000): sgmediation2 diff_win_pts, iv(diff_win_coach_player_suc) mv(diff_win_rel_suc) cv(diff_era_win_loss_bin_3  diff_ops_win_loss_bin_3   i.visitor_name_id  i.home_name_id  i.seasonyear)  
estat bootstrap, bc percentile


sgmediation2 diff_win_pts, iv(diff_win_coach_player_all) mv(diff_win_rel_all) cv(diff_era_win_loss_bin_3  diff_ops_win_loss_bin_3   i.visitor_name_id  i.home_name_id  i.seasonyear)

bootstrap r(ind_eff) r(dir_eff) r(tot_eff), reps(1000): sgmediation2 diff_win_pts, iv(diff_win_coach_player_all) mv(diff_win_rel_all) cv(diff_era_win_loss_bin_3  diff_ops_win_loss_bin_3   i.visitor_name_id  i.home_name_id  i.seasonyear)  
estat bootstrap, bc percentile



// soccer


 gen diff_score_win_loss = score_home - score_away if score_home > score_away 
 replace diff_score_win_loss = score_away - score_home if score_away > score_home 


 gen diff_goals_win_loss_bin_3 = mean_goals_t2_bin_3 - mean_goals_t1_bin_3 if score_away > score_home 
 replace diff_goals_win_loss_bin_3 = mean_goals_t1_bin_3 - mean_goals_t2_bin_3 if score_home  > score_away  

  gen diff_goals_win_loss_bin_5 = mean_goals_t2_bin_5 - mean_goals_t1_bin_5 if score_away > score_home 
  replace diff_goals_win_loss_bin_5 = mean_goals_t1_bin_5 - mean_goals_t2_bin_5 if score_home  > score_away  

  gen diff_goals_win_loss_bin_1 = mean_goals_t2_bin_1 - mean_goals_t1_bin_1 if score_away > score_home 
  replace diff_goals_win_loss_bin_1 = mean_goals_t1_bin_1 - mean_goals_t2_bin_1 if score_home  > score_away  
  
 
 gen diff_assists_win_loss_bin_3 = mean_assists_t2_bin_3 - mean_assists_t1_bin_3 if score_away > score_home 
 replace diff_assists_win_loss_bin_3 = mean_assists_t1_bin_3 - mean_assists_t2_bin_3 if score_home  > score_away  

  gen diff_assists_win_loss_bin_5 = mean_assists_t2_bin_5 - mean_assists_t1_bin_5 if score_away > score_home 
  replace diff_assists_win_loss_bin_5 = mean_assists_t1_bin_5 - mean_assists_t2_bin_5 if score_home  > score_away  

  gen diff_assists_win_loss_bin_1 = mean_assists_t2_bin_1 - mean_assists_t1_bin_1 if score_away > score_home 
  replace diff_assists_win_loss_bin_1 = mean_assists_t1_bin_1 - mean_assists_t2_bin_1 if score_home  > score_away  
   
 
 gen diff_pl_pl_suc_win_loss = mu_rel_suc_t2 - mu_rel_suc_t1  if score_away > score_home
 replace diff_pl_pl_suc_win_loss = mu_rel_suc_t1 - mu_rel_suc_t2  if score_home  > score_away


 gen diff_pl_coach_suc_win_loss = mu_coach_player_suc_t2  - mu_coach_player_suc_t1   if score_away > score_home
 replace diff_pl_coach_suc_win_loss = mu_coach_player_suc_t1  - mu_coach_player_suc_t2   if score_home  > score_away



 gen diff_pl_pl_all_win_loss = mu_rel_all_t2 - mu_rel_all_t1  if score_away > score_home
 replace diff_pl_pl_all_win_loss = mu_rel_all_t1 - mu_rel_all_t2  if score_home  > score_away


 gen diff_pl_coach_all_win_loss = mu_coach_player_all_t2  - mu_coach_player_all_t1   if score_away > score_home
 replace diff_pl_coach_all_win_loss = mu_coach_player_all_t1  - mu_coach_player_all_t2   if score_home  > score_away
 
 xi: nbreg diff_score_win_loss diff_goals_win_loss_bin_3 diff_assists_win_loss_bin_3   i.team_home_id i.team_away_id i.seasonyear, robust
estat ic

xi: nbreg diff_score_win_loss diff_goals_win_loss_bin_3 diff_assists_win_loss_bin_3 diff_pl_pl_suc_win_loss   i.team_home_id i.team_away_id  i.seasonyear, robust
estat ic

xi: nbreg diff_score_win_loss diff_goals_win_loss_bin_3 diff_assists_win_loss_bin_3  diff_pl_coach_suc_win_loss  i.team_home_id i.team_away_id  i.seasonyear, robust
estat ic

xi: nbreg diff_score_win_loss diff_goals_win_loss_bin_3 diff_assists_win_loss_bin_3  diff_pl_pl_suc_win_loss diff_pl_coach_suc_win_loss  i.team_home_id i.team_away_id  i.seasonyear, robust
estat ic



 xi: nbreg diff_score_win_loss diff_goals_win_loss_bin_3 diff_assists_win_loss_bin_3   i.team_home_id i.team_away_id i.seasonyear, robust
estat ic

xi: nbreg diff_score_win_loss diff_goals_win_loss_bin_3 diff_assists_win_loss_bin_3 diff_pl_pl_all_win_loss   i.team_home_id i.team_away_id  i.seasonyear, robust
estat ic

xi: nbreg diff_score_win_loss diff_goals_win_loss_bin_3 diff_assists_win_loss_bin_3  diff_pl_coach_all_win_loss  i.team_home_id i.team_away_id  i.seasonyear, robust
estat ic

xi: nbreg diff_score_win_loss diff_goals_win_loss_bin_3 diff_assists_win_loss_bin_3  diff_pl_pl_all_win_loss diff_pl_coach_all_win_loss  i.team_home_id i.team_away_id  i.seasonyear, robust
estat ic
 

sgmediation2 diff_score_win_loss, iv(diff_pl_coach_suc_win_loss) mv(diff_pl_pl_suc_win_loss) cv(diff_goals_win_loss_bin_3 diff_assists_win_loss_bin_3   i.team_away_id  i.team_home_id  i.seasonyear)

bootstrap r(ind_eff) r(dir_eff) r(tot_eff), reps(1000): sgmediation2 diff_score_win_loss, iv(diff_pl_coach_suc_win_loss) mv(diff_pl_pl_suc_win_loss) cv(diff_goals_win_loss_bin_3 diff_assists_win_loss_bin_3   i.team_away_id  i.team_home_id  i.seasonyear)  
estat bootstrap, bc percentile


sgmediation2 diff_score_win_loss, iv(diff_pl_coach_all_win_loss) mv(diff_pl_pl_all_win_loss) cv(diff_goals_win_loss_bin_3 diff_assists_win_loss_bin_3   i.team_away_id  i.team_home_id  i.seasonyear)

bootstrap r(ind_eff) r(dir_eff) r(tot_eff), reps(1000): sgmediation2 diff_score_win_loss, iv(diff_pl_coach_all_win_loss) mv(diff_pl_pl_all_win_loss) cv(diff_goals_win_loss_bin_3 diff_assists_win_loss_bin_3   i.team_away_id  i.team_home_id  i.seasonyear)  
estat bootstrap, bc percentile


 	


