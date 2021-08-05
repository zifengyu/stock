import sys


if __name__ == '__main__':
    v, g, r = sys.argv[1:]
    
    a = (1 + float(g)/ 100) / (1 + float(r)/ 100)
    
    for n in [5, 10]:
        total = 0
        for i in range(1, n+1):
            total += a ** i
        print(n, total *float(v))       