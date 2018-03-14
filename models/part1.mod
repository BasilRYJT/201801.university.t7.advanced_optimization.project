set VER ordered;
set PAIRS := {i in VER, j in VER: ord(i) < ord(j)};

param weight {(i,j) in PAIRS}>=0;

var X {PAIRS} binary;

minimize Tour_Length: sum {(i,j) in PAIRS} weight[i,j] * X[i,j];

subject to Visit_All {i in VER}:
   sum {(i,j) in PAIRS} X[i,j] + sum {(j,i) in PAIRS} X[j,i] = 2;

# -------

param nSubtours >= 0 integer;
set SUB {1..nSubtours} within VER;

subject to Subtour_Elimination {k in 1..nSubtours}:
   sum {i in SUB[k], j in VER diff SUB[k]} 
      if (i,j) in PAIRS then X[i,j] else X[j,i] >= 2;
