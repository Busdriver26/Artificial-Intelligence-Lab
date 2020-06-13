import os
import sys
import math

NUM = 1000 # point num default
MAXINT = 99999999 #maxint for distance

#INPUT argv and check if inputs are legal
if(len(sys.argv)!=6):
    print("WRONG INPUT, check input argvs")
    os._exit(0)
func_num = int(sys.argv[1])
if (not isinstance(func_num,int)) or (func_num<1) or func_num>2:
    print("ERROR: input amount not right")
    os._exit(0)
cityfile = sys.argv[2]
if not os.path.isfile(cityfile):
    print("ERROR:can't find city data, check files")
    os._exit(0)
with open(cityfile,'r') as f:
    dat1 = f.readlines()
    NUM = len(dat1) #Update the number of cities(NUM)
#print(NUM)
linkfile = sys.argv[3]
if not os.path.isfile(linkfile):
    print("ERROR:can't find link data, check files")
    os._exit(0)
src = int(sys.argv[4])
if(src<0 or src>=NUM):
    print("ERROR: source unavaliable")
    os._exit(0)
dest = int(sys.argv[5])
if(dest<0 or dest>=NUM):
    print("ERROR: destination unavaliable")
    os._exit(0)

#read files and set lists
city_x = []
city_y = []
roads = [[MAXINT for i in range(NUM)] for i in range(NUM)]
with open(cityfile,'r') as f:
    dat1 = f.readlines()
    for line in dat1:
        liney = line.split()
        city_x.append(float(liney[1]))
        city_y.append(float(liney[2]))

#calculate the distance
def distance(city1,city2):
    x1 = float(city_x[city1])
    x2 = float(city_x[city2])
    y1 = float(city_y[city1])
    y2 = float(city_y[city2])
    return math.sqrt((y2-y1)*(y2-y1)+(x2-x1)*(x2-x1))

with open(linkfile,'r') as f:
    dat2 = f.readlines()
    for line in dat2:
        liney = line.split()
        city1 = int(liney[0])
        city2 = int(liney[1])
        d = distance(city1,city2)
        roads[city1][city2] = d
        roads[city2][city1] = d

#first algorithm- Dijkstra
if func_num == 1:
    visited = [0 for i in range(NUM)]
    pre = [-1 for i in range(NUM)]
    dist = [MAXINT for i in range(NUM)]
    pre[src] = 0
    dist[src] = 0
    for i in range(NUM):
        dist[i] = roads[src][i]
        if(dist[i]<MAXINT):
            pre[i] = src
    for i in range(NUM):
        min = MAXINT
        k = -1
        for j in range(NUM):
            if visited[j]==0:
                if dist[j]!=0 and dist[j]<min:
                    min = dist[j]
                    k = j
        if k==-1:
            continue
        visited[k] = 1
        for j in range(NUM):
            if visited[j]==0 and roads[k][j]<MAXINT:
                if dist[k]+ roads[k][j]<dist[j]:
                    dist[j] = dist[k]+roads[k][j]
                    pre[j] = k
    o = dest
    rmp = []
    if dist[dest] ==MAXINT:
        print("NO available route!")
        os._exit(0)
    while o!=src:
        rmp.append(o)
        o = pre[o]
    rmp.append(src)
    rmp = rmp[::-1]
    print("length:",end="")
    print(dist[dest],end=" ")
    print("path:",end="")
    for i in range(len(rmp)):
        print(rmp[i],end="")
        if i!=len(rmp)-1:
            print("-",end="")
    print()
    os._exit(0)

#second algorithm A*
#in a* algorithm, the h(n)<=h*(n) so that h(n) can be the straight distance.
h = [distance(i,dest) for i in range(NUM)]
g = [0 for i in range(NUM)]
pre = [-1 for i in range(NUM)]

def cmpre(a):
    return h[a] + g[a]

if func_num==2:
    #print("This function is in Alpha Version(testing).")
    #os._exit(0)  
    op = [src]
    cl = [0 for i in range(NUM)] 
    #notice that 'open' is a stack of cities while 'close' is the bool list
    while len(op)!=0:
        n = op.pop()
        cl[n] = 1
        if n == dest:
            break
        for i in range(NUM):
            if roads[n][i]>0 and roads[n][i]<MAXINT:
                if cl[i] == 1:
                    if(g[i]>g[n]+roads[i][n]):
                        g[i]=g[n]+roads[i][n]
                        pre[i]=n
                        op.append(i)
                    else:
                        continue
                sgn = 0
                for j in range(len(op)):
                    if op[j] == i:
                        if(g[i]>g[n]+roads[i][n]):
                            g[i]=g[n]+roads[i][n]
                            pre[i]=n
                        else:
                            sgn = 1
                        break
                if sgn==1:
                    continue
                pre[i] = n
                g[i] = g[n] + roads[i][n]
                op.append(i)
        op = sorted(op,key = cmpre,reverse = True) #sort the open table
    o = dest
    rmp = []
    while o!=src:
        rmp.append(o)
        o = pre[o]
    rmp.append(src)
    rmp = rmp[::-1]
    print("length:",end="")
    print(g[dest],end=" ")
    print("path:",end="")
    for i in range(len(rmp)):
        print(rmp[i],end="")
        if i!=len(rmp)-1:
            print("-",end="")
    print()
    os._exit(0)
   
   #LICENSE: MIT LICENSE
   #ECNU_CS_10172100163_GongZezheng