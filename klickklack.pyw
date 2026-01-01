import pygame
import random
import math
import os
from configparser import ConfigParser
import tkinter
from tkinter import messagebox
import traceback
import sys

try:
    width, height = 800,600
    win = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Klicker Elektro")

    directory = os.path.dirname(__file__)
    print(directory)

    pygame.font.init()
    font = pygame.font.SysFont("bahnschrift",24)

    save = open(os.path.join(directory,"data.ini"),"a")
    save.close()

    config = ConfigParser()
    config.read(os.path.join(directory,"data.ini"))
    if config.has_option("klickklack","highscore"):
        highscore = int(config.get("klickklack","highscore"))
    else:
        highscore = 0

    if config.has_option("klickklack","sound"):
        volume = int(config.get("klickklack","sound"))
    else:
        volume = 1

    FPS = 60
    blue = (0,0,255)
    grey = (160,160,160)
    dkgrey = (64,64,64)
    black = (0,0,0)
    red = (255,0,0)
    teal = (0,128,255)
    white = (255,255,255)
    block_col = []
    block_col.append((0,0,255))
    block_col.append((255,0,0))
    block_col.append((0,255,0))
    block_col.append((255,255,0))
    block_col.append((255,255,255))
    block_col.append((128,128,128))

    spd = 8

    background = pygame.image.load(os.path.join(directory,"images","background.png"))
    num = pygame.image.load(os.path.join(directory,"images","numbers2.png"))
    cube = pygame.image.load(os.path.join(directory,"images","cubes.png"))
    highlight = pygame.image.load(os.path.join(directory,"images","highlight.png"))
    radioactivity = pygame.image.load(os.path.join(directory,"images","radioactive.png"))
    border1 = pygame.image.load(os.path.join(directory,"images","border1.png"))
    border2 = pygame.image.load(os.path.join(directory,"images","border2.png"))
    beam = pygame.image.load(os.path.join(directory,"images","beam.png"))
    blast = pygame.image.load(os.path.join(directory,"images","blast.png"))
    board = pygame.image.load(os.path.join(directory,"images","scoreboard.png"))
    background_outro = pygame.image.load(os.path.join(directory,"images","gameover.png"))
    icon = pygame.image.load(os.path.join(directory,"images","icon.ico"))

    blast_scaled = pygame.transform.scale(blast,(256,32))
    pygame.display.set_icon(icon)

    pygame.mixer.init()
    sound_combo = pygame.mixer.Sound(os.path.join(directory,"sounds","combo.mp3"))
    sound_bomb = pygame.mixer.Sound(os.path.join(directory,"sounds","bomb.mp3"))
    sound_over = pygame.mixer.Sound(os.path.join(directory,"sounds","game_over.mp3"))
    sound_intro = pygame.mixer.Sound(os.path.join(directory,"sounds","intro.mp3"))
    sound_cleared = pygame.mixer.Sound(os.path.join(directory,"sounds","level_cleared.mp3"))
    sound_start = pygame.mixer.Sound(os.path.join(directory,"sounds","level_starts.mp3"))
    sound_loop = pygame.mixer.Sound(os.path.join(directory,"sounds","loop.mp3"))
    sound_no_combo = pygame.mixer.Sound(os.path.join(directory,"sounds","no_combo.mp3"))
    sound_radioactive = pygame.mixer.Sound(os.path.join(directory,"sounds","radioactive.mp3"))
    sound_blast = pygame.mixer.Sound(os.path.join(directory,"sounds","blast_released.mp3"))
    sound_blast_active = pygame.mixer.Sound(os.path.join(directory,"sounds","blast_activated.mp3"))
    sound_warning = pygame.mixer.Sound(os.path.join(directory,"sounds","time_warning.mp3"))
    sound_perfect = pygame.mixer.Sound(os.path.join(directory,"sounds","100percent.mp3"))

    class block():
        def __init__(self,x,y):
            self.colour = random.randrange(4)
            if level == 3:
                self.colour += 1
                #self.colour = random.randrange(5)
            self.x = x
            self.y = y
            self.width = 32
            self.matched = False
            self.highlighted = False

            chance = 0.05

            if random.random() < chance:
                self.colour = 5

            if self.colour != 5 and random.random() < chance:
                self.radioactive = 1
            else:
                self.radioactive = 0

        def move(self):
            if self.y < 400:
                if self.move_down():
                    self.y += spd
                    return True

            return False

        def check(self):
            if self.y < 400:
                if self.move_down():
                    return True

            return False

        def draw(self):
            if self.highlighted == 1:
                if self.colour == 5 and self.y <= 336:
                    draw_sprite(highlight,self.x,self.y,6)
                else:
                    draw_sprite(highlight,self.x,self.y,self.colour)
            else:
                if self.colour == 5 and self.y <= 336:
                    draw_sprite(cube,self.x,self.y,6)
                else:
                    draw_sprite(cube,self.x,self.y,self.colour)

            if self.radioactive == 1:
                win.blit(radioactivity,(self.x,self.y))

        def move_down(self):
            if self.y == 368:
                return False
            for i in blocks:
                if i.x == self.x and i.y == self.y + 32:
                    return False

            return True

        def match(self):
            self.matched = True
            for i in reversed(blocks):
                if i.matched == False and i.colour == self.colour:
                    if i.x == self.x + 32 and i.y == self.y:
                        i.match()
                    if i.x == self.x - 32 and i.y == self.y:
                        i.match()
                    if i.x == self.x and i.y == self.y + 32:
                        i.match()
                    if i.x == self.x and i.y == self.y - 32:
                        i.match()

        def move_check(self):
            if self.colour == 5 and self.y == 368:
                return(True)
            if self.colour < 5:
                for i in reversed(blocks):
                    if i.colour == self.colour:
                        if i.x == self.x + 32 and i.y == self.y:
                            return(True)
                        if i.x == self.x - 32 and i.y == self.y:
                            return(True)
                        if i.x == self.x and i.y == self.y + 32:
                            return(True)
                        if i.x == self.x and i.y == self.y - 32:
                            return(True)

            return(False)

        def light(self):
            self.highlighted = True
            for i in blocks:
                if i.highlighted == False and i.colour == self.colour:
                    if i.x == self.x + 32 and i.y == self.y:
                        i.light()
                    if i.x == self.x - 32 and i.y == self.y:
                        i.light()
                    if i.x == self.x and i.y == self.y + 32:
                        i.light()
                    if i.x == self.x and i.y == self.y - 32:
                        i.light()

    class points_get():

        def __init__(self,points,x,y):
            self.points = points
            self.x = x
            self.y = y
            self.counter = 60

        def step(self):
            self.y -= 0.5
            self.counter -= 1

        def draw(self):
            font_render = pygame.font.Font.render(font,str(self.points),1,white)
            win.blit(font_render,(self.x - font_render.get_width()/2, int(self.y - font_render.get_height()/2)))

    class scoreboard():

        def __init__(self,reason,score,clear) -> None:
            self.time = 9
            self.x = 80
            self.y = -420
            self.clear = 0
            self.reason = reason
            self.score = score
            self.clearance = int(clear)
            self.bonus = 0
            self.total = score
            self.count = 2

            pygame.mixer.stop()
            pygame.mixer.Sound.play(sound_cleared)

        def step(self):
            if self.y < 80:
                self.y += 16
                if self.y > 80:
                    self.y = 80
            else:
                self.time -= 1/60
                self.count -= 1
                if self.count == 0:
                    self.count = 2
                    if self.clear < self.clearance:
                        self.clear += 1
                        if self.clear == 100:
                            pygame.mixer.Sound.play(sound_perfect)

                self.bonus = int(self.clear*block_amount/10)
                self.total = self.score + self.bonus


        def draw(self):
            win.blit(board,(self.x,self.y))

            text = pygame.font.Font.render(font,"LEVEL OVER",1,black)
            win.blit(text,(400-text.get_width()/2, self.y+16))

            text = pygame.font.Font.render(font,self.reason,1,black)
            win.blit(text,(self.x+32, self.y+96))
            if self.clear == self.clearance:
                if block_amount == 200:
                    text = pygame.font.Font.render(font,"Game finished!",1,black)
                elif self.clearance < 80:
                    text = pygame.font.Font.render(font,"You did not qualify!",1,black)
                else:
                    text = pygame.font.Font.render(font,"You qualified to the next level!",1,black)
                win.blit(text,(self.x+32, self.y+120))

            text = pygame.font.Font.render(font,"Clearance:",1,black)
            win.blit(text,(self.x+400, self.y+96))

            text = pygame.font.Font.render(font,"Score:",1,black)
            win.blit(text,(self.x+32, self.y+168))

            text = pygame.font.Font.render(font,"Bonus:",1,black)
            win.blit(text,(self.x+32, self.y+216))

            text = pygame.font.Font.render(font,"Total:",1,black)
            win.blit(text,(self.x+32, self.y+264))

            text = pygame.font.Font.render(font,str(self.score),1,black)
            win.blit(text,(self.x+128, self.y+168))

            text = pygame.font.Font.render(font,str(self.bonus),1,black)
            win.blit(text,(self.x+128, self.y+216))

            text = pygame.font.Font.render(font,str(self.total),1,black)
            win.blit(text,(self.x+128, self.y+264))

            if self.clear < 10:
                draw_sprite(num,self.x+416,self.y+140,-1)
                draw_sprite(num,self.x+448,self.y+140,-1)
                draw_sprite(num,self.x+480,self.y+140,self.clear)
            elif self.clear < 100:
                draw_sprite(num,self.x+416,self.y+140,-1)
                draw_sprite(num,self.x+448,self.y+140,int(str(self.clear)[0]))
                draw_sprite(num,self.x+480,self.y+140,int(str(self.clear)[1]))
            else:
                if int(self.time * 4) % 2 == 0:
                    draw_sprite(num,self.x+416,self.y+140,int(str(self.clear)[0]))
                    draw_sprite(num,self.x+448,self.y+140,int(str(self.clear)[1]))
                    draw_sprite(num,self.x+480,self.y+140,int(str(self.clear)[2]))
                else:
                    draw_sprite(num,self.x+416,self.y+140,-1)
                    draw_sprite(num,self.x+448,self.y+140,-1)
                    draw_sprite(num,self.x+480,self.y+140,-1)

            text = pygame.font.Font.render(font,"Continuing in:",1,black)
            win.blit(text,(self.x+540-text.get_width(), self.y+320))

            draw_sprite(num,self.x+572,self.y+312,math.ceil(self.time))



    def move_left(x):
        column = 0
        right = 1
        for i in blocks:
            if i.x == x:
                column = 1
            if i.x >= x:
                right = 0

        if right == 1:
            return 0
        if column == 0:
            return x
        if x < 720 and column == 1:
            return move_left(x+32)

        return 0

    def clearance():
        return (block_amount-len(blocks))/block_amount*100

    def sound(volume):
        pygame.mixer.Sound.set_volume(sound_blast,volume)
        pygame.mixer.Sound.set_volume(sound_blast_active,volume)
        pygame.mixer.Sound.set_volume(sound_bomb,volume)
        pygame.mixer.Sound.set_volume(sound_cleared,volume)
        pygame.mixer.Sound.set_volume(sound_combo,volume)
        pygame.mixer.Sound.set_volume(sound_intro,volume)
        pygame.mixer.Sound.set_volume(sound_warning,volume)
        pygame.mixer.Sound.set_volume(sound_loop,volume)
        pygame.mixer.Sound.set_volume(sound_no_combo,volume)
        pygame.mixer.Sound.set_volume(sound_over,volume)
        pygame.mixer.Sound.set_volume(sound_radioactive,volume)
        pygame.mixer.Sound.set_volume(sound_start,volume)
        pygame.mixer.Sound.set_volume(sound_warning,volume)

    def draw_sprite(sprite,x,y,number):
        if sprite == num:
            win.blit(sprite,(x,y),(number*30+30,0,30,54))
        elif sprite == cube or sprite == highlight:
            win.blit(sprite,(x,y),(number*32,0,32,32))
        elif sprite == blast:
            win.blit(sprite,(x,y),(number*68,0,68,68))

    def tutorial():
        text = pygame.font.Font.render(font,"Game instructions:",1,white)
        win.blit(text,(96, 96))

        text = pygame.font.Font.render(font,"Click on groups of two or more cubes to remove them.",1,white)
        win.blit(text,(96, 144))
        text = pygame.font.Font.render(font,"Level ends when you run out of moves or time.",1,white)
        win.blit(text,(96, 168))
        text = pygame.font.Font.render(font,"Clear at least 80% of the board to pass.",1,white)
        win.blit(text,(96, 192))

        text = pygame.font.Font.render(font,"Radioactive cubes double the score",1,white)
        win.blit(text,(144, 240))
        text = pygame.font.Font.render(font,"Fill up the blast to clear a column",1,white)
        win.blit(text,(144, 276))
        text = pygame.font.Font.render(font,"Bomb cubes activate when reaching the bottom",1,white)
        win.blit(text,(144, 312))

        draw_sprite(cube,96,308,5)
        win.blit(blast_scaled,(96,272),(224,0,32,32))
        draw_sprite(cube,96,236,3)
        win.blit(radioactivity,(96,236))


        text = pygame.font.Font.render(font,"Click to start now. The game will start in " + str(math.ceil(tutorial_time)),1,white)
        win.blit(text,(96, 384-text.get_height()))


    def main(_score,_level,_bonus):
        clock = pygame.time.Clock()

        score = _score
        global level
        level = _level
        if level == 1:
            time = 60
        elif level == 2:
            time = 90
        else:
            time = 180

        level_multi = level*0.1+0.9

        bonus_total = _bonus

        x = 80
        y = 80
        global block_amount
        block_amount = 0
        global blocks
        blocks = []
        for i in range(level*5+5):
            for i in range(10):
                blocks.append(block(x,y))
                y += 32
                block_amount += 1
            y = 80
            x += 32

        points_list = []
        run = True

        moving = 0
        move_x = 0

        lightning_mode = False
        lightning_x = 0

        blast_level = 0

        time_decimal = 0

        volume = pygame.mixer.Sound.get_volume(sound_loop)
        sound(volume)

        if level == 1:
            game = 0
            in_tutorial = 1
            global tutorial_time
            tutorial_time = 15
            pygame.mixer.Sound.play(sound_intro)
        else:
            game = 1
            in_tutorial = 0
            pygame.mixer.Sound.play(sound_start)


        board1 = 0
        reason = ""
        end_cooldown = 1

        busy = 1

        while run:
            clock.tick(FPS)

            if moving > 0:
                busy = 1
            else:
                #busy = 0
                for i in reversed(blocks):
                    moved = i.move()
                    if moved:
                        busy = 1

            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]


            if game == 1:
                if lightning_mode:
                    if mouse_x > 80 and mouse_x < 720 and mouse_y > 80 and mouse_y < 400:
                        lightning_x = int((mouse_x-80)/32)*32+80
                    else:
                        lightning_x = 0
                else:
                    for i in blocks:
                        i.highlighted = False
                    for i in blocks:
                        if mouse_x >= i.x and mouse_x < i.x + i.width and mouse_y >= i.y and mouse_y < i.y + i.width and busy == 0:
                            i.highlighted = True
                            if i.colour < 5:
                                i.light()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit()


                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x = pygame.mouse.get_pos()[0]
                    mouse_y = pygame.mouse.get_pos()[1]

                    text = pygame.font.Font.render(font,"End game",1,white)
                    if mouse_y > 564 and mouse_x < text.get_width() + 16:
                        gameover(score,bonus_total)

                    text = pygame.font.Font.render(font,"Sound off",1,white)
                    if mouse_y > 564 and mouse_x > 800 - text.get_width() - 16:
                        volume = pygame.mixer.Sound.get_volume(sound_loop)
                        volume = 1-volume
                        sound(volume)

                    if in_tutorial == 1:
                        in_tutorial = 0
                        game = 1
                        pygame.mixer.stop()
                        pygame.mixer.Sound.play(sound_start)

                    elif board1 != 0:
                        board1.time = 0

                    elif busy == 0 and game == 1:
                        matches = 0
                        multiplier = 1
                        if lightning_mode:
                            if lightning_x != 0:
                                lightning_mode = False
                                for i in reversed(blocks):
                                    if i.x == lightning_x:
                                        blocks.remove(i)
                                        matches += 1
                                        if i.radioactive == 1:
                                            multiplier *= 2
                                score_add = int((matches*matches*10)*multiplier*level_multi)
                                points_list.append(points_get(score_add,lightning_x+16,240))
                                score += score_add
                                busy = 1
                                pygame.mixer.Sound.play(sound_blast)
                        else:
                            for i in blocks:
                                if mouse_x >= i.x and mouse_x < i.x + i.width and mouse_y >= i.y and mouse_y < i.y + i.width:
                                    match_x = i.x + 16
                                    match_y = i.y
                                    if i.colour == 5:
                                        if i.y == 368:
                                            for j in reversed(blocks):
                                                if math.dist((i.x,i.y),(j.x,j.y)) < 64:
                                                    matches += 1
                                                    if j.radioactive == 1:
                                                        multiplier *= 2
                                                    blocks.remove(j)

                                            score_add = int((matches*matches*10)*multiplier*level_multi)
                                            points_list.append(points_get(score_add,match_x,match_y))
                                            score += score_add
                                            if blast_level < 100:
                                                blast_level += matches+(matches*0.5)*multiplier
                                                if blast_level >= 100:
                                                    pygame.mixer.Sound.play(sound_blast_active)
                                            busy = 1
                                            pygame.mixer.Sound.play(sound_bomb)

                                    else:
                                        i.match()
                                        for j in blocks:
                                            if j.matched:
                                                matches += 1
                                                if j.radioactive == 1:
                                                    multiplier *= 2
                                        if matches > 1:
                                            for k in reversed(blocks):
                                                if k.matched:
                                                    blocks.remove(k)
                                                else:
                                                    k.matched = False

                                            score_add = int((matches*matches*10)*multiplier*level_multi)
                                            points_list.append(points_get(score_add,match_x,match_y))
                                            score += score_add
                                            if blast_level < 100:
                                                blast_level += matches+(matches*0.5)*multiplier
                                                if blast_level >= 100:
                                                    pygame.mixer.Sound.play(sound_blast_active)
                                            busy = 1
                                            if multiplier > 1:
                                                pygame.mixer.Sound.play(sound_radioactive)
                                            else:
                                                pygame.mixer.Sound.play(sound_combo)


                                        else:
                                            for i in reversed(blocks):
                                                i.matched = False

                            if mouse_x > 652 and mouse_x < 720 and mouse_y > 484 and mouse_y < 552 and blast_level == 100:
                                lightning_mode = True
                                blast_level = 0

            was_busy = busy
            if moving == 0 and busy == 1:
                #if len(blocks) == 0:
                    #busy = 0
                #else:
                    moved = False
                    for i in reversed(blocks):
                        self_moved = i.check()
                        if self_moved and moved == False:
                            moved = True
                    if moved == False:
                        busy = 0

            if moving > 0:
                for i in blocks:
                    if i.x > move_x:
                        i.x -= spd
                moving -= spd
                busy = 1

            if busy == 0:
                move_x = move_left(80)
                if move_x > 0:
                    moving = 32
                    busy = 1

            if busy == 0 and was_busy == 1:
                matches = False
                i = len(blocks)-1
                while matches == False and i >= 0:
                    j = blocks[i]
                    matches = j.move_check()
                    i -= 1

                if matches == False:
                    game = 0
                    blast_level = 0
                    percentage = clearance()
                    reason = "No more moves"

            if game == 1:
                time_decimal += 1/FPS
                if time_decimal >= 1:
                    time_decimal = 0
                    time -= 1

                    if time == 5:
                        pygame.mixer.Sound.play(sound_warning,-1)

                if pygame.mixer.Sound.get_num_channels(sound_start) == 0 and pygame.mixer.Sound.get_num_channels(sound_loop) == 0:
                    pygame.mixer.Sound.play(sound_loop,-1)

            if game == 0 and pygame.mixer.Sound.get_num_channels(sound_warning) != 0:
                pygame.mixer.Sound.stop(sound_warning)

            if time == 0 and game == 1:
                game = 0
                blast_level = 0
                percentage = clearance()
                reason = "Time ran out"

            if blast_level > 100:
                blast_level = 100

            if game == 0 and board1 == 0 and in_tutorial == 0:
                end_cooldown -= 1/60
                if end_cooldown <= 0:
                    board1 = scoreboard(reason,score,percentage)



            #Drawing

            win.blit(background,(0,0))

            if in_tutorial:
                tutorial_time -= 1/60
                tutorial()
                if tutorial_time <= 0:
                    in_tutorial = 0
                    game = 1
                    pygame.mixer.Sound.play(sound_start)
            else:
                for i in blocks:
                    i.draw()

                if level == 1:
                    win.blit(border1,(400,80))
                if level == 2:
                    win.blit(border2,(560,80))

            if lightning_mode and lightning_x != 0:
                win.blit(beam,(lightning_x,80))

            draw_sprite(num,92,496,level)
            score_string = str(score).zfill(9)
            j = 0
            for i in score_string:
                draw_sprite(num,172+j*32,496,int(i))
                j += 1
            #win.blit(num,(80,432))

            minutes = math.floor(time/60)
            seconds = str(time % 60).zfill(2)

            draw_sprite(num,500,496,minutes)
            draw_sprite(num,532,496,10)
            draw_sprite(num,544,496,int(seconds[0]))
            draw_sprite(num,576,496,int(seconds[1]))
            blast_frame = int(blast_level/100*7)
            draw_sprite(blast,652,484,blast_frame)

            for i in reversed(points_list):
                i.step()
                if i.counter == 0:
                    points_list.remove(i)
                i.draw()

            text = pygame.font.Font.render(font,"End game",1,white)
            win.blit(text,(8, 568))

            if volume:
                text = pygame.font.Font.render(font,"Sound off",1,white)
            else:
                text = pygame.font.Font.render(font,"Sound on",1,white)
            win.blit(text,(792-text.get_width(), 568))

            if game == 0:
                if board1 != 0:
                    board1.step()
                    board1.draw()
                    if board1.y == -404:
                        bonus = int(int(percentage)*block_amount/10)
                        score += bonus
                        bonus_total += bonus
                    if board1.time <= 0:
                        if level < 3 and board1.clearance >= 80:
                            main(score,level+1,bonus_total)
                        else:
                            gameover(score,bonus_total)

            #text = pygame.font.Font.render(font,"FPS "+str(clock.get_fps()),1,white)
            #win.blit(text,(8, 8))

            pygame.display.update()

    def gameover(score,bonus):
        clock = pygame.time.Clock()
        time = 15
        run = True

        volume = int(pygame.mixer.Sound.get_volume(sound_loop))

        pygame.mixer.stop()
        pygame.mixer.Sound.play(sound_over)

        config = ConfigParser()
        if score > highscore:
            config["klickklack"] = {
                "highscore": str(score),
                "sound": str(volume)
            }
        else:
            config["klickklack"] = {
                "highscore": str(highscore),
                "sound": str(volume)
            }

        with open(os.path.join(directory,"data.ini"),"w") as save:
            config.write(save)



        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit()

            clock.tick(FPS)
            time -= 1/FPS

            if time <= 0:
                sys.exit()

            win.blit(background_outro,(0,0))

            prev_score = score - bonus

            text = pygame.font.Font.render(font,"GAME OVER",1,white)
            win.blit(text,(32, 96))
            text = pygame.font.Font.render(font,"Score:",1,white)
            win.blit(text,(32, 168))
            text = pygame.font.Font.render(font,"Bonus:",1,white)
            win.blit(text,(32, 216))
            text = pygame.font.Font.render(font,"Total:",1,white)
            win.blit(text,(32, 264))

            text = pygame.font.Font.render(font,"Personal Highscore: " + str(highscore),1,white)
            win.blit(text,(32, 336))

            text = pygame.font.Font.render(font,str(prev_score),1,white)
            win.blit(text,(128, 168))
            text = pygame.font.Font.render(font,str(bonus),1,white)
            win.blit(text,(128, 216))
            text = pygame.font.Font.render(font,str(score),1,white)
            win.blit(text,(128, 264))

            text = pygame.font.Font.render(font,"Game ends in: " + str(math.ceil(time)),1,white)
            win.blit(text,(32, 544))

            pygame.display.update()

    sound(volume)

    if __name__ == "__main__":
        main(0,1,0)

except Exception as e:
    tk = tkinter.Tk().withdraw()
    txt = "An error has occured \n \n" + traceback.format_exc(0)

    tk = messagebox.showerror("Klicker Elektro",txt)