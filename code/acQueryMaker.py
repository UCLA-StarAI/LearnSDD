import sys

# PARITY

def even(literals):
  for x in sum_modulo(literals,2,0):
    yield x

# SUM
def sum_matches(literals, possible_sums):
  dnf = []
  for k in possible_sums:
    for x in k_sublists(literals,k):
      yield x

def sum_max(literals, maxsum):
  return sum_matches(literals, range(0,maxsum+1))

def sum_min(literals, minsum):
  return sum_matches(literals, range(minsum,len(literals)+1))

def sum_modulo(literals, divisor, remainder):
  for x in sum_matches(literals, range(remainder,len(literals)+1,divisor)):
    yield x

def sum_between(literals, minsum, maxsum):
  return sum_matches(literals, range(minsum,maxsum+1))


# WEIGHTED SUM

def weighted_sum_operation(literals, weights, operation):
  for powerset_element in powerset(range(len(literals))):
    if operation(reduce(lambda x,y:x+weights[y],powerset_element,0)):
      yield [(literals[i] if i in powerset_element else -literals[i]) for i in range(len(literals))]

def weighted_sum_max(literals, weights, maxsum):  
  return weighted_sum_operation(literals, weights, lambda x: x<=maxsum)

def weighted_sum_min(literals, weights, minsum):
  return weighted_sum_operation(literals, weights, lambda x: x>=minsum)

def weighted_sum_modulo(literals, weights, divisor, remainder):
  return weighted_sum_operation(literals, weights, lambda x: x%divisor==remainder)

def weighted_sum_between(literals, weights, minsum, maxsum):
  return weighted_sum_operation(literals, weights, lambda x: x>=minsum and x<=maxsum)

def weighted_sum_matches(literals, weights, sums):
  return weighted_sum_operation(literals, weights, lambda x: x in sums)



# GROUP COMPARISON
# TODO
# special case: groups should be able to contain the same variables => remove conflicting cases


def greater_than_no_overlap(group1,group2):
  for size1 in range(1, len(group1)+1):
    for size2 in range(size1):
      for x1 in k_sublists(group1,size1):
	for x2 in k_sublists(group2,size2):
	  yield x1+x2
	  
	  
def conj(literals):
  return [literals]

def ordered_ascending(groups):
  pass

def ordered_strict_ascending(groups):
  pass

def equal_groups(groups):
  pass




# HELPERS

def k_subsets_i(n, k):
    '''
    Yield each subset of size k from the set of intergers 0 .. n - 1
    n -- an integer > 0
    k -- an integer > 0
    '''
    # Validate args
    if n < 0:
        raise ValueError('n must be > 0, got n=%d' % n)
    if k < 0:
        raise ValueError('k must be > 0, got k=%d' % k)
    # check base cases
    if k == 0 or n < k:
        yield set()
    elif n == k:
        yield set(range(n))

    else:
        # Use recursive formula based on binomial coeffecients:
        # choose(n, k) = choose(n - 1, k - 1) + choose(n - 1, k)
        for s in k_subsets_i(n - 1, k - 1):
            s.add(n - 1)
            yield s
        for s in k_subsets_i(n - 1, k):
            yield s

def k_sublists(lst, k):
  n = len(lst)
  for k_set in k_subsets_i(n, k):
    yield [(lst[i] if i in k_set else -lst[i]) for i in range(len(lst))]



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
