#ifndef EVOLUTION_SIMILARITY_VECTORIAL_H
#define EVOLUTION_SIMILARITY_VECTORIAL_H

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "axelrod.h"

int increase_similarity(axl_network *, int, int);
int is_there_active_links(axl_network *);
int shared_features(axl_network *, int, int);

int evolution_similarity_vectorial(axl_network *);

#endif
