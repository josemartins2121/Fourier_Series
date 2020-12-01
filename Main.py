from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.integrate as integrate

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



with open('teste copy.svg','r') as f:
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

#transcrição de string para float e alteração do centro de massa 
for instruction in code:
    try :
        instruction[1]= [float(x) for x in instruction[1].split(",")]  
    except:
        pass

print(code)

class instruction():  
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
    
    def set_startpoint(self,startpoint):
        self.startpoint = startpoint 
    
    def set_endpoint(self,endpoint):
        self.endpoint = endpoint

    def function_t(self,t):
        return  (self.startpoint*(1-t)+t*self.endpoint)


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

def change_centre_of_mass(path):
    for instruction in path:
        instruction.set_startpoint(complex(instruction.startpoint.real-25,12.5-instruction.startpoint.imag))
        instruction.set_endpoint(complex(instruction.endpoint.real-25,12.5-instruction.endpoint.imag))



def main(code):
    path = parser(code)

    ## alterar o centro de massa e as coordenadas de y 
    change_centre_of_mass(path)



    #path.pop(8)
    list_points = []
    for instruction in path:
        #instruction.print()
        if instruction.startpoint not in list_points:
            list_points.append(instruction.startpoint)
        if instruction.endpoint not in list_points:
            list_points.append(instruction.endpoint)         
    #print_points(list_points)
    print_points_f(path)
    #fourier_coefficients(2,path)


def image_func(t,path):
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
       
import cmath
import quadpy

def fourier_coefficients(lenght,path):
    coefficientes = []

    interval = 2*(math.pi)/len(path)
    #for t in np.arange(0,2*math.pi,0.1):
        #print(t)
       # value = path[int(t/interval)].function_t((t%interval)/interval)

    for i in range(0,len+1):
        coef = (1/(2*math.pi))*quadpy.quad(lambda x:image_func(x,path)*cmath.exp(complex(0,-1)*i*2*math.pi*x),0,2*math.pi)



main(code)
#print_points(code) 

    
