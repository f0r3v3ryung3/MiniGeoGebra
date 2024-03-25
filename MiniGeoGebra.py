import math


EPS = 10 ** -8


class Point:
    def __init__(self, x, y=None, polar=False):
        if polar:
            self.x = x * math.cos(y)
            self.y = x * math.sin(y)
        elif y is not None:
            self.x = x
            self.y = y
        else:
            self.x = x.x
            self.y = x.y
    
    def __abs__(self):
        return math.hypot(self.x, self.y)
    
    def dist(self, x=None, y=None):
        if x is None and y is None:
            return abs(self)
        elif y is None:
            if x.__class__.__name__ == "Point" or x.__class__.__name__ == "DrawPoint":
                return math.hypot(abs(self.x - x.x), abs(self.y - x.y))
            elif x.__class__.__name__ == "Line" or x.__class__.__name__ == "DrawLine":
                return x.dist(self)
            elif x.__class__.__name__ == "Circle" or x.__class__.__name__ == "DrawCircle":
                return abs(math.hypot(abs(self.x - x.x), abs(self.y - x.y)) - x.r)
            elif x.__class__.__name__ == "Triangle" or x.__class__.__name__ == "DrawTriangle":
                return x.dist(self)
        else:
            A = self
            B = x
            C = y
            a = Vector(B, C)
            a1 = Vector(C, B)
            b = Vector(B, A)
            c = Vector(C, A)
            if abs(b.dist()) < EPS or abs(c.dist()) < EPS:
                return 0
            elif a ** b - (math.pi / 2) < EPS and a1 ** c - (math.pi / 2) < EPS:
                return abs(a ^ b) / a.dist()
            else:
                return min(A.dist(B), A.dist(C))
    
    def in_injection(self, P, A, B):
        a = Vector(self, A)
        b = Vector(self, B)
        c = Vector(self, P)
        if a ** c < EPS or b ** c < EPS:
            return True
        elif a ** c + b ** c - a ** b < EPS:
            return True
        else:
            return False

    def turnAlpha(self, x):
        return Point(self.x * math.cos(x) - self.y * math.sin(x), self.x * math.sin(x) + self.y * math.cos(x))
        
    def __str__(self):
        return f"{round(self.x, 5)} {round(self.y, 5)}"


class Vector(Point):
    def __init__(self, a, b=None, c=None, d=None):
        if d is not None:
            self.x = c - a
            self.y = d - b
        elif b is None:
            self.x = a.x
            self.y = a.y
        elif type(b) == int or type(b) == float:
            self.x = a
            self.y = b
        else:
            self.x = b.x - a.x
            self.y = b.y - a.y
    
    def normal(self):
        return Vector(self.y, -self.x)
    
    def dot_product(self, b):
        return self.x * b.x + self.y * b.y
    
    def __mul__(self, b):
        return self.dot_product(b)
    
    def cross_product(self, b):
        return self.x * b.y - self.y * b.x
    
    def __xor__(self, b):
        return self.cross_product(b)
    
    def mul(self, n):
        return Vector(Point(self.x * n, self.y * n))
        
    def __rmul__(self, n):
        return self.mul(n)
    
    def turn(self, alpha):
        return Vector(Point(self.x, self.y).turnAlpha(alpha))
    
    def __pow__(self, b):
        if self.dist() * b.dist() < EPS:
            return 1
        return math.acos(round(self * b / (self.dist() * b.dist()), 11))


class Line(Vector):
    def __init__(self, a, b=None, c=None, d=None):
        if b is None:
            self.A = a.A
            self.B = a.B
            self.C = a.C
        
        elif c is None:
            self.A = b.y - a.y
            self.B = a.x - b.x
            self.C = -a.x * self.A - a.y * self.B
            super().__init__(-self.B, self.A)
        
        elif d is None:
            self.A = a
            self.B = b
            self.C = c
            super().__init__(-self.B, self.A)
        
        else:
            self.A = round(b, 9)
            self.B = -round(a, 9)
            self.C = round(-b * c + a * d, 9)
            super().__init__(-self.B, self.A)
    
    def contains(self, x, y):
        if abs(self.A * x + self.B * y + self.C) < EPS:
            return True
        return False
    
    def oneLocation(self, a, b):
        if (self.A * a.x + self.B * a.y + self.C) * (self.A * b.x + self.B * b.y + self.C) > -EPS:
            return True
        return False
    
    def is_parallel(self, sec):
        if round(self.A * sec.B) == round(sec.A * self.B) and round(self.A * sec.C) == round(sec.A * self.C) and round(self.C * sec.B) == round(sec.C * self.B):
            return 1
        elif (self.x, self.y) == (sec.x, sec.y) or (self.x, self.y) == (-sec.x, -sec.y):
            return 2
        elif (sec.x, sec.y) == (self.y, -self.x):
            return 3
        else:
            return 0
    
    def __str__(self):
        return f"{round(self.A, 9)} {round(self.B, 9)} {round(self.C, 9)}"
    
    def dist(self, a=None):
        if a is None:
            return Vector(self.x, self.y).dist()
        elif a.__class__.__name__ == "Point" or a.__class__.__name__ == "DrawPoint":
            return round(abs(self.A * a.x + self.B * a.y + self.C) / (self.A ** 2 + self.B ** 2) ** 0.5, 5)
        elif a.__class__.__name__ == "Circle" or a.__class__.__name__ == "DrawCircle":
            return Point(a.x, a.y).dist(self)
    
    def parallel(self, dist):
        if self.B == 0:
            return Line(self.A, self.B, self.C + self.A * dist)
        elif self.A == 0:
            return Line(self.A, self.B, self.C + self.B * dist)
        else:
            return Line(self.A, self.B, self.C + self.B * dist / math.cos(math.atan(-self.A / self.B)))
        
    def crossLine(self, sec):
        x = -(self.C * sec.B - sec.C * self.B) / (self.A * sec.B - self.B * sec.A)
        y = -(self.A * sec.C - sec.A * self.C) / (self.A * sec.B - self.B * sec.A)
        p = Point(x, y)
        return p
    
    def cross(self, sec):
        if sec.__class__.__name__ == "Line" or sec.__class__.__name__ == "DrawLine":
            return self.crossLine(sec)
        
        elif sec.__class__.__name__ == "Circle" or sec.__class__.__name__ == "DrawCircle":
            return sec.cross(self)
        
        elif sec.__class__.__name__ == "Section" or sec.__class__.__name__ == "DrawSection":
            return sec.cross(self)
        
        elif sec.__class__.__name__ == "Triangle" or sec.__class__.__name__ == "DrawTriangle":
            return sec.cross(self)
    
    def foot_of_perp(self, a):
        line1 = Line(self.A, self.B, a.x, a.y)
        return self.cross(line1)
    
    def turn(self, alp):
        p1, p2 = Point(0, -self.C / self.B).turnAlpha(alp), Point(-self.C / self.A, 0).turnAlpha(alp)
        line_new = Line(Point(p1.x, p1.y), Point(p2.x, p2.y))
        return line_new


class Section(Line):
    def __init__(self, a, b=None, c=None, d=None):
        if b is None:
            self.p1 = Point(0, 0)
            self.p2 = Point(a.x, a.y)
        
        elif c is None:
            self.p1 = Point(a.x, a.y)
            self.p2 = Point(b.x, b.y)
        
        else:
            self.p1 = Point(a, b)
            self.p2 = Point(c, d)
        
        super().__init__(self.p1, self.p2)
    
    def dist(self, a=None):
        if a is None:
            return self.p1.dist(self.p2)
        else:
            point = Line(self.p1, self.p2).foot_of_perp(Point(a.x, a.y))
            if a.in_injection(point, self.p1, self.p2):
                return a.dist(point)
            else:
                return min(self.p1.dist(Point(a.x, a.y)), self.p2.dist(Point(a.x, a.y)))
        
    def crossSection_or_not(self, sec):
        if Line(self.p1, self.p2).is_parallel(Line(sec.p1, sec.p2)) == 1:
            if Vector(self.p1, sec.p1) ** Vector(self.p2, sec.p1) < EPS and Vector(self.p1, sec.p2) ** Vector(self.p2, sec.p2) < EPS:
                return False
            return True
        elif self.p1.dist(sec.p1) < EPS or self.p1.dist(sec.p2) < EPS or self.p2.dist(sec.p1) < EPS or self.p2.dist(sec.p2) < EPS:
            return True
        elif self.oneLocation(sec.p1, sec.p2) or sec.oneLocation(self.p1, self.p2):
            return False
        return True

    def crossCircle_or_not(self, circle):
        if self.dist(Point(circle.x, circle.y)) - circle.r > -EPS:
            return False
        elif abs(self.dist(Point(circle.x, circle.y)) - circle.r) < EPS:
            return True
        else:
            points = circle.crossLine(Line(self.p1, self.p2))
            sect = Section(points[0], points[1])
            if self.crossSection_or_not(sect):
                return True
            return False
    
    def crossLine_or_not(self, sec):
        if sec.oneLocation(self.p1, self.p2):
            return False
        return True
    
    def cross_or_not(self, sec):
        if sec.__class__.__name__ == "Section" or sec.__class__.__name__ == "DrawSection":
            return self.crossSection_or_not(sec)
        
        elif sec.__class__.__name__ == "Circle" or sec.__class__.__name__ == "DrawCircle":
            return self.crossCircle_or_not(sec)
        
        elif sec.__class__.__name__ == "Line" or sec.__class__.__name__ == "DrawLine":
            return self.crossLine_or_not(sec)
        
    def crossSection(self, sec):
        if self.cross_or_not(sec):
            return [Line(self.p1, self.p2).cross(Line(sec))]
        return []
    
    def crossCircle(self, sec):
        if self.cross_or_not(sec):
            points = Line(self.p1, self.p2).cross(sec)
            if len(points) == 2:
                res = []
                if Vector(self.p1, points[0]) ** Vector(self.p2, points[0]) > EPS:
                    res.append(points[0])
                if Vector(self.p1, points[1]) ** Vector(self.p2, points[1]) > EPS:
                    res.append(points[1])
                return res
            else:
                if Vector(self.p1, points[0]) ** Vector(self.p2, points[0]) > EPS:
                    return [points[0]]
        return []
    
    def crossLine(self, sec):
        if self.cross_or_not(sec):
            return [Line(self.p1, self.p2).cross(sec)]
        return []
    
    def crossTriangle(self, sec):
        return sec.cross(self)
    
    def cross(self, sec):
        if sec.__class__.__name__ == "Section" or sec.__class__.__name__ == "DrawSection":
            return self.crossSection(sec)
        
        elif sec.__class__.__name__ == "Circle" or sec.__class__.__name__ == "DrawCircle":
            return self.crossCircle(sec)
        
        elif sec.__class__.__name__ == "Line" or sec.__class__.__name__ == "DrawLine":
            return self.crossLine(sec)
        
        elif sec.__class__.__name__ == "Triangle" or sec.__class__.__name__ == "DrawTriangle":
            return self.crossTriangle(sec)
    
    def __str__(self):
        return f"({self.p1}) ({self.p2})"
    

class Circle(Point):
    def __init__(self, x, y, r):
        super().__init__(x, y)
        self.r = r
    
    def dist(self, a):
        if a.__class__.__name__ == "Point" or a.__class__.__name__ == "DrawPoint":
            return a.dist(self)
        elif a.__class__.__name__ == "Line" or a.__class__.__name__ == "DrawLine":
            point = a.foot_of_perp(Point(self.x, self.y))
            if point.dist(Point(self.x, self.y)) - self.r > -EPS:
                return point.dist(Point(self.x, self.y)) - self.r
            else:
                return 0
        elif a.__class__.__name__ == "Circle" or a.__class__.__name__ == "DrawCircle":
            if self.dist(a) - self.r - a.r > - EPS:
                return self.dist(a) - self.r - a.r
            else:
                return 0
    
    def crossLine(self, line):
        p = line.cross(Line(line.y, -line.x, self.x, self.y))
        dist = Point(self.x, self.y).dist(line)
        if dist - self.r > EPS:
            return []
        elif abs(dist - self.r) < EPS:
            return [Point(p.x, p.y)]
        else:
            mult = (self.r ** 2 - dist ** 2) ** 0.5
            x1 = mult * line.x / Vector(line.x, line.y).dist()
            y1 = mult * line.y / Vector(line.x, line.y).dist()
            return [Point(round(p.x + x1, 6), round(p.y + y1, 6)), Point(round(p.x - x1, 6), round(p.y - y1, 6))]
    
    def crossCircle(self, sec):
        line = Line(2 * (sec.x - self.x), 2 * (sec.y - self.y), sec.r ** 2 - self.r ** 2 + self.x ** 2 - sec.x ** 2 - sec.y ** 2 + self.y ** 2)
        return self.crossLine(line)
    
    def cross(self, sec):
        if sec.__class__.__name__ == "Line" or sec.__class__.__name__ == "DrawLine":
            return self.crossLine(sec)
        
        elif sec.__class__.__name__ == "Circle" or sec.__class__.__name__ == "DrawCircle":
            return self.crossCircle(sec)
        
        elif sec.__class__.__name__ == "Section" or sec.__class__.__name__ == "DrawSection":
            return sec.cross(self)
        
        elif sec.__class__.__name__ == "Triangle" or sec.__class__.__name__ == "DrawTriangle":
            return sec.cross(self)
    
    def injection(self, p):
        return 2 * math.asin(self.r / self.dist(p))
    
    def arc(self, p1, p2):
        return Vector(self.x, self.y, p1.x, p1.y) ** Vector(self.x, self.y, p2.x, p2.y) * self.r
    
    def tangent(self, p):
        points = self.tangent_points(p)
        return [Line(points[0], p), Line(points[1], p)]
    
    def tangent_points(self, p):
        OP = Vector(Point(self.x, self.y), Point(p.x, p.y))
        normOP = OP.normal()
        distAP = (OP.dist() ** 2 - self.r ** 2) ** 0.5
        OH = self.r ** 2 / OP.dist()
        h = distAP * self.r / OP.dist()
        line = Line(normOP.x, normOP.y, OH * OP.x / OP.dist() + self.x, OH * OP.y / OP.dist() + self. y)
        H = line.cross(Line(OP.x, OP.y, self.x, self.y))
        pointA = Point(line.x * h / line.dist() + H.x, line.y * h / line.dist() + H.y)
        pointB = Point(-line.x * h / line.dist() + H.x, -line.y * h / line.dist() + H.y)
        return [pointA, pointB]
    
    def __str__(self):
        return f"{round(self.x, 9)} {round(self.y, 9)} {round(self.r, 9)}"


class Triangle:
    def __init__(self, a, b, c, d=None, e=None, f=None):
        if f is None:
            self.a = a
            self.b = b
            self.c = c
        else:
            self.a = Point(a, b)
            self.b = Point(c, d)
            self.c = Point(e, f)
    
    def dist(self, sec):
        if sec.__class__.__name__ == "Point" or sec.__class__.__name__ == "DrawPoint":
            return min(Section(self.a, self.b).dist(sec), Section(self.a, self.c).dist(sec), Section(self.c, self.b).dist(sec))
    
    def nearPoint(self, sec):
        if sec.__class__.__name__ == "Point" or sec.__class__.__name__ == "DrawPoint":
            return self.cross(Circle(sec.x, sec.y, self.dist(sec) + 0.3))[0]
    
    def bisector_point(self):
        A = self.c.dist(self.b)
        B = self.a.dist(self.c)
        C = self.b.dist(self.a)
        vect1 = Vector(self.a, self.b)
        vect2 = Vector(self.a, self.c)
        p1 = Point(self.a.x + vect1.x / vect1.dist() * C * B / (A + B), self.a.y + vect1.y / vect1.dist() * C * B / (A + B))
        p2 = Point(self.a.x + vect2.x / vect2.dist() * B * C / (A + C), self.a.y + vect2.y / vect2.dist() * B * C / (A + C))
        return Line(self.c, p1).cross(Line(self.b, p2))
    
    def bisector(self, p):
        return Line(p, self.bisector_point())
    
    def median_point(self):
        return Line(self.a, Point((self.b.x + self.c.x) / 2, (self.b.y + self.c.y) / 2)).cross(Line(self.b, Point((self.a.x + self.c.x) / 2, (self.a.y + self.c.y) / 2)))
    
    def height_point(self):
        return Line(self.a, Line(self.b, self.c).foot_of_perp(self.a)).cross(Line(self.b, Line(self.a, self.c).foot_of_perp(self.b)))
    
    def mid_perp_point(self):
        line1 = Line(self.a, self.b)
        line2 = Line(self.a, self.c)
        vect1 = Vector(line1.x, line1.y).normal()
        vect2 = Vector(line2.x, line2.y).normal()
        return Line(vect1.x, vect1.y, (self.a.x + self.b.x) / 2, (self.a.y + self.b.y) / 2).cross(Line(vect2.x, vect2.y, (self.a.x + self.c.x) / 2, (self.a.y + self.c.y) / 2))
    
    def r_in_circ(self):
        return Line(self.a, self.b).dist(self.bisector_point())
    
    def r_out_circ(self):
        return self.a.dist(self.mid_perp_point())
    
    def p_in_tri(self, p):
        if Line(self.a, self.b).oneLocation(p, self.c) and Line(self.c, self.b).oneLocation(p, self.a) and Line(self.a, self.c).oneLocation(p, self.b):
            return True
        return False
    
    def circ_in(self):
        p = self.bisector_point()
        return Circle(p.x, p.y, self.r_in_circ())
    
    def circ_out(self):
        p = self.mid_perp_point()
        return Circle(p.x, p.y, self.r_out_circ())
    
    def min_circ(self):
        alpha = Vector(self.a, self.b) ** Vector(self.a, self.c)
        beta = Vector(self.b, self.c) ** Vector(self.b, self.a)
        gamma = math.pi - alpha - beta
        if alpha - math.pi / 2 > -EPS:
            return Circle((self.c.x + self.b.x) / 2, (self.c.y + self.b.y) / 2, self.b.dist(self.c) / 2)
        elif beta - math.pi / 2 > -EPS:
            return Circle((self.a.x + self.c.x) / 2, (self.a.y + self.c.y) / 2, self.a.dist(self.c) / 2)
        elif gamma - math.pi / 2 > -EPS:
            return Circle((self.a.x + self.b.x) / 2, (self.a.y + self.b.y) / 2, self.b.dist(self.a) / 2)
        else:
            p = self.mid_perp_point()
            return Circle(p.x, p.y, self.r_out_circ())
    
    def cross(self, sec):
        return Section(self.a, self.b).cross(sec) + Section(self.a, self.c).cross(sec) + Section(self.c, self.b).cross(sec)


def ClosestElement(p):
    lol = elements + allP
    minDist = p.dist(lol[0])
    res = lol[0]
    for i in lol:
        if p.dist(i) < minDist:
            minDist = p.dist(i)
            res = i
    if minDist < 25: 
        return res


def ClosestPoint(p):
    if len(allP) > 0:
        minDistP = p.dist(allP[0])
        p2 = allP[0]
        for P in allP:
            if p.dist(P) <= minDistP:
                minDistP = p.dist(P)
                p2 = P
        if minDistP < 30:
            return p2
            


def delete(el):
    ind = allEl.index(el)
    for i in dependents[ind]:
        delete(allEl[i])
    for i in dependents_from[ind]:
        dependents[i].remove(ind)
    if el.__class__.__name__ == "DrawPoint":
        allP.remove(el)
    else:
        elements.remove(el)
    allEl[ind] = None


def crosses(light):
    crosses = []
    for i in range(0, len(light) - 1):
        for j in range(i + 1, len(light)):
            if light[i].el.__class__.__name__ == "DrawCircle" or light[j].el.__class__.__name__ == "DrawCircle" or light[i].el.__class__.__name__ == "DrawTriangle" or light[j].el.__class__.__name__ == "DrawTriangle":
                crosses += light[i].el.cross(light[j].el)
            else:
                crosses.append(Point(light[i].el.cross(light[j].el)))
    return crosses


def isNotIn(el, light):
    if el.__class__.__name__ == "Line" or el.__class__.__name__ == "DrawLine":
        for i in light:
            if i.el.__class__.__name__ == "Line" or i.el.__class__.__name__ == "DrawLine":
                if i.el.is_parallel(el) == 1:
                    return False
                return True
        return True
    else:
        for i in light:
            if i.el.__class__.__name__ == "Line" or i.el.__class__.__name__ == "DrawLine":
                kek = 0
            elif el == i.el:
                return False
        return True


def CreateNewPoint(x, y):
    global dependents, dependents_from
    p = DrawPoint(x, y)
    p1 = 0
    lol = []
    for g in allEl:
        if g is not None:
            lol.append(g)
    if len(lol) > 0:
        for j in allEl:
            if j is not None:
                minDist = p.dist(j)
                depEl = j
        for i in allEl:
            if i is not None:
                dist = p.dist(i)
                if dist <= minDist:
                    minDist = dist
                    if i.__class__.__name__ == "DrawLine":
                        depEl = i
                        p1 = i.foot_of_perp(p)
                        p1 = DrawPoint(p1.x, p1.y)
                    elif i.__class__.__name__ == "DrawPoint":
                        depEl = i
                        p1 = i
                    elif i.__class__.__name__ == "DrawCircle":
                        depEl = i
                        points = (Line(p, i).cross(i))
                        if points[0].dist(p) - points[1].dist(p) > EPS:
                            p1 = points[1]
                        else:
                            p1 = points[0]
                    elif i.__class__.__name__ == "DrawTriangle":
                        depEl = i
                        p1 = DrawPoint(i.nearPoint(p))
            
        minDistP = allP[0].dist(p)
        p2 = allP[0]
        for P in allP:
            if p.dist(P) <= minDistP:
                minDistP = p.dist(P)
                p2 = P
        if minDistP < 30:
            return allEl.index(p2)
        elif minDist < 15:
            if p1 in allEl:
                dependents_from[allEl.index(p1)].append(allEl.index(depEl))
                dependents[allEl.index(depEl)].append(allEl.index(p1))
            else:
                allEl.append(p1)
                allP.append(p1)
                dependents[allEl.index(p1)] = []
                dependents_from[allEl.index(p1)] = []
            return allEl.index(p1)
        else:
            allP.append(p)
            allEl.append(p)
            dependents[allEl.index(p)] = []
            dependents_from[allEl.index(p)] = []
            return allEl.index(p)
    else:
        allP.append(p)
        allEl.append(p)
        dependents[allEl.index(p)] = []
        dependents_from[allEl.index(p)] = []
        return allEl.index(p)


class DrawPoint(Point):
    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 4)


class DrawCircle(Circle):
    def __init__(self, types, points):
        self.types = types
        if self.types == "circle":
            self.p1 = points[0]
            self.p2 = points[1]
            super().__init__(allEl[self.p1].x, allEl[self.p1].y, allEl[self.p1].dist(allEl[self.p2]))
        elif self.types == "circ_in":
            self.tri = points
        elif self.types == "circ_out":
            self.tri = points
    def draw(self):
        if self.types == "circle":
            super().__init__(allEl[self.p1].x, allEl[self.p1].y, allEl[self.p1].dist(allEl[self.p2]))
        elif self.types == "circ_in":
            circ = allEl[self.tri].circ_in()
            super().__init__(circ.x, circ.y, circ.r + 0.00001)
        elif self.types == "circ_out":
            circ = allEl[self.tri].circ_out()
            super().__init__(circ.x, circ.y, circ.r)
        if self.r > 4:
            pygame.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), int(self.r), 4)  


class DrawLine(Line):
    def __init__(self, types, points, p=None):
        self.types = types
        if self.types == "line":
            self.p1 = points[0]
            self.p2 = points[1]
            super().__init__(allEl[self.p1], allEl[self.p2])
        
        elif self.types == "perp":
            self.line = points
            self.p = p
        
        elif self.types == "paral":
            self.line = points
            self.p = p
    
    def draw(self):
        if self.types == "line":
            super().__init__(allEl[self.p1], allEl[self.p2])
        elif self.types == "perp":
            super().__init__(allEl[self.line].y, -allEl[self.line].x, allEl[self.p].x, allEl[self.p].y)
        elif self.types == "paral":
            super().__init__(allEl[self.line].x, allEl[self.line].y, allEl[self.p].x, allEl[self.p].y)
        
        if abs(self.A) > EPS:
            pygame.draw.line(screen, (255, 255, 255), (-self.C / self.A - 2000 * self.x, -2000 * self.y), (-self.C / self.A + 2000 * self.x, 2000 * self.y), 3)
        else:
            pygame.draw.line(screen, (255, 255, 255), (-2000 * self.x, -self.C / self.B -2000 * self.y), (2000 * self.x, -self.C / self.B + 2000 * self.y), 3)


class DrawTriangle(Triangle):
    def __init__(self, points):
        self.p1 = points[0]
        self.p2 = points[1]
        self.p3 = points[2]
        super().__init__(allEl[self.p1], allEl[self.p2], allEl[self.p3])
    def draw(self):
        super().__init__(allEl[self.p1], allEl[self.p2], allEl[self.p3])
        pygame.draw.polygon(screen, (255, 255, 255), [(self.a.x, self.a.y), (self.b.x, self.b.y), (self.c.x, self.c.y)], 3)


class DrawLighter():
    def __init__(self, el):
        self.el = el
    def draw(self):
        if self.el.__class__.__name__ == "DrawCircle":
            pygame.draw.circle(screen, (0, 255, 0), (int(self.el.x), int(self.el.y)), int(self.el.r), 4)
        
        elif self.el.__class__.__name__ == "DrawLine":
            pygame.draw.line(screen, (0, 255, 0), (-self.el.C / self.el.A - 2000 * self.el.x, -2000 * self.el.y), (-self.el.C / self.el.A + 2000 * self.el.x, 2000 * self.el.y), 3)
        
        elif self.el.__class__.__name__ == "DrawTriangle":
            pygame.draw.polygon(screen, (0, 255, 0), [(self.el.a.x, self.el.a.y), (self.el.b.x, self.el.b.y), (self.el.c.x, self.el.c.y)], 3)



import pygame
pygame.init()
size = (1600, 900)
screen = pygame.display.set_mode(size)

color = (255, 255, 255)


def drawHud():
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 50, 50), 5)
    pygame.draw.line(screen, (255, 255, 255), (10, 10), (40, 40), 5)
    pygame.draw.rect(screen, (255, 255, 255), (50, 0, 100, 50), 5)
    pygame.draw.circle(screen, (255, 255, 255), (75, 25), 20, 4)
    pygame.draw.rect(screen, (255, 255, 255), (100, 0, 50, 50), 5)
    pygame.draw.circle(screen, (255, 255, 255), (125, 25), 4, 0)
    pygame.draw.rect(screen, (255, 255, 255), (150, 0, 50, 50), 5)
    pygame.draw.polygon(screen, (255, 255, 255), [(176, 10), (161, 40), (190, 40)], 5)
    pygame.draw.rect(screen, (255, 255, 255), (200, 0, 50, 50), 5)
    pygame.draw.circle(screen, (255, 255, 255), (225, 25), 15, 2)
    pygame.draw.line(screen, (255, 255, 255), (210, 40), (240, 10), 2)
    pygame.draw.circle(screen, (255, 0, 0), (217, 34), 4, 0)
    pygame.draw.circle(screen, (255, 0, 0), (234, 17), 4, 0)
    pygame.draw.rect(screen, (255, 255, 255), (250, 0, 50, 50), 5)
    pygame.draw.polygon(screen, (255, 255, 255), [(269, 22), (290, 10), (279, 33)], 0)
    pygame.draw.polygon(screen, (255, 255, 255), [(273, 25), (263, 33), (267, 37), (278, 26)], 0)
    pygame.draw.rect(screen, (255, 255, 255), (300, 0, 50, 50), 5)
    pygame.draw.line(screen, (255, 255, 255), (310, 30), (340, 30), 5)
    pygame.draw.line(screen, (255, 255, 255), (325, 10), (325, 40), 5)
    pygame.draw.rect(screen, (255, 255, 255), (350, 0, 50, 50), 5)
    pygame.draw.line(screen, (255, 255, 255), (360, 20), (390, 13), 5)
    pygame.draw.line(screen, (255, 255, 255), (360, 40), (390, 33), 5)
    pygame.draw.rect(screen, (255, 255, 255), (400, 0, 50, 50), 5)
    pygame.draw.circle(screen, (255, 255, 255), (425, 30), 10, 3)
    pygame.draw.polygon(screen, (255, 255, 255), [(410, 40), (425, 10), (440, 40)], 3)
    pygame.draw.rect(screen, (255, 255, 255), (450, 0, 50, 50), 5)
    pygame.draw.circle(screen, (255, 255, 255), (475, 25), 20, 3)
    pygame.draw.polygon(screen, (255, 255, 255), [(460, 35), (475, 5), (490, 35)], 3)

drawHud()
eventType = "None"
mouse = "UP"
points = []
elements = []
allP = []
allEl = []
light = []
dependents = dict()
dependents_from = dict()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEMOTION and mouse == "DOWN" and eventType == "move":
            p = ClosestPoint(Point(event.pos[0], event.pos[1]))
            if p is not None:
                p1 = DrawPoint(Point(event.pos[0], event.pos[1]))
                allEl[allEl.index(p)] = p1
                allP[allP.index(p)] = p1
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse = "UP"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = "DOWN"
            if event.button == 3:
                el = ClosestElement(DrawPoint(event.pos[0], event.pos[1]))
                if el is not None and isNotIn(el, light):
                    light.append(DrawLighter(el))
            
            elif event.button == 2:
                el = ClosestElement(DrawPoint(event.pos[0], event.pos[1]))
                delete(el)
            
            elif event.button == 1:
                event.pos = event.pos
                if event.pos[0] >= 1 and event.pos[0] <= 50 and event.pos[1] >= 0 and event.pos[1] <= 50:
                    eventType = "line"
                    light = []
                    points = []
                elif event.pos[0] >= 51 and event.pos[0] <= 100 and event.pos[1] >= 0 and event.pos[1] <= 50:
                    eventType = "circle"
                    light = []
                    points = []
                elif event.pos[0] >= 101 and event.pos[0] <= 150 and event.pos[1] >= 0 and event.pos[1] <= 50:
                    eventType = "point"
                    light = []
                    points = []
                elif event.pos[0] >= 151 and event.pos[0] <= 200 and event.pos[1] >= 0 and event.pos[1] <= 50:
                    eventType = "triangle"
                    light = []
                    points = []
                elif event.pos[0] >= 201 and event.pos[0] <= 250 and event.pos[1] >= 0 and event.pos[1] <= 50:
                    for i in crosses(light):
                        p = DrawPoint(i)
                        allP.append(p)
                        allEl.append(p)
                        dependents[allEl.index(p)] = []
                        dependents_from[allEl.index(p)] = []
                    light = []
                    points = []
                elif event.pos[0] >= 251 and event.pos[0] <= 300 and event.pos[1] >= 0 and event.pos[1] <= 50:
                    eventType = "move"
                    light = []
                    points = []
                elif event.pos[0] >= 301 and event.pos[0] <= 350 and event.pos[1] >= 0 and event.pos[1] <= 50:
                    eventType = "perp"
                    points = []
                elif event.pos[0] >= 351 and event.pos[0] <= 400 and event.pos[1] >= 0 and event.pos[1] <= 50:
                    eventType = "paral"
                    points = []
                elif event.pos[0] >= 401 and event.pos[0] <= 450 and event.pos[1] >= 0 and event.pos[1] <= 50:
                    for i in light:
                        if i.el.__class__.__name__ != "DrawTriangle":
                                light = []
                        else:
                            circ_in = DrawCircle("circ_in", allEl.index(i.el))
                            elements.append(circ_in)
                            allEl.append(circ_in)
                            dependents_from[allEl.index(circ_in)] = [allEl.index(i.el)]
                            dependents[allEl.index(i.el)].append(allEl.index(circ_in))
                            dependents[allEl.index(circ_in)] = []
                            light = []
                elif event.pos[0] >= 451 and event.pos[0] <= 500 and event.pos[1] >= 0 and event.pos[1] <= 50:
                    for i in light:
                        if i.el.__class__.__name__ != "DrawTriangle":
                                light = []
                        else:
                            circ_out = DrawCircle("circ_out", allEl.index(i.el))
                            elements.append(circ_out)
                            allEl.append(circ_out)
                            dependents_from[allEl.index(circ_out)] = [allEl.index(i.el)]
                            dependents[allEl.index(i.el)].append(allEl.index(circ_out))
                            dependents[allEl.index(circ_out)] = []
                            light = []
                else:
                    if eventType == "point":
                        ind = CreateNewPoint(event.pos[0], event.pos[1])
                
                    elif eventType == "circle":
                        if len(points) == 0:
                            p = CreateNewPoint(event.pos[0], event.pos[1])
                            points.append(p)
                        else:
                            p1 = CreateNewPoint(event.pos[0], event.pos[1])
                            points.append(p1)
                            circle = DrawCircle("circle", points)
                            elements.append(circle)
                            allEl.append(circle)
                            dependents[allEl.index(circle)] = []
                            dependents_from[allEl.index(circle)] = []
                            for p in points:
                                dependents[p].append(allEl.index(circle))
                                dependents_from[allEl.index(circle)].append(p)
                            points = []
                    
                    elif eventType == "line":
                        if len(points) == 0:
                            p = CreateNewPoint(event.pos[0], event.pos[1])
                            points.append(p)
                        else:
                            p1 = CreateNewPoint(event.pos[0], event.pos[1])
                            points.append(p1)
                            line = DrawLine("line", points)
                            elements.append(line)
                            allEl.append(line)
                            dependents[allEl.index(line)] = []
                            dependents_from[allEl.index(line)] = []
                            for p in points:
                                dependents[p].append(allEl.index(line))
                                dependents_from[allEl.index(line)].append(p)
                            points = []
                        
                    elif eventType == "triangle":
                        if len(points) < 2:
                            p = CreateNewPoint(event.pos[0], event.pos[1])
                            points.append(p)
                        else:
                            p1 = CreateNewPoint(event.pos[0], event.pos[1])
                            points.append(p1)
                            triangle = DrawTriangle(points)
                            elements.append(triangle)
                            allEl.append(triangle)
                            dependents[allEl.index(triangle)] = []
                            dependents_from[allEl.index(triangle)] = []
                            for p in points:
                                dependents[p].append(allEl.index(triangle))
                                dependents_from[allEl.index(triangle)].append(p)
                            points = []
                    
                    elif eventType == "perp":
                        for i in light:
                            if i.el.__class__.__name__ != "DrawLine":
                                light = []
                            else:
                                p = CreateNewPoint(event.pos[0], event.pos[1])
                                perp = DrawLine("perp", allEl.index(i.el), p)
                                elements.append(perp)
                                allEl.append(perp)
                                dependents_from[allEl.index(perp)] = [p, allEl.index(i.el)]
                                dependents[p].append(allEl.index(perp))
                                dependents[allEl.index(i.el)].append(allEl.index(perp))
                                dependents[allEl.index(perp)] = []
                                light = []
                    
                    elif eventType == "paral":
                        for i in light:
                            if i.el.__class__.__name__ != "DrawLine":
                                light = []
                            else:
                                p = CreateNewPoint(event.pos[0], event.pos[1])
                                paral = DrawLine("paral", allEl.index(i.el), p)
                                elements.append(paral)
                                allEl.append(paral)
                                dependents[p].append(allEl.index(paral))
                                dependents[allEl.index(i.el)].append(allEl.index(paral))
                                dependents_from[allEl.index(paral)] = [p, allEl.index(i.el)]
                                dependents[allEl.index(paral)] = []
                                light = []
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, size[0], size[1]), 0)
    for e in elements:
        e.draw()
    for i in light:
        i.draw()
    for p in allP:
        DrawPoint(p).draw()
    drawHud()
    pygame.display.update()