import numpy as np
from sklearn.metrics import accuracy_score

class MyLogisticRegression:
    def __init__(self):
        self.coef_=0 
        self.intercept_=0 
        self.w=[] 
        return
        
    def sigmoid(self,s):
        return 1/(1 + np.exp(-s))

    def fit(self,xTrain,yTrain,wInit=0,eta=0.05,tol = 1e-4,max_count=100000):
        N = xTrain.shape[1] ## Số lượng mẫu training
        d = xTrain.shape[0] ##Số lượng hệ số w
        yTrain = yTrain.reshape(-1, 1)
        xTrain = xTrain.T
        xTrain = np.concatenate((np.ones((1, xTrain.shape[1])), xTrain), axis=0)
        if(wInit==0):
            d = xTrain.shape[0]
            N = xTrain.shape[1] 
            wInit = np.random.randn(d, 1) 


        w = [wInit] ## Mảng chứa toàn bộ w trong quá trình training   
        count = 0 
        check_w_after = 1000

        while count < max_count:
            mix_id = np.random.permutation(N)
            for i in mix_id:
                xi = xTrain[:, i].reshape(d, 1)
                yi = yTrain[i]
                zi = self.sigmoid( np.dot(w[-1].T, xi)  )  

                w_new = w[-1] + eta*(yi - zi)*xi
                count += 1

                if count % check_w_after == 0:
                    if np.linalg.norm(w_new - w[-check_w_after]) < tol:
                        print("norm", np.linalg.norm(w_new - w[-check_w_after]))
                        w.append(w_new)
                        return
                  
                w.append(w_new)

        self.w.append(w[-1])   
        self.coef_=np.array(w[-1][1:-1]).reshape(1,-1)
        self.intercept_=w[-1][0]

    def predict(self,xTest):
        xTest=xTest.T
        xTest = np.concatenate((np.ones((1, xTest.shape[1])), xTest), axis=0)
        xTest=xTest.reshape(10,-1)

        return np.concatenate( np.around(self.sigmoid(np.dot(self.w[-1].T, xTest)),0)  )


    def score(self,xTrain,yTrain):
        yTrain = yTrain.reshape(-1, 1)
        xTrain = xTrain.T
        xTrain = np.concatenate((np.ones((1, xTrain.shape[1])), xTrain), axis=0)
        yHat=np.concatenate( np.around(self.sigmoid(np.dot(self.w[-1].T, xTrain)),0))
        score = accuracy_score(yTrain, yHat) 
        return score
