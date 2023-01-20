from Permutations import perms

A = perms(start={6:7,7:8,8:9,9:6,1:2,2:3,3:1,5:4,4:5})
print(A)
print(A.order)

B = {A, A, A}
print(B)