import random
import pygame
from sys import exit
from random import randint, choice

        

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) -start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 6

            if obstacle_rect.bottom == 300: screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list    
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = wolf_jump
    else:
        player_index += 0.1
        if player_index>= len(player_walk):player_index = 0 
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')

clock = pygame.time.Clock() #frames per second controller
test_font = pygame.font.Font('.\\pygame\\font\\Pixeltype.ttf',50)
game_active = True
start_time = 0
score = 0     

bg_Music = pygame.mixer.Sound('.//pygame//audio//music.wav')
bg_Music.play(loops = -1)  #loops = -1 means infinite time it will play


#test_surface = pygame.Surface((100,200)) #surface
#test_surface.fill('Red') #fill the surface color

sky_surface = pygame.image.load('.//pygame//graphics/bg.png').convert()
ground_surface = pygame.image.load('./pygame/graphics/ground.png').convert()
# score_surf = test_font.render('Bhag Manash Bhag', False,(64,64,64))
# score_rect = score_surf.get_rect(center=(400,50))

#moving surfaces
snail_frame_1 = pygame.image.load('./pygame/graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('./pygame/graphics/snail/snail2.png').convert_alpha()
obstacle_size = (50,27)
snail_frame_1 = pygame.transform.scale(snail_frame_1,obstacle_size)
snail_frame_2 = pygame.transform.scale(snail_frame_2,obstacle_size)
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]
snail_x_pos = 800
# snail_rect = snail_surf.get_rect(bottomright = (400,100))
snail_rect = snail_surf.get_rect(bottomright = (300,70))

fly_frame_1 = pygame.image.load('./pygame/graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('./pygame/graphics/fly/fly2.png').convert_alpha()
fly_frame_1 = pygame.transform.scale(fly_frame_1,(40,30))
fly_frame_2 = pygame.transform.scale(fly_frame_2,(40,30))
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

wolf_walk1 = pygame.image.load('./pygame/graphics/wolf/run1.png').convert_alpha()
wolf_walk2 = pygame.image.load('./pygame/graphics/wolf/run2.png').convert_alpha()
wolf_jump = pygame.image.load('./pygame/graphics/wolf/jump.png').convert_alpha()
wolf_size = (120,97)
wolf_walk1 = pygame.transform.scale(wolf_walk1,wolf_size)
wolf_walk2 = pygame.transform.scale(wolf_walk2,wolf_size)
wolf_jump = pygame.transform.scale(wolf_jump,wolf_size)

player_walk = [wolf_walk1,wolf_walk2]
player_index = 0

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(topleft=(90,150))
player_gravity = 0
# Set initial player movement speed
player_speed = 5
min_player_x = 0
max_player_x = 800 - player_rect.width

#intro screen
wolf_stand = pygame.image.load('./pygame/graphics/wolf/stand.png').convert_alpha()
wolf_stand= pygame.transform.rotozoom(wolf_stand,0,2)
wolf_stand_rect = wolf_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner' , False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

# game_message = test_font.render('Press space to run or close your fist in camera',False,(111,196,169))
# game_message_rect = game_message.get_rect(center=(400,320))

# First part of the sentence
first_part_message = "Press space to run"
first_part_surf = test_font.render(first_part_message, False, (111, 196, 169))
first_part_rect = first_part_surf.get_rect(center=(400, 300))

# Second part of the sentence
second_part_message = "or close your fist in camera"
second_part_surf = test_font.render(second_part_message, False, (111, 196, 169))
second_part_rect = second_part_surf.get_rect(center=(400, 340))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)


intro_screen = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #pygame.MOUSEBUTTONUP
        #pygame.MOUSEBUTTONDOWN
        #if event.type == pygame.MOUSEMOTION:
            #print(event.pos)
            #if player_rect.collidepoint(event.pos):print('Chot lag gai')

        # if event.type == pygame.KEYUP: #any key is up 
        #     print('key up')

         # Handle events for the intro screen
        if intro_screen:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                intro_screen = False
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)


        elif game_active:
            # Handle arrow key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_rect.x -= player_speed
                    

                elif event.key == pygame.K_RIGHT:
                    player_rect.x += player_speed
                    

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom>=300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN: #any key is pressed
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and player_rect.bottom>=300:
                    player_gravity = -20

            # Ensure the player does not go outside the frame
            player_rect.x = max(min_player_x, player_rect.x)
            if player_rect.x > max_player_x:
                player_rect.x = max_player_x

                   
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left = 800
                start_time = int(pygame.time.get_ticks()/1000 ) 


        if game_active:
            if event.type == obstacle_timer:
                # obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),180)))
            
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]


    if intro_screen:
        screen.fill((94, 129, 162))
        screen.blit(game_name, game_name_rect)
        # screen.blit(game_message, game_message_rect)
        screen.blit(first_part_surf, first_part_rect)
        screen.blit(second_part_surf, second_part_rect)
    
    elif game_active:
        screen.blit(sky_surface,(0,0)) #add the surface with location
        screen.blit(ground_surface,(0,300))
        # pygame.draw.rect(screen,'#c0e8ec',score_rect)
        # screen.blit(score_surf,score_rect)
        score = display_score()

        # snail_x_pos -= 3
        # if snail_x_pos < -100 : snail_x_pos = 800
        # #screen.blit(snail_surface,(snail_x_pos,265))
        # snail_rect.x -= 4
        # if snail_rect.right <= 0 : snail_rect.left = 800
        # screen.blit(snail_surf,snail_rect)

        #player
        # player_rect.left += 1
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf,player_rect)
        
        

        # player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed

        #sprite class
        # player.draw(screen)
        # player.update()

        # obstacle_group.draw(screen)
        # obstacle_group.update()


        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision
        game_active = collisions(player_rect,obstacle_rect_list)
        # game_active = collision_sprite()


    #key pressed
    #keys = pygame.key.get_pressed()
    #if keys[pygame.K_SPACE]:
        #print('jump')

    #collision with snail
    # if player_rect.colliderect(snail_rect):
    #     print('Collision')

    #collide with mouse
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     #print('Chuho mat') 
    #     print(pygame.mouse.get_pressed())


        # if snail_rect.colliderect(player_rect):
        #     game_active = False

    else:
        screen.fill((94,129,162))
        screen.blit(wolf_stand,wolf_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center=(400,330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            # screen.blit(game_message,game_message_rect)
            screen.blit(first_part_surf, first_part_rect)
            screen.blit(second_part_surf, second_part_rect)
        else:
            screen.blit(score_message,score_message_rect)
            
    pygame.display.update()
    clock.tick(60)