def value(profit, first_rate, second_rate, dividend_rate, pe, discount_rate):
    p = profit
    total = 0
    dc = 1
    for _ in range(5):
        p = p * (1 + first_rate)
        d = p * dividend_rate
        dc = dc * (1 + discount_rate)
        total += d / dc
        print(p, d, d / dc)
        
    for _ in range(5):
        p = p * (1 + second_rate)
        d = p * dividend_rate
        dc = dc * (1 + discount_rate)
        total += d / dc
        print(p, d, d / dc)
        
    total += (p * pe) / dc
    print(p * pe / dc)
        
    return total