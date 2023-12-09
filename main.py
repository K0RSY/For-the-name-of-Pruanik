# Емпорты
from tkinter import *
from pygame import mixer
import pyglet
import time
import math
import sys

pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file('assets/font/pixeleum-48.ttf')
mixer.init()

# ткшки
tk = Tk()
tk.geometry('1500x800')
tk.resizable(0,0)
tk.attributes("-fullscreen", True)
try:
    tk.iconbitmap('assets/icon.ico')
except:
    pass
tk.title("Во имя приника")
tk["bg"] = "#8e8065"

# Уровни
levels_current = int(open("saves/current level.txt", "r").read().split("\n")[0])
levels_count = int(open("saves/current level.txt", "r").read().split("\n")[1])

# ЯЕЦА
egg_mode = False

# фулскрин
fullscreen = False
def fullscreen(event):
    global fullscreen
    fullscreen = not fullscreen
    tk.attributes("-fullscreen", fullscreen)
tk.bind("<F11>", fullscreen)

# курент стате, не понятно что-ли?
current_state = "Menu"

def tick():
    try:
        tk.update()
    except:
        sys.exit()
    time.sleep(0.05)

# тут начинается МЯСО (ооп)

# меню
class Menu:
    # инит
    def __init__(self):
        # основной фрейм
        self.frame = Frame(tk, bg="black", highlightthickness=0)

        # звуки
        self.music = mixer.Sound("assets/sounds/music/menu.mp3")
        self.music.set_volume(0.1)

        self.button_press = mixer.Sound("assets/sounds/buttons/press.mp3")
        self.button_press.set_volume(0.5)

        # картники
        self.play_button_img = PhotoImage(file='assets/textures/buttons/play.png').zoom(8,8)
        self.play_button_pressed_img = PhotoImage(file='assets/textures/buttons/play_pressed.png').zoom(8,8)

        self.options_button_img = PhotoImage(file='assets/textures/buttons/options.png').zoom(8,8)
        self.options_button_pressed_img = PhotoImage(file='assets/textures/buttons/options_pressed.png').zoom(8,8)

        self.background_img = PhotoImage(file='assets/textures/backgrounds/menu.png').zoom(8,8)

        self.dithering_img = PhotoImage(file='assets/textures/backgrounds/dithering.png').zoom(8,8)

        # объедки для фрейма
        self.c = Canvas(self.frame, bg="black", highlightthickness=0, width=1920, height=1080, borderwidth=0)
        self.c.place(relx=0.5,rely=0.5, anchor=CENTER)
        
        self.play_button = Label(self.c, image=self.play_button_img, highlightthickness=0, borderwidth=0)

        self.options_button = Label(self.c, image=self.options_button_img, highlightthickness=0, borderwidth=0)

        # фоновые картинки
        self.background = self.c.create_image(0, 0, image=self.background_img, anchor=NW)

        #бинды
        self.play_button.bind("<Button-1>", self.play_button_press) # нажатие
        self.options_button.bind("<Button-1>", self.options_button_press)

        self.play_button.bind("<Enter>", self.play_button_enter) # вход
        self.options_button.bind("<Enter>", self.options_button_enter)

        self.play_button.bind("<Leave>", self.play_button_leave) # выход
        self.options_button.bind("<Leave>", self.options_button_leave)

        self.frame.bind("<Escape>", self.exit)

    # кнопочки
    def play_button_enter(self, event):
        self.button_press.play()
        self.play_button["image"] = self.play_button_pressed_img
    def play_button_leave(self, event):
        self.play_button["image"] = self.play_button_img
    def play_button_press(self, event):
        self.button_press.play()
        global current_state
        if levels_current == 0:
            current_state = "Cutscene"
        else:
            current_state = "Level"

    def options_button_enter(self, event):
        self.button_press.play()
        self.options_button["image"] = self.options_button_pressed_img
    def options_button_leave(self, event):
        self.options_button["image"] = self.options_button_img
    def options_button_press(self, event):
        self.button_press.play()
        global current_state; current_state = "Options"

    def exit(self, event):
        tk.destroy()

    #переходы
    def open(self):
        self.music.play(-1)
        self.frame.focus_set()

        # плейсы
        self.frame.place(relwidth=1,relheight=1)

        # дитхеринг
        self.dithering = self.c.create_image(0, 0, image=self.dithering_img, anchor=NW)

        # анимация появления
        for x in range(1, 9):
            self.c.move(self.dithering, 0, -296)
            tick()
        self.c.delete(self.dithering)

        # плейс кнопок
        self.play_button.place(x=1500, y=600, anchor=CENTER)
        self.options_button.place(x=1500, y=800, anchor=CENTER)

        # старт лупа
        self.loop()
    def loop(self):
        # старт лупа
        while current_state == "Menu":
            tick()

        # закрытие когда надо
        self.close()
    def close(self):
        mixer.stop()

        # дитхеринг
        self.dithering = self.c.create_image(0, -2432, image=self.dithering_img, anchor=NW)

        # опять кнопки
        self.play_button.place_forget()
        self.options_button.place_forget()

        # анимация появления
        for x in range(1, 9):
            self.c.move(self.dithering, 0, 296)
            tick()
        self.c.delete(self.dithering)

        # плейс форгет
        self.frame.place_forget()
        self.c.delete(self.background)
        self.frame.unbind("<Escape>")

        # удалить себя
        del self

        # переход на следующую фазу
        if not current_state == None:
            exec(current_state+'().open()')
        else:
            tk.destroy()

# меню
class Options:
    # инит
    def __init__(self):
        # основной фрейм
        self.frame = Frame(tk, bg="black", highlightthickness=0)

        # звуки
        self.music = mixer.Sound("assets/sounds/music/menu.mp3")
        self.music.set_volume(0.1)

        self.button_press = mixer.Sound("assets/sounds/buttons/press.mp3")
        self.button_press.set_volume(0.5)

        # картники
        self.egg_button_img = PhotoImage(file='assets/textures/buttons/egg.png').zoom(8,8)
        self.egg_button_pressed_img = PhotoImage(file='assets/textures/buttons/egg_pressed.png').zoom(8,8)

        self.background_img = PhotoImage(file='assets/textures/backgrounds/options.png').zoom(8,8)

        self.dithering_img = PhotoImage(file='assets/textures/backgrounds/dithering.png').zoom(8,8)

        # объедки для фрейма
        self.c = Canvas(self.frame, bg="black", highlightthickness=0, width=1920, height=1080, borderwidth=0)
        self.c.place(relx=0.5,rely=0.5, anchor=CENTER)
        
        self.egg_button = Label(self.c, image=self.egg_button_img, highlightthickness=0, borderwidth=0)

        # фоновые картинки
        self.background = self.c.create_image(0, 0, image=self.background_img, anchor=NW)

        #бинды
        self.egg_button.bind("<Button-1>", self.egg_button_press) # нажатие
        self.egg_button.bind("<Enter>", self.egg_button_enter) # вход
        self.egg_button.bind("<Leave>", self.egg_button_leave) # выход

        self.frame.bind("<Escape>", self.exit)

    # кнопочки
    def egg_button_enter(self, event):
        self.button_press.play()
        self.egg_button["image"] = self.egg_button_pressed_img
    def egg_button_leave(self, event):
        self.egg_button["image"] = self.egg_button_img
    def egg_button_press(self, event):
        self.button_press.play()
        global egg_mode; egg_mode = True
        global current_state; current_state = "Menu"

    def exit(self, event):
        global current_state; current_state = "Menu"

    #переходы
    def open(self):
        self.music.play(-1)
        self.frame.focus_set()

        # плейсы
        self.frame.place(relwidth=1,relheight=1)

        # дитхеринг
        self.dithering = self.c.create_image(0, 0, image=self.dithering_img, anchor=NW)

        # анимация появления
        for x in range(1, 9):
            self.c.move(self.dithering, 0, -296)
            tick()
        self.c.delete(self.dithering)

        # плейс кнопок
        self.egg_button.place(x=1250, y=848, anchor=CENTER)

        # старт лупа
        self.loop()
    def loop(self):
        # старт лупа
        while current_state == "Options":
            tick()

        # закрытие когда надо
        self.close()
    def close(self):
        mixer.stop()

        # дитхеринг
        self.dithering = self.c.create_image(0, -2432, image=self.dithering_img, anchor=NW)

        # опять кнопки
        self.egg_button.place_forget()

        # анимация появления
        for x in range(1, 9):
            self.c.move(self.dithering, 0, 296)
            tick()
        self.c.delete(self.dithering)

        # плейс форгет
        self.frame.place_forget()
        self.c.delete(self.background)

        # удалить себя
        del self

        # переход на следующую фазу
        if not current_state == None:
            exec(current_state+'().open()')
        else:
            tk.destroy()

class Cutscene:
    # инит
    def __init__(self):
        # основной фрейм
        self.frame = Frame(tk, bg="black", highlightthickness=0)

        # звуки
        self.music = mixer.Sound("assets/sounds/music/game.mp3")
        self.music.set_volume(0.07)

        self.grass_walk = mixer.Sound("assets/sounds/cutscene/grass_walk.mp3")
        self.grass_walk.set_volume(1)

        self.turn = mixer.Sound("assets/sounds/cutscene/turn.mp3")
        self.turn.set_volume(2)

        self.item_collect = mixer.Sound("assets/sounds/cutscene/item_collect.mp3")
        self.item_collect.set_volume(0.5)

        self.trapdoor_open = mixer.Sound("assets/sounds/cutscene/trapdoor_open.mp3")
        self.trapdoor_open.set_volume(0.5)

        # картники
        self.dithering_img = PhotoImage(file='assets/textures/backgrounds/dithering.png').zoom(8,8)
        self.dialogues = [['''Как-то раз вы решили прогулятся по поляне
близ леса. Ночью... Без никого...''',self.grass_walk],['''На горизонте показались развалины
какого-то небольшого здания.''',False],['''Вы зашли в него и увидели тульский
пряник, валяющийся на деревянной дощечке''',False],['''Почему бы его не взять?''',False],[False,self.item_collect],['''Дощечка упала вниз. Видимо это была ловушка
для какого-то маленького зверька.''',self.trapdoor_open],['''Вы почувствовали теплое дыхание за спиной.''',False],['''Обернувшись, вы увидели, что на вас смотрел
ни кто иной, как
АНОНИМУС!''',self.turn],['''Его глаза блеснули под маской...''',False],['''Он был настроен точно не позитивно.''',False]]
        self.images = [PhotoImage(file='assets/textures/cutscene/frame1.png').zoom(8,8),PhotoImage(file='assets/textures/cutscene/frame2.png').zoom(8,8),PhotoImage(file='assets/textures/cutscene/frame3.png').zoom(8,8),PhotoImage(file='assets/textures/cutscene/frame3.png').zoom(8,8),PhotoImage(file='assets/textures/cutscene/frame4.png').zoom(8,8),PhotoImage(file='assets/textures/cutscene/frame5.png').zoom(8,8),PhotoImage(file='assets/textures/cutscene/frame5.png').zoom(8,8),PhotoImage(file='assets/textures/cutscene/frame6.png').zoom(8,8),PhotoImage(file='assets/textures/cutscene/frame7.png').zoom(8,8),PhotoImage(file='assets/textures/cutscene/frame6.png').zoom(8,8)]
        self.number = 0
        self.dialogue_img = PhotoImage(file='assets/textures/cutscene/dialogue.png').zoom(6,6)

        # объедки для фрейма
        self.c = Canvas(self.frame, bg="black", highlightthickness=0, width=1920, height=1080, borderwidth=0)
        self.c.place(relx=0.5,rely=0.5, anchor=CENTER)

        #бинды
        self.frame.bind("<space>", self.cutscene_generate)

    #генерация картинки
    def cutscene_generate(self,event):
        if self.number <= 9:
            try:
                self.c.delete(self.dialogue_text)
                self.c.delete(self.dialogue)
                self.c.delete(self.background)
            except:
                pass
            if not self.dialogues[self.number][1] == False:
                self.dialogues[self.number][1].play()
            self.background = self.c.create_image(0, 0, image=self.images[self.number], anchor=NW)
            if not self.dialogues[self.number][0] == False:
                self.dialogue = self.c.create_image(self.c.winfo_width()//2, (self.c.winfo_width()-self.frame.winfo_width())//4, image=self.dialogue_img, anchor = N)
                self.dialogue_text = self.c.create_text(self.c.winfo_width()//2, ((self.c.winfo_width()-self.frame.winfo_width())//4)+20, anchor = N, text = self.dialogues[self.number][0], font = ('Pixeleum 48', 23), fill="#c2c3ab")
            self.number += 1
        else:
            global current_state; current_state = "Level"

    #переходы
    def open(self):
        self.frame.focus_set()
        self.music.play(-1)

        # плейсы
        self.frame.place(relwidth=1,relheight=1)

        tk.update()
        self.cutscene_generate("mish")

        # дитхеринг
        self.dithering = self.c.create_image(0, 0, image=self.dithering_img, anchor=NW)

        # анимация появления
        for x in range(1, 9):
            self.c.move(self.dithering, 0, -296)
            tick()
        self.c.delete(self.dithering)

        # старт лупа
        self.loop()
    def loop(self):
        # старт лупа
        while current_state == "Cutscene":
            self.c.coords(self.dialogue, self.c.winfo_width()//2, (self.c.winfo_width()-self.frame.winfo_width())//4)
            self.c.coords(self.dialogue_text, self.c.winfo_width()//2, ((self.c.winfo_width()-self.frame.winfo_width())//4)+20)
            tick()

        # закрытие когда надо
        self.close()
    def close(self):
        mixer.stop()
        self.frame.focus_set()
        self.frame.unbind("<space>")

        # дитхеринг
        self.dithering = self.c.create_image(0, -2432, image=self.dithering_img, anchor=NW)

        self.c.delete(self.dialogue_text)
        self.c.delete(self.dialogue)

        # анимация появления
        for x in range(1, 9):
            self.c.move(self.dithering, 0, 296)
            tick()
        self.c.delete(self.dithering)

        # плейс форгет
        self.frame.place_forget()
        self.c.delete(self.background)

        # удалить себя
        del self

        # переход на следующую фазу
        if not current_state == None:
            exec(current_state+'().open()')
        else:
            tk.destroy()

class Level:
    # блокиb
    class Entities:
        isnt_solid = True
        def placement(self, canvas):
            self.object = canvas.create_image((self.x*10+40)*8, (self.y*10+22)*8, image=self.texture, anchor=NW)
        def work(slef, canvas, player):
            pass

    # блоки, но конкретнее
    # игорёк
    class Player(Entities):
        def __init__(self, x, y, canvas):
            if not egg_mode:
                self.texture = PhotoImage(file='assets/textures/entities/player/right.png').zoom(8,8)
            else:
                self.texture = PhotoImage(file='assets/textures/entities/player/egg.png').zoom(8,8)
            self.direction = "right"
            self.x = x
            self.y = y
            self.type = "Player"
            self.placement(canvas)
    # стена
    class Wall(Entities):
        texture = PhotoImage(file='assets/textures/entities/blocks/wall.png').zoom(8,8)
        isnt_solid = False
        def __init__(self, x, y, canvas):
            self.x = x
            self.y = y
            self.type = "Wall"
            self.placement(canvas)
    # пряник
    class Pruanik(Entities):
        texture = PhotoImage(file='assets/textures/entities/blocks/pruanik.png').zoom(8,8)
        def __init__(self, x, y, canvas):
            self.x = x
            self.y = y
            self.type = "Pruanik"
            self.placement(canvas)
    # летящий пряник
    class PruanikFly(Entities):
        texture = PhotoImage(file='assets/textures/entities/blocks/pruanik_fly.png').zoom(8,8)
        def __init__(self, x, y, canvas):
            self.direction = "right"
            self.x = x
            self.y = y
            self.type = "PruanikFly"
            self.placement(canvas)
    # стена но хрпкая
    class WallCracked(Entities):
        texture = PhotoImage(file='assets/textures/entities/blocks/wall_crack.png').zoom(8,8)
        isnt_solid = False
        def __init__(self, x, y, canvas):
            self.x = x
            self.y = y
            self.type = "WallCracked"
            self.placement(canvas)
    # дверь
    class Door(Entities):
        def __init__(self, x, y, canvas, isnt_solid, horisontal):
            self.isnt_solid = isnt_solid
            self.horisontal = horisontal
            self.x = x
            self.y = y
            self.type = "Door"
            if self.isnt_solid and self.horisontal:
                self.texture = PhotoImage(file='assets/textures/entities/blocks/door_open_horisontal.png').zoom(8,8)
            elif not self.isnt_solid and self.horisontal:
                self.texture = PhotoImage(file='assets/textures/entities/blocks/door_close_horisontal.png').zoom(8,8)
            elif self.isnt_solid and not self.horisontal:
                self.texture = PhotoImage(file='assets/textures/entities/blocks/door_open_vertical.png').zoom(8,8)
            elif not self.isnt_solid and not self.horisontal:
                self.texture = PhotoImage(file='assets/textures/entities/blocks/door_close_vertical.png').zoom(8,8)
            self.placement(canvas)
    # стена но хрпкая
    class Pruanoprinimatel(Entities):
        texture = PhotoImage(file='assets/textures/entities/blocks/pruanoprinimatel.png').zoom(8,8)
        def __init__(self, x, y, canvas):
            self.x = x
            self.y = y
            self.type = "Pruanoprinimatel"
            self.placement(canvas)


    # инит
    def __init__(self):
        # основной фрейм
        self.frame = Frame(tk, bg="black", highlightthickness=0)

        # звуки
        self.music = mixer.Sound("assets/sounds/music/game.mp3")
        self.music.set_volume(0.1)

        self.step = mixer.Sound("assets/sounds/level/step.mp3")
        self.step.set_volume(2)

        self.item_collect = mixer.Sound("assets/sounds/cutscene/item_collect.mp3")
        self.item_collect.set_volume(0.5)

        self.pruanik_wall_boom = mixer.Sound("assets/sounds/level/pruanik_wall_boom.mp3")
        self.pruanik_wall_boom.set_volume(2)

        # картники
        self.background_img = PhotoImage(file='assets/textures/backgrounds/level.png').zoom(8,8)
        self.frontground_img = PhotoImage(file='assets/textures/backgrounds/level_front.png').zoom(8,8)

        self.dithering_img = PhotoImage(file='assets/textures/backgrounds/dithering.png').zoom(8,8)

        self.info_img = PhotoImage(file='assets/textures/backgrounds/level_info_1.png').zoom(8,8)

        # объедки для фрейма
        self.c = Canvas(self.frame, bg="black", highlightthickness=0, width=1920, height=1080, borderwidth=0)
        self.c.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.info = Label(self.frame, bg="black", highlightthickness=0, width=50*8, height=80, image=self.info_img, borderwidth=0)
        self.info_lebel = Label(self.info, height=1, bg = "#8E8065", text=f"{levels_current}", font = ('Pixeleum 48', 28, 'bold'), fg="#c2c3ab")
        self.info_lebel.place(x=96, y=36, anchor=W)

        # фоновые картинки
        self.background = self.c.create_image(0, 0, image=self.background_img, anchor=NW)

        # кол-во пряников
        self.pruaniks = 1

        # МАТРИЦА В ПАЙТОНЕ - ЭТО ИЗИ!!!
        self.entities_text = open(f"saves/levels/level{levels_current}.txt", "r").read().split("\n")
        self.entities = [[],[],[],[],[],[],[],[],[]]

        for self.i_y in range(0,len(self.entities_text)):
            for self.i_x in range(0, len(self.entities_text[self.i_y])):
                if self.entities_text[self.i_y][self.i_x] == "#":
                    self.entities[self.i_y].append(self.Wall(self.i_x, self.i_y, self.c))
                elif self.entities_text[self.i_y][self.i_x] == "-":
                    self.entities[self.i_y].append(self.Pruanik(self.i_x, self.i_y, self.c))
                elif self.entities_text[self.i_y][self.i_x] == "%":
                    self.entities[self.i_y].append(self.WallCracked(self.i_x, self.i_y, self.c))
                elif self.entities_text[self.i_y][self.i_x] == "H":
                    self.entities[self.i_y].append(self.Door(self.i_x, self.i_y, self.c, False, True))
                elif self.entities_text[self.i_y][self.i_x] == "h":
                    self.entities[self.i_y].append(self.Door(self.i_x, self.i_y, self.c, True, True))
                elif self.entities_text[self.i_y][self.i_x] == "F":
                    self.entities[self.i_y].append(self.Door(self.i_x, self.i_y, self.c, False, False))
                elif self.entities_text[self.i_y][self.i_x] == "f":
                    self.entities[self.i_y].append(self.Door(self.i_x, self.i_y, self.c, True, False))
                elif self.entities_text[self.i_y][self.i_x] == "w":
                    self.entities[self.i_y].append(self.Pruanoprinimatel(self.i_x, self.i_y, self.c))

        self.player = self.Player(0, 4, self.c)

        self.frontground = self.c.create_image(0, 0, image=self.frontground_img, anchor=NW)

        # бинды
        self.bind()

    # бинды, но по-другому
    def bind(self):
        self.frame.bind('w', self.tick)
        self.frame.bind('a', self.tick)
        self.frame.bind('s', self.tick)
        self.frame.bind('d', self.tick)
        self.frame.bind('e', self.tick)
        self.frame.bind('q', self.tick)
        self.frame.bind('r', self.tick)
        self.frame.bind('<Escape>', self.tick)

    def unbind(self):
        self.frame.unbind('w')
        self.frame.unbind('a')
        self.frame.unbind('s')
        self.frame.unbind('d')
        self.frame.unbind('e')
        self.frame.unbind('q')
        self.frame.unbind('r')
        self.frame.unbind('<Escape>')


    #переходы
    def open(self):
        self.frame.focus_set()
        self.music.play(-1)

        # плейсы
        self.frame.place(relwidth=1,relheight=1)

        # дитхеринг
        self.dithering = self.c.create_image(0, 0, image=self.dithering_img, anchor=NW)

        # анимация появления
        for x in range(1, 9):
            self.c.move(self.dithering, 0, -296)
            tick()
        self.c.delete(self.dithering)


        self.info.place(relx=0.5,rely=0, anchor=N)

        # старт лупа
        self.loop()

    def tick(self, event):
        global current_state
        if str(event.keysym) == 'w':
            self.c.delete(self.player.object)
            if not egg_mode:
                self.player.texture = PhotoImage(file='assets/textures/entities/player/up_scuish.png').zoom(8,8)
            else: 
                self.player.texture = PhotoImage(file='assets/textures/entities/player/egg_scuish.png').zoom(8,8)
            self.player.object = self.c.create_image((self.player.x*10+40)*8, (self.player.y*10+22)*8, image=self.player.texture, anchor=NW)
            wall_face = 0
            for i_y in range(0, len(self.entities)):
                for i_x in range(0, len(self.entities[i_y])):
                    if not self.entities[i_y][i_x].isnt_solid:
                        if self.player.y - 1 == self.entities[i_y][i_x].y and self.player.x == self.entities[i_y][i_x].x:
                            wall_face += 1
            if self.player.y - 1 < 0:
                wall_face += 1
            if wall_face == 0:
                for i in range (1, 4):
                    self.unbind()
                    self.c.move(self.player.object, 0, -25)
                    tick()
                self.player.y -= 1
                self.bind()
                self.step.play()
            self.player.direction = "up"
            self.c.delete(self.player.object)
            if not egg_mode:
                self.player.texture = PhotoImage(file='assets/textures/entities/player/up.png').zoom(8,8)
            else: 
                self.player.texture = PhotoImage(file='assets/textures/entities/player/egg.png').zoom(8,8)
            self.player.object = self.c.create_image((self.player.x*10+40)*8, (self.player.y*10+22)*8, image=self.player.texture, anchor=NW)

        elif str(event.keysym) == 's':
            self.c.delete(self.player.object)
            if not egg_mode:
                self.player.texture = PhotoImage(file='assets/textures/entities/player/down_scuish.png').zoom(8,8)
            else: 
                self.player.texture = PhotoImage(file='assets/textures/entities/player/egg_scuish.png').zoom(8,8)
            self.player.object = self.c.create_image((self.player.x*10+40)*8, (self.player.y*10+22)*8, image=self.player.texture, anchor=NW)
            wall_face = 0
            for i_y in range(0, len(self.entities)):
                for i_x in range(0, len(self.entities[i_y])):
                    if not self.entities[i_y][i_x].isnt_solid:
                        if self.player.y + 1 == self.entities[i_y][i_x].y and self.player.x == self.entities[i_y][i_x].x:
                            wall_face += 1
            if self.player.y + 1 > 8:
                wall_face += 1
            if wall_face == 0:
                for i in range (1, 4):
                    self.unbind()
                    self.c.move(self.player.object, 0, 25)
                    tick()
                self.player.y += 1
                self.bind()
                self.step.play()
            self.player.direction = "down"
            self.c.delete(self.player.object)
            if not egg_mode:
                self.player.texture = PhotoImage(file='assets/textures/entities/player/down.png').zoom(8,8)
            else: 
                self.player.texture = PhotoImage(file='assets/textures/entities/player/egg.png').zoom(8,8)
            self.player.object = self.c.create_image((self.player.x*10+40)*8, (self.player.y*10+22)*8, image=self.player.texture, anchor=NW)

        elif str(event.keysym) == 'd':
            self.c.delete(self.player.object)
            if not egg_mode:
                self.player.texture = PhotoImage(file='assets/textures/entities/player/right_scuish.png').zoom(8,8)
            else: 
                self.player.texture = PhotoImage(file='assets/textures/entities/player/egg_scuish.png').zoom(8,8)
            self.player.object = self.c.create_image((self.player.x*10+40)*8, (self.player.y*10+22)*8, image=self.player.texture, anchor=NW)
            wall_face = 0
            for i_y in range(0, len(self.entities)):
                for i_x in range(0, len(self.entities[i_y])):
                    if not self.entities[i_y][i_x].isnt_solid:
                        if self.player.x + 1 == self.entities[i_y][i_x].x and self.player.y == self.entities[i_y][i_x].y:
                            wall_face += 1
            if self.player.x + 1 > 15:
                wall_face += 1
            if wall_face == 0:
                for i in range (1, 4):
                    self.unbind()
                    self.c.move(self.player.object, 25, 0)
                    tick()
                self.player.x += 1
                self.bind()
                self.step.play()
            self.player.direction = "right"
            self.c.delete(self.player.object)
            if not egg_mode:
                self.player.texture = PhotoImage(file='assets/textures/entities/player/right.png').zoom(8,8)
            else: 
                self.player.texture = PhotoImage(file='assets/textures/entities/player/egg.png').zoom(8,8)
            self.player.object = self.c.create_image((self.player.x*10+40)*8, (self.player.y*10+22)*8, image=self.player.texture, anchor=NW)

        elif str(event.keysym) == 'a':
            self.c.delete(self.player.object)
            if not egg_mode:
                self.player.texture = PhotoImage(file='assets/textures/entities/player/left_scuish.png').zoom(8,8)
            else: 
                self.player.texture = PhotoImage(file='assets/textures/entities/player/egg_scuish.png').zoom(8,8)
            self.player.object = self.c.create_image((self.player.x*10+40)*8, (self.player.y*10+22)*8, image=self.player.texture, anchor=NW)
            wall_face = 0
            for i_y in range(0, len(self.entities)):
                for i_x in range(0, len(self.entities[i_y])):
                    if not self.entities[i_y][i_x].isnt_solid:
                        if self.player.x - 1 == self.entities[i_y][i_x].x and self.player.y == self.entities[i_y][i_x].y:
                            wall_face += 1
            if self.player.x - 1 < 0:
                wall_face += 1
            if wall_face == 0:
                for i in range (1, 4):
                    self.unbind()
                    self.c.move(self.player.object, -25, 0)
                    tick()
                self.player.x -= 1
                self.bind()
                self.step.play()
            self.player.direction = "left"
            self.c.delete(self.player.object)
            if not egg_mode:
                self.player.texture = PhotoImage(file='assets/textures/entities/player/left.png').zoom(8,8)
            else: 
                self.player.texture = PhotoImage(file='assets/textures/entities/player/egg.png').zoom(8,8)
            self.player.object = self.c.create_image((self.player.x*10+40)*8, (self.player.y*10+22)*8, image=self.player.texture, anchor=NW)

        elif str(event.keysym) == 'e':
            for i_y in range(0, len(self.entities)):
                for i_x in range(0, len(self.entities[i_y])):
                    if self.entities[i_y][i_x].type == "Pruanik":
                        if self.player.x == self.entities[i_y][i_x].x and self.player.y == self.entities[i_y][i_x].y and not self.pruaniks >= 3:
                            self.pruaniks += 1
                            self.info_img = PhotoImage(file=f'assets/textures/backgrounds/level_info_{self.pruaniks}.png').zoom(8,8)
                            self.info.config(image=self.info_img)
                            self.info_lebel = Label(self.info, height=1, bg = "#8E8065", text=f"{levels_current}", font = ('Pixeleum 48', 28, 'bold'), fg="#c2c3ab")
                            self.info_lebel.place(x=96, y=36, anchor=W)
                            self.item_collect.play()
                            self.c.delete(self.entities[i_y][i_x].object)
                            del self.entities[i_y][i_x]
                            break
                    if self.entities[i_y][i_x].type == "Pruanoprinimatel":
                        if self.player.x == self.entities[i_y][i_x].x and self.player.y == self.entities[i_y][i_x].y and self.pruaniks > 0:
                            self.pruaniks -= 1
                            self.info_img = PhotoImage(file=f'assets/textures/backgrounds/level_info_{self.pruaniks}.png').zoom(8,8)
                            self.info.config(image=self.info_img)
                            self.info_lebel = Label(self.info, height=1, bg = "#8E8065", text=f"{levels_current}", font = ('Pixeleum 48', 28, 'bold'), fg="#c2c3ab")
                            self.info_lebel.place(x=96, y=36, anchor=W)
                            self.item_collect.play()   
                            for i_y in range(0, len(self.entities)):
                                for i_x in range(0, len(self.entities[i_y])):
                                    if self.entities[i_y][i_x].type == "Door":
                                        self.entities[i_y][i_x].isnt_solid = not self.entities[i_y][i_x].isnt_solid  
                                        if self.entities[i_y][i_x].isnt_solid and self.entities[i_y][i_x].horisontal:
                                            self.entities[i_y][i_x].texture = PhotoImage(file='assets/textures/entities/blocks/door_open_horisontal.png').zoom(8,8)
                                        elif not self.entities[i_y][i_x].isnt_solid and self.entities[i_y][i_x].horisontal:
                                            self.entities[i_y][i_x].texture = PhotoImage(file='assets/textures/entities/blocks/door_close_horisontal.png').zoom(8,8)
                                        elif self.entities[i_y][i_x].isnt_solid and not self.entities[i_y][i_x].horisontal:
                                            self.entities[i_y][i_x].texture = PhotoImage(file='assets/textures/entities/blocks/door_open_vertical.png').zoom(8,8)
                                        elif not self.entities[i_y][i_x].isnt_solid and not self.entities[i_y][i_x].horisontal:
                                            self.entities[i_y][i_x].texture = PhotoImage(file='assets/textures/entities/blocks/door_close_vertical.png').zoom(8,8)
                                        self.c.delete(self.entities[i_y][i_x].object)
                                        self.entities[i_y][i_x].object = self.c.create_image((self.entities[i_y][i_x].x*10+40)*8, (self.entities[i_y][i_x].y*10+22)*8, image=self.entities[i_y][i_x].texture, anchor=NW)
                            break

        elif str(event.keysym) == 'q':
            if self.pruaniks > 0:
                self.unbind()
                self.pruanik_fly = self.PruanikFly(self.player.x,self.player.y,self.c)
                self.pruanik_fly.can_fly = True
                self.pruanik_fly.direction = self.player.direction
                self.unbind()
                self.pruaniks -= 1
                self.info_img = PhotoImage(file=f'assets/textures/backgrounds/level_info_{self.pruaniks}.png').zoom(8,8)
                self.info.config(image=self.info_img)
                self.info_lebel = Label(self.info, height=1, bg = "#8E8065", text=f"{levels_current}", font = ('Pixeleum 48', 28, 'bold'), fg="#c2c3ab")
                self.info_lebel.place(x=96, y=36, anchor=W)
                self.item_collect.play()
                while self.pruanik_fly.can_fly:
                    if self.pruanik_fly.direction == "right":
                        for i in range (1, 4):
                            self.c.move(self.pruanik_fly.object, 25, 0)
                            tick()
                        for i_y in range(0, len(self.entities)):
                            for i_x in range(0, len(self.entities[i_y])):
                                if self.pruanik_fly.x + 1 == self.entities[i_y][i_x].x and self.pruanik_fly.y == self.entities[i_y][i_x].y and not self.entities[i_y][i_x].isnt_solid:
                                    self.pruanik_fly.can_fly = False
                                    if self.entities[i_y][i_x].type == "WallCracked":
                                        self.c.delete(self.entities[i_y][i_x].object)
                                        del self.entities[i_y][i_x]
                                        break
                        self.pruanik_fly.x += 1
                        if self.pruanik_fly.x + 1 > 15:
                            self.pruanik_fly.can_fly = False
                    elif self.pruanik_fly.direction == "left":
                        for i in range (1, 4):
                            self.c.move(self.pruanik_fly.object, -25, 0)
                            tick()
                        for i_y in range(0, len(self.entities)):
                            for i_x in range(0, len(self.entities[i_y])):
                                if self.pruanik_fly.x - 1 == self.entities[i_y][i_x].x and self.pruanik_fly.y == self.entities[i_y][i_x].y and not self.entities[i_y][i_x].isnt_solid:
                                    self.pruanik_fly.can_fly = False
                                    if self.entities[i_y][i_x].type == "WallCracked":
                                        self.c.delete(self.entities[i_y][i_x].object)
                                        del self.entities[i_y][i_x]
                                        break
                        self.pruanik_fly.x -= 1
                        if self.pruanik_fly.x - 1 < 0:
                            self.pruanik_fly.can_fly = False
                    elif self.pruanik_fly.direction == "up":
                        for i in range (1, 4):
                            self.c.move(self.pruanik_fly.object, 0, -25)
                            tick()
                        for i_y in range(0, len(self.entities)):
                            for i_x in range(0, len(self.entities[i_y])):
                                if self.pruanik_fly.y - 1 == self.entities[i_y][i_x].y and self.pruanik_fly.x == self.entities[i_y][i_x].x and not self.entities[i_y][i_x].isnt_solid:
                                    self.pruanik_fly.can_fly = False
                                    if self.entities[i_y][i_x].type == "WallCracked":
                                        self.c.delete(self.entities[i_y][i_x].object)
                                        del self.entities[i_y][i_x]
                                        break 
                        self.pruanik_fly.y -= 1
                        if self.pruanik_fly.y - 1 < 0:
                            self.pruanik_fly.can_fly = False
                    elif self.pruanik_fly.direction == "down":
                        for i in range (1, 4):
                            self.c.move(self.pruanik_fly.object, 0, 25)
                            tick()
                        for i_y in range(0, len(self.entities)):
                            for i_x in range(0, len(self.entities[i_y])):
                                if self.pruanik_fly.y + 1 == self.entities[i_y][i_x].y and self.pruanik_fly.x == self.entities[i_y][i_x].x and not self.entities[i_y][i_x].isnt_solid:
                                    self.pruanik_fly.can_fly = False
                                    if self.entities[i_y][i_x].type == "WallCracked":
                                        self.c.delete(self.entities[i_y][i_x].object)
                                        del self.entities[i_y][i_x]
                                        break
                        self.pruanik_fly.y += 1
                        if self.pruanik_fly.y + 1 > 8:
                            self.pruanik_fly.can_fly = False
                self.pruanik_wall_boom.play()
                self.c.delete(self.pruanik_fly.object)
                del self.pruanik_fly
                self.bind()

        elif str(event.keysym) == 'r':
            self.close()

        elif str(event.keysym) == 'Escape':
            current_state = "Menu"
            
        
    def loop(self):
        global current_state, levels_current, levels_count
        # старт лупа
        while current_state == "Level":
            tick()
            if self.player.x == 15 and self.player.y == 4:
                if levels_current >= levels_count:
                    current_state = "End"
                    levels_current = 0
                    levels = open("saves/current level.txt", "w")
                    levels.write(f"{levels_current}\n{levels_count}")
                    levels.close()
                else:
                    levels_current += 1
                    levels = open("saves/current level.txt", "w")
                    levels.write(f"{levels_current}\n{levels_count}")
                    levels.close()
                    self.close()

        # закрытие когда надо
        self.close()

    def close(self):
        self.frame.focus_set()
        mixer.stop()
        self.unbind()

        self.info.place_forget()

        # дитхеринг
        self.dithering = self.c.create_image(0, -2432, image=self.dithering_img, anchor=NW)

        # анимация появления
        for x in range(1, 9):
            self.c.move(self.dithering, 0, 296)
            tick()
        self.c.delete(self.dithering)

        # плейс форгет
        self.frame.place_forget()
        self.info.place_forget()
        self.c.delete(self.background)
        self.c.delete(self.frontground)
        for i_y in range(0, len(self.entities)):
            for i_x in range(0, len(self.entities[i_y])):
                self.c.delete(self.entities[i_y][i_x].object)

        # удалить себя
        del self

        # переход на следующую фазу
        if not current_state == None:
            exec(current_state+'().open()')
        else:
            tk.destroy()


# меню
class End:
    # инит
    def __init__(self):
        # основной фрейм
        self.frame = Frame(tk, bg="black", highlightthickness=0)


        self.dithering_img = PhotoImage(file='assets/textures/backgrounds/dithering.png').zoom(8,8)

        # звуки
        self.music = mixer.Sound("assets/sounds/music/menu.mp3")
        self.music.set_volume(0.1)

        # объедки для фрейма
        self.c = Canvas(self.frame, bg="black", highlightthickness=0, width=1920, height=1080, borderwidth=0)
        self.c.place(relx=0.5,rely=0.5, anchor=CENTER)

        self.c.create_text(1920/2, 1080/2, text="Спасибо за игру!", font = ('Pixeleum 48', 70, 'bold'), fill="#c2c3ab")

        self.is_end = 1

    #переходы
    def open(self):
        self.music.play(-1)

        # плейсы
        self.frame.place(relwidth=1,relheight=1)

        # дитхеринг
        self.dithering = self.c.create_image(0, 0, image=self.dithering_img, anchor=NW)

        # анимация появления
        for x in range(1, 9):
            self.c.move(self.dithering, 0, -296)
            tick()
        self.c.delete(self.dithering)

        tk.after(3000, self.close)

        # старт лупа
        while self.is_end:
            tick()
    def close(self):
        global current_state
        current_state = "Menu"
        mixer.stop()
        self.is_end = 0

        # дитхеринг
        self.dithering = self.c.create_image(0, -2432, image=self.dithering_img, anchor=NW)

        # анимация появления
        for x in range(1, 9):
            self.c.move(self.dithering, 0, 296)
            tick()
        self.c.delete(self.dithering)

        # плейс форгет
        self.frame.place_forget()

        # удалить себя
        del self

        # переход на следующую фазу
        if not current_state == None:
            exec(current_state+'().open()')
        else:
            tk.destroy()

# глав пле цикл
Menu().open()