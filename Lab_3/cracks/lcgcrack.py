class LCGCrack():
    #LCG :=  X_i = (a * X_i-1 + c) mod m
    
    def __init__(self, client, m=2 ** 32, a=None, c=None, ):
        self.client = client
        self.a = a
        self.c = c
        self.m = m
        
        games_played = len(client.real_numbers)
        if games_played < 3:
            for i in range(3 - games_played):
                client.play(1, 1)
            
        self.numbers = client.real_numbers[-3:]
        
    def lcg(self):
        return self.int32((self.numbers[-1] * self.a + self.c) % self.m)
    
    def int32(self, num):
        MAX_INT = 2**31 - 1
        MIN_INT = -2**31
        if num > MAX_INT:
            return MIN_INT + num - MAX_INT - 1
        elif num < MIN_INT:
            return MAX_INT - MIN_INT + num + 1
        else:
            return num
    
    def predict(self):
        # find a_had as Modular multiplicative inverse
        a_hat = pow((self.numbers[-3]-self.numbers[-2]), -1, self.m)
        a_pred = ((self.numbers[-2] - self.numbers[-1]) * a_hat) % self.m
        c_pred = (self.numbers[-1] - a_pred * self.numbers[-2]) % self.m
        
        self.a = a_pred
        self.c = c_pred
        
        pred_num = self.lcg()
        self.numbers.append(pred_num)
        
        return pred_num