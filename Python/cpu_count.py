def fun(num):
    for i in range(0,100):
        for j in range(1,400):
            if (4*i*100.0)/(4*i+j) == num :
                return(i,j)
sum = 0 
for i in range(0,100):
    if fun(i) is not None:
        #print i,fun(i)
        sum += 1
print sum
        