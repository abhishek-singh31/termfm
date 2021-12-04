import os



data = list(os.walk(os.getcwd()))


# def recurse(index):
    # output = []
   
    # output.append(data[index][0])
    
    # if len(data[index][1]) == 0:
        # output.append([])

    # else:
        # for i in range(len(data[index][1])):
            # output.append(recurse(index+i+1))
        
    # output.append(data[index][2])

    # return output


# out = recurse(0)

# print(out)



# print(data)

for i in data:
    print(i)
