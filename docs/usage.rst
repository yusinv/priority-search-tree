=====
Usage
=====

To use priority-search-tree in a project::

	import priority_search_tree

	# create empty PST
	pst = PrioritySearchTree()

	# add items into PST
	pst[1] = 1
	pst[2] = 2

	# remove item from PST
	del pst[1]

	# query
	MIN_KEY = 1
	MAX_KEY = 3
	BOTTOM_PRIORITY = 2
	result = pst.query(MIN_KEY,MAX_KEY,BOTTOM_PRIORITY)
