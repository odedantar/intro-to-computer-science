def max_even_seq(n):
    odds = "13579"
    sequence = str(n)
    
    max_seq = 0
    length = 0
    
    for d in sequence:
        if d in odds: 
            length = 0
            
        else:
            length += 1
            if length > max_seq:
                max_seq = length

    return max_seq