function [ lag ] = Ask_Lag( WinSize )

    flag = true;
    
    while flag
        
        str = sprintf('\nPlease Enter the Lag in-between the range [1 and %d]:', WinSize-2);
        
        lag = input(str);
        
        if lag >= 1 &&  lag <= WinSize-2
            
            flag = false;
        
        else
            
            fprintf('\nNote: Lag should be in-between the range: [1, %d]', WinSize-2);
            
            flag = true;
        
        end
        
    end


end

