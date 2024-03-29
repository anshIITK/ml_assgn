import numpy as np
# This is the only scipy method you are allowed to use
# Use of scipy is not allowed otherwise
from scipy.linalg import khatri_rao
import random as rnd
import time as tm

# SUBMIT YOUR CODE AS A SINGLE PYTHON (.PY) FILE INSIDE A ZIP ARCHIVE
# THE NAME OF THE PYTHON FILE MUST BE submit.py
# DO NOT INCLUDE PACKAGES LIKE SKLEARN, SCIPY, KERAS ETC IN YOUR CODE
# THE USE OF ANY MACHINE LEARNING LIBRARIES FOR WHATEVER REASON WILL RESULT IN A STRAIGHT ZERO
# THIS IS BECAUSE THESE PACKAGES CONTAIN SOLVERS WHICH MAKE THIS ASSIGNMENT TRIVIAL
# THE ONLY EXCEPTION TO THIS IS THE USE OF THE KHATRI-RAO PRODUCT METHOD FROM THE SCIPY LIBRARY
# HOWEVER, NOTE THAT NO OTHER SCIPY METHOD MAY BE USED IN YOUR CODE

# DO NOT CHANGE THE NAME OF THE METHODS solver, get_features, get_renamed_labels BELOW
# THESE WILL BE INVOKED BY THE EVALUATION SCRIPT. CHANGING THESE NAMES WILL CAUSE EVALUATION FAILURE

# You may define any new functions, variables, classes here
# For example, functions to calculate next coordinate or step length

################################
# Non Editable Region Starting #
################################
def get_renamed_labels( y ):
################################
#  Non Editable Region Ending  #
################################

    # Since the dataset contain 0/1 labels and SVMs prefer -1/+1 labels,
    # Decide here how you want to rename the labels
    # For example, you may map 1 -> 1 and 0 -> -1 or else you may want to go with 1 -> -1 and 0 -> 1
    # Use whatever convention you seem fit but use the same mapping throughout your code
    # If you use one mapping for train and another for test, you will get poor accuracy
    y_new = np.where(y==0,-1, 1)
    return y_new.reshape( ( y_new.size, ) )                    # Reshape y_new as a vector

def add_bias(X):
    X = np.c_[X, np.ones(X.shape[0])]
    return X

def create_Features(X):
    return np.cumprod( np.flip( 2 * X - 1 , axis = 1 ), axis = 1 )
################################
# Non Editable Region Starting #
################################
def get_features( X ):
################################
#  Non Editable Region Ending  #
################################
    cf = create_Features(X)
    X = add_bias(cf)
    # Use this function to transform your input features (that are 0/1 valued)
    # into new features that can be fed into a linear model to solve the problem
    # Your new features may have a different dimensionality than the input features
    # For example, in this application, X will be 8 dimensional but your new
    # features can be 2 dimensional, 10 dimensional, 1000 dimensional, 123456 dimensional etc
    # Keep in mind that the more dimensions you use, the slower will be your solver too
    # so use only as many dimensions as are absolutely required to solve the problem
    X_trans = X.T
    X_prod = khatri_rao(X_trans, X_trans)
    phi_X = khatri_rao(X_trans,X_prod)
    X_new = phi_X.T
    return X_new


################################
# Non Editable Region Starting #
################################
def solver( X, y, timeout, spacing ):
    (n, d) = X.shape
    t = 0
    totTime = 0
    
    # W is the model vector and will get returned once timeout happens
    # B is the bias term that will get returned once timeout happens
    # The bias term is optional. If you feel you do not need a bias term at all, just keep it set to 0
    # However, if you do end up using a bias term, you are allowed to internally use a model vector
    # that hides the bias inside the model vector e.g. by defining a new variable such as
    # W_extended = np.concatenate( ( W, [B] ) )
    # However, you must maintain W and B variables separately as well so that they can get
    # returned when timeout happens. Take care to update W, B whenever you update your W_extended
    # variable otherwise you will get wrong results.
    # Also note that the dimensionality of W may be larger or smaller than 9
    
    
    B = 0
    tic = tm.perf_counter()

    X = get_features(X)
    
    lr = 0.1
    n_iters= 0
    C= 0.001
    n_samples, n_features = X.shape
    W = np.zeros(n_features)
    
    
################################
#  Non Editable Region Ending  #
################################

    # You may reinitialize W, B to your liking here e.g. set W to its correct dimensionality
    # You may also define new variables here e.g. step_length, mini-batch size etc

################################
# Non Editable Region Starting #
################################
    while True:
        t = t + 1
        if t % spacing == 0:
            toc = tm.perf_counter()
            totTime = totTime + (toc - tic)
            if totTime > timeout:
                return ( W.reshape( ( W.size, ) ), B, totTime )            # Reshape W as a vector
            else:
                tic = tm.perf_counter()
################################
#  Non Editable Region Ending  #
################################
        n_iters+=1
        randindex = np.random.randint(len(X))
        condition = y[randindex] * (np.dot(X[randindex], W)) >=1
        if(condition):
             W = W- lr/(np.sqrt(n_iters)) * (C * W)
        else:
             W = W- lr/(np.sqrt(n_iters)) * (C * W - np.dot(X[randindex], y[randindex]))
        # Write all code to perform your method updates here within the infinite while loop
        # The infinite loop will terminate once timeout is reached
        # Do not try to bypass the timer check e.g. by using continue
        # It is very easy for us to detect such bypasses which will be strictly penalized
        
        # Note that most likely, you should be using get_features( X ) and get_renamed_labels( y )
        # in this part of the code instead of X and y -- please take care
        
        # Please note that once timeout is reached, the code will simply return W, B
        # Thus, if you wish to return the average model (as is sometimes done for GD),
        # you need to make sure that W, B store the averages at all times
        # One way to do so is to define a "running" variable w_run, b_run
        # Make all GD updates to W_run e.g. W_run = W_run - step * delW (similarly for B_run)
        # Then use a running average formula to update W (similarly for B)
        # W = (W * (t-1) + W_run)/t
        # This way, W, B will always store the averages and can be returned at any time
        # In this scheme, W, B play the role of the "cumulative" variables in the course module optLib (see the cs771 library)
        # W_run, B_run on the other hand, play the role of the "theta" variable in the course module optLib (see the cs771 library)
        
    return ( W.reshape( ( W.size, ) ), B, totTime )            # This return statement will never be reached
