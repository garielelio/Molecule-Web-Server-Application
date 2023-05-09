import sys;
from http.server import HTTPServer, BaseHTTPRequestHandler;
import MolDisplay;
import urllib;
import molsql;
import html;
import io;
import molecule

files = ['/index.html','/uploadFile.html','/styles.css','/addRemoveJS.js', '/uploadFileJS.js', '/selectDisplayJS.js'];
defineDB = molsql.Database(reset=False);
defineDB.create_tables();

class MyHandler(BaseHTTPRequestHandler):
    returnedMolName = "";
    def do_GET(self):
        if self.path in files:
            self.send_response(200); # OK
            self.send_header("Content-type", "text/html");

            #Opening and reading the file
            filePtr = open(self.path[1:]);
            content = filePtr.read();
            filePtr.close();

            #Send header
            self.send_header("Content-length", len(content));
            self.end_headers();

            #Sending content
            self.wfile.write(bytes(content, "utf-8"));
        
        elif self.path == '/addRemove.html':
            self.send_response(200); # OK
            self.send_header("Content-type", "text/html");

            #Opening and reading the file
            filePtr = open(self.path[1:]);
            content = filePtr.read();
            filePtr.close();
        
            #Getting the elements from the database
            checkDictionary = defineDB.element_name();
        
            #Adding options
            optionTable = "";
            if len(checkDictionary) != 0:
                for k in checkDictionary.keys():
                    print(k);
                    keyEscape = html.escape(k);
                    optionTable += '<option value = "{}">{}</option>'.format(keyEscape,keyEscape);
        
                selectTable = '<select id="selectTable" required>{}</select>'.format(optionTable);
        
                content = content.replace('<select id="selectTable"></select>', selectTable);
        
            self.send_header("Content-length", len(content));
            self.end_headers();

            #Sending content
            self.wfile.write(bytes(content, "utf-8"));
        
        elif self.path == '/selectDisplay.html':
            self.send_response(200); # OK
            self.send_header("Content-type", "text/html");

            #Opening and reading the file
            filePtr = open(self.path[1:]);
            content = filePtr.read();
            filePtr.close();
        
            #Getting the molecule
            molNames = defineDB.conn.execute("SELECT * FROM Molecules;");
        
            fetchNames = molNames.fetchall();
        
            nameOption = "";
            if len(fetchNames) != 0:
                for k in fetchNames:
                    nameToPut = html.escape(k[1]);

                    #Selecting the atom number
                    atomNo = defineDB.conn.execute("SELECT ATOM_ID FROM MoleculeAtom WHERE MOLECULE_ID = ?",(k[0],));
                    fetchAtomNo = atomNo.fetchall();

                    #Selecting the bond number
                    bondNo = defineDB.conn.execute("SELECT BOND_ID FROM MoleculeBond WHERE MOLECULE_ID = ?",(k[0],));
                    fetchBondNo = bondNo.fetchall();

                    nameOption += '<option value = "{}">{}, Atoms: {}, Bonds: {}</option>'.format(nameToPut,nameToPut,len(fetchAtomNo), len(fetchBondNo));

                selectNameTable = '<select id="chooseMol" required>{}</select>'.format(nameOption);
        
                content = content.replace('<select id="chooseMol"></select>', selectNameTable);
            

        
            self.send_header("Content-length", len(content));
            self.end_headers();

            #Sending content
            self.wfile.write(bytes(content, "utf-8"));


        else:
            self.send_response(404);
            self.end_headers();
            self.wfile.write(bytes("404: not found", "utf-8"));

    def do_POST(self):
        if self.path == "/add_button.html":
            #Reading the request body
            conLength = int(self.headers['Content-Length']);
            requestBody = self.rfile.read(conLength);

            #Converting to a python dictionary
            addLibrary = urllib.parse.parse_qs(requestBody.decode('utf-8'));

            print(addLibrary);
            elementNum = int(addLibrary["elNum"][0]);
            elementCode = addLibrary["elCode"][0];
            elementName = addLibrary["elName"][0]; 
            elementColor1 = addLibrary["elColor1"][0][1:];
            elementColor2 = addLibrary["elColor2"][0][1:];
            elementColor3 = addLibrary["elColor3"][0][1:];
            elementRadius = int(addLibrary["elRadius"][0]);

            #TESTING=================================
            # print(elementNum);
            # print(elementCode);
            # print(elementName);
            # print(elementColor1);
            # print(elementColor2);
            # print(elementColor3);
            # print(elementRadius);
            #========================================

            #Checking to see if element already inside the database
            elementDictionary = defineDB.element_name();

            #print(elementDictionary);
            if elementCode in elementDictionary:
                sendBack = "Element code is already in the database.";
                self.send_response(200);
                self.send_header("Content-type", "text/plain");
                self.send_header("Content-length", len(sendBack));
                self.end_headers();

                self.wfile.write(bytes(sendBack, "utf-8"));

            else:
                #Inserting to the database
                defineDB['Elements'] = (elementNum, elementCode, elementName, elementColor1, elementColor2, elementColor3, elementRadius);
            
                sendBack = "Received successfully. Added to database.";

                self.send_response(200); # OK
                self.send_header("Content-type", "text/plain");
                self.send_header("Content-length", len(sendBack));
                self.end_headers();

                self.wfile.write(bytes(sendBack, "utf-8"));
        
        elif self.path == "/remove_button.html":
            #Reading the request body
            conLength = int(self.headers['Content-Length']);
            requestBody = self.rfile.read(conLength);
        
            #Converting to a python dictionary
            addLibrary = urllib.parse.parse_qs(requestBody.decode('utf-8'));

            delElementCode = addLibrary["elementToDelete"][0];

            #TESTING=========================================
            # print('to delete:' + delElementCode);
            #=================================================

            #Delete from the database
            defineDB.conn.execute("DELETE FROM Elements WHERE ELEMENT_CODE = ?",(delElementCode,));
            defineDB.conn.commit();
        
            sendBack = "Element deleted from database.";
        
            self.send_response(200); # OK
            self.send_header("Content-type", "text/plain");
            self.send_header("Content-length", len(sendBack));
            self.end_headers();

            self.wfile.write(bytes(sendBack, "utf-8"));
        
        elif self.path == "/upload_button.html":

            #Reading the request body
            conLength = int(self.headers['Content-Length']);
            requestBody = self.rfile.read(conLength);
            dataRead = io.TextIOWrapper(io.BytesIO(requestBody));
        
            #TESTING ===========================
            #print(dataRead.read());
            #===================================

            #Retrieving the molecule name
            for k in range(3):
                dataRead.readline();
            
            moleculeName = dataRead.readline();

            #Checking if filename is valid
            listName = defineDB.conn.execute("SELECT NAME FROM Molecules;");

            checkName = listName.fetchall();

            passOrNo = True;
            if len(checkName) != 0:
                for k in checkName:
                    if k[0] == moleculeName:
                        passOrNo = False;
                        break;
                
            if passOrNo:
                #Retrieving the sdf file
                for k in range(4):
                    dataRead.readline();
            
                try:
                    defineDB.add_molecule(moleculeName, dataRead);
                    sendBack = "File has been uploaded";
                except:
                    sendBack = "Error in reading file";
                
            else:
                sendBack = "Molecule name already in use. Please select a different molecule name.";
            
            self.send_response(200); # OK
            self.send_header("Content-type", "text/plain");
            self.send_header("Content-length", len(sendBack));
            self.end_headers();

            self.wfile.write(bytes(sendBack, "utf-8"));
        
        elif self.path == "/display_button":
            #Reading the request body
            conLength = int(self.headers['Content-Length']);
            requestBody = self.rfile.read(conLength);
        
            #Converting to a python dictionary
            addLibrary = urllib.parse.parse_qs(requestBody.decode('utf-8'));
        
            MyHandler.returnedMolName = addLibrary["molSelected"][0];
        
            MolDisplay.radius = defineDB.radius();
            MolDisplay.element_name = defineDB.element_name();
            MolDisplay.header += defineDB.radial_gradients();

            molRet = defineDB.load_mol(MyHandler.returnedMolName);
            molRet.sort();
            svgToWrite = molRet.svg();

            self.send_response(200); # OK
            self.send_header("Content-type", "text/plain");
            self.send_header("Content-length", len(svgToWrite));
            self.end_headers();
        
            self.wfile.write(bytes(svgToWrite, "utf-8"));
        
        elif self.path == "/mod_svg.html":
            #Reading the request body
            conLength = int(self.headers['Content-Length']);
            requestBody = self.rfile.read(conLength);
        
            #Converting to a python dictionary
            addLibrary = urllib.parse.parse_qs(requestBody.decode('utf-8'));
        
            changeType = addLibrary["axisChange"][0];
            degree = int(addLibrary["degreeChange"][0]);
        
            MolDisplay.radius = defineDB.radius();
            MolDisplay.element_name = defineDB.element_name();
            MolDisplay.header += defineDB.radial_gradients();
        
            molRet = defineDB.load_mol(MyHandler.returnedMolName);
            
            if changeType == "x":
                mx = molecule.mx_wrapper(degree,0,0);
                molRet.xform(mx.xform_matrix);
            
            elif changeType == "y":
                mx = molecule.mx_wrapper(0,degree,0);
                molRet.xform(mx.xform_matrix);

            else:
                mx = molecule.mx_wrapper(0,0,degree);
                molRet.xform(mx.xform_matrix);

            molRet.sort();
            svgToWrite = molRet.svg();

            print("inside mod: " + MyHandler.returnedMolName);

            self.send_response(200); # OK
            self.send_header("Content-type", "text/plain");
            self.send_header("Content-length", len(svgToWrite));
            self.end_headers();
        
            self.wfile.write(bytes(svgToWrite, "utf-8"));


        else:
            self.send_response(404);
            self.end_headers();
            self.wfile.write(bytes("404: not found", "utf-8"));


httpd = HTTPServer(('localhost', int(sys.argv[1])),MyHandler);
httpd.serve_forever();

