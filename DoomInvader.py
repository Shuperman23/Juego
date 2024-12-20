import pygame
import random
import math
from pygame import mixer
import sys
import time
import json

pygame.init()

# Inicializa la pantalla
icono = pygame.image.load("Virus.png")
pygame.display.set_icon(icono)
fondo_juego = pygame.image.load("Fondo.png")
fondos_ani = [
    pygame.image.load("Fondo1.png"),
    pygame.image.load("Fondo2.png"),
    pygame.image.load("Fondo3.png")
]
Fondo_juegoF = pygame.image.load("Fondo4.png")

pantalla = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Doom Invaders")


# Función para cargar y mostrar el fondo en el menú
def fondo_menu():
    fondo_menu_img = pygame.image.load("FondoDooom.jpg")
    pantalla_ancho, pantalla_alto = pantalla.get_size()
    imagen_escalada = pygame.transform.scale(fondo_menu_img, (pantalla_ancho, pantalla_alto))
    pantalla.blit(imagen_escalada, (0, 0))


# Elementos de texto en pantalla
puntaje = 0
vidas_default = 5
vidas = vidas_default
enemigos_eliminados = 0
total_enemigos = 100
enemigos_restantes = total_enemigos
enemigos_generados = 0
inicio_juego = time.time()
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10
fuente_final = pygame.font.Font('freesansbold.ttf', 40)
volumen_global = 0.5



# Clase para crear botones con temática retro demoníaca
class Boton:
    def __init__(self, texto, pos, tamano):
        self.texto = texto
        self.rect = pygame.Rect(pos, tamano)
        self.color_normal = (50, 0, 0)  # Rojo oscuro
        self.color_hover = (200, 0, 0)  # Rojo sangre
        self.color_borde = (255, 69, 0)  # Naranja resplandeciente
        self.color_actual = self.color_normal
        self.fuente = pygame.font.Font("fuentes/UnifrakturCook.ttf", 24)  # Tamaño 24

    def dibujar(self, pantalla):
        # Dibuja el fondo del botón
        pygame.draw.rect(pantalla, self.color_actual, self.rect)

        # Dibuja el borde
        pygame.draw.rect(pantalla, self.color_borde, self.rect, 3)

        # Renderiza el texto
        texto_renderizado = self.fuente.render(self.texto, True, (255, 255, 255))
        pantalla.blit(texto_renderizado, texto_renderizado.get_rect(center=self.rect.center))

    def actualizar(self, posicion_mouse):
        if self.rect.collidepoint(posicion_mouse):
            self.color_actual = self.color_hover
            self.color_borde = (255, 0, 0)  # Intensifica el resplandor
        else:
            self.color_actual = self.color_normal
            self.color_borde = (255, 69, 0)

    def fueClicado(self, posicion_mouse):
        return self.rect.collidepoint(posicion_mouse)

# Función para renderizar el texto con contorno
def render_con_contorno(texto, x, y, fuente, color_texto, color_contorno):
    # Dibuja el contorno
    for dx in [-2, -1, 0, 1, 2]:
        for dy in [-2, -1, 0, 1, 2]:
            pantalla.blit(fuente.render(texto, True, color_contorno), (x + dx, y + dy))
    # Dibuja el texto principal
    pantalla.blit(fuente.render(texto, True, color_texto), (x, y))

# Función para mostrar Lore
def mostrar_lore():
    # Carga de la fuente personalizada
    fuente_lore = pygame.font.Font('fuentes/UnifrakturCook.ttf', 50)  # Aquí se cambia la fuente
    texto_lore = fuente_lore.render("Lore", True, (255, 255, 255))

    # Contorno rojo para el título
    color_contorno = (0, 0, 0)
    texto_lore_contorno = fuente_lore.render("Lore", True, color_contorno)

    # Texto dividido por líneas
    texto_detalle = "El Infierno ha desatado su furia, enviando legiones de horrores más allá de la imaginación: demonios sedientos de sangre, gritos desgarradores de almas atrapadas, y un aire pesado de desesperación. Ahora, eres Doomslayer, enfrentándote a un mal ancestral que no se detendrá hasta consumirlo todo. No puedes huir; la única opción es luchar contra los demonios y contra el propio Infierno, armado con la *poderosa* eres el unico que salvará a toda la humanidad."
    lineas_detalle = dividir_texto_en_lineas(texto_detalle, pygame.font.Font('fuentes/UnifrakturCook.ttf', 24), 700)

    boton_regresar = Boton("Regresar al Menu", (300, 500), (200, 50))
    enLore = True
    while enLore:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_regresar.fueClicado(pygame.mouse.get_pos()):
                    enLore = False
                    return

        posicion_mouse = pygame.mouse.get_pos()
        boton_regresar.actualizar(posicion_mouse)

        fondo = pygame.image.load("FondoDooom.jpg")
        fondo = pygame.transform.scale(fondo, (800, 600))
        pantalla.blit(fondo, (0, 0))

        # Dibuja el contorno rojo del título primero
        pantalla.blit(texto_lore_contorno, (335, 145))
        # Dibuja el título en blanco sobre el contorno
        pantalla.blit(texto_lore, (340, 150))

        # Renderizamos cada línea de texto con la fuente personalizada
        y = 250
        for linea in lineas_detalle:
            texto_linea = pygame.font.Font('fuentes/UnifrakturCook.ttf', 24).render(linea, True, (
            255, 255, 255))  # Usar la fuente personalizada aquí
            # Contorno rojo para el texto
            texto_linea_contorno = pygame.font.Font('fuentes/UnifrakturCook.ttf', 24).render(linea, True,
                                                                                             color_contorno)
            # Dibuja el contorno del texto antes de dibujar el texto en blanco
            pantalla.blit(texto_linea_contorno, (48, y + 2))  # Ajusta la posición del contorno
            pantalla.blit(texto_linea, (50, y))  # Dibuja el texto en blanco sobre el contorno
            y += 30  # Ajusta el espacio entre líneas según sea necesario

        boton_regresar.dibujar(pantalla)
        pygame.display.update()

def reiniciar_juego():
    global puntaje, vidas, vidas_default, enemigos_eliminados, enemigos_restantes, enemigos_generados, inicio_juego
    puntaje = 0
    vidas = vidas_default
    enemigos_eliminados = 0
    enemigos_restantes = total_enemigos
    enemigos_generados = 0
    inicio_juego = time.time()

# Función para mostrar Créditos
def mostrar_creditos():
    # Carga de la fuente personalizada
    fuente_creditos = pygame.font.Font('fuentes/UnifrakturCook.ttf', 50)  # Usamos la fuente personalizada aquí
    color_texto = (255, 255, 255)
    color_contorno = (0, 0, 0)

    # Renderizar el texto con contorno
    def render_con_contorno(texto, x, y, fuente):
        # Dibuja el contorno
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                pantalla.blit(fuente.render(texto, True, color_contorno), (x + dx, y + dy))
        # Dibuja el texto principal
        pantalla.blit(fuente.render(texto, True, color_texto), (x, y))

    # Título de créditos con contorno
    texto_creditos = "Créditos"
    render_con_contorno(texto_creditos, 340, 150, fuente_creditos)

    # Texto dividido por líneas
    texto_detalle = " Proyecto Final Desarrollo de Aplicaciones de ultima generación."  \
                    "\n Juego desarrollado por -@AndrésMolinaRamirez -@MoisésAriasUreña -@RonnyARuizDíaz -@MarcoCordoba *grupo 1* ..." \
                    "\n Música inspirada en el juego de doom original, remasterizada a 8bits y pixelarts realizados por @RonnyARD."
    lineas_detalle = dividir_texto_en_lineas(texto_detalle, pygame.font.Font('fuentes/UnifrakturCook.ttf', 24), 700)  # Fuente personalizada también aquí

    boton_regresar = Boton("Regresar al Menu", (300, 500), (200, 50))
    enCreditos = True
    while enCreditos:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_regresar.fueClicado(pygame.mouse.get_pos()):
                    enCreditos = False
                    return

        posicion_mouse = pygame.mouse.get_pos()
        boton_regresar.actualizar(posicion_mouse)

        fondo = pygame.image.load("FondoDooom.jpg")
        fondo = pygame.transform.scale(fondo, (800, 600))
        pantalla.blit(fondo, (0, 0))

        # Renderizamos cada línea de texto con contorno
        y = 250
        for linea in lineas_detalle:
            render_con_contorno(linea, 50, y, pygame.font.Font('fuentes/UnifrakturCook.ttf', 24))  # Fuente personalizada aquí
            y += 30  # Ajusta el espacio entre líneas según sea necesario

        boton_regresar.dibujar(pantalla)
        pygame.display.update()

# Función para dividir texto en líneas
def dividir_texto_en_lineas(texto, fuente, max_ancho):
    palabras = texto.split()
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        if fuente.size(linea_actual + palabra)[0] <= max_ancho:
            linea_actual += palabra + " "
        else:
            lineas.append(linea_actual)
            linea_actual = palabra + " "

    lineas.append(linea_actual)
    return lineas


def menu_principal():
    global volumen_global
    mixer.music.load("MenuPrincipalJuego.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(volumen_global)

    # Obtén el tamaño de la pantalla para centrar los botones
    pantalla_ancho, pantalla_alto = pantalla.get_size()
    espacio_vertical = 60  # Espacio vertical entre cada botón
    altura_inicial = 100  # Reducir para subir los botones

    # Ajusta las posiciones para que los botones estén centrados horizontalmente
    botonJugar = Boton("Jugar", ((pantalla_ancho - 200) // 2, altura_inicial), (200, 50))
    botonjugarMultijugador = Boton("Multijugador", ((pantalla_ancho - 200) // 2, altura_inicial + espacio_vertical),
                                   (200, 50))
    botonOpciones = Boton("Opciones", ((pantalla_ancho - 200) // 2, altura_inicial + 2 * espacio_vertical), (200, 50))
    botonLore = Boton("Ver Lore", ((pantalla_ancho - 200) // 2, altura_inicial + 3 * espacio_vertical), (200, 50))
    botonCreditos = Boton("Ver Créditos", ((pantalla_ancho - 200) // 2, altura_inicial + 4 * espacio_vertical),
                          (200, 50))
    botonRanking = Boton("Ranking", ((pantalla_ancho - 200) // 2, altura_inicial + 5 * espacio_vertical), (200, 50))
    botonSalir = Boton("Salir", ((pantalla_ancho - 200) // 2, altura_inicial + 6 * espacio_vertical), (200, 50))

    corriendo = True

    while corriendo:
        fondo_menu()  # Mostrar el fondo del menu

        posicion_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botonJugar.fueClicado(posicion_mouse):
                    corriendo = False  # Iniciar juego
                    return "jugar"
                elif botonjugarMultijugador.fueClicado(posicion_mouse):
                    corriendo = False  # Iniciar juego
                    return "Multijugador"
                elif botonLore.fueClicado(posicion_mouse):
                    mostrar_lore()
                elif botonOpciones.fueClicado(posicion_mouse):
                    mostrar_opciones()
                elif botonCreditos.fueClicado(posicion_mouse):
                    mostrar_creditos()
                elif botonRanking.fueClicado(posicion_mouse):
                    mostrar_ranking()
                elif botonSalir.fueClicado(posicion_mouse):
                    pygame.quit()
                    sys.exit()

        botonJugar.actualizar(posicion_mouse)
        botonjugarMultijugador.actualizar(posicion_mouse)
        botonOpciones.actualizar(posicion_mouse)
        botonLore.actualizar(posicion_mouse)
        botonCreditos.actualizar(posicion_mouse)
        botonRanking.actualizar(posicion_mouse)
        botonSalir.actualizar(posicion_mouse)

        botonJugar.dibujar(pantalla)
        botonjugarMultijugador.dibujar(pantalla)
        botonOpciones.dibujar(pantalla)
        botonLore.dibujar(pantalla)
        botonCreditos.dibujar(pantalla)
        botonRanking.dibujar(pantalla)
        botonSalir.dibujar(pantalla)

        pygame.display.update()



def mostrar_pantalla_pausa():
    fuente_pausa = pygame.font.Font('freesansbold.ttf', 50)
    texto_pausa = fuente_pausa.render("Pausa", True, (255, 255, 255))
    pantalla.blit(texto_pausa, (340, 150))

    boton_continuar = Boton("Continuar", (300, 250), (200, 50))
    boton_menu_principal = Boton("Menu Principal", (300, 350), (200, 50))

    enPausa = True
    while enPausa:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_continuar.fueClicado(pygame.mouse.get_pos()):
                    enPausa = False
                elif boton_menu_principal.fueClicado(pygame.mouse.get_pos()):
                    menu_principal()
                    enPausa = False
                    return "menu"

        pantalla.blit(fondo_juego, (0, 0))
        mostrar_puntaje(texto_x, texto_y)
        pantalla.blit(texto_pausa, (340, 150))

        boton_continuar.dibujar(pantalla)
        boton_menu_principal.dibujar(pantalla)

        pygame.display.update()


# Función para mostrar el menú de opciones
def mostrar_opciones():
    global volumen_global
    fuente_opciones = pygame.font.Font('freesansbold.ttf', 50)
    texto_opciones = fuente_opciones.render("Opciones", True, (255, 255, 255))
    pantalla.blit(texto_opciones,
                  (800 // 2 - texto_opciones.get_width() // 2, 100))  # Ajuste en la posición para el título

    volumen = 0.5  # Volumen inicial (50%)
    fuente_volumen = pygame.font.Font('freesansbold.ttf', 30)

    # Anchos de los botones
    ancho_boton_incrementar_volumen = 300
    ancho_boton_disminuir_volumen = 300
    ancho_boton_menu = 300

    # Creación de botones centrados
    boton_incrementar_volumen = Boton("Aumentar Volumen", ((800 - ancho_boton_incrementar_volumen) // 2, 250), (ancho_boton_incrementar_volumen, 50))
    boton_disminuir_volumen = Boton("Disminuir Volumen", ((800 - ancho_boton_disminuir_volumen) // 2, 320), (ancho_boton_disminuir_volumen, 50))
    boton_menu_principal = Boton("Menu Principal", ((800 - ancho_boton_menu) // 2, 390), (ancho_boton_menu, 50))

    enOpciones = True
    while enOpciones:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_incrementar_volumen.fueClicado(pygame.mouse.get_pos()):
                    volumen_global = min(1.0, volumen_global + 0.1)  # Incrementar volumen sin pasar de 1.0
                    pygame.mixer.music.set_volume(volumen_global)
                elif boton_disminuir_volumen.fueClicado(pygame.mouse.get_pos()):
                    volumen_global = max(0.0, volumen_global - 0.1)  # Disminuir volumen sin bajar de 0.0
                    pygame.mixer.music.set_volume(volumen_global)
                elif boton_menu_principal.fueClicado(pygame.mouse.get_pos()):
                    # Regresar al menú principal
                    return

        posicion_mouse = pygame.mouse.get_pos()

        # Actualizar estados de los botones
        boton_incrementar_volumen.actualizar(posicion_mouse)
        boton_disminuir_volumen.actualizar(posicion_mouse)
        boton_menu_principal.actualizar(posicion_mouse)

        # Dibujar fondo
        fondo = pygame.image.load("FondoDooom.jpg")
        fondo = pygame.transform.scale(fondo, (800, 600))
        pantalla.blit(fondo, (0, 0))

        # Dibujar texto y botones
        pantalla.blit(texto_opciones, (800 // 2 - texto_opciones.get_width() // 2, 100))  # Centro del título
        boton_incrementar_volumen.dibujar(pantalla)
        boton_disminuir_volumen.dibujar(pantalla)
        boton_menu_principal.dibujar(pantalla)

        # Mostrar el nivel de volumen
        texto_volumen = fuente_volumen.render(f"Volumen: {int(volumen_global * 100)}%", True, (255, 255, 255))
        pantalla.blit(texto_volumen, (800 // 2 - texto_volumen.get_width() // 2, 200))

        pygame.display.update()



def guardar_ranking(nombre, puntaje, tiempo):
    try:
        with open('ranking.json', 'r') as file:
            ranking = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        ranking = []

    ranking.append({"nombre": nombre, "puntaje": puntaje, "tiempo": tiempo})
    ranking.sort(key=lambda x: (x.get("puntaje", 0), -x.get("tiempo", 0)), reverse=True)

    with open('ranking.json', 'w') as file:
        json.dump(ranking, file)

def mostrar_ranking():
    try:
        with open('ranking.json', 'r') as file:
            ranking = json.load(file)
            print("Ranking cargado:", ranking)  # Depuración
    except (FileNotFoundError, json.JSONDecodeError):
        ranking = []
        print("Error al cargar el ranking")  # Depuración

    # Ordenar el ranking primero por puntaje de forma descendente, luego por tiempo de forma ascendente
    ranking.sort(key=lambda jugador: (-jugador.get('puntaje', 0), jugador.get('tiempo', float('inf'))))

    fuente_ranking = pygame.font.Font('fuentes/PressStart2P.ttf', 24)
    fuente_titulo = pygame.font.Font('fuentes/PressStart2P.ttf', 10)

    color_texto = (0, 0, 0)  # Texto negro
    color_contorno = (255, 255, 255)  # Contorno blanco

    y = 150
    textos = []
    for i, jugador in enumerate(ranking[:7]):
        nombre = jugador.get('nombre', 'Desconocido')
        puntaje = jugador.get('puntaje', 0)
        tiempo = jugador.get('tiempo', 'No especificado')

        texto = f"{i + 1}. {nombre}: {puntaje} - {tiempo}s"
        textos.append((texto, y))
        y += 50

    boton_regresar = Boton("Regresar al Menu", (300, 500), (200, 50))
    enRanking = True
    while enRanking:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_regresar.fueClicado(pygame.mouse.get_pos()):
                    enRanking = False
                    return

        posicion_mouse = pygame.mouse.get_pos()
        boton_regresar.actualizar(posicion_mouse)

        fondo = pygame.image.load("FondoDooom.jpg")
        fondo = pygame.transform.scale(fondo, (800, 600))
        pantalla.blit(fondo, (0, 0))

        for texto, y_pos in textos:
            render_con_contorno(texto, 100, y_pos, fuente_ranking, color_texto, color_contorno)

        boton_regresar.dibujar(pantalla)
        pygame.display.update()


# Función de fin de juego
def texto_final():
    tiempo_transcurrido = int(time.time() - inicio_juego)

    mi_fuente_final = pygame.font.Font('fuentes/PressStart2P.ttf', 25)
    color_texto = (0, 0, 0)
    color_contorno = (255, 255, 255)

    def render_con_contorno(texto, x, y):
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                pantalla.blit(mi_fuente_final.render(texto, True, color_contorno), (x + dx, y + dy))
        pantalla.blit(mi_fuente_final.render(texto, True, color_texto), (x, y))

    render_con_contorno(f"Vidas Perdidas: {vidas_default - vidas}", 100, 200)
    render_con_contorno(f"Enemigos Eliminados: {enemigos_eliminados}", 100, 250)
    render_con_contorno(f"Tiempo: {tiempo_transcurrido}s", 100, 300)
    render_con_contorno(f"Enemigos Restantes: {enemigos_restantes}", 100, 350)

    mixer.music.load("ZombieSpawn.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(0.9)

    boton_intentar = Boton("Intentar de Nuevo", (300, 450), (200, 50))
    boton_menu = Boton("Volver al Menu", (300, 520), (200, 50))

    seleccion = None
    while seleccion is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_intentar.fueClicado(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    seleccion = "intentar"
                elif boton_menu.fueClicado(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    seleccion = "menu"

        boton_intentar.dibujar(pantalla)
        boton_menu.dibujar(pantalla)
        pygame.display.update()

    # Guardar el puntaje y tiempo del jugador
    guardar_ranking(jugador_nombre, puntaje, tiempo_transcurrido)

    return seleccion

#ESTE METODO ES PARA EL FINAL DEL MULTIJUGADOR
def texto_final_Multijugador():
    tiempo_transcurrido = int(time.time() - inicio_juego)

    mi_fuente_final = pygame.font.Font('fuentes/PressStart2P.ttf', 25)
    color_texto = (0, 0, 0)
    color_contorno = (255, 255, 255)

    def render_con_contorno(texto, x, y):
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                pantalla.blit(mi_fuente_final.render(texto, True, color_contorno), (x + dx, y + dy))
        pantalla.blit(mi_fuente_final.render(texto, True, color_texto), (x, y))

    render_con_contorno(f"Vidas Perdidas: {vidas_default - vidas}", 100, 200)
    render_con_contorno(f"Enemigos Eliminados: {enemigos_eliminados}", 100, 250)
    render_con_contorno(f"Tiempo: {tiempo_transcurrido}s", 100, 300)
    render_con_contorno(f"Enemigos Restantes: {enemigos_restantes}", 100, 350)

    mixer.music.load("ZombieSpawn.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(0.9)

    #boton_Turno_Jugador2 = Boton("Listo Jugador 2?", (300, 600), (200, 50))
    boton_intentar = Boton("Jugador 2 preparado", (300, 450), (200, 50))
    boton_menu = Boton("Volver al Menu", (300, 520), (200, 50))

    seleccion = None
    while seleccion is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_intentar.fueClicado(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    seleccion = "intentar"
                elif boton_menu.fueClicado(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    seleccion = "menu"


        #boton_Turno_Jugador2.dibujar(pantalla)
        boton_intentar.dibujar(pantalla)
        boton_menu.dibujar(pantalla)
        pygame.display.update()

    # Guardar el puntaje y tiempo del jugador
    guardar_ranking(jugador_nombre, puntaje, tiempo_transcurrido)

    return seleccion

#ESTE METODO NOS MUESTRA EL JUGADOR QUE GANO
def texto_final_Multijugador_Ganador():
    tiempo_transcurrido = int(time.time() - inicio_juego)

    mi_fuente_final = pygame.font.Font('fuentes/PressStart2P.ttf', 25)
    color_texto = (0, 0, 0)
    color_contorno = (255, 255, 255)

    def render_con_contorno(texto, x, y):

        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                pantalla.blit(mi_fuente_final.render(texto, True, color_contorno), (x + dx, y + dy))
        pantalla.blit(mi_fuente_final.render(texto, True, color_texto), (x, y))


    Ganador = max(record, key=lambda x:x[2])
    Perdedor = min(record, key=lambda x: x[2])
    render_con_contorno(f"1: {Ganador[1]} con {Ganador[2]} puntos " , 50, 300)
    render_con_contorno(f"2: {Perdedor[1]} con {Perdedor[2]} puntos", 50, 350)

    mixer.music.load("ZombieSpawn.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(0.9)

    #boton_Turno_Jugador2 = Boton("Listo Jugador 2?", (300, 600), (200, 50))
    boton_intentar = Boton("Revancha?", (300, 450), (200, 50))
    boton_menu = Boton("Volver al Menu", (300, 520), (200, 50))

    seleccion = None
    while seleccion is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_intentar.fueClicado(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    seleccion = "intentar"
                elif boton_menu.fueClicado(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    seleccion = "menu"


        #boton_Turno_Jugador2.dibujar(pantalla)
        boton_intentar.dibujar(pantalla)
        boton_menu.dibujar(pantalla)
        pygame.display.update()

    # Guardar el puntaje y tiempo del jugador
    guardar_ranking(jugador_nombre, puntaje, tiempo_transcurrido)

    return seleccion

# Ajustar la dificultad
def modificar_dificultad():
    global dificultad, velocidad_maxima, incremento_velocidad, total_enemigos, vidas_default
    dificultad = "Intermedia"  # Definir dificultad por defecto como Intermedia

    # Pantalla
    ancho, alto = 800, 600
    pantalla = pygame.display.set_mode((ancho, alto))

    # Fuente y colores
    fuente_texto = pygame.font.Font('freesansbold.ttf', 32)
    color_borde = (255, 69, 0)

    # Fondo
    fondo = pygame.image.load("FondoDooom.jpg")
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    # Botones
    boton_noob = Boton("Noob", (300, 200), (200, 50))
    boton_intermedio = Boton("Intermedia", (300, 270), (200, 50))
    boton_pesadilla = Boton("Pesadilla", (300, 340), (200, 50))
    boton_volver = Boton("Volver al menú", (300, 410), (200, 50))

    en_modificar_dificultad = True
    while en_modificar_dificultad:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Procesar clic en los botones
            if evento.type == pygame.MOUSEBUTTONDOWN:
                posicion_mouse = pygame.mouse.get_pos()
                if boton_noob.fueClicado(posicion_mouse):
                    # Ajustar parámetros para la dificultad Noob
                    dificultad = "Noob"
                    velocidad_maxima = 0.7  # Velocidad limitada
                    incremento_velocidad = 0.001  # Incremento bajo
                    total_enemigos = 50  # Límite de enemigos
                    vidas_default = 5  # Más vidas para principiantes
                    en_modificar_dificultad = False

                elif boton_intermedio.fueClicado(posicion_mouse):
                    # Ajustar parámetros para la dificultad Intermedio
                    dificultad = "Intermedio"
                    velocidad_maxima = 1.0  # Velocidad estándar
                    incremento_velocidad = 0.005  # Incremento regular
                    total_enemigos = 100  # Límite estándar
                    vidas_default = 3  # Vidas estándar
                    en_modificar_dificultad = False

                elif boton_pesadilla.fueClicado(posicion_mouse):
                    # Ajustar parámetros para la dificultad Pesadilla
                    dificultad = "Pesadilla"
                    velocidad_maxima = float('inf')  # Sin límite de velocidad
                    incremento_velocidad = 0.01  # Aceleración constante
                    total_enemigos = float('inf')  # Enemigos infinitos
                    vidas_default = 1  # Solo una vida
                    en_modificar_dificultad = False

                elif boton_volver.fueClicado(posicion_mouse):
                    # Volver al menú
                    en_modificar_dificultad = False

        # Actualizar los botones
        posicion_mouse = pygame.mouse.get_pos()
        boton_noob.actualizar(posicion_mouse)
        boton_intermedio.actualizar(posicion_mouse)
        boton_pesadilla.actualizar(posicion_mouse)
        boton_volver.actualizar(posicion_mouse)

        # Dibujar la pantalla
        pantalla.blit(fondo, (0, 0))

        # Dibujar encabezado
        texto_encabezado = fuente_texto.render("Selecciona la dificultad:", True, (255, 255, 255))
        pantalla.blit(texto_encabezado, (ancho // 2 - texto_encabezado.get_width() // 2, 100))

        # Dibujar botones
        boton_noob.dibujar(pantalla)
        boton_intermedio.dibujar(pantalla)
        boton_pesadilla.dibujar(pantalla)
        boton_volver.dibujar(pantalla)

        pygame.display.update()


# Ajustes en modificar_vidas()
def modificar_vidas():
    global vidas, vidas_default
    texto_ingreso = ""

    # Pantalla
    ancho, alto = 800, 600
    pantalla = pygame.display.set_mode((ancho, alto))

    # Fuente y colores
    fuente_texto = pygame.font.Font('freesansbold.ttf', 32)
    color_input = (255, 255, 255)
    color_borde = (255, 69, 0)
    color_fondo = (0, 0, 0)

    # Fondo
    fondo = pygame.image.load("FondoDooom.jpg")
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    # Cuadro de texto
    input_rect = pygame.Rect(300, 250, 200, 50)

    # Botón
    boton_confirmar = Boton("Confirmar", (300, 320), (200, 50))

    en_modificar_vidas = True
    while en_modificar_vidas:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Procesar teclas
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:  # Borrar último carácter
                    texto_ingreso = texto_ingreso[:-1]
                elif evento.key == pygame.K_RETURN:  # Confirmar con Enter
                    if texto_ingreso.isdigit():
                        nueva_cantidad = int(texto_ingreso)
                        if 1 <= nueva_cantidad <= 99:  # Limitar rango
                            vidas = nueva_cantidad
                            vidas_default = nueva_cantidad  # Actualiza el valor global
                            print(f"Vidas actualizadas a: {vidas}")
                        en_modificar_vidas = False
                    else:
                        print("Por favor ingrese un número válido.")
                elif evento.unicode.isdigit():  # Solo aceptar números
                    texto_ingreso += evento.unicode

            # Procesar clic en el botón
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_confirmar.fueClicado(pygame.mouse.get_pos()):
                    if texto_ingreso.isdigit():
                        nueva_cantidad = int(texto_ingreso)
                        if 1 <= nueva_cantidad <= 99:
                            vidas = nueva_cantidad
                            vidas_default = nueva_cantidad  # Actualiza el valor global
                            print(f"Vidas actualizadas a: {vidas}")
                        en_modificar_vidas = False
                    else:
                        print("Por favor ingrese un número válido.")

        # Actualizar el botón
        boton_confirmar.actualizar(pygame.mouse.get_pos())

        # Dibujar la pantalla
        pantalla.blit(fondo, (0, 0))

        # Texto informativo
        texto_pedir = fuente_texto.render("Ingrese cantidad de vidas:", True, (255, 255, 255))
        pantalla.blit(texto_pedir, (ancho // 2 - texto_pedir.get_width() // 2, 180))

        # Dibujar cuadro de texto
        pygame.draw.rect(pantalla, color_fondo, input_rect)
        pygame.draw.rect(pantalla, color_borde, input_rect, 2)
        texto_renderizado = fuente_texto.render(texto_ingreso, True, color_input)
        pantalla.blit(texto_renderizado, (input_rect.x + 10, input_rect.y + 10))

        # Dibujar botón
        boton_confirmar.dibujar(pantalla)

        pygame.display.update()


# Función mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje} Vidas: {vidas}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Propiedades del Jugador
# Lista de imágenes del jugador
icono_jugador = [
    pygame.image.load("SLAYER4.png"),
    pygame.image.load("SLAYER5.png"),
    pygame.image.load("SLAYER6.png")
]
num_frames_jugador = len(icono_jugador)

# Inicializar listas de imágenes para la animación al moverse
icono_jugador_derecha = [
    pygame.image.load("SLAYER0.png"),
    pygame.image.load("SLAYER1.png"),
    pygame.image.load("SLAYER2.png"),
    pygame.image.load("SLAYER3.png")
]
icono_jugador_izquierda = [
    pygame.transform.flip(img, True, False) for img in icono_jugador_derecha
]

# Variables del Jugador
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0
jugador_img_index = 2
jugador_animacion_espacio = False  # Indica si la animación de espacio está en progreso
jugador_contador_frames = 0
jugador_direccion = "frente"  # Dirección inicial del jugador


# Función para mostrar el jugador con animación de movimiento
def jugador(x, y):
    if jugador_direccion == "derecha":
        frames = icono_jugador_derecha
    elif jugador_direccion == "izquierda":
        frames = icono_jugador_izquierda
    else:
        frames = icono_jugador  # Imagen estática

    # Asegúrate de que el índice de la imagen está dentro del rango
    actual_index = jugador_img_index % len(frames)

    pantalla.blit(frames[actual_index], (x, y))


# Propiedades de los disparos
# Variables del Disparo
balas = []
icono_bala = pygame.image.load("bala.png")


# Función disparar balas
def disparar_bala(x, y):
    pantalla.blit(icono_bala, (x + 40, y + 10))


# Propiedades de los enemigos
# Cargar imágenes en una lista para ambas direcciones
icono_enemigo_der = [
    pygame.image.load("Zombie0.png"),
    pygame.image.load("Zombie1.png"),
    pygame.image.load("Zombie2.png")
]

icono_enemigo_izq = [
    pygame.transform.flip(img, True, False) for img in icono_enemigo_der
]  # Invertir las imágenes horizontalmente

# Cargar nuevas imágenes de Calaveras
icono_calavera_der = [
    pygame.image.load("Calavera0.png"),
    pygame.image.load("Calavera1.png"),
    pygame.image.load("Calavera2.png")
]

icono_calavera_izq = [
    pygame.transform.flip(img, True, False) for img in icono_calavera_der
]

num_frames_zombie = len(icono_enemigo_der)  # Número de imágenes

num_frames_calavera = len(icono_calavera_der)  # Número de imágenes para calaveras

# Variables del Enemigo
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
estado_explosion = []
tiempo_explosion = []
indice_imagen = []
contador_frames = 0
direccion_enemigo = []
gameover = []
max_enemigos_en_pantalla = 8
cantidad_enemigos = min(total_enemigos, max_enemigos_en_pantalla)

while len(enemigo_x) < max_enemigos_en_pantalla and (enemigos_generados < total_enemigos or dificultad == "Pesadilla"):
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)
    estado_explosion.append(False)  # Estado inicial de "no explotando"
    tiempo_explosion.append(0)  # Contador de tiempo para la explosión
    indice_imagen.append(0)  # Inicializar índice de imagen
    direccion_enemigo.append(True)  # Inicializar dirección derecha
    gameover.append(False) # Check del gameover en false.
# Variables del tiempo de explosión
TIEMPO_EXPLOSION = 60


# Función enemigo
def controla_enemigo(x, y, img_index, direccion, es_calavera):
    if es_calavera:
        if direccion:
            pantalla.blit(icono_calavera_der[img_index], (x, y))
        else:
            pantalla.blit(icono_calavera_izq[img_index], (x, y))
    else:
        if direccion:
            pantalla.blit(icono_enemigo_der[img_index], (x, y))
        else:
            pantalla.blit(icono_enemigo_izq[img_index], (x, y))


# Función detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    return distancia < 27


# Inicializar contador de frames al inicio del juego
contador_frames = 0  # Contador global de frames
jugador_contador_frames = 0  # Contador de frames específico para jugador


def solicitar_nombre_jugador():
    fuente_texto = pygame.font.Font('fuentes/UnifrakturCook.ttf', 20)# Fuente personalizada
    fuente_texto2 = pygame.font.Font('fuentes/UnifrakturCook.ttf', 30)
    color_texto = (0, 0, 0)  # Texto negro
    color_contorno = (255, 255, 255)  # Contorno blanco
    color_borde = (255, 69, 0)
    color_fondo = (0, 0, 0)  # Este se utiliza para el fondo del campo de texto
    color_input = (255, 255, 255)

    input_rect = pygame.Rect(300, 250, 200, 50)
    texto_ingreso = ""

    # Crear el botón de "Regresar al Menú"
    boton_regresar = Boton("Regresar al Menu", (300, 350), (200, 50))

    en_solicitud = True
    while en_solicitud:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    texto_ingreso = texto_ingreso[:-1]
                elif evento.key == pygame.K_RETURN:
                    en_solicitud = False
                elif len(texto_ingreso) < 10:  # Limitar a 9 caracteres
                    texto_ingreso += evento.unicode.upper() # mayus activado

            # Manejar el clic en el botón de regresar
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_regresar.fueClicado(pygame.mouse.get_pos()):
                    return "menu"  # Regresar al menú principal

        # Cargar y dibujar el fondo
        fondo = pygame.image.load("FondoDooom.jpg")
        fondo = pygame.transform.scale(fondo, (800, 600))  # Ajustar el tamaño del fondo
        pantalla.blit(fondo, (0, 0))  # Dibujar el fondo

        # Función para renderizar texto con contorno
        def render_con_contorno(texto, x, y, fuente, color_texto, color_contorno):
            # Dibuja el contorno
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    pantalla.blit(fuente.render(texto, True, color_contorno), (x + dx, y + dy))
            # Dibuja el texto principal
            pantalla.blit(fuente.render(texto, True, color_texto), (x, y))

        # Dibujar el texto "Nombre del jugador:" con contorno
        texto_nombre = "Nombre del jugador"
        render_con_contorno(texto_nombre, input_rect.x - 20, input_rect.y - 40, fuente_texto2, color_texto,
                            color_contorno)

        # Dibujar el campo de texto
        pygame.draw.rect(pantalla, color_fondo, input_rect)
        pygame.draw.rect(pantalla, color_borde, input_rect, 2)
        texto_renderizado = fuente_texto.render(texto_ingreso, True, color_input)
        pantalla.blit(texto_renderizado, (input_rect.x + 10, input_rect.y + 10))

        # Actualizar y dibujar el botón de regreso
        boton_regresar.actualizar(pygame.mouse.get_pos())
        boton_regresar.dibujar(pantalla)

        pygame.display.update()

    return texto_ingreso


def juego():
    global jugador_nombre, volumen_global
    resultado = solicitar_nombre_jugador()
    if resultado == "menu":
        return  # Regresar al menú principal
    jugador_nombre = resultado
    if not jugador_nombre:
        jugador_nombre = "Jugador Anónimo"

    mixer.music.stop()
    mixer.music.load("MusicaFondo.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(volumen_global)
    reiniciar_juego()

    # Reiniciar las variables del juego
    global vidas, puntaje, enemigos_generados, enemigos_restantes, enemigos_eliminados, dificultad
    global jugador_x, jugador_y, jugador_img_index, jugador_animacion_espacio, jugador_direccion, jugador_x_cambio, jugador_contador_frames
    global enemigo_x, enemigo_y, enemigo_x_cambio, enemigo_y_cambio, estado_explosion, tiempo_explosion
    global indice_imagen, direccion_enemigo, gameover, balas, contador_frames  # Asegurar que se pueda modificar el contador de frames

    # Reiniciar las estadisicas del juego
    vidas = vidas_default
    puntaje = 0
    enemigos_generados = 0
    enemigos_restantes = total_enemigos


    # Reiniciar estado del jugador
    jugador_x = 368
    jugador_y = 500
    jugador_x_cambio = 0
    jugador_img_index = 2
    jugador_animacion_espacio = False
    jugador_contador_frames = 0

    # Reiniciar enemigos
    enemigo_x = [random.randint(0, 736) for _ in range(cantidad_enemigos)]
    enemigo_y = [random.randint(50, 200) for _ in range(cantidad_enemigos)]
    enemigo_x_cambio = [0.5 for _ in range(cantidad_enemigos)]
    enemigo_y_cambio = [50 for _ in range(cantidad_enemigos)]
    estado_explosion = [False for _ in range(cantidad_enemigos)]
    tiempo_explosion = [0 for _ in range(cantidad_enemigos)]
    indice_imagen = [0 for _ in range(cantidad_enemigos)]
    direccion_enemigo = [True for _ in range(cantidad_enemigos)]
    gameover = [False for _ in range(cantidad_enemigos)]

    # Reiniciar balas
    balas = []

    en_ejecucion = True
    animacion_mostrada = False
    contador_animacion = 0
    indice_fondo = 0
    fondo_juego_cambiado = False

    while en_ejecucion:

        # Condicion de animación lvl50
        if (enemigos_eliminados >= 50) and not animacion_mostrada:
            if contador_animacion < len(fondos_ani) * 120:
                sonido_risa = mixer.Sound("jaja.mp3")
                sonido_risa.play()
                mixer.music.stop()
                mixer.music.load("lvl100.mp3")
                mixer.music.play(-1)
                mixer.music.set_volume(2.0)
                fondo_actual = fondos_ani[indice_fondo]

                pantalla.blit(fondo_actual, (0, 0))

                if contador_animacion % 120 == 0:
                    indice_fondo = (indice_fondo + 1) % len(fondos_ani)

                contador_animacion += 1
            else:
                animacion_mostrada = True
                if not fondo_juego_cambiado:
                    # Cambiar el fondo del juego
                    Fondo_juegoF = pygame.image.load("Fondo4.png")
                    fondo_juego_cambiado = True

                # Establecer la velocidad de todos los enemigos al máximo
                if dificultad != "Pesadilla":  # Respetar el límite en otros modos
                    if enemigo_x_cambio[j] > 0:
                        enemigo_x_cambio[j] = min(enemigo_x_cambio[j] + incremento_velocidad, velocidad_maxima)
                    else:
                        enemigo_x_cambio[j] = max(enemigo_x_cambio[j] - incremento_velocidad, -velocidad_maxima)
                else:  # En Pesadilla, la velocidad sigue creciendo sin límite
                    if enemigo_x_cambio[j] > 0:
                        enemigo_x_cambio[j] += incremento_velocidad
                    else:
                        enemigo_x_cambio[j] -= incremento_velocidad

            pygame.display.update()
            continue

        # Fondo regular del juego
        if fondo_juego_cambiado:
            pantalla.blit(Fondo_juegoF, (0, 0))
        else:
            pantalla.blit(fondo_juego, (0, 0))

        # Eventos
        for evento in pygame.event.get():
            # Cerrar evento
            if evento.type == pygame.QUIT:
                en_ejecucion = False

            # evento presionar teclas
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador_x_cambio = -1
                    jugador_direccion = "izquierda"
                elif evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = 1
                    jugador_direccion = "derecha"

                if evento.key == pygame.K_SPACE:  # logica del disparo
                    sonido_bala = mixer.Sound("disparo.mp3")
                    sonido_bala.set_volume(0.1)
                    sonido_bala.play()

                    nueva_bala = {
                        "x": jugador_x,
                        "y": jugador_y,
                        "velocidad": -5
                    }
                    balas.append(nueva_bala)

                    # Iniciar animación de espacio
                    jugador_animacion_espacio = True
                    jugador_img_index = 0

                if evento.key == pygame.K_ESCAPE:
                    resultado_pausa = mostrar_pantalla_pausa()
                    if resultado_pausa == "menu":
                        return

            # evento soltar teclas
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = 0
                    jugador_direccion = "frente"

        # Define el incremento de velocidad para los enemigos
        incremento_velocidad = 0.005
        velocidad_maxima = 1.0

        # Mantener constante el número de enemigos en pantalla
        while len(enemigo_x) < max_enemigos_en_pantalla and enemigos_generados < total_enemigos:
            enemigo_x.append(random.randint(0, 736))
            enemigo_y.append(random.randint(50, 200))
            enemigo_x_cambio.append(0.5)
            enemigo_y_cambio.append(50)
            estado_explosion.append(False)
            tiempo_explosion.append(0)
            indice_imagen.append(0)
            direccion_enemigo.append(True)
            gameover.append(False)

        # Modificar la ubicación del enemigo
        for i, enemigo in enumerate(range(len(enemigo_x))):
            if estado_explosion[i]:
                # Cambiar la imagen de explosión según el número de enemigos eliminados
                if enemigos_eliminados >= 50:
                    pantalla.blit(pygame.image.load("Calavera3.png"), (enemigo_x[i], enemigo_y[i]))
                else:
                    pantalla.blit(pygame.image.load("Zombie3.png"), (enemigo_x[i], enemigo_y[i]))
                tiempo_explosion[i] += 1
                if tiempo_explosion[i] > TIEMPO_EXPLOSION:
                    estado_explosion[i] = False
                    tiempo_explosion[i] = 0
                    enemigos_eliminados += 1
                    enemigos_restantes -= 1

                    # Incrementar velocidad de todos los enemigos después de la explosión
                    for j in range(len(enemigo_x_cambio)):
                        # Incrementar solo si no se ha alcanzado la velocidad máxima
                        if enemigo_x_cambio[j] > 0:
                            enemigo_x_cambio[j] = min(enemigo_x_cambio[j] + incremento_velocidad, velocidad_maxima)
                        else:
                            enemigo_x_cambio[j] = max(enemigo_x_cambio[j] - incremento_velocidad, -velocidad_maxima)

                    # Asegurarse de mantener siempre el número de enemigos en pantalla
                    if enemigos_generados < total_enemigos:
                        enemigo_x[i] = random.randint(0, 736)
                        enemigo_y[i] = random.randint(50, 200)
                        enemigos_generados += 1
                    else:
                        # Si un enemigo es eliminado y el total generado ya alcanzó el límite, simplemente respawnéalo
                        enemigo_x[i] = random.randint(0, 736)
                        enemigo_y[i] = random.randint(50, 200)

            else:
                # Para la muerte por colisión
                colision_con_jugador = hay_colision(enemigo_x[i], enemigo_y[i], jugador_x, jugador_y)
                if colision_con_jugador and not gameover[i]:
                    vidas -= 1
                    gameover[i] = True  # Marca al enemigo como "muerto"
                    if vidas > 0:  # Hacer que el enemigo respawnee si aún quedan vidas.
                        enemigo_x[i] = random.randint(0, 736)
                        enemigo_y[i] = random.randint(50, 200)
                        gameover[i] = False  # Reiniciar el estado del enemigo a "activo"

                        # Restablecer otras propiedades necesarias para la colisión
                        estado_explosion[i] = False
                        tiempo_explosion[i] = 0
                        direccion_enemigo[i] = True
                        enemigo_x_cambio[i] = 0.5  # Reinicia la velocidad
                    else:
                        enemigo_x[i] = 1000  # Mandarlo afuera de la pantalla si es gameover

                # Fin del juego si el enemigo llega a la parte inferior
                if enemigo_y[i] > 500 and not gameover[i]:
                    vidas -= 1
                    gameover[i] = True
                    if vidas > 0:  # Hacer que el enemigo respawnee si aún quedan vidas.
                        enemigo_x[i] = random.randint(0, 736)
                        enemigo_y[i] = random.randint(50, 200)
                        gameover[i] = False  # Reiniciar el estado del enemigo a "activo"
                    else:
                        enemigo_x[i] = 1000  # Mandarlo afuera de la pantalla si es gameover

                enemigo_x[i] += enemigo_x_cambio[i]

                # Cambiar dirección en los bordes
                if enemigo_x[i] <= -50:
                    enemigo_x_cambio[i] = abs(enemigo_x_cambio[i])  # Cambiar a positiva
                    enemigo_y[i] += enemigo_y_cambio[i]
                    direccion_enemigo[i] = True  # Cambiar dirección a derecha
                elif enemigo_x[i] >= 736:
                    enemigo_x_cambio[i] = -abs(enemigo_x_cambio[i])  # Cambiar a negativa
                    enemigo_y[i] += enemigo_y_cambio[i]
                    direccion_enemigo[i] = False  # Cambiar dirección a izquierda

                # Colisiones
                for bala in balas:
                    colision_bala_enemigo = hay_colision(enemigo_x[i], enemigo_y[i], bala["x"], bala["y"])
                    if colision_bala_enemigo:
                        sonido_colision = mixer.Sound("ZombieMuerte.mp3")
                        sonido_colision.set_volume(0.3)
                        sonido_colision.play()
                        balas.remove(bala)
                        puntaje += 1
                        estado_explosion[i] = True  # Inicia la explosión
                        break

                # Actualizar índice de imagen para la animación
                es_calavera = enemigos_eliminados >= 50
                if contador_frames % 60 == 0:  # Cambiar imagen cada 60 frames
                    indice_imagen[i] = (indice_imagen[i] + 1) % (
                        num_frames_calavera if es_calavera else num_frames_zombie)

                # Mostrar enemigo solo si no está explotando
                if not estado_explosion[i]:
                    controla_enemigo(enemigo_x[i], enemigo_y[i], indice_imagen[i], direccion_enemigo[i], es_calavera)

        # Incrementar el contador de frames
        contador_frames += 1

        # Animación de jugador
        if jugador_animacion_espacio:
            if jugador_contador_frames % 30 == 0:  # Cambiar imagen cada 30 frames
                jugador_img_index += 1
                if jugador_img_index >= num_frames_jugador:
                    jugador_animacion_espacio = False  # Terminar la animación especial
                    jugador_img_index = 2  # Estado normal del jugador (Humano2)

        if jugador_x_cambio != 0:
            if jugador_contador_frames % 100 == 0:  # Cambiar imagen cada 10 frames
                # Asegurar que no exceda el índice de imágenes de derecha/izquierda
                if jugador_direccion == "derecha":
                    jugador_img_index = (jugador_img_index + 1) % len(icono_jugador_derecha)
                elif jugador_direccion == "izquierda":
                    jugador_img_index = (jugador_img_index + 1) % len(icono_jugador_izquierda)

        jugador_contador_frames += 1

        # Movimiento bala
        for bala in balas:
            bala["y"] += bala["velocidad"]
            pantalla.blit(icono_bala, (bala["x"] + 40, bala["y"] + 10))
            if bala["y"] < 0:
                balas.remove(bala)

        # modificar ubicación del jugador
        jugador_x += jugador_x_cambio

        # mantener dentro de los bordes al jugador
        if jugador_x <= 0:
            jugador_x = 0
        elif jugador_x >= 736:
            jugador_x = 736

        jugador(jugador_x, jugador_y)

        mostrar_puntaje(texto_x, texto_y)

        # Mostrar el final
        if vidas <= 0 or enemigos_restantes <= 0:
            # Cambiar el fondo a Game Over
            fondo = pygame.image.load("GameOver.png")
            fondo = pygame.transform.scale(fondo, (800, 600))
            pantalla.blit(fondo, (0, 0))
            seleccion = texto_final()

            if seleccion == "intentar":
                juego()  # Reiniciando el juego
            elif seleccion == "menu":
                return  # Regresando al jugador al menu

        pygame.display.update()


record=[]
intento = 0
def Juego_Multijugador():
    global jugador_nombre, intento,record, volumen_global
    resultado = solicitar_nombre_jugador()
    if resultado == "menu":
        return  # Regresar al menú principal
    jugador_nombre = resultado
    if not jugador_nombre:
        jugador_nombre = "Jugador Anónimo"

    mixer.music.stop()
    mixer.music.load("MusicaFondo.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(volumen_global)
    reiniciar_juego()

    # Reiniciar las variables del juego
    global vidas, puntaje, enemigos_generados, enemigos_restantes, enemigos_eliminados
    global jugador_x, jugador_y, jugador_img_index, jugador_animacion_espacio, jugador_direccion, jugador_x_cambio, jugador_contador_frames
    global enemigo_x, enemigo_y, enemigo_x_cambio, enemigo_y_cambio, estado_explosion, tiempo_explosion
    global indice_imagen, direccion_enemigo, gameover, balas, contador_frames  # Asegurar que se pueda modificar el contador de frames

    # Inicializar las condiciones del juego
    dificultad = "Pesadilla"
    velocidad_maxima = float('inf')  # Sin límite de velocidad
    incremento_velocidad = 0.01  # Aceleración constante
    total_enemigos = float('inf')  # Enemigos infinitos
    vidas_default = 1  # Solo una vida
    en_modificar_dificultad = False

    # Reiniciar las estadisicas del juego
    vidas = vidas_default
    puntaje = 0
    enemigos_generados = 0
    enemigos_restantes = total_enemigos


    # Reiniciar estado del jugador
    jugador_x = 368
    jugador_y = 500
    jugador_x_cambio = 0
    jugador_img_index = 2
    jugador_animacion_espacio = False
    jugador_contador_frames = 0

    # Reiniciar enemigos
    enemigo_x = [random.randint(0, 736) for _ in range(cantidad_enemigos)]
    enemigo_y = [random.randint(50, 200) for _ in range(cantidad_enemigos)]
    enemigo_x_cambio = [0.5 for _ in range(cantidad_enemigos)]
    enemigo_y_cambio = [50 for _ in range(cantidad_enemigos)]
    estado_explosion = [False for _ in range(cantidad_enemigos)]
    tiempo_explosion = [0 for _ in range(cantidad_enemigos)]
    indice_imagen = [0 for _ in range(cantidad_enemigos)]
    direccion_enemigo = [True for _ in range(cantidad_enemigos)]
    gameover = [False for _ in range(cantidad_enemigos)]

    # Reiniciar balas
    balas = []


    en_ejecucion = True
    animacion_mostrada = False
    contador_animacion = 0
    indice_fondo = 0
    fondo_juego_cambiado = False

    while en_ejecucion and intento<=1:

        # Condicion de animación lvl50
        if (enemigos_eliminados >= 50 or enemigos_restantes <= 50) and not animacion_mostrada:
            if contador_animacion < len(fondos_ani) * 120:
                sonido_risa = mixer.Sound("jaja.mp3")
                sonido_risa.play()
                mixer.music.stop()
                mixer.music.load("lvl100.mp3")
                mixer.music.play(-1)
                mixer.music.set_volume(2.0)
                fondo_actual = fondos_ani[indice_fondo]

                pantalla.blit(fondo_actual, (0, 0))

                if contador_animacion % 120 == 0:
                    indice_fondo = (indice_fondo + 1) % len(fondos_ani)

                contador_animacion += 1
            else:
                animacion_mostrada = True
                if not fondo_juego_cambiado:
                    # Cambiar el fondo del juego
                    Fondo_juegoF = pygame.image.load("Fondo4.png")
                    fondo_juego_cambiado = True

                # Establecer la velocidad de todos los enemigos al máximo
                for j in range(len(enemigo_x_cambio)):
                    if enemigo_x_cambio[j] > 0:
                        enemigo_x_cambio[j] = velocidad_maxima  # Ajustar a la velocidad máxima
                    else:
                        enemigo_x_cambio[j] = -velocidad_maxima  # Ajustar a la velocidad máxima

            pygame.display.update()
            continue

        # Fondo regular del juego
        if fondo_juego_cambiado:
            pantalla.blit(Fondo_juegoF, (0, 0))
        else:
            pantalla.blit(fondo_juego, (0, 0))

        # Eventos
        for evento in pygame.event.get():
            # Cerrar evento
            if evento.type == pygame.QUIT:
                en_ejecucion = False

            # evento presionar teclas
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador_x_cambio = -1
                    jugador_direccion = "izquierda"
                elif evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = 1
                    jugador_direccion = "derecha"

                if evento.key == pygame.K_SPACE:  # logica del disparo
                    sonido_bala = mixer.Sound("disparo.mp3")
                    sonido_bala.set_volume(0.1)
                    sonido_bala.play()

                    nueva_bala = {
                        "x": jugador_x,
                        "y": jugador_y,
                        "velocidad": -5
                    }
                    balas.append(nueva_bala)

                    # Iniciar animación de espacio
                    jugador_animacion_espacio = True
                    jugador_img_index = 0

                if evento.key == pygame.K_ESCAPE:
                    resultado_pausa = mostrar_pantalla_pausa()
                    if resultado_pausa == "menu":
                        return

            # evento soltar teclas
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = 0
                    jugador_direccion = "frente"

        # Define el incremento de velocidad para los enemigos
        incremento_velocidad = 0.005
        velocidad_maxima = 1.0

        # Mantener constante el número de enemigos en pantalla
        while len(enemigo_x) < max_enemigos_en_pantalla and enemigos_generados < total_enemigos:
            enemigo_x.append(random.randint(0, 736))
            enemigo_y.append(random.randint(50, 200))
            enemigo_x_cambio.append(0.5)
            enemigo_y_cambio.append(50)
            estado_explosion.append(False)
            tiempo_explosion.append(0)
            indice_imagen.append(0)
            direccion_enemigo.append(True)
            gameover.append(False)

        # Modificar la ubicación del enemigo
        for i, enemigo in enumerate(range(len(enemigo_x))):
            if estado_explosion[i]:
                # Cambiar la imagen de explosión según el número de enemigos eliminados
                if enemigos_eliminados >= 50:
                    pantalla.blit(pygame.image.load("Calavera3.png"), (enemigo_x[i], enemigo_y[i]))
                else:
                    pantalla.blit(pygame.image.load("Zombie3.png"), (enemigo_x[i], enemigo_y[i]))
                tiempo_explosion[i] += 1
                if tiempo_explosion[i] > TIEMPO_EXPLOSION:
                    estado_explosion[i] = False
                    tiempo_explosion[i] = 0
                    enemigos_eliminados += 1
                    enemigos_restantes -= 1

                    # Incrementar velocidad de todos los enemigos después de la explosión
                    for j in range(len(enemigo_x_cambio)):
                        # Incrementar solo si no se ha alcanzado la velocidad máxima
                        if enemigo_x_cambio[j] > 0:
                            enemigo_x_cambio[j] = min(enemigo_x_cambio[j] + incremento_velocidad, velocidad_maxima)
                        else:
                            enemigo_x_cambio[j] = max(enemigo_x_cambio[j] - incremento_velocidad, -velocidad_maxima)

                    # Asegurarse de mantener siempre el número de enemigos en pantalla
                    if enemigos_generados < total_enemigos:
                        enemigo_x[i] = random.randint(0, 736)
                        enemigo_y[i] = random.randint(50, 200)
                        enemigos_generados += 1
                    else:
                        # Si un enemigo es eliminado y el total generado ya alcanzó el límite, simplemente respawnéalo
                        enemigo_x[i] = random.randint(0, 736)
                        enemigo_y[i] = random.randint(50, 200)

            else:
                # Para la muerte por colisión
                colision_con_jugador = hay_colision(enemigo_x[i], enemigo_y[i], jugador_x, jugador_y)
                if colision_con_jugador and not gameover[i]:
                    vidas -= 1
                    gameover[i] = True  # Marca al enemigo como "muerto"
                    if vidas > 0:  # Hacer que el enemigo respawnee si aún quedan vidas.
                        enemigo_x[i] = random.randint(0, 736)
                        enemigo_y[i] = random.randint(50, 200)
                        gameover[i] = False  # Reiniciar el estado del enemigo a "activo"

                        # Restablecer otras propiedades necesarias para la colisión
                        estado_explosion[i] = False
                        tiempo_explosion[i] = 0
                        direccion_enemigo[i] = True
                        enemigo_x_cambio[i] = 0.5  # Reinicia la velocidad
                    else:
                        enemigo_x[i] = 1000  # Mandarlo afuera de la pantalla si es gameover

                # Fin del juego si el enemigo llega a la parte inferior
                if enemigo_y[i] > 500 and not gameover[i]:
                    vidas -= 1
                    gameover[i] = True
                    if vidas > 0:  # Hacer que el enemigo respawnee si aún quedan vidas.
                        enemigo_x[i] = random.randint(0, 736)
                        enemigo_y[i] = random.randint(50, 200)
                        gameover[i] = False  # Reiniciar el estado del enemigo a "activo"
                    else:
                        enemigo_x[i] = 1000  # Mandarlo afuera de la pantalla si es gameover

                enemigo_x[i] += enemigo_x_cambio[i]

                # Cambiar dirección en los bordes
                if enemigo_x[i] <= -50:
                    enemigo_x_cambio[i] = abs(enemigo_x_cambio[i])  # Cambiar a positiva
                    enemigo_y[i] += enemigo_y_cambio[i]
                    direccion_enemigo[i] = True  # Cambiar dirección a derecha
                elif enemigo_x[i] >= 736:
                    enemigo_x_cambio[i] = -abs(enemigo_x_cambio[i])  # Cambiar a negativa
                    enemigo_y[i] += enemigo_y_cambio[i]
                    direccion_enemigo[i] = False  # Cambiar dirección a izquierda

                # Colisiones
                for bala in balas:
                    colision_bala_enemigo = hay_colision(enemigo_x[i], enemigo_y[i], bala["x"], bala["y"])
                    if colision_bala_enemigo:
                        sonido_colision = mixer.Sound("ZombieMuerte.mp3")
                        sonido_colision.set_volume(0.3)
                        sonido_colision.play()
                        balas.remove(bala)
                        puntaje += 1
                        estado_explosion[i] = True  # Inicia la explosión
                        break

                # Actualizar índice de imagen para la animación
                es_calavera = enemigos_eliminados >= 50
                if contador_frames % 60 == 0:  # Cambiar imagen cada 60 frames
                    indice_imagen[i] = (indice_imagen[i] + 1) % (
                        num_frames_calavera if es_calavera else num_frames_zombie)

                # Mostrar enemigo solo si no está explotando
                if not estado_explosion[i]:
                    controla_enemigo(enemigo_x[i], enemigo_y[i], indice_imagen[i], direccion_enemigo[i], es_calavera)

        # Incrementar el contador de frames
        contador_frames += 1

        # Animación de jugador
        if jugador_animacion_espacio:
            if jugador_contador_frames % 30 == 0:  # Cambiar imagen cada 30 frames
                jugador_img_index += 1
                if jugador_img_index >= num_frames_jugador:
                    jugador_animacion_espacio = False  # Terminar la animación especial
                    jugador_img_index = 2  # Estado normal del jugador (Humano2)

        if jugador_x_cambio != 0:
            if jugador_contador_frames % 100 == 0:  # Cambiar imagen cada 10 frames
                # Asegurar que no exceda el índice de imágenes de derecha/izquierda
                if jugador_direccion == "derecha":
                    jugador_img_index = (jugador_img_index + 1) % len(icono_jugador_derecha)
                elif jugador_direccion == "izquierda":
                    jugador_img_index = (jugador_img_index + 1) % len(icono_jugador_izquierda)

        jugador_contador_frames += 1

        # Movimiento bala
        for bala in balas:
            bala["y"] += bala["velocidad"]
            pantalla.blit(icono_bala, (bala["x"] + 40, bala["y"] + 10))
            if bala["y"] < 0:
                balas.remove(bala)

        # modificar ubicación del jugador
        jugador_x += jugador_x_cambio

        # mantener dentro de los bordes al jugador
        if jugador_x <= 0:
            jugador_x = 0
        elif jugador_x >= 736:
            jugador_x = 736

        jugador(jugador_x, jugador_y)

        mostrar_puntaje(texto_x, texto_y)

        if vidas <= 0 or enemigos_restantes <= 0:
            # Cambiar el fondo a Game Over
            fondo = pygame.image.load("GameOver.png")
            fondo = pygame.transform.scale(fondo, (800, 600))
            pantalla.blit(fondo, (0, 0))
            intento +=1
            record.append((intento,jugador_nombre, puntaje,))
            if intento == 1:
                seleccion = texto_final_Multijugador()
                if seleccion == "intentar":
                    Juego_Multijugador()
                elif seleccion == "menu":
                    menu_principal()  # Regresando al jugador al menu
            else:
                seleccion = texto_final_Multijugador_Ganador()
                if seleccion == "menu":
                    return
                elif seleccion=="intentar":
                    record.clear()
                    intento = 0
                    Juego_Multijugador()




        pygame.display.update()

while True:
    accion_menu = menu_principal()
    if accion_menu == "jugar":
        modificar_dificultad()
        juego()
    elif accion_menu == "Multijugador":
        Juego_Multijugador()