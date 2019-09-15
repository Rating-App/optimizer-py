import numpy, scipy.sparse
from sparsesvd import sparsesvd
mat = numpy.random.rand(200, 100)
smat = scipy.sparse.csc_matrix(mat)
ut, s, vt = sparsesvd(smat, 100)
assert numpy.allclose(mat, numpy.dot(ut.T, numpy.dot(numpy.diag(s), vt)))

