import matplotlib.pyplot as plt

def bar(x,y,ax,c,label):
    for i in range(len(x)-1):
        print(x[i],x[i+1])
        print(y[i])
        ax.fill_between([x[i], x[i+1]], y[i], 0, alpha=0.3,color=c, label=label)
    return ax