import numpy as np

try:
    from pracweb.registry import classifier, corrector
except ImportError:
    classifier = lambda x: lambda y: y
    corrector = classifier


#@corrector("independent_optimum")
def independent_optimum(X):
    def optimum_for_one_matrix(Y):
        col_min = np.min(Y,axis = 0)
        col_min[col_min > 0] = 0
        positive_Y = Y - col_min
        res = np.mean(positive_Y,axis=0)/np.max(positive_Y,axis=0)
        return Y[:,np.argmin(res)]
    result = np.empty((X.shape[0],X.shape[1]))
    for i in range(len(X)):
        result[i,:] = optimum_for_one_matrix(X[i])
    return result


#@corrector("dependent_optimum")
def dependent_optimum(X):
    def optimum_for_one_matrix(Y):
        col_min = np.min(Y,axis = 0)
        col_min[col_min > 0] = 0
        positive_Y = Y - col_min
        norm_Y = positive_Y/np.sum(positive_Y,axis=0)
        votes = np.sum(norm_Y,axis=1)
        return Y[:,np.argmax(norm_Y[:,np.argmax(votes)])]
    result = np.empty((X.shape[0],X.shape[1]))
    for i in range(len(X)):
        result[i,:] = optimum_for_one_matrix(X[i])
    return result


def prepare_weights(Y, W):
    N = Y.shape[0]
    D = Y.shape[1]
    if W is None:
        weights = -0.01*np.ones(D)
        weights[0] = 1
        W = np.tile(weights,[N,N])
        i = 0
        for row in W:
            W[i,:] = np.roll(row,i)
            i = i + 1
    if not isinstance(W, np.ndarray):
        W = np.array(W, dtype=float)
    W.shape = (N, N*D)
    return W


#@corrector("true_linear")
def true_correct_linear(X):
    def optimum_for_one_matrix(Y):
        W = prepare_weights(Y, None)
        Y = np.reshape(Y,Y.shape[0]*Y.shape[1],1)
        return np.dot(W,Y)
    result = np.empty((X.shape[0],X.shape[1]))
    for i in range(len(X)):
        result[i,:] = optimum_for_one_matrix(X[i])
    return result


def run_test():
    Y = np.empty((2,2,3))
    Y[0,:,:] = np.array([[ 0.1 ,  0.7 ,  0.15], [ 0.2 ,  0.01 ,  0.8 ]])
    Y[1,:,:] = np.array([[ 0.1 ,  7 ,  0.15], [ 0.2 ,  0.01 ,  0.8 ]])
    print independent_optimum(Y)
    print dependent_optimum(Y)
    print true_correct_linear(Y)


if __name__ == '__main__':
    run_test()
