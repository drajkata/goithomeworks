def all_sub_lists(data):
    list_result = []
    for i in range(len(data)):
        for i in range(len(data)):
            data[0:i]
            list_result.append(data[0:i])
        data.remove(data[0])
    print(list_result)
    return list_result
    
data = [1, 2, 3, 4]
all_sub_lists(data)     
            
    