"""
PLOTING CAUSALITY MATRIX

@author: PUNEET DHEER
"""

from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import numpy as np

fig,ax = plt.subplots()
plt.subplots_adjust(bottom = 0.3, right = 0.775)

dataDM = Direction_MAT

cmap = 'jet'

plt.imshow(dataDM[0,:,:], cmap = cmap )
plt.colorbar(ax = ax)

ax.set_xticks(np.arange(0, dataDM.shape[1], 1))
ax.set_yticks(np.arange(0, dataDM.shape[1], 1))
ax.set_title("Window number: %d / %d" % (0, dataDM.shape[0]-1))
ax.set_xlabel("Channel No.")
ax.set_ylabel("Channel No.")
#ax.tick_params(top=True, bottom=False,labeltop=True, labelbottom=False)



class D_MAT:
    
    dataDM = Direction_MAT
    data_min = 0
    data_max = dataDM.shape[0]-1
    selected = 0
    
    def Next(self, event):
        
        if self.selected >= self.data_max:
            self.selected = self.data_max
            ax.set_title("Window number: %d / %d \nLast Window reached" % (self.selected, self.data_max))
            ax.set_xlabel("Channel No.")
            ax.set_ylabel("Channel No.")
            plt.draw()
        else:
            self.selected += 1
            ax.cla()
            ax.imshow(dataDM[self.selected,:,:], cmap = cmap )
            ax.set_xticks(np.arange(0, dataDM.shape[1], 1))
            ax.set_yticks(np.arange(0, dataDM.shape[1], 1))
            ax.set_title("Window number: %d / %d" % (self.selected, self.data_max))
            ax.set_xlabel("Channel No.")
            ax.set_ylabel("Channel No.")
            plt.draw()
            
    def Prev(self, event):
        
        if self.selected <= self.data_min:
            self.selected = 0
            ax.set_title('Window number: %d / %d \nFirst Window reached' % (self.selected, self.data_max))
            ax.set_xlabel("Channel No.")
            ax.set_ylabel("Channel No.")
            plt.draw()
            
        else:
            self.selected -= 1
            ax.cla()
            ax.imshow(dataDM[self.selected,:,:], cmap = cmap )
            ax.set_xticks(np.arange(0, dataDM.shape[1], 1))
            ax.set_yticks(np.arange(0, dataDM.shape[1], 1))
            ax.set_title("Window number: %d / %d" % (self.selected, self.data_max))
            ax.set_xlabel("Channel No.")
            ax.set_ylabel("Channel No.")
            plt.draw()


callback = D_MAT()
axprev = plt.axes([0.55, 0.05, 0.15, 0.075]) #plt.axes((left, bottom, width, height))
axnext = plt.axes([0.73, 0.05, 0.15, 0.075])

bnext = Button(axnext, 'NEXT')
bnext.on_clicked(callback.Next)

bprev = Button(axprev, 'PREVIOUS')
bprev.on_clicked(callback.Prev)