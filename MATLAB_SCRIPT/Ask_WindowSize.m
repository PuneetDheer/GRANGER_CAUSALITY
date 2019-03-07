function [ WindowSize ] = Ask_WindowSize( Data_Length )


    flag = true;
    
    while flag
        
        fprintf ('\n\n[Length of the given Input data is %d]', Data_Length)
        
        str = sprintf('\nPlease Enter the Moving Window Size [ >= 3 and <= %d]:', Data_Length);
        
        WindowSize = input(str);
        
        if WindowSize >= 3 &&  WindowSize <= Data_Length
            
            flag = false;
        
        else
            
            fprintf('\nNote: Window Size should be in-between the range: [3, %d]', Data_Length)
            
            flag = true;
        
        end
        
    end
    
end

