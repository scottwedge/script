def fun(value,weight=200,threshold=96.0):
    Load = 10**(((float(threshold)-value)/float(threshold))*weight/100)
    return Load

def result(cpu,mem,disk):
    cpu = fun(cpu)
    mem_cpu = fun(mem) + cpu
    all = fun(disk) + mem_cpu
    print cpu,mem_cpu,all
    return int(all)

def fun_all():
    return (result(95,95,95),result(95,95,95),result(2,2,2))

print fun_all()