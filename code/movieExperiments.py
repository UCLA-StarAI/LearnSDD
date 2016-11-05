import sys, threading, time, math, random, os, re


import acQueryMaker, sddQueryMaker

from timeout_subprocess import run_with_timeout


pos_words = [69,87,88,105,80,282,283,285,300,357,358,378,392,413,439,447,451,589,614,631,632,847,875,864,941,6,30,48,153,156,187,8,86,949,361,58,290,220,586,753,532,353,833,981,2,365,902,488,424,319,694,967,747,629,398,860,637,441,528,970,883,208,193,711,65,650,683,462,44,739,895,453,17,731,242,183,670,778,788,918,400,777,565,630,841,230,725,682,882,24,390,271,989,411,803,955,245,649,359,688]
neg_words = [66,72,73,179,238,241,244,313,395,422,484,719,653,842,874,930,157,161,263,769,605,524,713,915,591,965,640,792,62,78,399,551,616,721,699,12,539,738,109,222,324,997,954,754,717,899,448,95,113,321,345,260,444,480,375,162,320,692,581,971,878,76,408,177,945,352,5,314,474,973,402,804,554,341,226,832,927,931,809,592,147,638,287,379,977,877,510,446,663,826,891,344,558,690,476,596,121,64,284,559]


nbvars = 1000
params=range(5,101)
exp_name=params

random.seed(2184632)
weights= [round(random.uniform(0,5),1) for i in range(100)]

threshold = 5

def run_experiment(executeQuery, outpath, reviews,answer_in_example, timeout):
  with open(outpath, 'a+') as outfile:
    for i in range(len(params)):
      param = params[i]
      print param
      exp = exp_name[i]
      ll = 0.0
      count = 0.0
      time = 0.0
      tot = 0.0
      
      i = 0
      
      timedout = False
      for review in reviews:
	if not timedout:
	  #print 'example'
	  example_answer = answer_in_example(review, param)
	  #print 'example answer', example_answer
	  weight = review[0]
	  evidence = review[1]
	  res  = executeQuery(param, evidence)
	  #print res
	  
	  modelprob = res[0]
	  t = res[1]
	  if math.isnan(modelprob):
	    timedout=True
	  try:
	    dll = weight*math.log(1-abs(example_answer-modelprob))
	    ll+=dll
	    time += t
	    tot += weight
	    count +=1
	    print param, i,example_answer,modelprob,t, dll, ll
	  except:
	    print "PROBLEM", weight, example_answer, modelprob
	    
	  
	  
	  i+=1
	
      print ll, tot, time, count
      
      if time/count<=timeout and not timedout:
	outfile.write(str(exp)+','+str(param)+','+str(ll/tot)+','+str(time/count)+'\n')
	outfile.flush()  
      

def to_count_sdd_query(param, count_vars,tr):
  return sddQueryMaker.sum_min(count_vars[0:param], tr)

def to_group_sdd_query(param, group1,group2):
  return sddQueryMaker.greater_than_no_overlap(group1[0:param], group2[0:param])

def to_parity_sdd_query(param):
  return sddQueryMaker.even(range(1,param+1))

def to_conj_sdd_query(param):
  return range(1,param+1)

def to_wthresh_sdd_query(param, weights):
  return sddQueryMaker.weighted_sum_min(range(1,param+1), weights[:param],sum(weights[:param])/2)

        
def to_count_ac_query(param, count_vars,tr):
  return acQueryMaker.sum_min(count_vars[0:param], tr)

def to_group_ac_query(param, group1,group2):
  return acQueryMaker.greater_than_no_overlap(group1[0:param], group2[0:param])

def to_parity_ac_query(param):
  return acQueryMaker.even(range(1,param+1))

def to_conj_ac_query(param):
  return acQueryMaker.conj(range(1,param+1))

def to_wthresh_ac_query(param, weights):
  return acQueryMaker.weighted_sum_min(range(1,param+1), weights[:param],sum(weights[:param])/2)
  

def executeQuerySDD(sddpath, vtreepath, weightspath,queryfun,param, evidence, timeout, fname,):
  from SDDquery import querySDD
  start = time.time()
  query = queryfun(param)
  mid = time.time()
  
  q_info = run_with_timeout(querySDD, (sddpath,vtreepath,weightspath,query,fname,evidence), timeout,  {'t_total':timeout-(mid-start)})
  end = time.time()
  
  probability, modelsize, querysize, qmodelsize, Tconj, Twmc_m, Twmc_qm,Tparse, Tev,Tmin,modelevsize = q_info.get('prob',float('nan')),q_info.get('size_m',float('nan')),q_info.get('size_q',float('nan')),q_info.get('size_qm',float('nan')),q_info.get('t_conj',float('nan')),q_info.get('t_wmc_m',float('nan')),q_info.get('t_wmc_qm',float('nan')),q_info.get('t_query_parse',float('nan')),q_info.get('t_ev',float('nan')),q_info.get('t_min',float('nan')),q_info.get('size_me',float('nan'))
  
  
  return probability, end-start,mid-start, end-mid, Tparse, Tev,Tmin, Tconj, Twmc_m,Twmc_qm, len(query), modelsize,modelevsize,querysize, qmodelsize

def executeConjQuerySDD(sddpath, vtreepath, weightspath,queryfun,param, evidence, timeout, fname,):
  from SDDquery import querySDD_conj as querySDD
  start = time.time()
  query = queryfun(param)
  mid = time.time()
  
  q_info = run_with_timeout(querySDD, (sddpath,vtreepath,weightspath,query,fname,evidence), timeout,  {'t_total':timeout-(mid-start)})
  end = time.time()
  
  #print q_info
  
  probability, modelsize, querysize, qmodelsize, Tconj, Twmc_m, Twmc_qm,Tparse, Tev,Tmin,modelevsize = q_info.get('prob',float('nan')),q_info.get('size_m',float('nan')),q_info.get('size_q',float('nan')),q_info.get('size_qm',float('nan')),q_info.get('t_conj',float('nan')),q_info.get('t_wmc_m',float('nan')),q_info.get('t_wmc_qm',float('nan')),q_info.get('t_query_parse',float('nan')),q_info.get('t_ev',float('nan')),q_info.get('t_min',float('nan')),q_info.get('size_me',float('nan'))
  
  
  return probability, end-start,mid-start, end-mid, Tparse, Tev,Tmin, Tconj, Twmc_m,Twmc_qm, len(query), modelsize,modelevsize,querysize, qmodelsize


      
def executeQueryAC(modelpath, queryfun, param, evidence,nbvars, timeout, fname,):
  from ACquery import queryAC
  start = time.time()
  query = queryfun(param)
  mid = time.time()
  probability, nbClauses , makefile_time, ac_time = run_with_timeout(queryAC, (modelpath, query, nbvars, fname,evidence), timeout, (float('nan'),float('nan'),float('nan'),float('nan')))
  end = time.time()
  return probability, end-start,mid-start, end-mid, makefile_time, ac_time, nbClauses, nbClauses


def main():
  
  import argparse
  
  parser = argparse.ArgumentParser(description='Run query experiment')
  parser.add_argument('modeltype', choices=['ac', 'sdd'])
  parser.add_argument('querytype', choices=['pos', 'neg','group','parity','conj','wthresh',])
  parser.add_argument('modelpath',type=str)
  parser.add_argument('modelname',type=str)
  parser.add_argument('outpath',type=str)
  parser.add_argument('timeout', type=int)
  parser.add_argument('datapath', type=str)
  parser.add_argument('evidencepath', type=str)
  parser.add_argument('-params', type=str)
  parser.add_argument('-cont')
  
  args = vars(parser.parse_args())
  
  modeltype = args['modeltype']
  querytype = args['querytype']
  modelpath = args['modelpath']
  modelname = args['modelname']
  outpath = args['outpath']
  timeout = args['timeout']
  datapath = args['datapath']
  evidencepath = args['evidencepath']
  
  indiv_timeout = 10*timeout
  
  if 'params' in args and args['params'] is not None:
    low,up = args['params'].split(':')
    global params
    params = range(int(low),int(up))
    exp_name=params
  
  
  if 'sdd' in modeltype:
    
    if modelpath[-1]!='/':
      modelpath+='/'
  
    sddpath = modelpath+'model_'+modelname+'.sdd'
    vtreepath = modelpath+'vtree_'+modelname+'.vtree'
    weightspath = modelpath+'weights_'+modelname+'.csv'
    
    queries ={"pos":lambda param: to_count_sdd_query(param,pos_words,threshold),
	      "neg":lambda param: to_count_sdd_query(param,neg_words,threshold),
	      "group":lambda param: to_group_sdd_query(param,pos_words,neg_words),
	      "parity":lambda param: to_parity_sdd_query(param),
	      "conj":lambda param: to_conj_sdd_query(param),
	      "wthresh":lambda param: to_wthresh_sdd_query(param, weights)}
    
    if (querytype=='conj'):
      executeQuery = lambda param, evidence: executeConjQuerySDD(sddpath, vtreepath, weightspath,queries[querytype], param, evidence, indiv_timeout, outpath)
    else :
      executeQuery = lambda param, evidence: executeQuerySDD(sddpath, vtreepath, weightspath,queries[querytype], param, evidence, indiv_timeout, outpath)
      
    
  else:    
    
    queries ={"pos":lambda param: to_count_ac_query(param,pos_words,threshold),
	      "neg":lambda param: to_count_ac_query(param,neg_words,threshold),
	      "group":lambda param: to_group_ac_query(param,pos_words,neg_words),
	      "parity":lambda param: to_parity_ac_query(param),
	      "conj":lambda param: to_conj_ac_query(param),
	      "wthresh":lambda param: to_wthresh_ac_query(param,weights)}
    
    executeQuery = lambda param, evidence: executeQueryAC(modelpath, queries[querytype],param, evidence, nbvars, indiv_timeout, outpath)
    
  
  if  'cont' not in args or args['cont'] not in ["y","1","yes"]:
    with open(outpath, 'w+') as outfile:
      outfile.write('experiment, param,LL,T\n')
  
  reviews = []
  with open(datapath) as datafile:
    with open(evidencepath) as evidencefile:

      dataline = datafile.readline()
      while (dataline):
	evidenceline = evidencefile.readline()
	dw, di = dataline.split('|')
	ew, ei = evidenceline.split('|')
	
	assert (dw==ew)
	
	data = [int(d) for d in di.split(',')]
	evidence = [e for e in ei.split(',')]
	evidence = [i+1 if int(evidence[i])>0 else -i-1  for i in range(len(evidence)) if not '*' in evidence[i]]
	pos = [data[w-1] for w in pos_words]
	neg = [data[w-1] for w in neg_words]
	reviews.append((float(dw), evidence, pos, neg, data[:params[-1]+1]))
	dataline = datafile.readline()
	
      
      
  
  answer_in_example = {	"pos":lambda review, param: 1.0 if (sum(review[2][:param])>=threshold) else 0.0,
			"neg":lambda review, param: 1.0 if (sum(review[3][:param])>=threshold) else 0.0,
			"group":lambda review, param: 1.0 if (sum(review[2][:param])>sum(review[3][:param])) else 0.0,
			"parity":lambda review, param: 1.0 if (sum(review[4][:param])%2==0) else 0.0,
			"conj":lambda review, param: 1.0 if (sum(review[4][:param])==param) else 0.0,
			"wthresh":lambda review, param: 1.0 if sum([review[4][i]*weights[i] for i in range(param)])>=sum(weights[:param])/2 else 0.0,  
			}
  
  print "len(reviews): ", len(reviews)
    
  run_experiment(executeQuery, outpath,reviews, answer_in_example[querytype], timeout)
  
  

 
  
if __name__ == "__main__":
  main()

