% Directionality_Index

function [ D ] = Directionality_Index( Direction_MAT )

    tic
    
    [CHAnnels,~,Windows] = size(Direction_MAT);
    
    MAT = Direction_MAT;
    
    TotalD = nchoosek(CHAnnels, 2);
    D = zeros(Windows,TotalD);
    
    ind = 1;
    
    for i = 1: Windows
        
        for chan1 = 1 : (CHAnnels-1)
            
            for chan2 = chan1+1 : CHAnnels
                
                Dir = ( MAT(chan1,chan2,i) - MAT(chan2,chan1,i) ) / ( MAT(chan1,chan2,i) + MAT(chan2,chan1,i) );
                D(i, ind) = Dir;
                ind = ind + 1;
            end
            
        end
        
        ind = 1;
    
    end
    
    fprintf('\nDirectionality Index Calculation. DONE!')
    fprintf('\n')
    toc
    
    
end

