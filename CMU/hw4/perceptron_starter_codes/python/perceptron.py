import numpy as np
import math

########################################################################
#######  you should maintain the  return type in starter codes   #######
########################################################################


def perceptron_predict(w, x):
  # Input:
  #   w is the weight vector (d,),  1-d array
  #   x is feature values for test example (d,), 1-d array
  # Output:
  #   the predicted label for x, scalar -1 or 1
  w = w.reshape(w.shape[0], 1)
  x = x.reshape(x.shape[0], 1)
  sum = np.dot(w.transpose(),x)
  if sum > 0:
    return 1
  return -1


def perceptron_train(w0, XTrain, yTrain, num_epoch):
  # Input:
  #   w0 is the initial weight vector (d,), 1-d array
  #   XTrain is feature values of training examples (n,d), 2-d array
  #   yTrain is labels of training examples (n,), 1-d array
  #   num_epoch is the number of times to go through the data, scalar
  # Output:
  #   the trained weight vector, (d,), 1-d array
  w0 = w0.reshape(w0.shape[0], 1)
  yTrain = yTrain.reshape(yTrain.shape[0], 1)
  for epoch in range(0,num_epoch):
    for i in range(0,yTrain.shape[0]):
      new_y = perceptron_predict(w0,XTrain[i])
      if new_y != yTrain[i][0]:
        tmp = np.dot(yTrain[i][0],XTrain[i]) # 1 x 1 * 1 * d
        tmp = tmp.reshape(tmp.shape[0],1)
        w0 = np.add(w0,tmp)
  w0 = w0.reshape(w0.shape[0],)
  return w0


def RBF_kernel(X1, X2, sigma):
  # Input:
  #   X1 is a feature matrix (n,d), 2-d array or 1-d array (d,) when n = 1
  #   X2 is a feature matrix (m,d), 2-d array or 1-d array (d,) when m = 1
    #   sigma is the parameter $\sigma$ in RBF function, scalar
  # Output:
  #   K is a kernel matrix (n,m), 2-d array

  #----------------------------------------------------------------------------------------------
  # Special notes: numpy will automatically convert one column/row of a 2d array to 1d array
  #                which is  unexpected in the implementation
  #                make sure you always return a 2-d array even n = 1 or m = 1
  #                your implementation should work when X1, X2 are either 2d array or 1d array
  #                we provide you with some starter codes to make your life easier
  #---------------------------------------------------------------------------------------------
  if len(X1.shape) == 2:
    n = X1.shape[0]
  else:
    n = 1
    X1 = np.reshape(X1, (1, X1.shape[0]))
  if len(X2.shape) == 2:
    m = X2.shape[0]
  else:
    m = 1  
    X2 = np.reshape(X2, (1, X2.shape[0]))
  K = np.zeros((n,m))
  for i in range(0,X1.shape[0]):
    for j in range(0,X2.shape[0]):
       top = np.sum(np.power(np.subtract(X1[i],X2[j]),2))
       bottom = 2 * sigma * sigma
       K[i][j] = math.exp( - top / bottom )
  return K

def kernel_perceptron_predict(a, XTrain, yTrain, x, sigma):
  # Input:
  #   a is the counting vector (n,),  1-d array
  #   XTrain is feature values of training examples (n,d), 2-d array
  #   yTrain is labels of training examples (n,), 1-d array
  #   x is feature values for test example (d,), 1-d array
  #   sigma is the parameter $\sigma$ in RBF function, scalar
  # Output:
  #   the predicted label for x, scalar -1 or 1
  new_y = 0
  for r in range(0,XTrain.shape[0]):
    # n*m, n = 1, m = d
    if a[r] == 0:
      continue
    if yTrain[r] == 0:
      continue
    new_y += a[r] * yTrain[r] * RBF_kernel(x,XTrain[r],sigma)
  if new_y > 0:
    return 1
  return -1
 
def kernel_perceptron_train(a0, XTrain, yTrain, num_epoch, sigma):
  # Input:
  #   a0 is the initial counting vector (n,), 1-d array
  #   XTrain is feature values of training examples (n,d), 2-d array
  #   yTrain is labels of training examples (n,), 1-d array
  #   num_epoch is the number of times to go through the data, scalar
  #   sigma is the parameter $\sigma$ in RBF function, scalar
  # Output:
  #   the trained counting vector, (n,), 1-d array
  a0 = a0.reshape(a0.shape[0], 1)
  yTrain = yTrain.reshape(yTrain.shape[0], 1)
  for epoch in range(0, num_epoch):
    for i in range(0, yTrain.shape[0]):
      new_y = kernel_perceptron_predict(a0, XTrain, yTrain, XTrain[i], sigma)
      if new_y != yTrain[i][0]:
        a0[i] = a0[i]+1
  a0 = a0.reshape(a0.shape[0], )
  return a0