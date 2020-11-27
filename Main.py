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
code = code.replace("z","Z")


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
    def __init__(self, type,endpoint,startpoint,controlpoints=[]):  
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
    startpoint_path = [float(x) for x in start_command[1].split(",")]
    startpoint_path = complex(startpoint_path[0],startpoint_path[1])

    startpoint_new = startpoint_path
    for i,command in enumerate(code):

        new_type = command[0]
        new_type_upper = new_type.upper()

        if new_type_upper == 'V':

            Y = float(command[1])

            #linha vertical mantém-se o x   
            if new_type.islower():
                y_end = startpoint_new.imag+Y
            else:
                y_end = Y
            aux_endpoints = complex(startpoint_new.real,y_end)


            new_instruction = instruction(type = new_type,startpoint=startpoint_new,endpoint=aux_endpoints)
        

        if new_type_upper == 'Z':
            new_instruction = instruction(type = new_type,startpoint=startpoint_new,endpoint=startpoint_path)
            aux_endpoints = startpoint_path
            

        if new_type_upper == 'L':

            aux_endpoints = [float(x) for x in command[1].split(",")]
            aux_endpoints = complex(aux_endpoints[0],aux_endpoints[1])

            new_instruction = instruction(type = new_type,startpoint=startpoint_new,endpoint=aux_endpoints)
            new_instruction.endpoint=aux_endpoints
        
        path.append(new_instruction)
        new_instruction.print()
        #print(aux_endpoints)
        startpoint_new = aux_endpoints


    return path

def main(code):
    path = parser(code)
    list_points = []
    for instruction in path:
        #instruction.print()
        if instruction.startpoint not in list_points:
            list_points.append(instruction.startpoint)
        if instruction.endpoint not in list_points:
            list_points.append(instruction.endpoint)         
    print_points(list_points)



def print_points(list_points):
    X = []
    Y = []
    for point in list_points:
            X.append(point.real)
            Y.append(point.imag)
    plt.scatter(X,Y, color='red')
    plt.show()

main(code)
#print_points(code) 


    
