% BIVARIATE GRANGER CAUSALITY OLS
%
% INPUT:
% data = column-wise data
% Window Size
% Leave Point (shift the window by leaving the no. of points)
% Lag (Autoregressive order)
% Normalization = 'temporal' or 'entire' or 'none'
% 
% OUTPUT:
% Direction_MAT = window-wise causality matrix
% DI = Directionality index (each column represent pair-wise interaction) 
%
%%
function [ Direction_MAT, DI  ] = Main_Bivariate_GC( data )

    Normalization = 'temporal'; % 'entire' or 'temporal' or 'none'

    Direction_MAT = Directionality_Mat( double(data), Normalization );

    DI = Directionality_Index( Direction_MAT );
    
end
