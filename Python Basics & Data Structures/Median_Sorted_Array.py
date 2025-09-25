## median of two sorted array
num1=[1,2]
num2=[3,4]
merged_array=num1
for i in range(len(num2)):
    merged_array.append(num2[i])

merged_array.sort()

if(len(merged_array)%2==0):
    mid=int(len(merged_array)/2)
    print(mid)
    median=(merged_array[mid-1]+merged_array[mid])/2 
else:
    mid=int(len(merged_array)/2)
    median=merged_array[mid]           
        
print(merged_array)
print(median)
