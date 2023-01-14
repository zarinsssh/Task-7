Python 3.10.9 (tags/v3.10.9:1dd9be6, Dec  6 2022, 20:01:21) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> class Node:
...     def __init__(self, val):
...         self.val = val
...         self.left = None
...         self.right = None
... 
... class BST:
...     def __init__(self):
...         self.root = None
... 
...     def insert(self, val):
...         new_node = Node(val)
...         if self.root is None:
...             self.root = new_node
...         else:
...             current = self.root
...             while True:
...                 if val < current.val:
...                     if current.left is None:
...                         current.left = new_node
...                         break
...                     else:
...                         current = current.left
...                 else:
...                     if current.right is None:
...                         current.right = new_node
...                         break
...                     else:
...                         current = current.right
... 
...     def search(self, val):
...         current = self.root
...         while current is not None:
...             if val == current.val:
...                 return True
...             elif val < current.val:
...                 current = current.left
...             else:
...                 current = current.right
