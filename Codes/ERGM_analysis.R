library("purrr")
library(latentnet)
library(ergm)
library(sna)
library(statnet)
library("igraph")
library(network)
library(latticeExtra)
library("broom")
library(ergMargins)
library(flexmix)

rm(list=ls())


# setwd("/Users/satyammukherjee/satyam.mukherjee@snu.edu.in - Google Drive/My Drive/ResearchWorks/ProjectsResearch/CoachPlayerPriorSharedSuccess/Data/data_for_analysis/data_networks/Bundesliga/")
#setwd("G:/.shortcut-targets-by-id/17SduF5VCeXjT8gSD3IY1ipK14Eq8daN3/ProjectsResearch/CoachPlayerPriorSharedSuccess/Data/data_for_analysis/data_networks/NBA/")
#setwd("E:/Dropbox/Research/ProjectResearch/CoachPlayerPriorSharedSuccess/Data/data_networks/EPL/")
#graph_list<-read_graph('agg_networks_revision_2012_2019.gml',format=c("gml"))
#summary(graph_list)

args<-commandArgs(trailingOnly = TRUE)
dirwd <- args[1]
setwd(dirwd)

f <- args[2]
print(f)
graph_list<-read_graph(f,format=c("gml"))
summary(graph_list)

###create the team loss-->win network
el1 <-cbind(as_edgelist(graph_list))
g<-graph_from_data_frame(el1, directed = TRUE)
gmat<-as_adjacency_matrix(g,sparse = FALSE)
network_unw<-network(gmat,directed=TRUE, vertex.attr=vertex.attributes(graph_list))
class(network_unw)
options(tibble.print_max = Inf)

Nmat<-vcount(g)


### total weights 

el_w0<-cbind(as_edgelist(graph_list))
g0<-graph_from_data_frame(el_w0, directed = TRUE)
gmat0<-matrix(0,Nmat,Nmat)
gmat0[el_w0]<-E(graph_list)$diff_score_sum

el_w1<-cbind(as_edgelist(graph_list))
g1<-graph_from_data_frame(el_w1, directed = TRUE)
gmat1<-matrix(0,Nmat,Nmat)
gmat1[el_w1]<-E(graph_list)$pl_coach_sum_all

el_w2<-cbind(as_edgelist(graph_list))
g2<-graph_from_data_frame(el_w2, directed = TRUE)
gmat2<-matrix(0,Nmat,Nmat)
gmat2[el_w2]<-E(graph_list)$pl_pl_sum_all

el_w3<-cbind(as_edgelist(graph_list))
g3<-graph_from_data_frame(el_w3, directed = TRUE)
gmat3<-matrix(0,Nmat,Nmat)
gmat3[el_w3]<- E(graph_list)$skill1_bin5_sum 

el_w4<-cbind(as_edgelist(graph_list))
g4<-graph_from_data_frame(el_w4, directed = TRUE)
gmat4<-matrix(0,Nmat,Nmat)
gmat4[el_w4]<-E(graph_list)$skill2_bin5_sum

set.seed(21093)
model.02b <- ergm(network_unw ~ istar(1) + edgecov(gmat3) + edgecov(gmat4) , estimate = "MLE",  control=control.ergm(MCMC.burnin = 1000, MCMC.samplesize = 2000, MCMLE.maxit= 25)) ## endogenous+controls
summary(model.02b)
tidy(model.02b, exponentiate = FALSE, conf.int = TRUE, conf.level = 0.95)

set.seed(21093)
model.02c <- ergm(network_unw ~ istar(1)  + edgecov(gmat3) + edgecov(gmat4) + edgecov(gmat1), estimate = "MLE", control=control.ergm(MCMC.burnin = 1000, MCMC.samplesize = 2000, MCMLE.maxit= 25)) ### endogenous + controls + IV
summary(model.02c)
tidy(model.02c, exponentiate = FALSE, conf.int = TRUE, conf.level = 0.95)

set.seed(21093)
model.02d <- ergm(network_unw ~ istar(1)  + edgecov(gmat3) + edgecov(gmat4) + edgecov(gmat2), estimate = "MLE",  control=control.ergm(MCMC.burnin = 1000, MCMC.samplesize = 2000, MCMLE.maxit= 25)) ### endogenous + controls + IV
summary(model.02d)
tidy(model.02d, exponentiate = FALSE, conf.int = TRUE, conf.level = 0.95)

set.seed(21093)
model.02e <- ergm(network_unw ~  istar(1)  + edgecov(gmat3) + edgecov(gmat4) + edgecov(gmat2) + edgecov(gmat1), estimate = "MLE", control=control.ergm(MCMC.burnin = 1000, MCMC.samplesize = 2000, MCMLE.maxit= 25)) ### endogenous + controls + IV
summary(model.02e)
tidy(model.02e, exponentiate = FALSE, conf.int = TRUE, conf.level = 0.95)

#Mediation Analysis
set.seed(21093)
model.02f7 <- ergm(network_unw ~ istar(1) + edgecov(gmat3) + edgecov(gmat4) + edgecov(gmat1), estimate = "MLE", control=control.ergm(MCMC.burnin = 1000, MCMC.samplesize = 2000, MCMLE.maxit= 25)) ### endogenous + controls + IV

set.seed(21093)
model.02f8 <- ergm(network_unw ~ istar(1) + edgecov(gmat3) + edgecov(gmat4) + edgecov(gmat2) + edgecov(gmat1), estimate = "MLE", control=control.ergm(MCMC.burnin = 1000, MCMC.samplesize = 2000, MCMLE.maxit= 25)) ### endogenous + controls + IV
ergm.mma(model.02f7,model.02f8,mediator="edgecov(gmat2)", direct.effect="edgecov.gmat1")



#Mediation Analysis

#set.seed(21093)
#model.02f7 <- ergm(network_unw ~ edges + nodeicov('instrength_matches') + edgecov(gmat3) + edgecov(gmat4) + edgecov(gmat1), estimate = "MLE", control=control.ergm(MCMC.samplesize = 1000, MCMLE.maxit= 25)) ### endogenous + controls + IV
#set.seed(21093)
#model.02f8 <- ergm(network_unw ~ edges + nodeicov('instrength_matches') + edgecov(gmat3) + edgecov(gmat4) + edgecov(gmat2) + edgecov(gmat1), estimate = "MLE", control=control.ergm(MCMC.samplesize = 1000, MCMLE.maxit= 25)) ### endogenous + controls + IV
#ergm.mma(model.02f7,model.02f8,mediator="edgecov(gmat2)", direct.effect="nodeicov.instrength_matches")


