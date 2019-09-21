def sequence_match(a, b):
	"""
  	Compare two unique sequences to match variables to each position of the other.
  	>>> sequence_match([1, 2, 3, 4], [1, 7, 3, 4])
 	>>> [1, 3, 4]
  	Arguments:
    	a {list} -- First Sequence
    	b {list} -- Second Sequence
  
  	Returns:
      	list -- List of matches.
  	"""
	m = []
	for i in range(len(a)):
		if a[i] == b[i]:
			m.append(a[i])
	return m