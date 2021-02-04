
X=input()
arr=[]
while(1):
    temp=input()
    if(temp=='Y'):
        y=input()
        y=y.split(',')
        print(y)
        for i in range(len(y)):
            arr.append(y[i])
        break
    else:
        break
if(len(arr)>0):   
    comm=500*len(arr)
else:
    comm=250
print('TOTAL MEMBERS:',len(arr)+1)
print('COMMISSION DETAILS')

print(X,':',comm)
for z in range(len(arr)):
    print(y[z],":250")



