import math

############################################################
################ -- VALORES MODIFICABLES -- ################
############################################################

f  = lambda x: x*math.sin(x)
df = lambda x: x*math.cos(x) + math.sin(x)
rango = (-15, 15)
espacio_entre_aprox = 1

############################################################

aprox = [x for x in range(rango[0], rango[1], espacio_entre_aprox)]
resultados = []

for aa, a in enumerate(aprox[:]):
    while abs(f(a)) > 1e-10:
        try:
            aprox[aa] = a - f(a)/df(a)
        except ZeroDivisionError:
            aprox[aa] = None
            break
        a = aprox[aa]
        
    if aprox[aa] != None:   
        resultados.append(round(aprox[aa], 100))   
    
for x in resultados[:]:
    if not (f(x) < 1e-120) or not (rango[0] < x < rango[1]):
        resultados.remove(x)

resultados = set(resultados)
        
print("las raices de la funcion f(x) son: ", resultados)