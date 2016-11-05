import random, math, time, os, sys, subprocess

acquery = "acquery"


def powerset(seq):
    """
    Returns all the subsets of this set. This is a generator.
    """
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item
            
def lenpowerset(l):
    """
    Returns all the subsets of this set. This is a generator.
    """
    if l <= 1:
        yield 1
        yield 0
    else:
        for item in lenpowerset(l-1):
            yield item+1
            yield item
            
def evidence_to_file(evidence,path, nbvars):
  with open(path,'w+') as f:
    ev = ['*']*nbvars
    if isinstance(evidence,list):
      for lit in evidence:
	ev[abs(lit)-1]=('1' if lit>0 else '0')
    
    f.write(','.join(ev)+'\n')


def queryAC(modelpath,query,nbvars,fname='q', evidence = None):
  
  rando = str(random.randint(0,1000000000))
  querypath = fname+rando
  evidence_path = fname+'_e_'+rando
  
  evidence_to_file(evidence,evidence_path,nbvars)
  
  dnfsize = 0
  
  start = time.time()
  if not isinstance(query,str):
    with open(querypath,"w+") as queryfile:
      for clause in query:
	conjquery = to_conj_query(clause,nbvars)
	#print clause,conjquery
	queryfile.write(conjquery+'\n')
	dnfsize+=1
	
    if dnfsize==0:
      os.remove(querypath)
      os.remove(evidence_path)
      return 0.0,0,0.0,0.0
    
  else:
    querypath = query
  filemade_time = time.time()
  
  
  queryres = run_acquery(modelpath,querypath,evidence_path)
  
  ac_time = time.time()
  
  def to_prob(string):
    try:
      return math.exp(float(string.rstrip('\n')))
    except:
      return 0
  
  probs = [to_prob(p) for p in queryres.split()[:dnfsize]]
  #print probs
  probability = sum(probs)
  
  if isinstance(query,list):
    os.remove(querypath)
  os.remove(evidence_path)
  
  return  probability, dnfsize, filemade_time-start, ac_time-filemade_time
  

def to_conj_query(conjunction,nbvars):
  query = ["*"]*nbvars
  for lit in conjunction:
    if lit>0:
      if query[lit-1]=='0':
	return None
      query[lit-1]='1'
    else:
      if query[-lit-1]=='1':
	return None
      query[-lit-1]='0'
  return ",".join(query)

def run_acquery(modelpath,querypath, evidencepath=None):
  if evidencepath==None:
    return subprocess.check_output([acquery, "-m", modelpath, "-q", querypath])
  else:
    return subprocess.check_output([acquery, "-m", modelpath, "-q", querypath, '-ev', evidencepath, '-sameev'])
  