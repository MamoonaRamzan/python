## Two sum
nums=[3,2,4]
target=6
indices=[0,0]
for i in range(0,len(nums)-1):
    sum=0
    print(i)
    for j in range(i+1,len(nums)-1):
        print(j)
        sum=nums[i]+nums[j]
        print(sum)
        print('-----------------')
        if(sum==target):
            indices=[i,j]

print(indices)            
