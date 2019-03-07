% Vector_AutoRegression

function [ coefficients, Y_predicted ] = Vector_AutoRegression(  X, Y )

    coefficients = regress ( Y, X );
    
    Y_predicted = X * coefficients;

end

