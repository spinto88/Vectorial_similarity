from axelrod_py import *

N = 100
F = 10
q = 40

rand.seed(123452)

fz = lambda f, q: (1.00 - 1.00/q)**f
    
mysys = Axl_network(n = N, f = F, q = q, topology = 'lattice', degree = N)

print mysys.corr[0][1][:F]
print mysys.corr[1][0][:F]

#print mysys.shared_features(0,1)
#print mysys.shared_features(1,0)
#print mysys.corr[0][2][:F]

for i in range(1):
    mysys.evolution(1000)
    print mysys.check_triangle_inequality()

print mysys.corr[0][1][:F]
print mysys.corr[1][0][:F]

#print np.max(mysys.fragments_size())

#mysys.evolution(1000)
#mysys.evol2convergence()

#print np.max(mysys.fragments_size())
"""

for q in np.arange(5, 96, 10):

  for i in range(5):

    mysys.re_init_agents(F,q)

    mysys.evol2convergence()

    mysys.save_fragments_distribution("Prueba.dat")

    print q, fz(F,q), np.max(mysys.fragments_size())
"""
