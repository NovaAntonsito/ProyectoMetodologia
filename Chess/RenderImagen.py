import pygame as p

class imagen():
    def __init__(self,x,y, imagen, escala):
        anchoImagen = imagen.get_width()
        alturaImagen = imagen.get_height()
        self.imagen = p.transform.scale(imagen,(int(anchoImagen*escala), int(alturaImagen*escala)))
        self.cuadrado = self.imagen.get_rect()
        self.cuadrado.topleft = (x,y)
    def draw(self,supercifie):
        supercifie.blit(self.imagen, (self.cuadrado.x, self.cuadrado.y))
