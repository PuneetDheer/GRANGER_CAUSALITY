"""
PLOTING DIRECTIONALITY INDEX

@author: PUNEET DHEER
"""

from matplotlib.widgets import Button
import numpy as np

import matplotlib.pyplot as plt
from itertools import combinations


fig,ax = plt.subplots()
plt.subplots_adjust(bottom = 0.3)

dataDI = DI

index = np.arange(0, dataDI.shape[0],1)

pos_DI= dataDI.copy()
neg_DI = dataDI.copy()

pos_DI[pos_DI <= 0] = np.nan
neg_DI[neg_DI > 0] = np.nan

plt.bar( index, pos_DI[:,0], label = 'X -> Y', color ='b', alpha = 0.6)
plt.bar( index, neg_DI[:,0], label = 'Y -> X', color ='r', alpha = 0.6 )

ax.legend(loc='upper left', ncol=2);

ax.set_title("DI between: %d[X] and %d[Y]" % (0, 1))
ax.set_xlabel("Window No.")
ax.set_ylabel("Directionality Index")
    
  

class D_Index:
    
    dataDM = Direction_MAT
    dataDI = DI
    data_min = 0
    data_max = dataDI.shape[1]-1
    selected = 0
    index = np.arange(dataDI.shape[0])
    combi = list(combinations(range(dataDM.shape[1]),2))
    
    def Next(self, event):
        
        if self.selected >= self.data_max:
            self.selected = self.data_max
            ax.set_title("DI between: %d[X] and %d[Y] \nLast DI reached" % (self.combi[self.selected][0], self.combi[self.selected][1]))
            ax.set_xlabel("Window No.")
            ax.set_ylabel("Directionality Index")
            plt.draw()
            
        else:
            self.selected += 1
            ax.cla()
            ax.bar( index, pos_DI[:,self.selected], label = 'X -> Y', color ='b', alpha = 0.6 )
            ax.bar( index, neg_DI[:,self.selected], label = 'Y -> X', color ='r', alpha = 0.6 )
            ax.legend( loc='upper left', ncol=2 );
            ax.set_title("DI between: %d[X] and %d[Y]" % (self.combi[self.selected][0], self.combi[self.selected][1]))
            ax.set_xlabel("Window No.")
            ax.set_ylabel("Directionality Index")
            plt.draw()
            
            
            
    def Prev(self, event):
        
        if self.selected <= self.data_min:
            self.selected = 0
            ax.set_title('DI between: %d[X] and %d[Y] \nFirst DI reached' % (self.combi[self.selected][0], self.combi[self.selected][1]))
            ax.set_xlabel("Window No.")
            ax.set_ylabel("Directionality Index")
            plt.draw()
            
        else:
            self.selected -= 1
            ax.cla()
            ax.bar( index, pos_DI[:,self.selected], label = 'X -> Y', color ='b', alpha = 0.6 )
            ax.bar( index, neg_DI[:,self.selected], label = 'Y -> X', color ='r', alpha = 0.6 )
            ax.legend( loc='upper left', ncol=2 );
            ax.set_title("DI between: %d[X] and %d[Y]" % (self.combi[self.selected][0], self.combi[self.selected][1]))
            ax.set_xlabel("Window No.")
            ax.set_ylabel("Directionality Index")
            plt.draw()


    


callback = D_Index()
axprev = plt.axes([0.55, 0.05, 0.15, 0.075]) #plt.axes((left, bottom, width, height))
axnext = plt.axes([0.73, 0.05, 0.15, 0.075])

bnext = Button(axnext, 'NEXT')
bnext.on_clicked(callback.Next)

bprev = Button(axprev, 'PREVIOUS')
bprev.on_clicked(callback.Prev)