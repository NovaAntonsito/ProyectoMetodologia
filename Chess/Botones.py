import pygame as p

class boton():
    def __init__(self,x,y, imagen, escala):
        anchoImagen = imagen.get_width()
        alturaImagen = imagen.get_height()
        self.imagen = p.transform.scale(imagen,(int(anchoImagen*escala), int(alturaImagen*escala)))
        self.cuadrado = self.imagen.get_rect()
        self.cuadrado.topleft = (x,y)
        self.clicked = False
    def draw(self,supercifie):
        accion = False
        supercifie.blit(self.imagen, (self.cuadrado.x, self.cuadrado.y))
        pos = p.mouse.get_pos()
        if self.cuadrado.collidepoint(pos):
            if p.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                accion = True


            if p.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return accion