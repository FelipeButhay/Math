def divisores(n: int) -> set[float]:
    divs = []
    n = abs(n)
    for x in range(1, n+1):
        if n/x - int(n/x) == 0:
            divs.extend([x, -x])
            
    return set(divs)
            
def gauss(ti_divs: list, cp_divs: list) -> set[float]:
    combinations = []
    for ti in ti_divs:
        for cp in cp_divs:
            combinations.append(ti/cp)
    
    return set(combinations)
            
def ruffini(poly: list) -> tuple[list, float]:
    divs = gauss(divisores(int(poly[-1])), divisores(int(poly[0])))
    for d in divs:
        new_poly = []
        carry = 0
        for p in poly:
            new_poly.append(p + carry)
            carry = (p + carry)*d
            
        if new_poly[-1] == 0:
            return  new_poly[:-1], d
        
    return None, None

def left_zeros(poly: list) -> list:
    for xx, x in enumerate(poly):
        if x != 0:
            return poly[xx:]
            
def print_poly(poly: list, factors: list) -> None:
    result = "("
    terms = len(poly)-1
    for pp, p in enumerate(poly):
        if p >= 0:
            p = f"+{abs(p)}"
            
        else:
            p = f"-{abs(p)}"

        if terms-pp == 0:
            result += f"{p}"
        elif terms-pp == 1:
            result += f"{p}x"
        else:
            result += f"{p}x^{terms-pp}"

    result += ")"
    for f in factors:
        if f > 0:
            f = f"-{abs(f)}"
        else:
            f = f"+{abs(f)}"
        result += f"(x{f})"

    print(result)
            
polynomial_input = input("Escribir los coeficientes del polinomio separados por espacios: ")

polynomial_input = [int(x) for x in polynomial_input.split(" ")]
polynomial = left_zeros(polynomial_input)

factor_list = []
while len(polynomial) > 2:
    polynomial_save = polynomial
    polynomial, factor = ruffini(polynomial)
    if factor == None:
        print("No es posible seguir factorizando el polinomio ni por ruffini ni por gauss")
        print_poly(polynomial_save, factor_list)
        break
    factor_list.append(factor)
else:
    print("El polinomio factorizado es:")
    print_poly(polynomial, factor_list)