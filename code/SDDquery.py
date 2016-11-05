import subprocess, os, random, sys

sddBinary = 'sddQuery'

def to_file(formula, path):
  with open(path,'w+') as f:
    f.write(str(len(formula))+'\n')
    for line in formula:
      f.write(line+'\n')
      
      
def to_ev_file(evidence, path):
  with open(path,'w+') as f:
    if isinstance(evidence,list):
      f.write(str(len(evidence))+'\n')
      for lit in evidence:
	f.write(str(lit)+'\n')
    else:
      f.write('0\n')


def to_dict(string):
  dictionary = {}
  for line in string.split('\n'):
    try:
      key,val = [a.replace(' ','') for a in line.split(':')]
      if key[0:2]=="t_" or key[0:2]=="pr":
	val = float(val)
      elif "size" in key:
	val = int(val)
      dictionary[key]=val
    except:
      pass
  return dictionary
      
      
def querySDD(sddpath, vtreepath, weightspath, query, fname ='s', evidence = None):
  
  rando = str(random.randint(0,10000000000))
  querypath = fname+rando
  evidence_path = fname+'_e_'+rando
  to_file(query,querypath)      
  to_ev_file(evidence,evidence_path)
  
  out = to_dict(str(subprocess.check_output([sddBinary,'gen',sddpath,vtreepath,weightspath,querypath,evidence_path])))
  
  os.remove(querypath)
  os.remove(evidence_path)
  
  return out

def querySDD_dnf(sddpath, vtreepath, weightspath, query, fname ='s',evidence = None):
  #print query
  
  rando = str(random.randint(0,10000000000))
  querypath = fname+rando
  evidence_path = fname+'_e_'+rando
  #print 'querypath',querypath
  with open(querypath,'w+') as f:
    for clause in query:
      f.write(','.join([str(a) for a in clause])+';')
      
  
  out = to_dict(str(subprocess.check_output([sddBinary,'dnf',sddpath,vtreepath,weightspath,querypath,evidence_path])))
  
  os.remove(querypath)
  os.remove(evidence_path)
  
  return out

    
def querySDD_conj(sddpath, vtreepath, weightspath, query, fname ='s', evidence = None):
  
  rando = str(random.randint(0,10000000000))
  querypath = fname+rando
  evidence_path = fname+'_e_'+rando
  to_ev_file(query,querypath)      
  to_ev_file(evidence,evidence_path)
  
  out = to_dict(str(subprocess.check_output([sddBinary,'conj',sddpath,vtreepath,weightspath,querypath,evidence_path])))
  
  os.remove(querypath)
  os.remove(evidence_path)
  
  return out

