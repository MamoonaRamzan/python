# longest common prefix
strs=['flow','flower','flight']
strs.sort()
common_prefix=""
print(common_prefix)
for i in range(len(strs[0])):
    print(strs[0][i])
    print(strs[len(strs)-1][i])
    if(strs[0][i]==strs[len(strs)-1][i]):
        common_prefix=common_prefix + strs[0][i]
    else:
        break

print(common_prefix)        