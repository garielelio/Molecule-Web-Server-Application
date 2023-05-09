import molecule
import html

header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">""";

footer = """</svg>""";

defGrad = """
            <radialGradient id="def" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
              <stop offset="0%" stop-color="#000000"/>
              <stop offset="50%" stop-color="#000000"/>
              <stop offset="100%" stop-color="#000000"/>
            </radialGradient>"""

offsetx = 500;
offsety = 500;

#Creating a class
class Atom:
    #Init for atom
    def __init__(self, atom):
        self.atom = atom;
        self.z = atom.z;
    
    #Str function for atom
    def __str__(self):
        return '%s %lf %lf %lf' % (self.atom.element, self.atom.x, self.atom.y, self.atom.z);

    #Svg function for atom
    def svg(self):
        cx = (self.atom.x * 100.0) + offsetx;
        cy = (self.atom.y * 100.0) + offsety;

        if self.atom.element not in element_name:
            r = 40;
            fill = "def";
        else:
            r = radius[self.atom.element];
            fill = element_name[self.atom.element];

        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (cx, cy, r, html.escape(fill));

#Creating a class bond
class Bond:
    #Init function for bond
    def __init__(self, bond):
        self.bond = bond;
        self.z = bond.z;

    #Str function for bond
    def __str__(self):
        return '%lf %lf - %lf %lf' % (self.bond.x1, self.bond.y1, self.bond.x2, self.bond.y2);

    #Svg function for bond
    def svg(self):

        #Calculating values to return
        cx1 = (self.bond.x1 * 100.0) + offsetx;
        cy1 = (self.bond.y1 * 100.0) + offsety;
        cx2 = (self.bond.x2 * 100.0) + offsetx;
        cy2 = (self.bond.y2 * 100.0) + offsety;

        cx1mod1 = cx1 + self.bond.dy * 10;
        cy1mod1 = cy1 - self.bond.dx * 10;

        cx1mod2 = cx1 - self.bond.dy * 10;
        cy1mod2 = cy1 + self.bond.dx * 10;

        cx2mod1 = cx2 - self.bond.dy * 10;
        cy2mod1 = cy2 + self.bond.dx * 10;

        cx2mod2 = cx2 + self.bond.dy * 10;
        cy2mod2 = cy2 - self.bond.dx * 10;
        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (cx1mod1, cy1mod1, cx1mod2, cy1mod2, cx2mod1, cy2mod1, cx2mod2, cy2mod2);

class Molecule(molecule.molecule):
    #Str function for molecule
    def __str__(self):
        return 'WRITE SOMETHING';

    #Svg function for molecule
    def svg(self):
        svgRet = '';
        j = 0;
        k = 0;

        #Combining the atom and bond according to z value
        while j < self.atom_no and k < self.bond_no:
            obj1 = Atom(self.get_atom(j));
            obj2 = Bond(self.get_bond(k));
            if obj1.z < obj2.z:
                svgRet += obj1.svg();
                j = j + 1;
            else:
                svgRet += obj2.svg();
                k = k + 1;

        while j < self.atom_no:
            obj1 = Atom(self.get_atom(j));
            svgRet += obj1.svg();
            j = j + 1;

        while k < self.bond_no:
            obj2 = Bond(self.get_bond(k));
            svgRet += obj2.svg();
            k = k + 1;

        #Return the svg file content
        return header + '\n'+ defGrad + svgRet + footer + '\n'; 

    #Parse function for molecule
    def parse(self, fobj):
        for i in range(3):
            fobj.readline();
        
        elementLine = fobj.readline();
        elementSplit = elementLine.split();
        while '' in elementSplit:
            elementSplit.remove('');

        numAtoms = int(elementSplit[0]);
        numBonds = int(elementSplit[1]);

        for i in range(numAtoms):
            elementLine = fobj.readline();
            elementSplit = elementLine.split();
            while '' in elementSplit:
                elementSplit.remove('');

            self.append_atom(elementSplit[3], float(elementSplit[0]), float(elementSplit[1]), float(elementSplit[2]));

        for i in range(numBonds):
            elementLine = fobj.readline();
            elementSplit = elementLine.split();
            while '' in elementSplit:
                elementSplit.remove('');

            self.append_bond(int(elementSplit[0]) - 1, int(elementSplit[1]) - 1, int(elementSplit[2]));


        
   
