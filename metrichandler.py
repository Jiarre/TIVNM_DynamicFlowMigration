import numpy as np

class MetricHandler:
    def __init__(self,net,env,strategyName):
        self.strategyName = strategyName
        self.r2c = []
        self.saturation = []
        self.net = net
        self.env = env
        
    def printStats(self):
        f = open(f"{self.strategyName}.csv", "w+")
        f.write("episode,meanR2C,meanSaturation\n")
        f.close()
        count = 0
        while True:
            yield self.env.timeout(3000)
            f = open(f"{self.strategyName}.csv", "a")
            f.write(f"{count},{np.mean(self.r2c)},{np.mean(self.saturation)}\n")
            self.r2c = []
            self.saturation = []
            count+=1

