from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np

def replace_char(path,letters):
    result = []
    aux = ""
    for i in path:
        if i in letters:
            result.append(aux)
            aux = ""
        aux += i
    result.append(aux)
    return result



with open('teste.svg','r') as f:
    code = f.read()

start = code.find('<path d="') + 9
end = code.find('"', start)
code = code[start:end].replace(" ",'')
   
letters=[]
for i in code:
    if i.isalpha():
        if i not in letters:
            letters.append(i)
            
code = replace_char(code,letters)
code.remove("")


code = [[instruction[0],instruction.replace(instruction[0],'')]for instruction in code]
print(code)



class instruction:  
    def __init__(self, type,endpoint,startpoint=[],controlpoints=[]):  
        self.type = type 
        self.startpoint = startpoint 
        self.controlpoints = controlpoints 
        self.endpoint = endpoint 

    def print(self):
        print("Instruction type: {type} \t Startpoint: {startpoint} controlpoint: {controlpoint} endpoint: {endpoint}\t ".format(type = self.type,
        startpoint=self.startpoint,
        endpoint = self.endpoint,
        controlpoint= self.controlpoints))


def parser(code):
    path = []

    #primeira instrução tipo M
    start_command = code.pop(0)

    #coordenadas do início do desenho 
    startpoint_path = np.array(start_command[1].split(",")).astype(np.float)


    startpoint = startpoint_path
    for i,command in enumerate(code):

        switch(command[0])





        if command[0] != 'z':
            points = np.array(command[1].split(",")).astype(np.float)
        else: 
            points = startpoint_path
        
        path.append(instruction(type=command[0],startpoint=startpoint,endpoint = points))
        
        startpoint = points
        print(i+1)
        path[i].print()

    #print(path[0].type)
    #print(path[0].endpoint)



    return path

def main(code):
    path = parser(code)
    














def print_points(path):
    X = []
    Y = []
    for instruction in path:
        if instruction[1] != '' and instruction[0] != 'V' and instruction[0] != 'v':
            print(instruction)
            x,y = instruction[1].split(",")
            x = float(x)
            y = float(y)
            X.append(x)
            Y.append(y*1j)
    plt.scatter(X,Y, color='red')
    plt.show()

main(code)
#print_points(code) 


    
