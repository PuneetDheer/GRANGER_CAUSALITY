% Prediction_Call
% Prediction of dependent variable

function [ coeff, pred ] = Prediction_Call( X, Y )
    
    [rowX,colX] = size(X);
    
    [rowY,colY] = size(Y);
    
    coeff = zeros(colX, colY);
    
    pred = zeros(rowX, colY);
    
    for chan = 1 : colY
        
        [coeff(:,chan), pred(:,chan)] = Vector_AutoRegression(X,Y(:,chan));
        
    end


end

