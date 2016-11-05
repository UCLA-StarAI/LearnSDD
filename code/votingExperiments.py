import sys, threading, time, math, random, os
from timeout_subprocess import run_with_timeout

nb_people = 453
threshold = 0.5
nb_need_to_pass = int(math.ceil(nb_people*threshold))

yes=0
no=1
nv=2
nb_values=3

nbvars = nb_people*nb_values


yes_vars = range(yes+1,nbvars+1, nb_values)

#params is the number of people that we do not have evidence for
exp_name=[p for p in range(1,101)]
params = [int(p*nb_people/100) for p in range(1,101)]

def run_experiment(executeQuery, outpath, data, timeout):
  with open(outpath, 'a+') as outfile:
    for i in range(len(params)):
      param = params[i]
      print param
      exp = exp_name[i]
      ll = 0.0
      tot = 0.0
      count = 0.0
      time = 0.0
      
      
      i = 0
      timedout = False
      
      for example in data:
	if not timedout:
	  #print 'example'
	  
	  weight, instantiation, yes_values, example_answer = example
	  threshold = max(nb_need_to_pass-sum(yes_values[:nb_people-param]),0)
	  evidence = get_evidence_vars(param, instantiation)
	  
	  res  = executeQuery(param, threshold, evidence)
	  modelprob = res[0]
	  t = res[1]
	  
	  if math.isnan(modelprob):
	    timedout=True
	  try:
	    dll = weight*math.log(1-abs(example_answer-modelprob))
	  except:
	    print "PROBLEM", weight, example_answer, modelprob, threshold
	  
	  ll+=dll
	  time += t
	  tot += weight
	  count +=1
	  
	  print param, i,threshold,example_answer,modelprob,t, dll, ll
	  i+=1
	        
      print ll, tot, time, count
      
      if time/count<=timeout and not timedout:
	outfile.write(str(exp)+','+str(param)+','+str(ll/tot)+','+str(time/count)+'\n')
	outfile.flush()  

  
def get_evidence_vars(param, example):
  
  return [i+1 if example[i]==1 else -(i+1) for i in range((nb_people-param)*nb_values)]
  
def executeQuerySDD(sddpath, vtreepath, weightspath,param, threshold, evidence, timeout, fname,):
  from SDDquery import querySDD
  from sddQueryMaker import sum_min
  start = time.time()
  
  yvars = yes_vars[nb_people-param:]
  
  query = sum_min(yvars, threshold)
  mid = time.time()
  
  q_info = run_with_timeout(querySDD, (sddpath,vtreepath,weightspath,query, fname,evidence), timeout,  {'t_total':timeout-(mid-start)})
  end = time.time()
  
  probability, modelsize, querysize, qmodelsize, Tconj, Twmc_m, Twmc_qm,Tparse, Tev,Tmin,modelevsize = q_info.get('prob',float('nan')),q_info.get('size_m',float('nan')),q_info.get('size_q',float('nan')),q_info.get('size_qm',float('nan')),q_info.get('t_conj',float('nan')),q_info.get('t_wmc_m',float('nan')),q_info.get('t_wmc_qm',float('nan')),q_info.get('t_query_parse',float('nan')),q_info.get('t_ev',float('nan')),q_info.get('t_min',float('nan')),q_info.get('size_me',float('nan'))
  
  
  return probability, end-start,mid-start, end-mid, Tparse, Tev,Tmin, Tconj, Twmc_m,Twmc_qm, len(query), modelsize,modelevsize,querysize, qmodelsize

      
def executeQueryAC(modelpath, param, nbvars, threshold, evidence, timeout, fname,):
  from ACquery import queryAC
  from acQueryMaker import sum_min
  start = time.time()
  
  yvars = yes_vars[nb_people-param:]
  
  query = sum_min(yvars, threshold)
  mid = time.time()
  
  probability, nbClauses , makefile_time, ac_time = run_with_timeout(queryAC, (modelpath, query, nbvars, fname,evidence), timeout, (float('nan'),float('nan'),float('nan'),float('nan')))
  end = time.time()
  
  return probability, end-start,mid-start, end-mid,makefile_time, ac_time, nbClauses, nbClauses

def main():
  
  import argparse
  
  parser = argparse.ArgumentParser(description='Run query experiment')
  parser.add_argument('modeltype', choices=['ac', 'sdd'])
  parser.add_argument('modelpath',type=str)
  parser.add_argument('modelname',type=str)
  parser.add_argument('outpath',type=str)
  parser.add_argument('timeout', type=int)
  parser.add_argument('datapath', type=str)
  
  args = vars(parser.parse_args())
  
  modeltype = args['modeltype']
  modelpath = args['modelpath']
  modelname = args['modelname']
  outpath = args['outpath']
  timeout = args['timeout']
  datapath = args['datapath']
  
  indiv_timeout = 10*timeout
  
  if 'sdd' in modeltype:
    
    if modelpath[-1]!='/':
      modelpath+='/'
  
    sddpath = modelpath+'model_'+modelname+'.sdd'
    vtreepath = modelpath+'vtree_'+modelname+'.vtree'
    weightspath = modelpath+'weights_'+modelname+'.csv'
    
    executeQuery = lambda param, threshold, evidence: executeQuerySDD(sddpath, vtreepath, weightspath, param, threshold, evidence, indiv_timeout, outpath)
    with open(outpath, 'w+') as outfile:
      outfile.write('experiment,param,LL,T\n')
      
    
  elif 'ac' in modeltype:    
    executeQuery = lambda param, threshold, evidence: executeQueryAC(modelpath, param, nbvars, threshold, evidence, indiv_timeout,outpath)
    with open(outpath, 'w+') as outfile:
      outfile.write('experiment, param,LL,T\n')
  
  data = []
  with open(datapath) as datafile:
    for line in datafile.readlines():
      w,d = line.split('|')
      weight = float(w)
      instantiation = [int(a) for a in d.split(',')]
      yes_values = [instantiation[i] for i in range(len(instantiation)) if i%nb_values==yes]
      answer = 1.0 if sum(yes_values)>=nb_need_to_pass else 0.0
      data.append((weight, instantiation, yes_values, answer))
  
  run_experiment(executeQuery, outpath, data, timeout)
  

 
  
if __name__ == "__main__":
  main()
