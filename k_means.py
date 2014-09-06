# -*- coding: utf-8 -*-
from __future__ import division
from time import time, sleep
import random
import arff
import mysql_to_arff

def distance(a, b):
    """ Calcula a distancia """
    distancia = sum([(a.coord[i]-b.coord[i])**2 for i in range(len(a.coord))])**0.5
    #print "Cluster " + str(a.label) + "\t -> Distancia " + str(distancia)
    return distancia
 
class Point:
 
    """ Objetos do tipo tem coordenadas (x, y) e label no formato Point((x,y), "A") """
 
    def __init__(self, coordinates, label=-1):
        self.coord = coordinates
        self.label = label
 
    def dist(self, other):
        return distance(self, other)
 
    def __str__(self):
        return 'Ponto(%s,%s)'%(self.coord, self.label)
 
class Cluster:
 
    """ Objeto do tipo Cluster tem uma lista de pontos e um centroid calculado  """
 
    def __init__(self, points):
        self.points = points
        self.center = self._calcCenter()
 
    def update(self, points):
        self.points = points
        self.center = self._calcCenter()
 
    def _calcCenter(self):
        x = [i for i in self.points[0].coord]
        for p in self.points[1:]:
            for j in range(len(p.coord)):
                x[j] += p.coord[j]
        M = len(self.points)
        return Point([xx/M for xx in x], label='center')
        
    def __str__(self):
        return 'Point(%s,%s)'%(self.coord, self.label)
 
def kmeans(points, k, max_iter=1000, min_shift_frac=0.01):

    # inicializa a lista de centroides hardcoded
    #ponto_c1 = Point((10,30), "C1")
    #ponto_c2 = Point((45,46), "C2")
    #ponto_c3 = Point((55,57), "C3")
    #clusters = [Cluster([ponto_c1]), Cluster([ponto_c2]), Cluster([ponto_c3])]
    
    # se quiser pode comecar com centroids sendo um sorteio dos pontos
    clusters = gera_centroides(points)
 
    # iteracao do algoritmo
    this_iter = 0
    while this_iter < max_iter:
        this_iter += 1
        lists = [[] for c in range(k)]
        shifts = 0
        for p in points:
            dx = min([(p.dist(clusters[h].center), h) for h in range(k)])[1]
            if dx != p.label: shifts += 1
            p.label = dx
            lists[dx].append(p)
        for i in range(k):
            clusters[i].update(lists[i])
         

        # parada se os pontos mudam alem do limites
        if shifts/len(points) < min_shift_frac:
            break
 
    return (clusters, this_iter)

# Gerador de pontos aleatorios
def gera_pontos(n):
 
    points = []
    for i in range(n):
        points.append(Point(numpy.random.random(2)))

    return points

# Gerador de centroides aleatorios
def gera_centroides(points):
    clusters = []
    for p in random.sample(points, k):
        clusters.append(Cluster([p]))
        
    return clusters

if __name__ == '__main__':
    import pylab, numpy
    
    # Valor hardcoded para o exercicio
    #points = [Point((32,27),"A"), Point((55,43),"B"),Point((80,63),"C"),Point((85,50),"D"),Point((58,38),"E"),Point((82,55),"F"), Point((25,31),"G"),Point((66,42),"H"),Point((60,49),"I"),Point((35,12),"J"),]
    
    # se quiser pode gerar um numero aleatorio de pontos, por exemplo 1000
    # points = gera_pontos(1000)
    
    points = []

    mysql_to_arff.user_by_tweets()
   
    # id, - 0
    #twitter_id, -1
    #username, - 2
    #data_end, -3 
    #data_start, - 4
    #friend_count_end, -5 
    #friend_count_start,- 6
    #folowers_end, -7 
    #folowers_start,- 8
    #statuses_end,- 9
    #statuses_start, -10
	# 21,100220864,BrunoMars,2013-06-01 20:00:15,2013-06-11 14:32:45,76,77,16282451,16205047,2657,2655,
    for row in arff.load('input_file.arff'):
        #seguidores por posts
        points.append(Point(((row[7]-row[8]), (row[9]-row[10]))))
        #numero de seguidores por  pessoas que ele segui
        #points.append(Point(((row[7]-row[8]), (row[5]-row[6]))))
        #twittes por amigos
        #points.append(Point(((row[5]-row[6]), (row[9]-row[10]))))
        #print  str(row[2]) +' - '+ str(row[7]-row[8])
        #points.append(Point((row[4],row[3])))
    
    # Numero de centroides k fixado
    k = 3
    # Numero de iteracoes maximasrow[7]
    n = 30
    clusters, num_iters = kmeans(points, k, n)

    # print 'Numero de interacoes: ' + str(num_iters)
    # for cluster in clusters:
    #    print cluster.center
    #    for p in cluster.points:
    #         print "Cluster: " + str(p.label) + " -> " + str(p.coord) 
 
    # Eixo X = LARANJA e Y=LIMAO
    x = [clusters[i].center.coord[0] for i in range(k)]
    y = [clusters[i].center.coord[1] for i in range(k)]
    
    # plota o grafico
    pylab.plot(x, y, 'ok')
    pylab.ylabel('Numero de Tweets')
    pylab.xlabel('Numero de Seguidores')
    
    # plota os pontos
    for cluster in clusters:
        x = [p.coord[0] for p in cluster.points]
        #print x
        y = [p.coord[1] for p in cluster.points]
        #print y
        pylab.plot(x, y, '.')
     
    pylab.show()
