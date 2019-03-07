"""
BIVARIATE GRANGER CAUSALITY OLS
QR Decomposition and np.linalg.solve()

@author: PUNEET DHEER

# INPUT
# data = row-wise data
# Window Size
# Leave Point (shift the window by leaving the no. of points)
# Lag (Autoregressive order)
# Normalization = 'temporal' or 'entire' or None

# OUTPUT
# Direction_MAT = window-wise causality matrix
# DI = Directionality index (each column represent pair-wise interaction) 

"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import random
import time
import scipy


def Lagged_Vector_AutoReg_MatrixData( lag, row_data ):
               
    first = 1
    last = lag + 1
    channels , signalLength = row_data.shape
    rows = row_data.shape[1] - lag
    cols = ( lag * channels ) + 1
    X = np.zeros(( rows , cols )) #Pre-Memory allocation of lagged Previous values in row-wise of each time series
    Y_actual = np.zeros(( rows, channels )) #Actual values in column-wise of each time series
    X[:,0] = 1 #insert one's in 1st column for intercept
    
    for chan in range(channels):
        for start , end in enumerate(range( lag , signalLength )):
            X[start , first : last] = row_data[chan , start : end]
        Y_actual[: , chan] = row_data[chan , lag:]
        first = first + lag
        last = last + lag
    
    return X , Y_actual



def Lagged_Self_AutoReg_MatrixData( lag, row_data ):
    
    self_auto = row_data.reshape(1,len(row_data))
    self_X_mat, self_Y_actual = Lagged_Vector_AutoReg_MatrixData(lag, self_auto)
    
    return self_X_mat, self_Y_actual

    
    
def Vector_AutoRegression( X, Y ):
    
    Q, R = np.linalg.qr(X)
    y = np.dot(Q.T, Y)
    
    #coefficients = np.linalg.inv(R).dot(Q.T).dot(Y)
    coefficients = np.linalg.solve(R, y)
    #coefficients = np.linalg.lstsq(R, y)[0]
    predicted = X.dot(coefficients)
    
    return coefficients, predicted



def Prediction_Call( X, Y ):
    
    coeff = np.zeros( (X.shape[1], Y.shape[1]) )
    pred = np.zeros( (X.shape[0], Y.shape[1]) )
    for chan in range(Y.shape[1]):
        coeff[:,chan], pred[:,chan] = Vector_AutoRegression(X,Y[:,chan])
    
    return coeff, pred



def MSE_Metric( actual, predicted ):
    # Mean square error
    
    error = actual - predicted #residuals
    mse = np.mean( np.square( error ), axis = 0 ) # assuming the mean of error is zero ~N(0,var)
    #mse = np.var(  error , axis = 0, ddof = 0 )
    
    return mse, error



def Directionality_Mat( data, Normalization = None ):
    
    Chan, Data_Length = data.shape
    
    WinSize = Ask_WindowSize( Data_Length )
    
    Start_Win = 0
    End_Win = WinSize
    
    Lp = Ask_LeavePoint( WinSize )
    
    lag = Ask_Lag( WinSize )
    
    start_time = time.time()
    
    Windows = int(np.ceil((Data_Length - WinSize + 1)/float(Lp)))
    
    Direction_MAT = np.zeros(( Windows,Chan,Chan ))
    
    if Normalization == 'entire':
            data = stats.zscore(data, axis = 1, ddof = 0)
    
    for i in range(Windows):
        
        if Normalization == 'temporal':
            WinData = stats.zscore(data[:,Start_Win:End_Win], axis = 1, ddof = 0)
        else:
            WinData = data[:,Start_Win:End_Win] #raw data
        
        for chan1 in range(Chan-1):
            
            self_X_MAT, self_Y_actual = Lagged_Self_AutoReg_MatrixData(lag, WinData[chan1,:])
            self_coeff, self_Y_pred = Prediction_Call(self_X_MAT, self_Y_actual)
            selfErr2,_ = MSE_Metric(self_Y_actual, self_Y_pred)
            
            chan2 = chan1+1
            
            for chan2 in range(chan2,Chan):
                
                self_X_MAT, self_Y_actual = Lagged_Self_AutoReg_MatrixData(lag, WinData[chan2,:])
                self_coeff, self_Y_pred = Prediction_Call(self_X_MAT, self_Y_actual)
                selfErr1,_ = MSE_Metric(self_Y_actual, self_Y_pred)
                
                                
                joint_XY_MAT , joint_Y_actual = Lagged_Vector_AutoReg_MatrixData(lag, WinData[(chan1,chan2),:])
                joint_coeff, joint_Y_pred = Prediction_Call(joint_XY_MAT, joint_Y_actual)
                jointErr,_ = MSE_Metric(joint_Y_actual, joint_Y_pred)
                    
                D = np.log(selfErr1/jointErr[1])
                Direction_MAT[i,chan1,chan2] = D
                
                D = np.log(selfErr2/jointErr[0])
                Direction_MAT[i,chan2,chan1] = D
                    
                    
            
        Start_Win = Start_Win + Lp
        End_Win = End_Win + Lp
    
    print("\n--- %s seconds ---" % (time.time() - start_time))
    
    return Direction_MAT

    
def Directionality_Index( Direction_MAT ):
    
    start_time = time.time()
    
    CHAnnels = Direction_MAT.shape[1]
    Windows = Direction_MAT.shape[0]
    MAT = Direction_MAT
    
    TotalD = scipy.special.comb(MAT.shape[1], 2,exact=True)
    D = np.zeros((MAT.shape[0],TotalD))
    
    ind = 0
    
    for i in range( Windows ):
        
        for chan1 in range( CHAnnels-1 ):
            
            chan2 = chan1+1
            
            for chan2 in range( chan2,CHAnnels ):
                
                Dir = ( MAT[i,chan1,chan2] - MAT[i,chan2,chan1] ) / ( MAT[i,chan1,chan2] + MAT[i,chan2,chan1] )
                D[i, ind] = Dir
                ind += 1
                
        ind = 0
    
    print("\n--- %s seconds ---" % (time.time() - start_time))
    
    return D



def Ask_Lag( WinSize ):
    
    flag = True
    
    while flag:
        lag = int(raw_input("Please Enter the Lag in-between the range [1 "+str(WinSize-2) +'] : '))
        
        if lag >= 1 and  lag <= (WinSize-2):
            flag = False
        else:
            print "\nNote: Lag should be in-between the range: [", 1, WinSize-2,"]"
            flag = True
    
    return lag



def Ask_LeavePoint( WinSize ):
    
    flag = True
    
    while flag:
        LeavePoint = int(raw_input("Please Enter the Leave Point in-between the range [1 "+str(WinSize) +'] : '))
        
        if LeavePoint >= 1 and  LeavePoint <= WinSize:
            flag = False
        else:
            print "\nNote: Leave Point should be in-between the range: [", 1, WinSize,"]"
            flag = True
    
    return LeavePoint



def Ask_WindowSize( Data_Length ):
    
    flag = True
    
    while flag:
        print "\nLength of the given Input data is ["+str(Data_Length) +']'
        WindowSize = int(raw_input("Please Enter the Moving Window Size [ >=3 and <=" +str(Data_Length) + '] : '))
        
        if WindowSize >= 3 and  WindowSize <= Data_Length:
            flag = False
        else:
            print "\nNote: Window Size should be in-between the range: [",3, Data_Length,"]"
            flag = True
    
    return WindowSize



if __name__ == "__main__":
    
#    data = pd.read_csv('sample1.txt', header = None)
#    data = data.iloc[:, :].values
#    data = data.T #Channels Row-wise data
#    data = data[0:10, :] #[chanrowstart:chanrowend, colstart:colend]
   

#Random data    
#    data=[]
#    data=np.empty([4,10001])
#    for j in range(4):
#        for i in range(10001):
#            data[j,i]=(random.randint(1,101))

    
    Normalization = 'temporal' # 'entire' or 'temporal' or None
    
    Direction_MAT = Directionality_Mat( data, Normalization )
            
    DI = Directionality_Index( Direction_MAT ) 
    
    
