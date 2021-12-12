import random

class RecommendedProduct:
    
    def generate_random(self, number):
        
        #initializating list
        randomlist=[]
        
        # loop will run 3 times
        for x in range (3):
            
            # to get proper index reduce the length by 1, coz index starts from 0
            n=random.randint(0,len(number)-1)
            print(n)
            
            # adding to list that random number
            randomlist.append(number[n])
            
            # deleting it from parent list to prevent dublication 
            number.pop(n)
        return randomlist
        
if __name__ == '__main__':
    rp=RecommendedProduct()
    number=10
    
    inputNum=[1,2,3,4,5]
    
    print(len(inputNum))
    randomlist=[]
    #for x in range (3):
        
    rand=rp.generate_random(inputNum)
    #randomlist.append(rand)
    print('\n Random number:{}'.format(rand))
      
    #print(randomlist) 