import pygame
from network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, all_player):
    win.fill((255,255,255))
    for name_player in all_player:
        all_player[name_player].draw(win)
    pygame.display.update()

def main():
    run = True
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()

    if p:
        while run:
            clock.tick(60)
            all_player = n.send(p)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            p.move()
            redrawWindow(win, all_player)
            #redrawWindow(win, p2)

main()