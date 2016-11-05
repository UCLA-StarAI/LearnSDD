
def weighted_sum_min(literals, weights, min_s, prev = None,litdic = None, cache = None):
  if prev==None or prev==[]:
    prev = []
    weights,literals = zip(*reversed(sorted(zip(weights,literals))))
    print_prev_at_end = True
    
    litdic = {}
    for literal in literals:
      prev.append('v '+str(literal))#
      litdic[literal]=str(len(prev)-1)
      
    cache = {}
    
  # BASE CASES
  cache_val = cache.get((len(weights), min_s))
  if cache_val!=None:
      if cache_val=='F' or cache_val=='T':
	prev.append(cache_val)
      else:
	prev.append('r '+cache_val)
      return prev
    
  
  if min_s<=0:
    prev.append("T")
    return prev
  
  #if len(literals)==0:
  if sum(weights)<min_s:
    prev.append("F")
    return prev
  
  len_before_with_first = len(prev)
  
  weighted_sum_min(literals[1:], weights[1:], min_s, prev, litdic, cache)
  
  
  #if always possible without biggest weight => always possible. No need to change prev
  if prev[-1]=="T":
    cache[(len(weights)-1,min_s)] = "T"
    return prev
  
  #if never possible without  biggest weight => 
  if prev[-1]=="F":
    cache[(len(weights)-1,min_s)] = "F"
    del prev[-1]
    weighted_sum_min(literals[1:], weights[1:], min_s-weights[0], prev, litdic, cache)
    
    if prev[-1] == "F":
      cache[(len(weights)-1,min_s-weights[0])] = "F"
      return prev
    if prev[-1] =="T":
      cache[(len(weights)-1,min_s-weights[0])] = "T"
      del prev[-1]
      prev.append('r '+litdic[literals[0]])
      return prev
    
    #check if previous line was a repeated one. if so, delete it.
    if prev[-1][0]=='r':
      line_with = prev[-1].split()[1]
      del prev[-1]
    else:
      line_with = str(len(prev)-1)
      cache[(len(weights)-1,min_s-weights[0])] = line_with
    
    # result: literal[0] and correct combinations of other ones
    prev.append('* '+litdic[literals[0]]+' '+line_with)
    return prev
  
  if prev[-1][0]=='r':
    line_without = prev[-1].split()[1]
    del prev[-1]
  else:
    line_without = str(len(prev)-1)
    cache[(len(weights)-1,min_s)] = line_without
    
  
  weighted_sum_min(literals[1:], weights[1:], min_s-weights[0], prev, litdic, cache)
  
  #if prev[-1] =="F": # Not possible because then without biggest weight would also have been false
  
  if prev[-1] == "T":
    cache[(len(weights)-1,min_s-weights[0])] = "T"
    del prev[-1]
    prev.append('+ '+litdic[literals[0]]+' '+line_without)
    return prev
  
  #check if previous line was a repeated one. if so, delete it.
  if prev[-1][0]=='r':
    line_with = prev[-1].split()[1]
    del prev[-1]
  else:
    line_with = str(len(prev)-1)
    cache[(len(weights)-1,min_s-weights[0])] = line_with
  
  prev.append('* '+litdic[literals[0]]+' '+line_with)
  prev.append('+ '+str(len(prev)-1)+' '+line_without)
  return prev
 

def sum_min(literals, min_s):
  
  prev = []
  
  litdic = {}
  for literal in literals:
    prev.append('v '+str(literal))#
    litdic[literal]=str(len(prev)-1)
    
  cache = {}

  return at_least(literals, min_s, prev, litdic, cache)


def at_least(literals, min_s, prev, litdic, cache):
  #return weighted_sum_min(literals, [1]*len(literals),min_s, prev, litdic, cache)
  
  
  
##|====================|
##| #literals >= min+s |
##|====================|

  
  ## BASE CASES
  
  cache_val = cache.get((len(literals),min_s))
  if cache_val!=None:
    if cache_val=='F' or cache_val=='T':
      prev.append(cache_val)
    else:
      prev.append('r '+cache_val)
    return prev
  
  if min_s<=0:
    prev.append("T")
    return prev
  
  if len(literals)<min_s:
    prev.append("F")
    return prev

  
  at_least(literals[1:], min_s, prev, litdic, cache)
  
  #if always possible without first val => always possible. No need to change prev (should be catched as base case)
  if prev[-1]=="T":
    cache[(len(literals)-1,min_s)] = "T"
    return prev
  
  #if never possible without first val => only possible with first val
  if prev[-1]=="F":
    cache[(len(literals)-1,min_s)] = "F"
    del prev[-1]
    
    # with first
    at_least(literals[1:], min_s-1, prev, litdic, cache)
    
    if prev[-1] == "F":
      cache[(len(literals)-1,min_s-1)] = "F"
      return prev
    if prev[-1] =="T":
      cache[(len(literals)-1,min_s-1)] = "T"
      del prev[-1]
      prev.append('r '+litdic[literals[0]])
      return prev
    
    #check if previous line was a repeated one. if so, delete it.
    line_with = check_last_line(prev)
    cache[(len(literals)-1,min_s-1)] = line_with
    
    # result: literal[0] and correct combinations of other ones
    prev.append('* '+litdic[literals[0]]+' '+line_with)
    return prev
  
  #if sometimes possible without first value:
  
  line_without = check_last_line(prev)
  cache[(len(literals)-1,min_s)] = line_without
  
  at_least(literals[1:], min_s-1, prev, litdic, cache)
  
  #always possible with first val: first val or possibilities without first val
  if prev[-1] == "T":
    cache[(len(literals)-1,min_s-1)] = "T"
    del prev[-1]
    prev.append('+ '+litdic[literals[0]]+' '+line_without)
    return prev
  
  #never possible with first val: then it was catched in base case
  
  #sometimes possible with first val:
  line_with = check_last_line(prev)
  cache[(len(literals)-1,min_s-1)] = line_with
  
  prev.append('* '+litdic[literals[0]]+' '+line_with)
  prev.append('+ '+str(len(prev)-1)+' '+line_without)

  return prev

   
def check_last_line(prev):
  """
  take the last line. This is the line number of the last line, unless it was a repeated line (r), then give the original line and remove the last line
  """
  
  if prev[-1][0]=='r':
    last_line = prev[-1].split()[1]
    del prev[-1]
    return last_line
  else:
    return str(len(prev)-1)

def greater_lesser_than_i(i, group1, group2, cache1, cache2, litdic, prev):
  # |group1| >= i
  # |group2| <i
  # |group2'| >=len(group2)-i+1
  # precondition: group2' has the negative literals of the literals in group2. group2' is the one that is given as a parameter
  
  len_before_first_group = len(prev)
  
  at_least(group1, i, prev, litdic, cache1)
  
  if prev[-1]=='F':
    return prev
  elif prev[-1]=='T':
    del prev[-1]
    at_least(group2, len(group2)-i+1, prev, litdic, cache2)
    return prev
  
  else:
    line_group1 = check_last_line(prev)
    len_before_second_group = len(prev)
    at_least(group2, len(group2)-i+1, prev, litdic, cache2)
    if prev[-1]=='F':
      while len(prev)>len_before_first_group:
	del prev[-1]
      prev.append('F')
      return prev
    
    elif prev[-1]=='T':
      while len(prev)>len_before_second_group:
	del prev[-1]
      return prev
    
    else:
      line_group2 = check_last_line(prev)
      prev.append('* '+line_group1+' '+line_group2)
      return prev

def greater_than_no_overlap(group1,group2):
  
  cache1 = {}
  cache2 = {}
  prev = []
  litdic = {}
  
  group2 = [-lit for lit in group2]
  
  i = 0
  for literal in group1:
    prev.append('v '+str(literal))
    litdic[literal]=str(i)
    i+=1
  for literal in group2:
    prev.append('v '+str(literal))
    litdic[literal]=str(i)
    i+=1
    
  len_empty = len(prev)
      
  
  no_prev = True
  
  for i in range(1,len(group1)+1):
    len_before = len(prev)
    greater_lesser_than_i(i, group1, group2, cache1, cache2, litdic, prev)
    if prev[-1]=='T':
      while len(prev)>len_empty:
	del prev[-1]
      prev.append('T')
      return prev
    
    elif prev[-1]=='F':
      while len(prev)>len_before:
	del prev[-1]
      if no_prev and i==len(group1):
	prev.append('F')
      
    else:
      line_cur = check_last_line(prev)
      if not no_prev:
	prev.append('+ '+line_prev+' '+line_cur)
      no_prev = False
      line_prev=str(len(prev)-1)
      
  return prev


def odd(literals,litdic=None, cache=None, prev=None):
  if prev==None:
    cache = {}
    prev = []
    litdic = {}
    
    i = 0
    for literal in literals:
      prev.append('v '+str(literal))
      litdic[literal]=str(i)
      prev.append('v '+str(-literal))
      litdic[-literal]=str(i+1)
      i+=2
  
  # BASE CASES
  
  cache_val = cache.get((len(literals),'odd'))
  if cache_val!=None:
    if cache_val=='F' or cache_val=='T':
      prev.append(cache_val)
    else:
      prev.append('r '+cache_val)
    return prev
  
  if len(literals)==0:
    prev.append("F")
    return prev
  
  if len(literals)==1:
    prev.append("r "+litdic[literals[0]])
    return prev
  
  odd(literals[1:], litdic, cache,prev)
  without_first = check_last_line(prev)
  cache[(len(literals)-1,'odd')]=without_first
  
  even(literals[1:],  litdic, cache,prev)
  with_first = check_last_line(prev)
  cache[(len(literals)-1,'even')]=with_first
  
  prev.append('* '+litdic[-literals[0]]+' '+without_first)
  prev.append('* '+litdic[literals[0]]+' '+with_first)
  prev.append('+ '+str(len(prev)-2)+' '+str(len(prev)-1))
  
  return prev

      

def even(literals,litdic=None, cache=None, prev=None):
  if prev==None:
    cache = {}
    prev = []
    litdic = {}
    
    i = 0
    for literal in literals:
      prev.append('v '+str(literal))
      litdic[literal]=str(i)
      prev.append('v '+str(-literal))
      litdic[-literal]=str(i+1)
      i+=2
      
    
  # BASE CASES
  
  cache_val = cache.get((len(literals),'even'))
  if cache_val!=None:
    if cache_val=='F' or cache_val=='T':
      prev.append(cache_val)
    else:
      prev.append('r '+cache_val)
    return prev
  
  if len(literals)==0:
    prev.append("T")
    return prev
  
  if len(literals)==1:
    prev.append("r "+litdic[-literals[0]])
    return prev
  
  even(literals[1:], litdic, cache,prev)
  without_first = check_last_line(prev)
  cache[(len(literals)-1,'even')]=without_first
  
  odd(literals[1:], litdic, cache, prev)
  with_first = check_last_line(prev)
  cache[(len(literals)-1,'odd')]=with_first
  
  prev.append('* '+litdic[-literals[0]]+' '+without_first)
  prev.append('* '+litdic[literals[0]]+' '+with_first)
  prev.append('+ '+str(len(prev)-2)+' '+str(len(prev)-1))
  
  return prev


def conj(literals):
  first=True
  prev = []
  for lit in literals:
    prev.append("v "+str(lit))
    if first:
      first=False
    else:
      prev.append("* "+str(len(prev)-2) +" "+str(len(prev)-1))
  return prev
      
    
    
def prettyprint(lst):
  print
  i=0
  for line in lst:
    print i, line
    i+=1
  print
  
def to_file(formula, path):
  with open(path,'w+') as f:
    f.write(str(len(formula))+'\n')
    for line in formula:
      f.write(line+'\n')
      