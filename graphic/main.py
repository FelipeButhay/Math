import pygame, os, math
import func
import tkinter as tk

resolution_screen = tk.Tk()
SX = resolution_screen.winfo_screenwidth()
SY = resolution_screen.winfo_screenheight()

SX, SY = int(SX*.7), int(SY*.7)

S_RATIO = SX/SY
direc = os.path.dirname(os.path.abspath(__file__)).replace('\'', '/')

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SX, SY))
pygame.display.set_caption("Calculadora Grafica")
pygame.mouse.get_visible
        
font = tuple(pygame.font.Font(f"{direc}/CONSOLA.TTF", int(x*SY)) for x in [.1, .07, .028, .016])

scales = [n*(10**m) for m in range(-3, 10) for n in (1, 2, 5)]

# CENTER (que cordenada se encuentran en el centro de la pantalla), SIZE (unidades desde un borde de la pantalla al otro en x)
camera = [[0,0], 50]

def get_numeration(size) -> float:
    scale_value = size/20
    true_value = (0, float('inf'))
    for x in scales:
        if abs(x-scale_value) < true_value[1]:
            true_value = (x, abs(x-scale_value))
        
    print(true_value[0])
    return true_value[0]

def xycoord_pixels(center: tuple[float, float], size: float, coordxy: tuple[float, float]) -> tuple[int, int]:
    coordxy = list(coordxy)
    
    coordxy[0] = (coordxy[0]-center[0]+size/2)/size
    coordxy[1] = (coordxy[1]-center[1]+size/(2*S_RATIO))/size
    
    return [int(coordxy[0]*SX), int(SY-(coordxy[1]*SX))]

def pixels_xycoord(center: tuple[float, float], size: float, pixels: tuple[float, float]) -> tuple[int, int]:
    coordxy = [0,0]
    coordxy[0] = center[0] + ((2*pixels[0]-SX)/SX*size)/2
    coordxy[1] = center[1] - ((2*pixels[1]-SY)/SX*size)/2

    return coordxy
    
# LA ESCALA A LA QUE ESTA EL GRAFICO (SEPARACION ENTRE LOS NUMEROS DE REFERENCIA)
numeration = get_numeration(camera[1])

thiccness = lambda condition: 3 if condition else 1

import f_of_x
f = f_of_x.function_f

if __name__ == "__main__":
    value_table = func.get_value_table(f, camera[0], camera[1])

mouse = False
rel_pos_in = [0, 0]

running = (__name__ == "__main__")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEWHEEL:
            if event.dict["y"] != 0:
                camera[1] -= (abs(event.dict["y"])/event.dict["y"]) * (camera[1]/10)
            numeration = get_numeration(camera[1])
            value_table = func.get_value_table(f, camera[0], camera[1])
            
    mouse_pos = pygame.mouse.get_pos()
    mouse_save = mouse
    mouse = pygame.mouse.get_pressed()[0]
    
    if mouse and not mouse_save:
        rel_pos_in = pixels_xycoord(*camera, mouse_pos)
        
    if mouse:
        rel_pos_now = pixels_xycoord(*camera, mouse_pos)
        camera[0][0] -= rel_pos_now[0] - rel_pos_in[0] 
        camera[0][1] -= rel_pos_now[1] - rel_pos_in[1] 
        value_table = func.get_value_table(f, *camera)
        
    screen.fill(tuple(35 for x in range(3)))
    
    for x in range(40): # X NUMBERS
        coords_x = (x-20+camera[0][0]//numeration)*numeration
        num_txt = font[3].render(str(round(coords_x, 3)), True, "white")
        xycoord = xycoord_pixels(*camera, (coords_x, 0))
        screen.blit(num_txt, xycoord)
        
        pygame.draw.line(screen, tuple(100 for x in range(3)), (xycoord[0], 0), (xycoord[0], SY), thiccness(coords_x==0))
            
    for y in range(40): # Y NUMBERS
        coords_y = (y-20+camera[0][1]//numeration)*numeration
        num_txt = font[3].render(str(round(coords_y, 3)), True, "white")
        xycoord = xycoord_pixels(*camera, (0, coords_y))
        screen.blit(num_txt, xycoord)
        
        print(xycoord)
        pygame.draw.line(screen, tuple(100 for x in range(3)), (0, xycoord[1]), (SX, xycoord[1]), thiccness(coords_y==0))
    
    for s in value_table:
        if len(s) < 2:
            continue
        pygame.draw.lines(screen, "red", False, s, 2)
    
    pygame.display.update()
    clock.tick(60)