% Temporal_data
% This function perform standardization of temporal data using zscore

function [ zscored_Data ] = Temporal_data( data, WinSize, Lp )

    [Data_Length, ~]  = size(data);
    
    Start_Win = 1;
    End_Win = WinSize;
    zscored_Data =[];
    
    Windows = ceil((Data_Length - WinSize + 1)/Lp);
    
    for i =1 : Windows
        
        zscored_Data = [zscored_Data; zscore(data(Start_Win:End_Win,:))];
        
        Start_Win = Start_Win + Lp;
        End_Win = End_Win + Lp;
        
    end


end

