import pygame as p

class boton():
    def __init__(self,x,y, imagen, escala):
        anchoImagen = imagen.get_width()
        alturaImagen = imagen.get_height()
        self.escala = escala
        self.imagen = p.transform.scale(imagen,(int(anchoImagen*self.escala), int(alturaImagen*self.escala)))
        self.cuadrado = self.imagen.get_rect()
        self.x = x
        self.y = y
        self.cuadrado.topleft = (self.x,self.y)
        self.clicked = False


    def cambiarImagen(self,imagen):
        anchoImagen = imagen.get_width()
        alturaImagen = imagen.get_height()
        self.imagen = p.transform.scale(imagen, (int(anchoImagen * self.escala), int(alturaImagen * self.escala)))

    def mostrarEnPantalla(self, supercifie):
        accion = False
        supercifie.blit(self.imagen, (self.cuadrado.x, self.cuadrado.y))
        pos = p.mouse.get_pos()
        if self.cuadrado.collidepoint(pos):
            if p.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                accion = True

            if not p.mouse.get_pressed()[0]:
                self.clicked = False
        return accion