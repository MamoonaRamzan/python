## pick second largest number
arr=[9,9,9,9,9]
arr.sort()
print(arr)

arr.reverse()
print(arr)

def pick(arr):
    if(len(arr)==1):
        return -1
    if(arr[0]>arr[1]):
        return arr[1]
    else:
        return pick(arr[1:len(arr)-1])

print(pick(arr))