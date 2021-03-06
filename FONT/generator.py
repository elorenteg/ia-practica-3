#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import sys
import re


if len(sys.argv)-1 != 3:
    print 'python generator.py <version> <ntareas> <nprogs>'
    print 'version = {b,1,2,3,4}'
    sys.exit()

version = sys.argv[1]
ntareas = sys.argv[2]
nprogs = sys.argv[3]
file = open("Generator/problema.pddl", "w")

file_nombres = open('Generator/nombres.csv', "r")
file_verbos = open('Generator/verbos.csv', "r")
file_objetos = open('Generator/objetos.csv', "r")
lines_nombres = file_nombres.readlines()
lines_verbos = file_verbos.readlines()
lines_objetos = file_objetos.readlines()
MAX_NOMBRES = len(lines_nombres)
MAX_VERBOS = len(lines_verbos)
MAX_OBJETOS = len(lines_objetos)

LIST_TAREA = []
LIST_PROGS = []


def indent(n):
    while n > 0:
        file.write('    ')
        n -= 1;
        
def nomProg():
    rand = randint(0,MAX_NOMBRES-1)
    nomb = lines_nombres[rand].lower()
    nomb = " ".join(nomb.split())
    nomb = nomb.replace(" ","_")
    nomb = re.sub("[^a-zA-Z|^0-9|^_]+", "", nomb) #nomb solo puede tener caracteres a-zA-Z, 0-9, _
    if nomb in LIST_PROGS:
        return nomProg()
    return nomb

def nomTarea():
    randV = randint(0,MAX_VERBOS-1)
    randO = randint(0,MAX_OBJETOS-1)
    verbo = lines_verbos[randV].lower()
    objeto = lines_objetos[randO].lower()
    verbo = " ".join(verbo.split())
    objeto = " ".join(objeto.split())
    tarea = verbo + " " + objeto
    tarea = tarea.replace(" ","_")
    tarea = re.sub("[^a-zA-Z|^0-9|^_]+", "", tarea) #tarea solo puede tener caracteres a-zA-Z, 0-9, _
    if tarea in LIST_TAREA:
        return nomTarea()
    return tarea

def create_objects(letra, tipo, max):
    indent(2)
    
    for i in range(1,int(max)+1):
        if letra == 'p':
            nomb = nomProg()
            file.write(nomb + " ")
            LIST_PROGS.append(nomb)
        else:
            tarea = nomTarea()
            file.write(tarea + " ")
            LIST_TAREA.append(tarea)
        
    file.write("- " + tipo + "\n")
    
def init_tarea(max):
    for i in range(0,int(max)):
        indent(2)
        tarea = LIST_TAREA[i]
        file.write("(= (dtarea " + tarea + ") " + str(randint(1,3)) + ") ")
        file.write("(= (ttarea " + tarea + ") " + str(randint(1,10)) + ") ")
        file.write("\n")

def init_programador(max):
    for i in range(0,int(max)):
        indent(2)
        prog = LIST_PROGS[i]
        file.write("(= (hprog " + prog + ") " + str(randint(1,3)) + ") ")
        file.write("(= (cprog " + prog + ") " + str(randint(1,2)) + ") ")
        if version in ['3','4']:
            file.write("(= (nprog " + prog + ") " + str(0) + ") ")
        file.write("\n")
        
    if version in ['2','3','4']:
        indent(2)
        file.write("(= (ttotal) " + str(0) + ") ")
        file.write("\n")
        
    if version in ['4']:
        indent(2)
        file.write("(= (ntrabajadores) " + str(0) + ") ")
        file.write("\n")
        
        
def create_goal():
    indent(2)
    if version == 'b':
        file.write("(forall (?t - tarea) (servida ?t))\n")
    else:
        file.write("(forall (?t - tarea) (revisada ?t))\n")
        
def create_minim():
    indent(1)
    file.write("(:metric minimize\n")
    indent(2)
    if version == '4':
        file.write("(+ (* 0.2 (ttotal)) (* 0.8 (ntrabajadores)))")
    else:
        file.write("(ttotal)")
    file.write("\n")
    indent(1)
    file.write(")\n")


def create_problem():    
    file.write("(define (problem problema)\n")
    indent(1)
    file.write("(:domain tareas-")
    if version == 'b':
        file.write("basic")
    else:
        file.write("ext" + version)
    file.write(")\n")
    
    indent(1)
    file.write("(:objects \n")
    create_objects("t","tarea",ntareas)
    create_objects("p","programador",nprogs)
    indent(1)
    file.write(")\n")
    
    indent(1)
    file.write("(:init\n")
    init_tarea(ntareas)
    init_programador(nprogs)
    indent(1)
    file.write(")\n")

    indent(1)
    file.write("(:goal\n")
    create_goal()
    indent(1)
    file.write(")\n")
    
    if version in ['2','3','4']:
        create_minim()
    
    file.write(")")
    file.close()
    
    
create_problem()