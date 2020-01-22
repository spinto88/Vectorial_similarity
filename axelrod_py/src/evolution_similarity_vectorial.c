#include "evolution_similarity_vectorial.h"

int shared_features(axl_network *mysys, int i, int j)
{
	int k;
	int sf = 0;

	for(k = 0; k < mysys->f; k++)
	{
		if(mysys->corr[i][j][k] == 1)
			sf++;
	}

	return sf;
}


int active_condition(axl_network *mysys, int i, int j)
{
        if(mysys->a[i][j] == 1)
        {
                if((shared_features(mysys, i, j) != 0) && (shared_features(mysys, i, j) != mysys->f))
                        return 1;
        }

        return 0;
}

int number_of_active_links(axl_network *mysys)
{
        int i, j;
        int n = mysys->nagents;
        int number_active_links = 0;

        for(i = 0; i < n; i++)
        {
                for(j = 0; j < n; j++)
                {
                        if(active_condition(mysys, i, j))
                                number_active_links++;
                }
        }
        return number_active_links;
}

int is_there_active_links(axl_network *mysys)
{
        int i, j;
        int n = mysys->nagents;

        for(i = 0; i < n; i++)
        {
                for(j = 0; j < n; j++)
                {
                        if(active_condition(mysys, i, j))
                                return 1;
                }
        }
        return 0;
}

int active_links(axl_network *mysys, active_link *list_active_links)
{
        int i, j, k;
        int n = mysys->nagents;

        k = 0;
        for(i = 0; i < n; i++)
        {
                for(j = 0; j < n; j++)
                {
                        if(active_condition(mysys, i, j))
                        {
                                list_active_links[k].source = i;
                                list_active_links[k].target = j;
                                k++;
                        }
                }
        }

        return 1;
}

int evolution_similarity_vectorial(axl_network *mysys)
{
	int i, j, k;
	int step_n = 0;
	int number_active_links = 0;
	active_link *list_active_links;

	srand(mysys->seed);

	number_active_links = number_of_active_links(mysys);
	if(number_active_links == 0)
		return 1;
	else
	{
		list_active_links = (active_link *)malloc(sizeof(active_link) * number_active_links);
		active_links(mysys, list_active_links);
	}
			
	while(step_n < number_active_links)
	{
		k = rand() % number_active_links;
		i = list_active_links[k].source;
		j = list_active_links[k].target;

		if(active_condition(mysys, i, j) == 1)
			increase_similarity(mysys, i, j);

		step_n++;
	}

	free(list_active_links);

        mysys->seed = rand();

	return 1;
}

int increase_similarity(axl_network *mysys, int i, int j)
{
	int k, r, feat2change;
	int n = mysys->nagents;

	srand(mysys->seed);

	r = rand() % mysys->f;
	if(r < shared_features(mysys, i, j))
	{

		r = rand() % mysys->f;
		while(mysys->corr[i][j][r] == 1)
			r = (r+1) % mysys->f;
		feat2change = r;

		mysys->corr[i][j][feat2change] = 1;
		mysys->corr[j][i][feat2change] = mysys->corr[i][j][feat2change];
				
		for(k = 0; k < n; k++)
		{
			if((k!=i) && (k!=j))
			{
				mysys->corr[i][k][feat2change] = mysys->corr[j][k][feat2change];
				mysys->corr[k][i][feat2change] = mysys->corr[i][k][feat2change];
			}
		}

	}	

        mysys->seed = rand();

	return 1;
}

