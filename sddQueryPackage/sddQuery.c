#include "sddQuery.h"
#include <unistd.h>

double time_diff(struct timeval start, struct timeval stop){
  return ((double) ((stop.tv_sec*1000000+stop.tv_usec) - (start.tv_sec*1000000+start.tv_usec)))/1000000.0;
}

double sdd_query(SddNode* model, const SddWmc* weights, SddNode* query, const SddLiteral var_count, SddManager* manager, int* evidence, int evidencec){
//   printf("conjoining model with query...\n");
  
  
  struct timeval  t_start,t_ev,t_min, t_conj, t_wmc_qm, t_wmc_m;
  SddSize msize = sdd_size(model);
  
  
  gettimeofday(&t_start, NULL);
  
  int i = 0;
  while (i < evidencec){
    model = sdd_condition(evidence[i], model, manager);
    i++;
  }
  
  i = 0;
  while (i < evidencec){
    query = sdd_condition(evidence[i], query, manager);
    i++;
  }
  
  gettimeofday(&t_ev, NULL);
  
  SddSize mesize = sdd_size(model);
  
  gettimeofday(&t_min, NULL);
  
  SddWmc wmcModel = wmc(model, weights, NULL, var_count, manager);
  gettimeofday(&t_wmc_m, NULL);
  
  
  SddNode* queryModel = sdd_conjoin(model, query, manager);
  gettimeofday(&t_conj, NULL);
  
//   printf("model and query conjoined\n");
  SddWmc wmcQueryModel = wmc(queryModel, weights, NULL, var_count, manager);
  gettimeofday(&t_wmc_qm, NULL);
  
  printf("size_m: %ld\nsize_me: %ld\nsize_q: %ld\nsize_qm: %ld\nt_ev: %lf\nt_min: %lf\nt_conj: %lf\nt_wmc_m: %lf\nt_wmc_qm: %lf\n",msize, mesize,sdd_size(query),sdd_size(queryModel), time_diff(t_start,t_ev),time_diff(t_ev,t_min),time_diff(t_wmc_m,t_conj), time_diff(t_min, t_wmc_m),time_diff(t_conj,t_wmc_qm));
  
  return exp(wmcQueryModel-wmcModel);
}

double timed_sdd_query(double* ttime, SddNode* model, const SddWmc* weights, SddNode* query, const SddLiteral var_count, SddManager* manager, int* evidence, int evidencec){
  time_t start = time(NULL);
  double probability = sdd_query(model, weights, query, var_count, manager, evidence, evidencec);
  time_t stop = time(NULL);
  *ttime = stop-start;
  return probability;
}


double sdd_conj_query(SddNode* model, SddWmc* weights, const SddLiteral var_count, SddManager* manager, int* literals, int litc, int* evidence, int evidencec){
  
  struct timeval  t_start,t_ev,t_min, t_conj, t_wmc_qm, t_wmc_m;
  
  WmcManager* wmc_manager = wmc_manager_new(model, 1, manager);
  SddWmc one  = wmc_one_weight(wmc_manager);
  SddWmc zero  = wmc_zero_weight(wmc_manager);
  wmc_manager_free(wmc_manager);
  
  SddWmc* negweights=(SddWmc*)malloc(sizeof(SddWmc)*(var_count+1));
  for (int i = 0; i<=var_count; i++){
    negweights[i]=one;
  }
  
  SddSize msize = sdd_size(model);  
  
  gettimeofday(&t_start, NULL);  

  gettimeofday(&t_ev, NULL);  
  
  gettimeofday(&t_min, NULL);
  
  for ( int i = 0; i< evidencec; i++){
    int lit = evidence[i];
    int neglit = -lit;
    if (lit>0) {
      negweights[lit]=zero;
    }
    else{
      weights[neglit]=zero;
    }
  }
  
  SddWmc wmcModel = wmc(model, weights, negweights, var_count, manager);
  gettimeofday(&t_wmc_m, NULL);
  
  gettimeofday(&t_conj, NULL);
  
    for ( int i = 0; i< litc; i++){
    int lit = literals[i];
    int neglit = -lit;
    if (lit>0) {
      negweights[lit]=zero;
    }
    else{
      weights[neglit]=zero;
    }
  }
  
  SddWmc wmcQueryModel = wmc(model, weights, negweights, var_count, manager);
  gettimeofday(&t_wmc_qm, NULL);
  
  printf("size_m: %ld\nsize_me: %ld\nsize_q: %ld\nsize_qm: %ld\nt_ev: %lf\nt_min: %lf\nt_conj: %lf\nt_wmc_m: %lf\nt_wmc_qm: %lf\n",msize,msize,0l,msize, time_diff(t_start,t_ev),time_diff(t_ev,t_min),time_diff(t_wmc_m,t_conj), time_diff(t_min, t_wmc_m),time_diff(t_conj,t_wmc_qm));
  
  return exp(wmcQueryModel-wmcModel);
}

double timed_sdd_conj_query(double* ttime, SddNode* model, SddWmc* weights, const SddLiteral var_count, SddManager* manager, int* literals, int litc, int* evidence, int evidencec){
  time_t start = time(NULL);
  double probability = sdd_conj_query(model, weights, var_count, manager, literals, litc, evidence, evidencec);
  time_t stop = time(NULL);
  *ttime = stop-start;
  return probability;
}


SddWmc wmc(SddNode* sdd, const SddWmc* weights, const SddWmc* negweights, const SddLiteral var_count, SddManager* manager){
  
  WmcManager* wmc_manager = wmc_manager_new(sdd, 1, manager);
  int i = 1;
  while (i<=var_count){
    wmc_set_literal_weight(i, weights[i], wmc_manager);
    i++;
  }
  
  
  if (NULL != negweights) {
    i = 1;
    while (i<=var_count){
      wmc_set_literal_weight(-i, negweights[i], wmc_manager);
      i++;
    }
  }
  
  SddWmc modelcount = wmc_propagate(wmc_manager);
  
  wmc_manager_free(wmc_manager);
  return modelcount;
}


SddWmc* weights_read(const char* path, const SddLiteral var_count){
  
  SddWmc* weights = (SddWmc*)malloc(sizeof(SddWmc)*(var_count+1));
  
  FILE * fp;
  SddWmc weight;
  char line[40];

  fp = fopen (path, "rt");  /* open the file for reading */
  /* elapsed.dta is the name of the file */
  /* "rt" means open the file for reading text */

  long i=0;
  while(i<=var_count)
  {
    fgets(line, 40, fp);
      
//     printf("%ld\n",i);
    /* get a line, up to 40 chars from fp.  done if NULL */
    sscanf (line, "%lf", &weight);
    /* convert the string to a long int */
    weights[i] = weight;
//     printf("%ld\n",i);
    
//     printf("%lf\n",weight);
    i++;
  }
  
//   printf ("%ld =?= %ld+1\n",i, var_count);
  
  fclose(fp);
//   printf("check\n");
  
  return weights;
}

SddNode* dnf_parse(const char* query, SddManager* manager){
  SddNode* dnfSdd = sdd_manager_false(manager);
  SddNode* clauseSdd = sdd_manager_true(manager);
  
  FILE* fp = fopen(query, "r");
  
  if (fp == NULL) {
    fprintf(stderr, "Can't open query file!\n");
    exit(1);
  }
  
  char delim;
  
  SddLiteral lit;
  int n;
  
  while (fscanf(fp, "%ld%c%n", &lit, &delim, &n) != EOF) {
      clauseSdd = sdd_conjoin(clauseSdd, sdd_manager_literal(lit,manager),manager);
//       printf("conj %ld\n",lit);
      if ( delim != ',' ){
	dnfSdd = sdd_disjoin(dnfSdd, clauseSdd, manager);
	clauseSdd = sdd_manager_true(manager);
// 	printf("disj\n");
	if ( delim != ';' ){
	  break;
	}
      }
  }
  
  fclose(fp);
  return dnfSdd;
  
}


SddNode* general_parse(const char* query, SddManager* manager){
    
  FILE *fp;
  char str[60];

  /* opening file for reading */
  fp = fopen(query, "r");
  if(fp == NULL) 
  {
    perror("Error opening file");
  }
  
  int nblines;
  fgets (str, 60, fp);
  sscanf(str, "%d", &nblines);
  SddNode* sdds[nblines];
  int i = 0;
  
  int node1, node2;
  
  while( fgets (str, 60, fp)!=NULL ) 
  {
//     printf("%s\n",str);

    if (sscanf(str, "v %d", &node1)!=0){
      sdds[i] = sdd_manager_literal(node1, manager);
//       printf("%d: var %d\n",i, node1);
    }
  
    else if (sscanf(str, "- %d", &node1)!=0){
      sdds[i] = sdd_negate(sdds[node1], manager);
//       printf("%d: neg %d\n",i, node1);
    }	
    else if (sscanf(str, "+ %d %d", &node1, &node2)!=0){
      sdds[i] = sdd_disjoin(sdds[node1],sdds[node2], manager);
//       printf("%d: disj %d %d\n",i,node1, node2);
    }
    else if (sscanf(str, "* %d %d", &node1, &node2)!=0){
      sdds[i] = sdd_conjoin(sdds[node1],sdds[node2], manager);
//       printf("%d: conj %d %d\n",i, node1, node2);
    }
    else if (sscanf(str, "r %d", &node1)!=0){
      sdds[i] = sdds[node1];
//       printf("%d: rep %d\n",i, node1);
    }	
    else if (strcmp(str, "F\n")==0){
      sdds[i] = sdd_manager_false(manager);
    }	
    else if (strcmp(str, "T\n")==0){
      sdds[i] = sdd_manager_true(manager);
//       printf("%d: True\n",i);
    }	
    
    i++;
  }
  fclose(fp);
//   printf("i-1: %d\n",i-1);
  return sdds[i-1];
  
}


int* parse_evidence(const char* evidence_path, int* evidencec){
  FILE *fp;
  char str[60];

  /* opening file for reading */
  fp = fopen(evidence_path, "r");
  if(fp == NULL) 
  {
    perror("Error opening evidence file");
  }
  
  fgets (str, 60, fp);
  sscanf(str, "%d", evidencec);
  int* evidence = (int *) malloc((*evidencec+1) * sizeof(int));
  
  int i = 0;
  while( fgets (str, 60, fp)!=NULL ) 
  {
    int ev;
    if (sscanf(str, "%d", &ev)!=0){
      evidence[i]=ev;
      i++;
    }
  }
  
  return evidence;
}


int main( int argc, const char* argv[] ){
  if (argc<6){
    printf("sddQuery <querytype> <sddpath> <vtreepath> <weightspath> <querypath> [evidencepath]\n querytype can be \"conj\" for conjunctive queries, \"dnf\" for any query formulated in dnf form or \"gen\" for any query formulated as an SDD generation\n");
    return 0;
  }
  int dnf  = strcmp("dnf", argv[1]);
  int gen  = strcmp("gen", argv[1]);
  int conj = strcmp("conj",argv[1]);
  
  if (dnf!=0 && gen!=0 &&conj!=0){
    printf("querytype should be one of the following: \"conj\", \"dnf\", \"gen\"\n");
    return 0;
  }
  
  const char* modelpath = argv[2];
  const char* vtreepath = argv[3];
  const char* weightspath = argv[4];
  const char* querypath = argv[5];
  
  int* evidence;
  int evidencec = 0;
  if (argc>6){
    const char* evidence_path = argv[6];
    evidence = parse_evidence(evidence_path, &evidencec);
  }
  
  
  struct timeval stop, start;
  gettimeofday(&start, NULL);
  
  Vtree* vtree = sdd_vtree_read(vtreepath);
  SddManager* manager = sdd_manager_new(vtree);
  sdd_manager_auto_gc_and_minimize_off(manager);
  SddNode* model = sdd_read(modelpath, manager);
  SddLiteral var_count = sdd_manager_var_count(manager);
  SddWmc* weights = weights_read(weightspath, var_count);
  
      
  struct timeval after_parse, before_parse;
  double ttime = 0.0;
  double probability  = 0.0;
  
  gettimeofday(&before_parse, NULL);
  SddNode* query;
  int queryc = 0;
  int* query_literals;
  if (dnf==0){
    query = dnf_parse(querypath, manager);
  } else if (gen==0){
    query = general_parse(querypath, manager);
  } else  if (conj==0) {
    query_literals = parse_evidence(querypath, &queryc);
  }
  
  gettimeofday(&after_parse, NULL);
  printf("t_query_parse: %lf\n",time_diff(before_parse,after_parse));
  
  if (conj==0) {
    probability = timed_sdd_conj_query(&ttime, model, weights, var_count, manager, query_literals, queryc, evidence, evidencec);
  } else {
    probability = timed_sdd_query(&ttime, model, weights, query, var_count, manager, evidence, evidencec);
  }
  
  gettimeofday(&stop, NULL);
  ttime = time_diff(start,stop);

  printf("prob: %lf\nt_total:%lf\n",probability,ttime);

}