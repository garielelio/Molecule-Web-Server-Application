#ifndef _mol_h
#define _mol_h

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>

#define M_PI 3.14159265358979323846

//Struct 1
typedef struct atom{
    char element[3];
    double x, y, z;
} atom;

//Struct 2
typedef struct bond{
    unsigned short a1, a2;
    unsigned char epairs;
    atom *atoms;
    double x1, x2, y1, y2, z, len, dx, dy;
} bond;

//Struct 3
typedef struct molecule{
    unsigned short atom_max, atom_no;
    atom *atoms, **atom_ptrs;
    unsigned short bond_max, bond_no;
    bond *bonds, **bond_ptrs;
} molecule;

//Typedef 1
typedef double xform_matrix[3][3];

//Typedef 2
typedef struct mx_wrapper
{
  xform_matrix xform_matrix;
} mx_wrapper;

//Function prototypes
void atomset(atom *atom, char element[3], double *x, double *y, double *z);

void atomget(atom *atom, char element[3], double *x, double *y, double *z);

//void bondset(bond *bond, atom *a1, atom *a2, unsigned char epairs);
void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs);

//void bondget(bond *bond, atom **a1, atom **a2, unsigned char *epairs);
void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs);

molecule *molmalloc(unsigned short atom_max, unsigned short bond_max);

molecule *molcopy(molecule *src);

void molfree(molecule *ptr);

void molappend_atom(molecule *molecule, atom *atom);

void molappend_bond(molecule *molecule, bond *bond);

void molsort(molecule *molecule);

void xrotation(xform_matrix xform_matrix, unsigned short deg);

void yrotation(xform_matrix xform_matrix, unsigned short deg);

void zrotation(xform_matrix xform_matrix, unsigned short deg);

void mol_xform(molecule *molecule, xform_matrix matrix);

int comparatorAtm(const void * p1, const void * p2);

int comparatorBnd(const void * p1, const void * p2);

void qsort(void *base, size_t nitems, size_t size, int (*comparator)(const void *, const void*));

void compute_coords(bond *bond);

#endif
