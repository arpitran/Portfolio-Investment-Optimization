from gurobipy import *
def solve(Project,year,K,R,a,b,h,r,w,c,d):

    # Model
    m=Model("Project Invested")

    #D.V.(Decision Variables
    x={}
    for j in year:
        for i in Project:
            x[i,j]=m.addVar(vtype=GRB.BINARY, name='x_%s,%d' %(i,j))

    y={}
    for j in year:
        y[j]=m.addVar(vtype=GRB.CONTINUOUS, name='y_%s' %j)

    m.update()

    # Objective
    m.setObjective(quicksum(quicksum(a[i,j]*x[i,j] for i in Project)for j in year), GRB.MAXIMIZE)

    # Constraints
    for j in year:
        if j==1:
            m.addConstr(y[j]==h-quicksum(b[i,j]*x[i,j] for i in Project))
        else:
            m.addConstr(y[j]==y[j-1]-quicksum(b[i,j]*x[i,j] for i in Project)+ quicksum(a[i,j-1]*x[i,j-1] for i in Project))

    for i in Project:
        m.addConstr(quicksum(x[i,j] for j in year)<=1)

    for j in year:
        m.addConstr(quicksum(r[i]*x[i,j] for i in Project)<=c[j])

    for j in year:
        m.addConstr(quicksum(w[i]*x[i,j] for i in Project)<=d[j])

    for j in year:
        for k in K:
            m.addConstr(quicksum(b[i,j]*x[i,j] for i in R[k])<=0.4*(quicksum(b[i,j]*x[i,j] for i in Project)))

    for j in year:
        if j==1:
            m.addConstr(quicksum(b[i,j]*x[i,j] for i in Project)<=h)
        else:
            m.addConstr(quicksum(b[i,j]*x[i,j] for i in Project)<=y[j-1])
    

    m.optimize()

    print("Maximum profit:%g" %m.objVal)

    for j in year:
        for i in project:
            print(" Project Invested_%s, Year_%d = %d" %(i,j,x[i,j].x))

    for j in year:
        print(" Money left at the end of year_%d=%g" %(j,y[j].x))

    
