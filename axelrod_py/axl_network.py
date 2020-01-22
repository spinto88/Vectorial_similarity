import os
import ctypes as C
import networkx as nx
import random as rand
import numpy as np
from axl_agent import *

libc = C.CDLL(os.getcwd() + '/axelrod_py/libc.so')

class Axl_network(nx.Graph, C.Structure):

    """
    Axelrod network: it has nagents axelrod agents, and an amount of noise in the dynamics of the system. This class inherites from the networkx.Graph the way to be described.
    """
    _fields_ = [('nagents', C.c_int),
                ('agent', C.POINTER(Axl_agent)),
		('f', C.c_int),
		('a', C.POINTER(C.POINTER(C.c_int))),
		('corr', C.POINTER(C.POINTER(C.POINTER(C.c_int)))),
		('seed', C.c_int)]

    def __init__(self, n, f, q, topology = 'lattice', **kwargs):
        
	"""
        Constructor: initializes the network.Graph first, and set the topology and the agents' states. 
	"""
        # Init graph properties
        nx.Graph.__init__(self)
        nx.empty_graph(n, self)
        self.nagents = n

        # Init agents' states
        self.init_agents(f, q)
 
        # Init topology
        self.set_topology(topology, **kwargs)

	# Random seed 
	self.seed = rand.randint(0, 10**7)


    def set_topology(self, topology, **kwargs):
        """
        Set the network's topology
        """
        import set_topology as setop

        self.id_topology = topology

        self.adjm = setop.set_topology(self, topology, **kwargs).toarray()

        self.a = (self.nagents * C.POINTER(C.c_int))()
        for i in range(self.nagents):
            self.a[i] = ((self.nagents) * C.c_int)(*self.adjm[i])

    def init_agents(self, f, q):
        """
        Iniatialize the agents' state.
        """
	from copy import deepcopy

	self.f = f
	self.q = q

        self.agent = (Axl_agent * self.nagents)()
    
        for i in range(self.nagents):
            self.agent[i] = Axl_agent(f, q)

        corr_matrix = np.zeros([self.nagents, self.nagents, f], dtype = np.int)
        for i in range(self.nagents):
            for j in range(i+1, self.nagents):
                corr_matrix[i,j] = self.agent[i].similarity_vector(self.agent[j])
		corr_matrix[j,i] = deepcopy(corr_matrix[i,j])


        self.corr = (self.nagents * C.POINTER(C.POINTER(C.c_int)))()
        for i in range(self.nagents):
            self.corr[i] = (self.nagents * C.POINTER(C.c_int))()
            for j in range(self.nagents):
                self.corr[i][j] = (f * C.c_int)(*corr_matrix[i][j])

     
    def evolution(self, steps = 1):
        """
	Make n steps asynchronius evolutions of the system
        """
	
        libc.evolution_similarity_vectorial.argtypes = [C.POINTER(Axl_network)]
        for step in range(steps):
            libc.evolution_similarity_vectorial(C.byref(self))
	 

    def fragments_size(self, fragment_tau = 0.00):

        final_ad_matrix = np.zeros([self.nagents, self.nagents], dtype = np.int)
        for i in range(self.nagents):
            for j in range(i+1, self.nagents):
                if self.shared_features(i,j) != 0 and self.adjm[i,j] == 1:
                    final_ad_matrix[i,j] = 1

        final_ad_matrix += final_ad_matrix.T
        final_graph = nx.from_numpy_array(final_ad_matrix)
        fragments = [len(x) for x in list(nx.connected_components(final_graph))]

        return fragments

    
    def is_there_active_links(self):
	
	libc.is_there_active_links.argtypes = [C.POINTER(Axl_network)]
	libc.is_there_active_links.restype = C.c_int

	return libc.is_there_active_links(C.byref(self))

    def evol2convergence(self):

	steps = 0
	while(self.is_there_active_links() != 0):
	   self.evolution(100)
	   steps += 100
	return steps

    def shared_features(self, i, j):

        libc.shared_features.argtypes = [C.POINTER(Axl_network), C.c_int, C.c_int]
	libc.shared_features.restype = C.c_int

	return libc.shared_features(C.byref(self),i,j)

    """
    def mean_similarity(self):

        corr_matrix = self.get_corr_matrix()
	return np.mean(corr_matrix - np.diag(np.ones(corr_matrix.shape[0])))
   
    def fraction_of_zeros(self):
        pass
    """
    def check_triangle_inequality(self):

        for i in range(self.nagents):
            for j in range(i+1, self.nagents):
                for k in range(j+1, self.nagents):
                    if (self.shared_features(i,j) + self.f < self.shared_features(i,k) + self.shared_features(j,k)):
#			return (i,j,k),(self.corr[i][j], self.corr[i][k], self.corr[j][k])
			return 0
		    if (self.shared_features(i,j) + np.abs(self.shared_features(i,k) - self.shared_features(j,k)) > self.f):
#			return (i,j,k),(self.corr[i][j], self.corr[i][k], self.corr[j][k])
			return 0
	return 1

    
    def save_fragments_distribution(self, fname):
	 
        fragment_sizes = [d for d in self.fragments_size()]

        fp = open(fname, 'a')
        fp.write('{},{},'.format(self.f, self.q))
        fp.write(', '.join([str(s) for s in fragment_sizes]))
        fp.write('\n')
        fp.close() 
