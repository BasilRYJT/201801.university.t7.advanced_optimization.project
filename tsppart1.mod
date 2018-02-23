set VER ordered; #vertices
set EDG:= {i in VER,j in VER: i != j}; # edges 
param weight{EDG} >=0; # weights
var X{EDG} binary;

minimize Tour_Length: sum{(i,j) in EDG} weight[i,j] * X[i,j];

subject to Visit_All{i in VER}:
   sum{(i,j) in EDG} X[i,j] + sum{(j,i) in EDG} X[j,i] = 2;

#   ---
param nSubtours >= 0 integer;
set SUB {1..nSubtours} within VER;

subject to Subtour_Elimination {k in 1..nSubtours}:
   sum {i in SUB[k], j in VER diff SUB[k]} 
      if (i,j) in EDG then X[i,j] else X[j,i] >= 2;