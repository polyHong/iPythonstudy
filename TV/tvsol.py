# Recover the original image using total variation in-painting
from cvxpy import *
U = Variable(rows,cols)
obj = Minimize(tv(U))
constraints = [mul_elemwise(Known,U) == mul_elemwise(Known,Ucorr)]
prob = Problem(obj,constraints)
# Use SCS to solve the problem
prob.solve(verbose=True, solver=SCS)