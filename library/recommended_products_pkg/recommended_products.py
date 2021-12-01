import random

class RecommendedProduct:
    
    def generate_random(self, number):
        n=random.randint(0,number)
        
        return n
        
if __name__ == '__main__':
    rp=RecommendedProduct()
    number=10
    
    randomlist=[]
    for x in range (3):
        
        rand=rp.generate_random(number)
        randomlist.append(rand)
        print('\n Random number:{}'.format(rand))
      
    print(randomlist) 