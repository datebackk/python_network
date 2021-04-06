matrix1 = [[1, 2], [3, 4]]
matrix2 = [[2, 0], [1, 2]]


length = len(matrix1)
result_matrix = [[0 for i in range(length)] for i in range(length)]
for i in range(length):
  for j in range(length):
    for k in range(length):
       result_matrix[i][j] += matrix1[i][k] * matrix2[k][j]

print(result_matrix)