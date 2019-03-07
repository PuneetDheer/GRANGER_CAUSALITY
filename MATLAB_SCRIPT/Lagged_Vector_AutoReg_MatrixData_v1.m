% Lagged_Vector_AutoReg_MatrixData_v1
% This function create a Vector Auto Regression Matrix along with first
% column as 1's intercept

function [ X , Y_actual ] = Lagged_Vector_AutoReg_MatrixData_v1( lag, column_data )
    
    first = 2;
    
    last = lag + 1;
    
    [signalLength, channels] = size(column_data);
    
    rows = signalLength - lag;
    
    cols = ( lag * channels ) + 1;
    
    X = zeros( rows , cols ); 
    
    Y_actual = zeros( rows, channels ); 
    
    X(:,1) = 1; %insert one's in 1st column for intercept
    
    lagged_list = lag:signalLength-1;
    
    for chan = 1: channels
        
        for starti = 1 : length(lagged_list)
            
            endi = lagged_list( starti );
            
            X(starti , first : last) = column_data(starti : endi, chan);
        
        end
        
        Y_actual(: , chan) = column_data(lag+1:end, chan);
        
        first = first + lag;
        
        last = last + lag;
    
    end


end

