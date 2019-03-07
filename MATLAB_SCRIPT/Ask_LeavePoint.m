function [ LeavePoint ] = Ask_LeavePoint( WinSize )

    flag = true;
    
    while flag
        
        str = sprintf('\nPlease Enter the Leave Point in-between the range [1 and %d]:', WinSize);
        
        LeavePoint = input(str);
        
        if LeavePoint >= 1 &&  LeavePoint <= WinSize
            
            flag = false;
            
        else
            
            fprintf('\nNote: Leave Point should be in-between the range: [1, %d]', WinSize)
            
            flag = true;
        
        end
        
    end

end

