% Directionality_Mat

function [ Direction_MAT ] = Directionality_Mat( data, Normalization )

    [Data_Length, Chan]  = size(data);
    
    WinSize = Ask_WindowSize( Data_Length );
    
    Start_Win = 1;
    End_Win = WinSize;
    
    Lp = Ask_LeavePoint( WinSize );
    
    lag = Ask_Lag( WinSize );
    
    tic
   
    Windows = ceil((Data_Length - WinSize + 1)/Lp);
    
    Direction_MAT = zeros( Chan, Chan, Windows );
    
    if strcmp(Normalization,'entire')
        
        data = zscore(data);
        
    elseif strcmp(Normalization, 'temporal')
        
        data = Temporal_Data(data, WinSize, Lp );
        
    elseif strcmp(Normalization, 'none')
        
        data; %raw data
        
    end
    
    for i =1 : Windows
        
        fprintf('\nWindow Number: %d / %d',i,Windows)
        
        WinData = data(Start_Win:End_Win,:);
               
        for chan1 = 1 : (Chan-1)
            
            [self_X_MAT2, self_Y_actual2] = Lagged_Vector_AutoReg_MatrixData_v2(lag, WinData(:,chan1));
            [self_coeff2, self_Y_pred2] = Prediction_Call(self_X_MAT2, self_Y_actual2);
            [selfErr2,~] = MSE_Metric(self_Y_actual2, self_Y_pred2);
            
            for chan2 =  chan1+1 : Chan
                
                [self_X_MAT1, self_Y_actual1] = Lagged_Vector_AutoReg_MatrixData_v2(lag, WinData(:,chan2));
                [self_coeff1, self_Y_pred1] = Prediction_Call(self_X_MAT1, self_Y_actual1);
                [selfErr1,~] = MSE_Metric(self_Y_actual1, self_Y_pred1);
                
                                
                %[joint_XY_MAT , joint_Y_actual] = Lagged_Vector_AutoReg_MatrixData_v2(lag, WinData(:,[chan1,chan2]));
                joint_XY_MAT = [self_X_MAT2 self_X_MAT1(:,2:end)];
                joint_Y_actual = WinData(lag+1:end,[chan1,chan2]);
                [joint_coeff, joint_Y_pred] = Prediction_Call(joint_XY_MAT, joint_Y_actual);
                [jointErr,~] = MSE_Metric(joint_Y_actual, joint_Y_pred);
                    
                D = log(selfErr1/jointErr(2));
                Direction_MAT(chan1,chan2,i) = D;
                
                D = log(selfErr2/jointErr(1));
                Direction_MAT(chan2,chan1,i) = D;
                    
            end    
            
        end
        
        Start_Win = Start_Win + Lp;
        End_Win = End_Win + Lp;
        
    end
    
    fprintf('\n\nDirectionality Matrix Calculation. DONE!')
    fprintf('\n')
    toc
    
end

