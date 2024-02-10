#username - complete info
#id1      - complete info 
#name1    - complete info 
#id2      - complete info
#name2    - complete info  



"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 

	@type key: int or None
	@type value: any
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		

	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child (if self is virtual)
	"""
	def get_left(self):
		return self.left




	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child (if self is virtual)
	"""
	def get_right(self):
		return self.right


	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""
	def get_parent(self):
		return self.parent if self.parent is not None else None


	"""returns the key

	@rtype: int or None
	@returns: the key of self, None if the node is virtual
	"""
	def get_key(self):
		return self.key if self.is_real_node() else None


	"""returns the value

	@rtype: any
	@returns: the value of self, None if the node is virtual
	"""
	def get_value(self):
		return self.value if self.is_real_node() else None


	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def get_height(self):
		return self.height if self.is_real_node() else -1

	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def set_left(self, node):
		self.left = node


	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def set_right(self, node):
		self.right = node


	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def set_parent(self, node):
		self.parent = node


	"""sets key

	@type key: int or None
	@param key: key
	"""
	def set_key(self, key):
		self.key = key


	"""sets value

	@type value: any
	@param value: data
	"""
	def set_value(self, value):
		self.value = value


	"""sets the height of the node

	@type h: int
	@param h: the height
	"""
	def set_height(self, h):
		self.height = h

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return not self.key is None



"""
A class implementing the ADT Dictionary, using an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root = None
		# add your fields here

	"""Set a new root

	@type node: AVLNode
	@param node: node to become a new root
	"""
	def _set_root(self, node):
		if node == None or not node.is_real_node():
			self.root = None
		else:
			self.root = node
			node.set_parent(None)

	"""searches for a AVLNode in the dictionary corresponding to the key | O(log(n))

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: the AVLNode corresponding to key or None if key is not found.
	"""
	def search(self, key):
		curr: AVLNode = self.root
		
		if curr is None:
			return None

		while curr.is_real_node():
			curr_key = curr.get_key()
			if key == curr_key:
				return curr
			elif key < curr_key:
				curr = curr.get_left()
			elif key > curr_key:
				curr = curr.get_right()

		return None

	"""inserts val at position i in the dictionary | O(log(n))

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: any
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, key, val):
		curr: AVLNode = self.get_root()

		# "Dictionary is empty" case
		if curr is None:
			# Set up a root
			self.root = AVLNode(key, val)
			self.root.set_height(0)
			self._add_virtual_children(self.root)

			return 0
		
		# Get to the node to fill
		curr_parent = None
		while curr.is_real_node():
			curr_parent = curr
			if key < curr.get_key():
				curr = curr.get_left()
			elif key > curr.get_key():
				curr = curr.get_right()
		
		# Set up a new node
		curr.set_key(key)
		curr.set_value(val)
		curr.set_parent(curr_parent)
		curr.set_height(0)
		self._add_virtual_children(curr)
		
		# Rebalance
		rebalance_actions_number = self._rebalance_from_node_to_root(curr, True)

		return rebalance_actions_number
			
	"""Rebalances the subtree making it AVL tree | O(1)

	@type node: AVLNode
	@param node: root of the subtree
	@type bf: int
	@param bf: current balance factor of a root node
	@type inserting: bool
	@param inserting: are we using this function after insert
	@rtype: tuple
	@returns: parent of the the subtree root and number of rebalancing operation due to AVL rebalancing
	"""
	def _rebalance_subtree(self, node, bf, inserting):
		rebalance_actions_number = 0
		if bf == 2:
			left_child_bf = self._calc_bf(node.get_left())
			if left_child_bf == 1 or (not inserting and left_child_bf == 0):
				# Performing R
				self._right_rotation(node)
				rebalance_actions_number = 1
			else:
				# Performing LR
				self._left_rotation(node.get_left())
				self._right_rotation(node)
				rebalance_actions_number = 2
		else:
			right_child_bf = self._calc_bf(node.get_right())
			if right_child_bf == -1 or (not inserting and right_child_bf == 0):
				# Performing L
				self._left_rotation(node)
				rebalance_actions_number = 1
			else:
				# Performing RL
				self._right_rotation(node.get_right())
				self._left_rotation(node)
				rebalance_actions_number = 2
		
		return (node.get_parent(), rebalance_actions_number)

	"""Perform a left rotation around a given node | O(1)

	@type node: AVLNode
	@param node: pivot node (the one that will go down)
	@rtype: AVLNode
	@returns: second pivot node (the one that will go up)
	"""
	def _left_rotation(self, node):
		x = node
		y = node.get_right()

		y.set_parent(x.get_parent())
		if y.get_parent() is not None:
			if y.get_parent().get_left() == x:
				y.get_parent().set_left(y)
			else:
				y.get_parent().set_right(y)
		x.set_parent(y)
		x.set_right(y.get_left())
		y.get_left().set_parent(x)
		y.set_left(x)

		self._recalc_height(x)
		self._recalc_height(y)

		return y

	"""Perform a right rotation around a given node | O(1)

	@type node: AVLNode
	@param node: pivot node (the one that will go down)
	@rtype: AVLNode
	@returns: second pivot node (the one that will go up)
	"""
	def _right_rotation(self, node: AVLNode):
		x = node
		y = node.get_left()

		y.set_parent(x.get_parent())
		if y.get_parent() is not None:
			if y.get_parent().get_left() == x:
				y.get_parent().set_left(y)
			else:
				y.get_parent().set_right(y)
		x.set_parent(y)
		x.set_left(y.get_right())
		y.get_right().set_parent(x)
		y.set_right(x)

		self._recalc_height(x)
		self._recalc_height(y)

		return y

	"""Recalculate height for a given node | O(1)

	@type node: AVLNode
	@param node: node to calculate height for
	"""
	def _recalc_height(self, node):
		node.set_height(max(node.get_left().get_height(), node.get_right().get_height()) + 1)

	"""Calculate balance factor for a given node | O(1)

	@type node: AVLNode
	@param node: node to calculate bf for
	"""
	def _calc_bf(self, node):
		return node.get_left().get_height() - node.get_right().get_height()

	"""Add default virtual children to a node | O(1)

	@type node: AVLNode
	@param node: parent node to add children to
	"""
	def _add_virtual_children(self, node):
		node.set_left(AVLNode(None, None))
		node.get_left().set_parent(node)
		node.set_right(AVLNode(None, None))
		node.get_right().set_parent(node)



	"""deletes node from the dictionary | O(log(n))

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		rebalance_actions_number = 0

		# Deleting root
		if node == self.get_root() and not node.get_left().is_real_node() and not node.get_right().is_real_node():
			self.root = None
			return 0
		
		# Deleting a childless node
		elif not node.get_left().is_real_node() and not node.get_right().is_real_node():
			rebalance_starting_node = node.get_right()
			self._connect_in_place_of_deleted(node, node.get_right())

		# Deleting a node with only right child
		elif node.get_right().is_real_node() and not node.get_left().is_real_node():
			rebalance_starting_node = node.get_right()
			self._connect_in_place_of_deleted(node, node.get_right())

		# Deleting a node with only left child
		elif node.get_left().is_real_node() and not node.get_right().is_real_node():
			rebalance_starting_node = node.get_left()
			self._connect_in_place_of_deleted(node, node.get_left())

		# Deleting a binary node
		else:
			# If the node is on left from it's parent
			if node.get_parent() is not None and node.get_parent().get_left() == node:
				dummy = node.get_right()
				while dummy.get_left().is_real_node():
					dummy = dummy.get_left()	

				rebalance_starting_node = dummy.get_right()

			# If the node is on right from it's parent
			else:
				dummy = node.get_left()
				while dummy.get_right().is_real_node():
					dummy = dummy.get_right()

				rebalance_starting_node = dummy.get_left()
			
			self.delete(dummy)
			self._replace_node(node, dummy)

		# Rebalance the tree after deletion
		rebalance_actions_number = self._rebalance_from_node_to_root(rebalance_starting_node, False)

		return rebalance_actions_number

	"""Traverse the tree from the given node up to it's root, calculate a balance factor for each node on the path and rebalance in case of need | O(log(n))

	@type starting_node: AVLNode
	@param starting_node: node from the parent of which we will start rebalancing
	@type inserting: bool
	@param inserting: are we using this function after insert
	@rtype: int
	@returns: overall number of rotations needed to rebalance everything
	"""
	def _rebalance_from_node_to_root(self, starting_node, inserting):
		rebalance_actions_number = 0

		asc_parent = starting_node.get_parent()
		while asc_parent is not None:
			previous_height = asc_parent.get_height()
			self._recalc_height(asc_parent)

			asc_parent_bf = asc_parent.get_left().get_height() - asc_parent.get_right().get_height()

			# If asc_parent subtree is AVL and it's height didn't change then the big tree is
			# still AVL, no need to rebalance or recalculate height
			if abs(asc_parent_bf) < 2 and previous_height == asc_parent.get_height():
				return rebalance_actions_number
			
			# If the parent's height changed, but bf is still valid - continue checking
			elif abs(asc_parent_bf) < 2 and previous_height != asc_parent.get_height():
				rebalance_actions_number += 1

			# If balance factor is not valid - rebalance
			elif abs(asc_parent_bf) == 2:
				criminal_node = asc_parent
				result = self._rebalance_subtree(asc_parent, asc_parent_bf, inserting)
				asc_parent = result[0]
				rebalance_actions_number = rebalance_actions_number + result[1]

				if criminal_node == self.get_root():
					self.root = asc_parent

			asc_parent = asc_parent.get_parent()

		return rebalance_actions_number

	"""Change all new_node connections to an old_node ones and disconnect old one | O(1)

	@type old_node: AVLNode
	@param old_node: node to take connections from
	@type new_node: AVLNode
	@param new_node: node to connect
	"""
	def _replace_node(self, old_node, new_node):
		if old_node == self.root:
			self.root = new_node
			
		old_node.get_left().set_parent(new_node)
		old_node.get_right().set_parent(new_node)

		new_node.set_left(old_node.get_left())
		new_node.set_right(old_node.get_right())
		new_node.set_height(old_node.get_height())

		self._connect_in_place_of_deleted(old_node, new_node)

		self._disconnect_node_internally(old_node)

	"""After deletion of a node, connects it's child to it's parent | O(1)

	@type node: AVLNode
	@param node: node that is supposed to be deleted
	@type child: AVLNode
	@param child: node's child to connect to node's parent
	"""
	def _connect_in_place_of_deleted(self, node, child):
		# If node is left child itself
		if node.get_parent() is not None and node.get_parent().get_left() == node:
			node.get_parent().set_left(child)
		# If node is right child itself
		elif node.get_parent() is not None and node.get_parent().get_right() == node:
			node.get_parent().set_right(child)

		child.set_parent(node.get_parent())

		if self.root == node:
			self.root = child

	"""Remove all outgoing connections within the node | O(1)

	@type node: AVLNode
	@param node: target node
	"""
	def _disconnect_node_internally(self, node):
		node.set_right(None)
		node.set_left(None)
		node.set_parent(None)

	"""returns an array representing dictionary | O(n)

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		arr = []

		if self.root == None:
			return arr

		self._avl_to_array_util(arr, self.root)
		return arr

	"""Recursively appends to the given array keys of a subtree which root is a given node | O(n) (n - number of elements in subtree)

	@type arr: list
	@param arr: global list to append elements of avl to
	@type node: AVLNode
	@param node: target node 
	"""
	def _avl_to_array_util(self, arr, node):
		if node.get_left().is_real_node():
			self._avl_to_array_util(arr, node.get_left())

		arr.append((node.get_key(), node.get_value()))

		if node.get_right().is_real_node():
			self._avl_to_array_util(arr, node.get_right())
		

	"""returns the number of items in dictionary | O(n)

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		size = 0

		if self.root == None:
			return -1
		
		size = self._size_util(self.root)
		return size

	"""Recursively gets the size of a subtree which root is a given node | O(n) (n - number of elements in subtree)

	@type node: AVLNode
	@param node: target node 
	"""
	def _size_util(self, node):
		size = 0
		if node.get_left().is_real_node():
			size += self._size_util(node.get_left())

		size += 1

		if node.get_right().is_real_node():
			size += self._size_util(node.get_right())

		return size
	
	"""splits the dictionary at the i'th index | O(log(n))

	@type node: AVLNode
	@pre: node is in self
	@param node: The intended node in the dictionary according to whom we split
	@rtype: list
	@returns: a list [left, right], where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		# Left and right meaning a tree with keys less than a split node key and a tree with keys greater
		left_tree = AVLTree()
		right_tree = AVLTree()
		temp_tree = AVLTree()

		# Add the children of a split node to left and right trees
		left_tree._set_root(node.get_left())
		right_tree._set_root(node.get_right())

		# For each parent of a split node join relevant child subtree to a relevant result tree
		child = node
		curr = node.get_parent()
		while curr is not None:
			child_was_from_left = child.get_key() < child.get_parent().get_key()
			if child_was_from_left:
				temp_tree._set_root(curr.get_right())
				right_tree.join(temp_tree, curr.get_key(), curr.get_value())
			else:
				temp_tree._set_root(curr.get_left())
				left_tree.join(temp_tree, curr.get_key(), curr.get_value())
			
			child = curr
			curr = curr.get_parent()

		# If one of the trees ended up with only virtual nodes - empty it
		if right_tree.get_root() is not None and not right_tree.get_root().is_real_node():
			right_tree._set_root(None)
		if left_tree.get_root() is not None and not left_tree.get_root().is_real_node():
			left_tree._set_root(None)

		return [left_tree, right_tree]

	
	"""joins self with key and another AVLTree | O(height_diff)

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: The key separting self with tree2
	@type val: any 
	@param val: The value attached to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def join(self, tree2, key, val):
		# If tree2 is empty
		if tree2.get_root() is None or not tree2.get_root().is_real_node():
			self.insert(key, val)
			return 0
		# If self is empty and tree2 is not
		elif self.root is None and tree2.get_root() is not None:
			self._set_root(tree2.get_root())
			self.insert(key, val)
			return self.get_root().get_height()
		# If both are not empty - continue

		# Min and max trees meaning by height
		min_tree = self if self.root.get_height() < tree2.get_root().get_height() else tree2
		max_tree = self if self.root.get_height() >= tree2.get_root().get_height() else tree2

		min_tree_height = min_tree.get_root().get_height()
		height_difference = abs(max_tree.get_root().get_height() - min_tree.get_root().get_height())
		min_is_from_left = min_tree.get_root().get_key() < max_tree.get_root().get_key()

		# Find a node from a max_tree that will be connected to the connection node
		curr = max_tree.get_root()
		while curr.is_real_node():
			if curr.get_height() > min_tree_height:
				if min_is_from_left:
					if curr.get_left().is_real_node():
						curr = curr.get_left()
					else:
						break
				else:
					if curr.get_right().is_real_node():
						curr = curr.get_right()
					else:
						break
			else:
				break
		
		# Connect it and it's parent to the connection node (key, val)
		curr_parent = curr.get_parent()
		connection_node = AVLNode(key, val)
		connection_node.set_height(min_tree_height + 1)
		if min_is_from_left:
			connection_node.set_left(min_tree.get_root())
			min_tree.get_root().set_parent(connection_node)
			connection_node.set_right(curr)
			curr.set_parent(connection_node)

			if curr_parent is not None:
				curr_parent.set_left(connection_node)
			else:
				max_tree._set_root(connection_node)
				max_tree._recalc_height(connection_node)
			connection_node.set_parent(curr_parent)
		else:
			connection_node.set_right(min_tree.get_root())
			min_tree.get_root().set_parent(connection_node)
			connection_node.set_left(curr)
			curr.set_parent(connection_node)

			if curr_parent is not None:
				curr_parent.set_right(connection_node)
			else:
				max_tree._set_root(connection_node)
				max_tree._recalc_height(connection_node)
			connection_node.set_parent(curr_parent)

		# If the connection node ended up being the highest then there it is, no need to rebalance
		self.root = max_tree.get_root()
		self._rebalance_from_node_to_root(connection_node, False)
		return height_difference + 1


	"""returns the root of the tree representing the dictionary | O(log(n))

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root
