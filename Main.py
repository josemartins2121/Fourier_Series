from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
import math

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

    
start = code.find('viewBox="') + 9
end = code.find('"', start)
aux_coordinates = code[start:end].split(" ")
width = aux_coordinates[2]
height = aux_coordinates[3]

#find path 
start = code.find('<path d="') + 9
end = code.find('"', start)
code = code[start:end].replace(" ",'')

# z e Z têm o mesmo significado 
code = code.replace("z","Z")


letters=[]
for i in code:
    if i.isalpha():
        if i not in letters:
            letters.append(i)
code = replace_char(code,letters)
code.remove("")

code = [[instruction[0],instruction.replace(instruction[0],'')]for instruction in code]


scaling_factor = 1

#transcrição de string para float 
for instruction in code:
    try :
        instruction[1]= [float(x) for x in instruction[1].split(",")]
        if instruction[0].isupper():
            for i,coordinates in enumerate(instruction[1]):
                instruction[1][i] = coordinates-25
    except:
        pass

""" for instruction in code:
    if instruction[0].upper() == 'V':
        code.pop(code.index(instruction)) """
#alterar centro de massa da imagem 




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

    def function_t(self,t):
        return self.startpoint*(1-t)+t*self.endpoint


def parser(code):
    path = []

    #primeira instrução tipo M
    start_command = code.pop(0)

    #coordenadas do início do desenho 
    startpoint_path = complex(start_command[1][0],start_command[1][1])

    startpoint_new = startpoint_path
    for i,command in enumerate(code):

        new_type = command[0]
        new_type_upper = new_type.upper()

        if new_type_upper == 'V':

            Y = command[1][0]

            #linha vertical mantém-se o x   
            if new_type.islower():
                y_end = startpoint_new.imag+Y
            else:
                y_end = Y
            aux_endpoints = complex(startpoint_new.real,y_end)
            new_instruction = instruction(type = new_type,startpoint=startpoint_new,endpoint=aux_endpoints)


        if new_type_upper == 'Z':
            aux_endpoints = startpoint_path
            new_instruction = instruction(type = new_type,startpoint=startpoint_new,endpoint=aux_endpoints)
            

        if new_type_upper == 'L':
            aux_endpoints = complex(command[1][0],command[1][1])
            new_instruction = instruction(type = new_type,startpoint=startpoint_new,endpoint=aux_endpoints)

        
        
        if new_type_upper == 'M':
            aux_endpoints = complex(command[1][0],command[1][1])


        path.append(new_instruction)
        new_instruction.print()
        startpoint_new = aux_endpoints


    return path

def main(code):
    path = parser(code)
    path.pop(8)
    list_points = []
    for instruction in path:
        
        #instruction.print()
        if instruction.startpoint not in list_points:
            list_points.append(instruction.startpoint)
        if instruction.endpoint not in list_points:
            list_points.append(instruction.endpoint)         
    #print_points(list_points)
    print_points_f(path)


def image_func(t):
    interval = 2*math.pi/len(path)
    return path[int(t/interval)].function_t((t%interval)/interval)



def print_points_f(path):

    #interval t [0,2pi]
    interval = 2*math.pi/len(path)

    X = []
    Y = []

    for t in np.arange(0,2*math.pi,0.001):
        value = path[int(t/interval)].function_t((t%interval)/interval)
        X.append(value.real)
        Y.append(value.imag)

    plt.scatter(X,Y, color='blue',s=2)
    plt.show()
       
"""  for t in np.arange(0,2*math.pi,0.5):
        value = path[int(t/interval)].function_t((t%interval)/interval)
        X.append(value.real)
        Y.append(value.imag) """
""" for i in range(len(path)):
        for t in np.arange(0,1,0.001):
            print(t)
            value = path[i].function_t(t)
            X.append(value.real)
            Y.append(value.imag)
    plt.scatter(X,Y, color='blue',s=2)
    plt.show() """

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

    
