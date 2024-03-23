=====
Usage
=====

To use priority-search-tree in a project::

	import priority_search_tree

	# create empty PST
	pst = PrioritySearchTree()

	# add items into PST
	pst.add((1,1))
	pst.add((2,2))

	# remove item from PST
	pst.remove((1,1))

	# query
	MIN_TREE_KEY_ITEM = (1,1)
	MAX_TREE_KEY_ITEM = (3,3)
	BOTTOM_HEAP_ITEM = (2,2)
	result = pst.query(MIN_TREE_KEY_ITEM,MAX_TREE_KEY_ITEM,BOTTOM_HEAP_ITEM)
