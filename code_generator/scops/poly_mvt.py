from scop import *
from scop_statement import *

stmt = (
    ScopStatement("stmt")
    .addDomain("[S] -> { S[i, j] : 0 <= i < S and 0 <= j < S }")
    .addSched("{ S[i, j] -> O[i,j] }")
    .addDomAnonymizer("{ S[i,j] -> [i,j] }")
    .addRead("{ S[i, j] -> X1[i] }")
    .addRead("{ S[i, j] -> A[i, j] }")
    .addRead("{ S[i, j] -> Y1[j] }")
    .addWrite("{ S[i, j] -> X1[i] }")
)
