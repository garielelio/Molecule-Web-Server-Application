import MolDisplay;
import os;
import sqlite3;
import html;

class Database:
    def __init__(self, reset=False):
        #Delete an existing database
        if reset == True:
            if os.path.exists('molecules.db'):
                os.remove('molecules.db');

        #Creating the database
        self.conn = sqlite3.connect('molecules.db');

    def create_tables(self):
        #Creating tables
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Elements(
                                  ELEMENT_NO    INTEGER    NOT NULL,
                                  ELEMENT_CODE  VARCHAR(3) NOT NULL,
                                  ELEMENT_NAME VARCHAR(32) NOT NULL,
                                  COLOUR1       CHAR(6)    NOT NULL,
                                  COLOUR2       CHAR(6)    NOT NULL,
                                  COLOUR3       CHAR(6)    NOT NULL,
                                  RADIUS        DECIMAL(3) NOT NULL,
                                  PRIMARY KEY(ELEMENT_CODE));""");

        self.conn.execute("""CREATE TABLE IF NOT EXISTS Atoms(
                                  ATOM_ID      INTEGER      PRIMARY KEY AUTOINCREMENT NOT NULL,
                                  ELEMENT_CODE VARCHAR(3)   NOT NULL,
                                  X            DECIMAL(7,4) NOT NULL,
                                  Y            DECIMAL(7,4) NOT NULL,
                                  Z            DECIMAL(7,4) NOT NULL,
                                  FOREIGN KEY(ELEMENT_CODE) REFERENCES Elements(ELEMENT_CODE));""");

        self.conn.execute("""CREATE TABLE IF NOT EXISTS Bonds(
                                  BOND_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                  A1      INTEGER NOT NULL,
                                  A2      INTEGER NOT NULL,
                                  EPAIRS  INTEGER NOT NULL);""");

        self.conn.execute("""CREATE TABLE IF NOT EXISTS Molecules(
                                  MOLECULE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                  NAME        TEXT    UNIQUE    NOT NULL);""");

        
        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeAtom(
                                  MOLECULE_ID INTEGER NOT NULL,
                                  ATOM_ID     INTEGER NOT NULL,
                                  PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                                  FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                                  FOREIGN KEY (ATOM_ID) REFERENCES Atoms(ATOM_ID));""");

        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeBond(
                                  MOLECULE_ID INTEGER NOT NULL,
                                  BOND_ID     INTEGER NOT NULL,
                                  PRIMARY KEY (MOLECULE_ID, BOND_ID),
                                  FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                                  FOREIGN KEY (BOND_ID) REFERENCES Bonds(BOND_ID));""");
                                  

    def __setitem__(self, table, values):
        #Inserting elements inside the table
        #strOfTuple = str(values);
        self.conn.execute("""INSERT
                              INTO {}
                              VALUES (?,?,?,?,?,?,?);""".format(table), values);
    
        self.conn.commit();
        
    
    def add_atom(self, molname, atom):
        atomElement = atom.atom.element;
        atomX = atom.atom.x;
        atomY = atom.atom.y;
        atomZ = atom.atom.z;

        atomXmod = "{:.4f}".format(atomX);
        atomYmod = "{:.4f}".format(atomY);
        atomZmod = "{:.4f}".format(atomZ);

        #Inserting elemenets to Atoms table
        self.conn.execute("""INSERT
                              INTO Atoms
                              VALUES (NULL, ?, ?, ?, ?);""",(atomElement, atomXmod, atomYmod, atomZmod));
        
        self.conn.commit();
    
        #Select and fetch atom id
        row = self.conn.execute("""SELECT * FROM Atoms
                                    WHERE ATOM_ID = last_insert_rowid();""");
        
        rowTuple = row.fetchone();
        atomId = rowTuple[0];
    
        #Select and fetch molecule id
        row2 = self.conn.execute("""SELECT * FROM Molecules
                                     WHERE NAME = ?""",(molname,));
    
        rowTuple2 = row2.fetchone();
        molId = rowTuple2[0];
    
        #Adding entry to MoleculeAtom
        self.conn.execute("""INSERT
                              INTO MoleculeAtom
                              VALUES (?, ?);""",(molId, atomId));
    
        self.conn.commit();
    

    def add_bond(self, molname, bond):
        bondA1 = bond.bond.a1;
        bondA2 = bond.bond.a2;
        bondEpairs = bond.bond.epairs;

        #Inserting elements to Bonds table
        self.conn.execute("""INSERT
                              INTO Bonds
                              VALUES (NULL, ?, ?, ?);""",(bondA1, bondA2, bondEpairs));
        
        self.conn.commit();
    
        #Select and fetch bond id
        row = self.conn.execute("""SELECT * FROM Bonds
                                    WHERE BOND_ID = last_insert_rowid();""");

        rowTuple = row.fetchone();
        bondId = rowTuple[0];
    
        #Select and fetch molecule id
        row2 = self.conn.execute("""SELECT * FROM Molecules
                              WHERE NAME = ?""",(molname,));
    
        rowTuple2 = row2.fetchone();
        molId = rowTuple2[0];
    
        #Adding entry to MoleculeBond
        self.conn.execute("""INSERT
                              INTO MoleculeBond
                              VALUES (?, ?);""",(molId, bondId));
    
        self.conn.commit();

    def add_molecule(self, name, fp):
        mol = MolDisplay.Molecule();
        mol.parse(fp);

        #Adding entry to Molecules
        self.conn.execute("""INSERT
                               INTO Molecules
                               VALUES (NULL, ?);""",(name,));
        
        self.conn.commit();

        #Calling add_atom and bond_atom
        j = 0;
        while j < mol.atom_no:
            getAtom = mol.get_atom(j);
            atomClass = MolDisplay.Atom(getAtom);
            self.add_atom(name, atomClass);
            j = j + 1;
        
        k = 0;
        while k < mol.bond_no:
            getBond = mol.get_bond(k);
            bondClass = MolDisplay.Bond(getBond);
            self.add_bond(name, bondClass);
            k = k + 1;

    def load_mol(self, name):
        nameMol = MolDisplay.Molecule();

        #Inner join for atom
        joinAtom = self.conn.execute("""SELECT Atoms.ELEMENT_CODE, Atoms.X, Atoms.Y, Atoms.Z
                                        FROM Atoms
                                        INNER JOIN MoleculeAtom ON MoleculeAtom.ATOM_ID = Atoms.ATOM_ID
                                        INNER JOIN Molecules ON Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID
                                        WHERE Molecules.NAME = ?
                                        ORDER BY Atoms.ATOM_ID ASC;""",(name,));

        fetchAtom = joinAtom.fetchall();

        #Appending the atoms
        for i in range(len(fetchAtom)):
            nameMol.append_atom(fetchAtom[i][0], fetchAtom[i][1], fetchAtom[i][2], fetchAtom[i][3]);

        #Inner join for bond
        joinBond = self.conn.execute("""SELECT Bonds.A1, Bonds.A2, Bonds.EPAIRS
                                        FROM Bonds
                                        INNER JOIN MoleculeBond ON MoleculeBond.BOND_ID = Bonds.BOND_ID
                                        INNER JOIN Molecules ON Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID
                                        WHERE Molecules.NAME = ?
                                        ORDER BY Bonds.BOND_ID ASC;""",(name,));

        fetchBond = joinBond.fetchall();

        #Appending the bonds
        for i in range(len(fetchBond)):
            nameMol.append_bond(fetchBond[i][0], fetchBond[i][1], fetchBond[i][2]);

        #Return the nameMol
        return nameMol;

    def radius(self):
        radDictionary = {};

        #Selecting element code and radius
        getVal = self.conn.execute("""SELECT ELEMENT_CODE, RADIUS
                                        FROM Elements;""");

        #Fetching the values
        fetchVal = getVal.fetchall();

        #Adding it into the dictionary
        for i in range(len(fetchVal)):
            keyVal = fetchVal[i][0];
            itemVal = fetchVal[i][1];
            radDictionary[keyVal] = itemVal;

        #Return the dictionary
        return radDictionary;
        
    def element_name(self):
        elementDictionary = {};

        #Selecting element code and element name
        getVal = self.conn.execute("""SELECT ELEMENT_CODE, ELEMENT_NAME
                                        FROM Elements;""");

        #Fetching the values
        fetchVal = getVal.fetchall();

        #Adding it into the dictionary
        for i in range(len(fetchVal)):
            keyVal = fetchVal[i][0];
            itemVal = fetchVal[i][1];
            elementDictionary[keyVal] = itemVal;

        #Return the dictionary
        return elementDictionary;

    def radial_gradients(self):
        retString = """""";

        #Selecting the required values
        getVal = self.conn.execute("""SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3
                                        FROM Elements;""");

        #Fetching the values
        fetchVal = getVal.fetchall();

        #Concantenate the values to the string
        for i in range(len(fetchVal)):
            #Defining string to add
            radialGradientSVG = """
            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
              <stop offset="0%%" stop-color="#%s"/>
              <stop offset="50%%" stop-color="#%s"/>
              <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>""" % (html.escape(fetchVal[i][0]), fetchVal[i][1], fetchVal[i][2], fetchVal[i][3]);

            retString = retString + radialGradientSVG;

        #Return the string
        return retString;
 

