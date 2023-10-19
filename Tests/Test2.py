def token_parser(s):
    tokens_result = []
    tokens_list = ["*", "/", "-", "+", "(", ")"]
    temp = ""
    for token in s:
        if token in tokens_list:
            tokens_result.append(temp)
            temp = ""
            tokens_result.append(token)
        elif token.isdigit():
            temp += token
    if temp:
        tokens_result.append(temp)
    print(tokens_result)

str = ['2', '+', '34', '-', '5', '*', '3']
token_parser(str)
                
        
    
    
    
        
                
                
                
                
                
                
        
            
            
        
            
            
                
                
            
        
            
    