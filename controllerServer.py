import turtle, socket, threading


class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("black")
        self.penup()
        self.speed(0)


class PenB(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed("slowest")


class PenG(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("green")
        self.penup()
        self.speed("slowest")


class PenR(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed("slowest")


class PenY(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("yellow")
        self.penup()
        self.speed("slowest")



def setup_maze(map):
    for y in range(len(map)):
        for x in range(len(map[y])):
            char=map[y][x]
            screen_x = -340+(x*24)
            screen_y = 340-(y*24)


            if char=='X':
                pen.goto(screen_x,screen_y)
                pen.stamp()
                bar=(x,y)
                barriers.append([bar])


def markStart(map,start):
    for y1 in range(len(map)):
     for x1 in range(len(map[y1])):
         char = map[y1][x1]
         screen_x = -340 + (x1 * 24)
         screen_y = 340 - (y1 * 24)

         if y1 == start[1] and x1 == start[0]:
             peng.goto(screen_x, screen_y)
             peng.stamp()

def markEnd(map,end):
    for y1 in range(len(map)):
     for x1 in range(len(map[y1])):
         char = map[y1][x1]
         screen_x = -340 + (x1 * 24)
         screen_y = 340 - (y1 * 24)

         if y1 == end[1] and x1 == end[0]:
             penr.goto(screen_x, screen_y)
             penr.stamp()



startFlag=0
start=()
end=()
cost=0
result=[]


def clicked(x,y):
    global startFlag
    global start
    global end
    global cost
    global result
    col=int((x+350)//24)
    row = int((-((y - 350) // 24))-1)
    if startFlag==0:
        start1=(col,row)
        start=start+start1
        startFlag=1
        wn.onscreenclick(None)
        markStart(map[1], start)
        wn.onscreenclick(clicked)
    else:
        end1=(col,row)
        end = end + end1
        wn.onscreenclick(None)
        markEnd(map[1], end)
        result, cost = AStarSearch(start,end)
        markPath(map[1],result)




def heuristic( start, end):

    D = 1
    D2 = 1
    dx = abs(start[0] - end[0])
    dy = abs(start[1] - end[1])
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

def getVertexNeighbours(pos):
    n = []

    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        x2 = pos[0] + dx
        y2 = pos[1] + dy
        if x2 < 0 or x2 > 290 or y2 < 0 or y2 > 290:
            continue
        n.append((x2, y2))
    return n

def moveCost(a,b):
    global barriers

    for barrier in barriers:
        if b in barrier:
            return 1000
    return 1


def AStarSearch(start, end):

    G = {}
    F = {}

    G[start] = 0
    F[start] = heuristic(start, end)
    closedVertices = set()
    openVertices = set([start])
    cameFrom = {}

    while len(openVertices) > 0:
        current = None
        currentFscore = None
        for pos in openVertices:
            if current is None or F[pos] < currentFscore:
                currentFscore = F[pos]
                current = pos


        if current == end:

            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            print(path,"\n",end," ",start)
            return path, F[end]


        openVertices.remove(current)
        closedVertices.add(current)


        for neighbour in getVertexNeighbours(current):
            if neighbour in closedVertices:
                continue
            x=moveCost(current, neighbour)
            candidateG = G[current] + x
            if neighbour not in openVertices:
                openVertices.add(neighbour)
            elif candidateG >= G[neighbour]:
                continue


            cameFrom[neighbour] = current
            G[neighbour] = candidateG
            H = heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + H

    raise RuntimeError("Unable To Find The Route")


def markPath(map, result):
    if cost < 1000:
        for y1 in range(len(map)):
            for x1 in range(len(map[y1])):
                char = map[y1][x1]
                screen_x = -340 + (x1 * 24)
                screen_y = 340 - (y1 * 24)
                temp=(x1,y1)
                if temp in result:
                    penb.goto(screen_x, screen_y)
                    penb.stamp()

    else:
        print("Unable To Find The Route")


def vehicles(dock,pen,number):
    SERVER = "192.168.43.91"
    PORT = 8080
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    flag = 0
    vstart = dock
    astamp=None
    screen_x = -340 + (vstart[0] * 24)
    screen_y = 340 - (vstart[1] * 24)
    pen.clearstamp(astamp)
    pen.goto(screen_x, screen_y)
    astamp=pen.stamp()
    pen.stamp()
    current = vstart
    print("Vehicle number ",number," is started")
    while True:
        if flag==0:
            client.connect((SERVER, PORT))
            client.sendall(bytes("pop".encode('UTF8')))
            data = client.recv(1024)
            data = data.decode().split()
        flag = 0
        l=[]
        for i in data: l.append(int(i))
        start = (l[0],l[1])
        end = (l[2],l[3])
        if start!=end:
            if start!=vstart:
                result, cost = AStarSearch(current,start)
                for i in result:
                    screen_x = -340 + (i[0] * 24)
                    screen_y = 340 - (i[1] * 24)
                    pen.clearstamp(astamp)
                    pen.goto(screen_x, screen_y)
                    pen.stamp()
                    astamp=pen.stamp()
                    current = (i[0],i[1])
            result, cost = AStarSearch(start,end)
            for i in result:
                screen_x = -340 + (i[0] * 24)
                screen_y = 340 - (i[1] * 24)
                pen.clearstamp(astamp)
                pen.goto(screen_x, screen_y)
                pen.stamp()
                astamp=pen.stamp()
                current = (i[0],i[1])
            result, cost = AStarSearch(end,vstart)
            for i in result:
                screen_x = -340 + (i[0] * 24)
                screen_y = 340 - (i[1] * 24)
                current = (i[0],i[1])
                pen.clearstamp(astamp)
                pen.goto(screen_x, screen_y)
                pen.stamp()
                astamp=pen.stamp()
                client.sendall(bytes("peek".encode('UTF8')))
                c = client.recv(1024)
                if c!='0':
                    client.sendall(bytes("pop".encode('UTF8')))
                    data = client.recv(1024)
                    data = data.decode().split()
                    flag = 1
                    break


if __name__ == "__main__":
    wn=turtle.Screen()
    wn.bgcolor("white")
    wn.title("Server Program")
    wn.setup(10000,10000)
    pen=Pen()
    penb = PenB()
    peng = PenG()
    penr = PenR()
    peny = PenY()

    barriers=[]
    map=[""]
    result=[]
    costA=0

    try:
        fh = open("map","r")
        fh.close()
    except:
        print("File Not Found!!!!!\nContact Admin")
        exit(0)
    fh = open("map","r")
    string=""
    graph=[]
    ch=0
    for j in fh:
        for i in j:
            if i == "|":
                graph.append(string)
                string=""
            else:
                string+=i
    map.append(graph)
    fh.close()
    setup_maze(map[1])
    dock = (0,7)
    t1 = threading.Thread(target=vehicles, args=(dock,penb,0))
    t2 = threading.Thread(target=vehicles, args=(dock,peny,1))
    t3 = threading.Thread(target=vehicles, args=(dock,penr,2))
    t1.start()
    t2.start()
    t3.start()



wn.mainloop()
