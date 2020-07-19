import numpy
import pandas
from tkinter import *

class regles_jdv:
    def __init__(self,n_plateau,min_around_survie,
                max_around_survie,min_around_naissance,
                max_around_naissance,n_random,can):
        self.can = can
        self.n_plateau = n_plateau
        self.plateau = numpy.zeros((n_plateau,n_plateau))
        self.plateau_next_gen = numpy.zeros((n_plateau,n_plateau))
        self.n_random = n_random
        self.min_around_survie = min_around_survie
        self.max_around_survie = max_around_survie
        self.min_around_naissance = min_around_naissance
        self.max_around_naissance = max_around_naissance
        self.n_random = n_random

    def init_fill(self):
        rand_1 = numpy.random.choice(range(self.n_plateau * self.n_plateau),replace = False,size = int(self.n_random * self.n_plateau * self.n_plateau))
        for r in rand_1:
            col_r = int(r / self.n_plateau)
            row_r = r % self.n_plateau
            self.plateau[row_r,col_r] = 1

    def survie(self,i,j):
        if self.plateau[i,j] == 1 and i - 1 >= 0 and i + 1 < self.n_plateau and j - 1 >= 0 and j + 1 < self.n_plateau:
            nb_around = self.plateau[(i-1):(i+2),(j-1):(j+2)]
            nb_around = numpy.sum(nb_around) - 1
            if nb_around >= self.min_around_survie and nb_around <= self.max_around_survie:
                self.plateau_next_gen[i,j] = 1
            else:
                self.plateau_next_gen[i,j] = 0

    def naissance(self,i,j):
        if self.plateau[i,j] == 0 and i - 1 >= 0 and i + 1 < self.n_plateau and j - 1 >= 0 and j + 1 < self.n_plateau:
            nb_around = self.plateau[(i-1):(i+2),(j-1):(j+2)]
            nb_around = numpy.sum(nb_around)
            if nb_around >= self.min_around_naissance and nb_around <= self.max_around_naissance:
                self.plateau_next_gen[i,j] = 1
            else:
                self.plateau_next_gen[i,j] = 0
    
    def next_gen(self):
        for i in range(self.n_plateau):
            for j in range(self.n_plateau):
                self.survie(i,j)
                self.naissance(i,j)
        self.plateau = self.plateau_next_gen.copy()
        self.plateau_next_gen = numpy.zeros((self.n_plateau,self.n_plateau))
    
    def display(self):
        self.can.delete(ALL)
        for i in range(self.n_plateau):
            for j in range(self.n_plateau):
                if self.plateau[i,j] == 1:
                    self.can.create_rectangle(i * 1000 / self.n_plateau,j * 1000 / self.n_plateau,(i + 1) * 1000 / self.n_plateau,(j + 1) * 1000 / self.n_plateau,fill='black')
                else:
                    self.can.create_rectangle(i * 1000 / self.n_plateau,j * 1000 / self.n_plateau,(i + 1) * 1000 / self.n_plateau,(j + 1) * 1000 / self.n_plateau,fill='white')

fen = Tk()
can = Canvas(fen, width =1000, height =1000, bg ='white')
can.pack(side =TOP, padx =5, pady =5)
jdv = regles_jdv(n_plateau = 1,
                min_around_survie = 2,
                max_around_survie = 3,
                min_around_naissance = 3,
                max_around_naissance = 3,
                n_random = 0.2,
                can = can)
        
def play():
    global jdv
    if jdv.n_plateau == 1:
        jdv = regles_jdv(n_plateau = int(entree.get()),
                        min_around_survie = 2,
                        max_around_survie = 3,
                        min_around_naissance = 3,
                        max_around_naissance = 3,
                        n_random = 0.2,
                        can = can)
        jdv.init_fill()

    jdv.next_gen()
    jdv.display()
    flag = numpy.sum(jdv.plateau)
    if flag > 0:
        fen.after(50,play)

b1 = Button(fen, text ='Go!', command =play)
b1.pack(side =LEFT, padx =3, pady =3)
entree = Entry(fen)
# entree.bind("<Return>", init_jeux_de_la_vie)
entree.pack(side =RIGHT)
chaine = Label(fen)
chaine.configure(text = "taille du jdv :")
chaine.pack(side =RIGHT)
fen.mainloop()