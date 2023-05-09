#include "mol.h"

//Function 1
void atomset(atom *atom, char element[3], double *x, double *y, double *z){
    //Copying x,y,z to the struct atom
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;

    strcpy(atom->element, element);
}

//Function 2
void atomget(atom *atom, char element[3], double *x, double *y, double *z){
    //Copying x,y,z from the struct atom
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;

    strcpy(element, atom->element);
}

//Function 3
void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs){
    //Copying a1, a2, epairs to struct bond
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->epairs = *epairs;
    bond->atoms = *atoms;
    compute_coords(bond);
}

//Function 4
void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs){
    //Copying a1, a2, epairs from struct bond
    *a1 = bond->a1;
    *a2 = bond->a2;
    *epairs = bond->epairs;
    *atoms = bond->atoms;
}

//Function 5
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max){
    //Malloc an array of atoms
    molecule* molPtr = malloc(sizeof(struct molecule));

    //If malloc fails
    if(molPtr == NULL){
        return NULL;
    }

    //Setting the structure
    molPtr->atom_max = atom_max;
    molPtr->atom_no = 0;
    molPtr->bond_max = bond_max;
    molPtr->bond_no = 0;

    //Malloc the atoms array
    molPtr->atoms = malloc(atom_max * sizeof(struct atom));
    molPtr->atom_ptrs = malloc(atom_max * sizeof(struct atom*));

    //If malloc fails
    if(molPtr->atoms == NULL || molPtr->atom_ptrs == NULL){
        return NULL;
    }

    //Malloc the bonds array
    molPtr->bonds = malloc(bond_max * sizeof(struct bond));
    molPtr->bond_ptrs = malloc(bond_max * sizeof(struct bond*));

    //If malloc fails
    if(molPtr->bonds == NULL || molPtr->bond_ptrs == NULL){
        return NULL;
    }

    return molPtr;
}

//Function 6
molecule *molcopy(molecule *src){
    //Calling function 5 to malloc the molecule
    molecule* molCopy = molmalloc(src->atom_max, src->bond_max);

    //Check if molCopy is null
    if(molCopy == NULL){
        return NULL;
    }

    //Copying atoms_no and bond_no
    for(int i = 0; i < src->atom_no; i++){
        molappend_atom(molCopy, &src->atoms[i]);
    }
    for(int k = 0; k < src->bond_no; k++){
        bond temp = src->bonds[k];
        temp.atoms = molCopy->atoms;
        molappend_bond(molCopy, &temp);
    }

    return molCopy;
}

//Function 7
void molfree(molecule *ptr){
    //Freeing the arrays and pointer arrays
    free(ptr->atom_ptrs);
    free(ptr->atoms);
    free(ptr->bond_ptrs);
    free(ptr->bonds);
    free(ptr);
}

//Function 8
void molappend_atom(molecule *molecule, atom *atom){
    //Copying the data and check if space is enough, if not space will be increased
    if((molecule->atom_no == molecule->atom_max) && (molecule->atom_max != 0)){
        molecule->atoms = realloc(molecule->atoms, 2 * molecule->atom_max * sizeof(struct atom));
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, 2 * molecule->atom_max * sizeof(struct atom*));

        //if realloc fails
        if(molecule->atoms == NULL || molecule->atom_ptrs == NULL){
            fprintf(stderr, "Error with realloc!\n");
            exit(1);
        }
        //Assigning the pointers
        for(int i = 0; i < molecule->atom_no; i++){
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }
        //Increase the atom max
        molecule->atom_max = 2 * molecule->atom_max;
    } 
    else if (molecule->atom_max == 0){
        molecule->atoms = realloc(molecule->atoms, 1 * sizeof(struct atom));
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, 1 * sizeof(struct atom*));

        //If realloc fails
        if(molecule->atoms == NULL || molecule->atom_ptrs == NULL){
            fprintf(stderr, "Error with realloc!\n");
            exit(1);
        }
        //Increase the atom max
        molecule->atom_max = 1;
    }

    //Adding the atom to molecule
    molecule->atoms[molecule->atom_no] = *atom;
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];
    molecule->atom_no = molecule->atom_no + 1;
}

//Function 9
void molappend_bond(molecule *molecule, bond *bond){
    //Copying the data and check if space is enough, if not space will be increased
    if((molecule->bond_no == molecule->bond_max) && (molecule->bond_max != 0)){
        molecule->bonds = realloc(molecule->bonds, (2 * molecule->bond_max) * sizeof(struct bond));
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, (2 * molecule->bond_max) * sizeof(struct bond*));

        //if realloc fails
        if(molecule->bonds == NULL || molecule->bond_ptrs == NULL){
            fprintf(stderr, "Error with realloc!\n");
            exit(1);
        }
        //Assigning to pointers 
        for(int i = 0; i < molecule->bond_no; i++){
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }
        //Increase the max size
        molecule->bond_max = 2 * molecule->bond_max;
    } 
    else if(molecule->bond_max == 0){
        molecule->bonds = realloc(molecule->bonds, 1 * sizeof(struct bond));
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, 1 * sizeof(struct bond*));

        //if realloc fails
        if(molecule->bonds == NULL || molecule->bond_ptrs == NULL){
            fprintf(stderr, "Error with realloc!\n");
            exit(1);
        }
        //Increase the max size
        molecule->bond_max = 1;
    }

    molecule->bonds[molecule->bond_no] = *bond;
    molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
    molecule->bond_no = molecule->bond_no + 1;
}

//Comparator function for qsort atom
int comparatorAtm(const void * p1, const void * p2){
    struct atom** cmp1 = (struct atom **)p1;
    struct atom** cmp2 = (struct atom **)p2;

    if(((*cmp1)->z - (*cmp2)->z) == 0){
        return 0;
    }
    else if(((*cmp1)->z - (*cmp2)->z) > 0){
        return 1;
    }
    else{
        return -1;
    }
}

//Comparator function for qsort bond
int comparatorBnd(const void * p1, const void * p2){
    struct bond** cmp1 = (struct bond **)p1;
    struct bond** cmp2 = (struct bond **)p2;

    double bndAvg1 = (*cmp1)->z;
    double bndAvg2 = (*cmp2)->z;

    if((bndAvg1 - bndAvg2) == 0){
        return 0;
    }
    else if ((bndAvg1 - bndAvg2) > 0){
        return 1;
    }
    else {
        return -1;
    }
}

//Function 10
void molsort(molecule *molecule){
    //Sorting the atom ptrs and bond ptrs
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom *), comparatorAtm);
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond *), comparatorBnd);
}

//Function 11
void xrotation(xform_matrix xform_matrix, unsigned short deg){
    //Defining the matrix
    double radians = deg * (M_PI / 180);
    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(radians);
    xform_matrix[1][2] = -sin(radians);
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(radians);
    xform_matrix[2][2] = cos(radians); 
}

//Function 12
void yrotation(xform_matrix xform_matrix, unsigned short deg){
    //Defining the matrix
    double radians = deg * (M_PI / 180);
    xform_matrix[0][0] = cos(radians);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(radians);
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = -sin(radians);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(radians); 
}

//Function 13
void zrotation(xform_matrix xform_matrix, unsigned short deg){
    //Defining the matrix
    double radians = deg * (M_PI / 180);
    xform_matrix[0][0] = cos(radians);
    xform_matrix[0][1] = -sin(radians);
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = sin(radians);
    xform_matrix[1][1] = cos(radians);
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

//Function 14
void mol_xform(molecule *molecule, xform_matrix matrix){
    //Performing matrix multiplication
    for(int i = 0; i < molecule->atom_no; i++){
        double xTran = molecule->atoms[i].x;
        double yTran = molecule->atoms[i].y;
        double zTran = molecule->atoms[i].z;

        molecule->atoms[i].x = (matrix[0][0] * xTran) 
        + (matrix[0][1] * yTran) 
        + (matrix[0][2] * zTran);

        molecule->atoms[i].y = (matrix[1][0] * xTran) 
        + (matrix[1][1] * yTran) 
        + (matrix[1][2] * zTran);  

        molecule->atoms[i].z = (matrix[2][0] * xTran) 
        + (matrix[2][1] * yTran) 
        + (matrix[2][2] * zTran);
    }

    for(int k = 0; k < molecule->bond_no; k++){
        compute_coords(&(molecule->bonds[k]));
    }
}

//Function 15
void compute_coords(bond *bond){
    //Computing and assigning x1, x2, y1, y2, z, len, dx, dy
    bond->x1 = bond->atoms[bond->a1].x;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y1 = bond->atoms[bond->a1].y;
    bond->y2 = bond->atoms[bond->a2].y;

    //Computing the average z
    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2;

    //Computing the len
    double x = bond->x2 - bond->x1;
    double y = bond->y2 - bond->y1;
    bond->len = sqrt((x * x) + (y * y));

    //Calculating dx and dy
    bond->dx = (bond->x2 - bond->x1) / bond->len;
    bond->dy = (bond->y2 - bond->y1) / bond->len;
}
