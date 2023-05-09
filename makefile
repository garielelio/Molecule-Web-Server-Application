CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all: mol.o libmol.so molecule_wrap.c molecule.py molecule_wrap.o _molecule.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

libmol.so: mol.o
	$(CC) mol.o -shared -o libmol.so

molecule_wrap.c molecule.py: molecule.i
	swig3.0 -python molecule.i

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -c molecule_wrap.c -I/usr/include/python3.7m -fPIC -o molecule_wrap.o

_molecule.so: molecule_wrap.o libmol.so
	$(CC) molecule_wrap.o -shared -L/usr/lib/python3.7/config-3.7m-x86_64-linux-gnu -L. -dynamiclib -lpython3.7m -lmol -o _molecule.so

clean:
	rm -f *.o *.so
	