## reverse an array
arr=[1,2,3,4,5,6,7]

end=len(arr)-1
print(end)
print(arr[end])
mid=int(end/2)
print(mid)
print(arr[mid])
print(arr)

for i in range(0,mid):
    temp=arr[i]
    arr[i]=arr[end-i]
    arr[end-i]=temp

print(arr)    


    