import pygame
import pygame.mixer
import matplotlib.image as mpimg
import numpy as np


def criar_indices(min_i, max_i, min_j, max_j):
    import itertools
    L = list(itertools.product(range(min_i, max_i), range(min_j, max_j)))
    idx_i = np.array([e[0] for e in L])
    idx_j = np.array([e[1] for e in L])
    idx = np.vstack( (idx_i, idx_j) )
    return idx

# d = distância
d = 200


# Read the image
image = mpimg.imread("C:/Users/jalfr/OneDrive/Desktop/MASP/Code/Test/bounding_box/bounding_box_test/img/WEB_JB_MASP_00112_01.jpg")


Xd = criar_indices(-int(image.shape[0]/8), int(image.shape[0]/8), -int(image.shape[1]/8), int(image.shape[1]/8))
Xd = np.vstack((Xd,np.ones((1,Xd.shape[1])) * -100))
cubo = np.vstack((Xd,np.ones((1,Xd.shape[1]))))


# matriz que representa o cubo em três dimensões (vértices)
# cubo = np.array([[-100,-100,-100,1],
#                  [100,-100,-100,1],
#                  [-100,100,-100,1],
#                  [100,100,-100,1]]).T

# print(cubo)

# matriz "pinhole"
M = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,-d],[0,0,-(1/d),0]])

# matriz de translação apenas em Z
Tz = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,350],[0,0,0,1]])

# matriz de translação para o centro da tela
T = np.array([[1,0,0,int(image.shape[0]/4)],[0,1,0,int(image.shape[1]/4)],[0,0,1,0],[0,0,0,1]])

# grau da rotação
a = np.deg2rad(1)

# rotação em X
rx = np.array([[1,0,0,0],[0,np.cos(a),-np.sin(a),0],[0,np.sin(a),np.cos(a),0],[0,0,0,1]])

# rotação em Y
ry = np.array([[np.cos(a),0,-np.sin(a),0],[0,1,0,0],[np.sin(a),0,np.cos(a),0],[0,0,0,1]])

# rotação em Z
rz = np.array([[np.cos(a),-np.sin(a),0,0],[np.sin(a),np.cos(a),0,0],[0,0,1,0],[0,0,0,1]])


# Tamanho da tela e definição do FPS
screen = pygame.display.set_mode((int(image.shape[0]/2), int(image.shape[1]/2)))
clock = pygame.time.Clock()
FPS = 60  # Frames per Second

# Cores básicas
BLACK = (0, 0, 0)
COR_ARESTAS = (224, 61, 20)
laranja = (224, 61, 20)
azul = (24, 8, 199)

# matriz de rotação geral (em todas as direções)
r = rx@ry@rz

# matriz identidade
ident = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

# início da matriz de rotação utilizada no código
R =ident

# lista de possíveis direções da rotação (listas de matrizes de rotação)
direcao = [np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]),np.linalg.inv(ry),ry,rx,np.linalg.inv(rx),rz,np.linalg.inv(rz)]
# índice da matriz de rotação utilizada naquele momento
dir = 0

# pygame rodando
rodando = True

# rotação "free" (contínua) -> False == rotação discreta
free = True

# mudanças na distância
mais_d = False
menos_d = False

while rodando:
    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            # quit
            if event.key == pygame.K_q:
                rodando = False
            # reset do cubo
            elif event.key == pygame.K_r:
                R = ident
                dir = 0

            # mudar a direção que o cubo roda
            elif event.key == pygame.K_d:
                dir = 1
            elif event.key == pygame.K_a:
                dir = 2
            elif event.key == pygame.K_w:
                dir = 3
            elif event.key == pygame.K_s:
                dir = 4
            elif event.key == pygame.K_l:
                dir = 5
            elif event.key == pygame.K_k:
                dir = 6

            # aumenta a distância
            if event.key == pygame.K_UP:
                mais_d = True
            # diminui a distância
            if event.key == pygame.K_DOWN:
                menos_d = True

            # muda o modo da rotação (discreta ou contínua)
            if event.key == pygame.K_f:
                free = not free

                # mudança na cor das arestas pra evidenciar qual o modo atual
                if COR_ARESTAS==laranja:
                    COR_ARESTAS=azul
                else:
                    COR_ARESTAS=laranja

        elif event.type == pygame.MOUSEWHEEL:
            if event.y>0:
                d += 10
            elif event.y<0 and d>1:
                d -= 10

        # se alguma tecla for levantada
        elif event.type == pygame.KEYUP:

            # se o modo não for contínuo, voltar a rotação a identidade
            if not free:
                dir=0
            
            # zera o processod e mudar a distância
            mais_d,menos_d=False,False


    # muda a distância
    if mais_d:
        d+=1
    elif menos_d and d>1:
        d-=1

    # cria a matriz de rotação
    R = direcao[dir]@R
    clock.tick(FPS)
    screen.fill(BLACK)

    # cria a matriz pinhole baseada na nova distância
    M = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,-d],[0,0,-(1/d),0]])

    # E = matriz que aplica todos os efeitos de uma única vez
    E = T @ M @ Tz @ R

    # matriz da projeção do cubo
    proj = E @ cubo



    # break


    for pixel in proj.T:
        screen.set_at((int(pixel[0]/pixel[3]), int(pixel[1]/pixel[3])), COR_ARESTAS)
    
    # rodando = False

    # Update! 0.0
    pygame.display.flip()
    # Update! 1.0
    pygame.display.update()

# Terminar tela
pygame.quit()