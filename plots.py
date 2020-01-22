import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def read_data(fName):

    fp = open(fName,'r').read().split('\n')
    fp = [f.split(',') for f in fp[:len(fp)-1]]

    nz = [int(f[1]) for f in fp]
    fragments = [[int(g) for g in f[2:]] for f in fp]

    return nz, fragments

def biggest_fragment(fName):

    import numpy as np
    p, fragments = read_data(fName)

    p_range = sorted(list(set(p)))
    bigfrag_p = []

    for p_iter in p_range:
        frag_p = []
        for d in range(len(fragments)):
            if p[d] == p_iter:
                frag_p += [np.max(fragments[d])]

        bigfrag_p.append([p_iter, frag_p])

    return bigfrag_p

def average_fragment(fName):

    import numpy as np

    p, fragments = read_data(fName)

    p_range = sorted(list(set(p)))

    def mean_frag_function(frags):

        if len(frags) >= 1:
          ns = np.bincount(frags)
          s = np.array(range(0,np.max(frags)+1), dtype = np.float)
          ms = ((ns * s)/ns.dot(s)).dot(s)
          return ms
        else:
            return 0.00

    bigfrag_p = []

    for p_iter in p_range:
        frag_p = []
        for d in range(len(fragments)):
            if p[d] == p_iter:
                aux = fragments[d]
                aux.remove(np.max(aux))
                frag_p += aux

        bigfrag_p.append([p_iter, mean_frag_function(frag_p)])

    return bigfrag_p

plt.figure(1, figsize = (4.5,3))
ax = plt.axes([0.175, 0.20, 0.725, 0.75])

color_dict = {400: 'b', 225: 'g', 1024: 'r'}

for N in [400]:#256, 512, 1024]:

  degree = 4

  data = biggest_fragment('Prueba.dat'.format(degree, N))
#  M = 0.5*N*(N-1)

  for b in data:
      plt.scatter([b[0]]*len(b[1]), np.array(b[1], dtype = np.float)/N, s = 20, alpha = 0.05, color = 'k')

  plt.plot([b[0] for b in data], [np.mean(b[1])/N for b in data], color_dict[N] + '-', linewidth = 3, alpha = 0.75, label = '$N = {}$'.format(N))


plt.ylabel(r'$S_{max}$', size = 20)
#plt.xlim([10**-4, 0.5])
plt.ylim([-0.05, 1.05])
plt.xlabel(r'$Q$', size = 25)
ax.xaxis.set_label_coords(1.00, -0.05)
#plt.xscale('log')
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.grid(True, alpha = 0.15)

#plt.legend(loc = 'best', fontsize = 11)
#plt.title(r'Random regular network - $k = 4$', size = 15)
#plt.savefig(r'Biggest_fragment_RG4.png', dpi = 400)
#plt.title(r'Complete network', size = 15)
#plt.savefig(r'Biggest_fragment_RGN.png', dpi = 400)
plt.show()

