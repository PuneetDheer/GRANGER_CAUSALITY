% MSE_Metric
% Mean Square Error

function [ mse, error ] = MSE_Metric( actual, predicted )
        
    error = actual - predicted; %residuals
    
    %mse = mean( error.^2 ); %assuming the mean of error is zero ~N(0,var)
    
    mse = var(  error );

end

