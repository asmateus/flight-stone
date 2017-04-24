from collections import namedtuple

# Node positions
Node = namedtuple('Node', ['x', 'y', 'z'])
n2 = Node(8,4,3)
n3 = Node(9,8,1)
n4 = Node(6,-7,8)

# Distance from target
d1 = 18.138357
d2 = 9.273618
d3 = 8.306624
d4 = 18.05547

# Data validation
if (n2.x == 0) or ((n3.x/n2.x)*n2.y - n3.y == 0) or ((n4.x/n2.x)*n2.y - n4.y == 0):
    quit()

# Equation variables
A2 = d2**2 - d1**2 - n2.x**2 - n2.y**2 - n2.z**2
A3 = d3**2 - d1**2 - n3.x**2 - n3.y**2 - n3.z**2
A4 = d4**2 - d1**2 - n4.x**2 - n4.y**2 - n4.z**2

C = 1/((n3.x/n2.x)*n2.y - n3.y)
D = A3/2 - (n3.x/(2*n2.x))*A2
E = 1/((n4.x/n2.x)*n2.y - n4.y)
F = A4/2 - (n4.x/(2*n2.x))*A2

# Equations
z = (E*F - D*C)/(C*n3.z - C*(n3.x/n2.x)*n2.z - E*n4.z + E*(n4.x/n2.x)*n2.z)
y = C*(z*n3.z - (n3.x/n2.x)*z*n2.z + D)
x = -(A2/2 + y*n2.y + z*n2.z)/n2.x

print('x',x,'y',y,'z',z)