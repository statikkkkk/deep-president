def cleanup(s):
    count=0
    i=0
    while i<len(s)-1:
        
        if s[i] is '.' or s[i] is '!' or s[i] is '?':  #capitalize first character of a setence 
            s1=s[i+1].upper()
            s=s[0:i+1]+s1+s[i+2:]
            count+=1
            if count is 1:  #delete all things before the first full stop
                s=s1+s[i+2:]
          
        i+=1
        
    return s



def main():
    cleanup('dihbiiiuhfkdg.dfonvoeinvoeivn.ffefef.fevkjebvkewrjvbwei')
    
    

# main()

