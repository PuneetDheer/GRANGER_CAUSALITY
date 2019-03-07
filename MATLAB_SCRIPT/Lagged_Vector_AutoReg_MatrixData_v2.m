% Lagged_Vector_AutoReg_MatrixData_v2
% This function create a Vector Auto Regression Matrix along with first
% column as 1's for intercept

function [ X , Y_actual ] = Lagged_Vector_AutoReg_MatrixData_v2( lag, column_data )


    [signalLength, channels] = size(column_data);

    rows = signalLength - lag;

    cols = ( lag * channels ) + 1;

    X = zeros( rows , 1 );
    
    Y_actual = zeros( rows, channels );
    
    X(:,1) = 1;

    x = convmtx ( column_data, lag );

    x = x ( lag: end - lag, : );

    x = flipdim ( x, 2 );
    
    X = [X x];
    
    for chan = 1: channels
        
        Y_actual(: , chan) = column_data(lag+1:end, chan);
        
    end


end

