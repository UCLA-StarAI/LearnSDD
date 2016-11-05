#ifndef SDDQUERY_H_
#define SDDQUERY_H_
#include <sddapi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include <sys/time.h>


double time_diff(struct timeval start, struct timeval stop);
double sdd_query(SddNode* model, const SddWmc* weights, SddNode* query, const SddLiteral var_count, SddManager* manager, int* evidence, int evidencec);
double timed_sdd_query(double* ttime, SddNode* model, const SddWmc* weights, SddNode* query, const SddLiteral var_count, SddManager* manager, int* evidence, int evidencec);
double sdd_conj_query(SddNode* model, SddWmc* weights, const SddLiteral var_count, SddManager* manager, int* literals, int litc, int* evidence, int evidencec);
double timed_sdd_conj_query(double* ttime, SddNode* model, SddWmc* weights, const SddLiteral var_count, SddManager* manager, int* literals, int litc, int* evidence, int evidencec);
SddWmc wmc(SddNode* sdd, const SddWmc* weights, const SddWmc* negweights, const SddLiteral var_count, SddManager* manager);
SddWmc* weights_read(const char* path, const SddLiteral var_count);
SddNode* dnf_parse(const char* query, SddManager* manager);
SddNode* general_parse(const char* query, SddManager* manager);
int* parse_evidence(const char* evidence_path, int* evidencec);

#endif // SDDQUERY_H_