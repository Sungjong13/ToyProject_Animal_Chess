import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from AC2_Variables import *
import glob
import os
import pathlib

root=tk.Tk()
root.title('Animal Chess')
root.geometry('600x700')
root.resizable(False,False)

#structure related code
_leftframe=tk.Frame(root)
_leftframe.pack(side='left')
_textboxtitle=tk.LabelFrame(_leftframe,text='Situation Report',width=460,height=70)
_textboxtitle.grid(row=4,columnspan=3)
_textboxtitle.grid_propagate(False)
sitrep=tk.Text(_textboxtitle)
sitrep.place(width=452,height=48,)

_rightframe=tk.Frame(root)
_rightframe.pack(side='right',fill='both')
_winningconditiontitle=tk.LabelFrame(_rightframe,text='Help',width=125,height=390)
_winningconditiontitle.pack(side='top')
_winningconditiontitle.pack_propagate(False)
_winningcondition=tk.Text(_winningconditiontitle,height=390)
_winningcondition.pack()
if pathlib.Path('winning_conditions.txt').is_file:
# if os.path.isfile(r'C:\Users\1000d\Desktop\program projects\simple game projects\animal chess\winning_conditions.txt'):
    with open(pathlib.Path('winning_conditions.txt'),'r',encoding='utf8') as file:
    # with open(r'C:\Users\1000d\Desktop\program projects\simple game projects\animal chess\winning_conditions.txt','r',encoding='utf8') as file:
        _winningcondition.insert(tk.END,file.read())
_winningcondition.configure(state='disabled')

_capturedareaframe=tk.LabelFrame(_rightframe,text='Captured Pieces')
_capturedareaframe.pack(side='bottom')
_p1capturearea=tk.LabelFrame(_capturedareaframe,text='P1')
_p1capturearea.pack(side='top')
_p2capturearea=tk.LabelFrame(_capturedareaframe,text='P2')
_p2capturearea.pack(side='bottom')

#button related code
def get_pic(animal_name):
    return Image.open(_pic_dic[animal_name])
def flip_pic(get_pic):
    img=get_pic.transpose(Image.FLIP_TOP_BOTTOM)
    img=img.convert('L')
    return ImageOps.invert(img)
def animal_pic(get_pic):
    return ImageTk.PhotoImage(get_pic.resize((150,150),Image.ANTIALIAS))
def small_animal_pic(get_pic):
    return ImageTk.PhotoImage(get_pic.resize((54,54),Image.ANTIALIAS))
    
_animal_name_list=['Chick','Chicken','Elephant','Empty','Giraff','Tiger']
_pic_dic=dict(zip(_animal_name_list,glob.glob('image_folder/*.png')))
image_dic={}
small_image_dic={}
flipped_image_dic={}
for i in _animal_name_list:
    image_dic[i]=animal_pic(get_pic(i))
for i in _animal_name_list:
    small_image_dic[i]=small_animal_pic(get_pic(i))
for i in _animal_name_list:
    flipped_image_dic[i]=animal_pic(flip_pic(get_pic(i)))

button_dic={}
click_var=tk.StringVar()
x,y=[0,0]

for location in board_code_list: #making 12 board buttons
    button_dic[location]=tk.Button(_leftframe,command=lambda location=location: click_var.set(location),image=image_dic['Empty'])
    button_dic[location].grid(row=x,column=y)
    y+=1
    if y==3:
        y=0;x+=1

x,y=[0,0]
for code in P1captured_code_list:
    button_dic[code]=tk.Button(_p1capturearea,command=lambda code=code: click_var.set(code),image=small_image_dic['Empty'])
    # capturebutton_dic[code].image=small_animal_pic(get_pic('Empty'))
    button_dic[code].grid(row=x,column=y)
    x+=1
    if x==2:
        y+=1;x=0
x,y=[0,0]
for code in P2captured_code_list:
    button_dic[code]=tk.Button(_p2capturearea,command=lambda code=code: click_var.set(code),image=small_image_dic['Empty'])
    # capturebutton_dic[code].image=small_animal_pic(get_pic('Empty'))
    button_dic[code].grid(row=x,column=y)
    x+=1
    if x==2:
        y+=1;x=0

def change_turn(currentturn):
    global turn
    if currentturn==1:
        turn=2
    elif currentturn==2:
        turn=1
def current_player(currentturn):
    if turn==1:
        return 'P1'
    elif turn==2:
        return 'P2'
def change_player(current_player):
    if current_player=='P1':
        return 'P2'
    elif current_player=='P2':
        return 'P1'
def update_sitrep(string): #updating the textbox on bottom
    sitrep.configure(state='normal')
    if sitrep.get('1.0',tk.END).count('\n')>=4:
        sitrep.delete('1.0','2.0')
    sitrep.insert(tk.END,string+'\n')
    sitrep.configure(state='disabled')
def update_image(location,entityname='Empty',entityowner='No_Owner'):
    if location in board_code_list:
        if entityowner=='P2':
            button_dic[location].configure(image=flipped_image_dic[entityname])
        # elif entityowner=='P1':
        else:
            button_dic[location].configure(image=image_dic[entityname])
    elif location in captured_code_list:
        button_dic[location].configure(image=small_image_dic[entityname])
    else:
        print('image update error')
def checkGG():
    global game_status, P1lairinvadecounter, P2lairinvadecounter
    for code in captured_code_list:
        if tile_dic[code][0]=='Tiger': #상대 호랑이 잡으면 승리
            update_sitrep(change_player(tile_dic[code][1])+tile_dic[code][0]+' was captured. '+tile_dic[code][1]+' wins!')
            print('tiger captured GG')
            game_status=False
    for code in lair_dic['P1']:
        if tile_dic[code][0]=='Tiger' and tile_dic[code][1]=='P2':
            P2lairinvadecounter+=1
            if P2lairinvadecounter==2:
                update_sitrep('P2Tiger claimed opponents lair. P2 wins!')
                print('tiger lair invade GG')
                game_status=False
                break
            update_sitrep("P2 tiger in P1 lair! P2 will win if tiger isn't captured!")
            print('laircounter added')
    for code in lair_dic['P2']:
        if tile_dic[code][0]=='Tiger' and tile_dic[code][1]=='P1':
            P1lairinvadecounter+=1
            if P1lairinvadecounter==2:
                update_sitrep('P1Tiger claimed opponents lair. P1 wins!')
                print('tiger lair invade GG')
                game_status=False
                break
            update_sitrep("P1 tiger in P2 lair! P1 will win if tiger isn't captured!")
            print('laircounter added')
def initial_board_setting():
    global turn, game_status, P1lairinvadecounter, P2lairinvadecounter
    for i in tile_code_list:
        tile_dic[i]=['Empty','No_Owner']
    turn=1
    game_status=True
    P1lairinvadecounter=0
    P2lairinvadecounter=0
    for i in tile_code_list:
        update_image(i)
    place_entity('Chick','P1','C2')
    place_entity('Elephant','P1','D1')
    place_entity('Giraff','P1','D3')
    place_entity('Tiger','P1','D2')
    place_entity('Chick','P2','B2')
    place_entity('Elephant','P2','A3')
    place_entity('Giraff','P2','A1')
    place_entity('Tiger','P2','A2')
    update_image('C2','Chick','P1')
    update_image('D1','Elephant','P1')
    update_image('D3','Giraff','P1')
    update_image('D2','Tiger','P1')
    update_image('B2','Chick','P2')
    update_image('A3','Elephant','P2')
    update_image('A1','Giraff','P2')
    update_image('A2','Tiger','P2')
# def undo_move(): #1.1 still working on it 2022.3.4
#     global P1lairinvadecounter,P2lairinvadecounter,turn
#     if P1lairinvadecounter #lair invade counter undo
#     if #chick evolve undo
#     if recorded_move_list[-1][4]==True: #capture undo
#         move_entity(recorded_move_list[-2][0],change_player(recorded_move_list[-2][1]),recorded_move_list[-2][3],recorded_move_list[-2][2])
#         move_entity(recorded_move_list[-1][0],change_player(recorded_move_list[-1][1]),recorded_move_list[-1][3],recorded_move_list[-1][2])
#         update_image(recorded_move_list[-2][2],recorded_move_list[-2][0],recorded_move_list[-2][1])
#         update_image(recorded_move_list[-2][3])
#         update_image(recorded_move_list[-1][2],recorded_move_list[-1][0],recorded_move_list[-1][1])
#         update_image(recorded_move_list[-1][3])
#     else: #move undo
#         move_entity(recorded_move_list[-1][0],recorded_move_list[-1][1],recorded_move_list[-1][3],recorded_move_list[-1][2])
#         update_image(recorded_move_list[-1][2],recorded_move_list[-1][0],recorded_move_list[-1][1])
#         update_image(recorded_move_list[-1][3])
#     del recorded_move_list[-1]
#     change_turn(turn)
#     infinite_loop() #need to do this????


#game scenario
def infinite_loop():
    global turn, game_status, tile_dic
    if game_status==True:
        # while game_status:
        update_sitrep('Player'+str(turn)+' your turn.')
        for i in tile_code_list:
            print('waiting for first click')
            button_dic[i].wait_variable(click_var)
            first_click=click_var.get()
            if tile_dic[first_click][0]=='Empty': #check if selected empty space
                update_sitrep('Empty space selected, try again.')
                print('first click empty space selected CONTINUE')
                continue
            if tile_dic[first_click][1]==change_player(current_player(turn)): #check if selected opponent entity
                update_sitrep('Cannot select opponents piece')
                print('first click opponent entity selected CONTINUE')
                continue
            if first_click in captured_dic[change_player(current_player(turn))]: #check if selected opponent captured space
                update_sitrep('Cannot select opponents captured pieces')
                print('first click opponent captured selected CONTINUE')
                continue
            if first_click in board_code_list:
                update_sitrep(tile_dic[first_click][1]+tile_dic[first_click][0]+' selected.')
                for i in tile_code_list:
                    print('waiting for second click')
                    button_dic[i].wait_variable(click_var)
                    second_click=click_var.get()
                    if second_click in captured_code_list: #check if selected captured space
                        update_sitrep('Cannot move into captured piece area')
                        print('move, second click selected captured area BREAK')
                        break
                    if check_valid_move(tile_dic[first_click][0],current_player(turn),first_click,second_click)==False: #check if selected invalid moving space
                        update_sitrep(tile_dic[first_click][0]+' cannot move that direction.')
                        print('move, second click invalid move BREAK')
                        break
                    if tile_dic[second_click][1]==current_player(turn): #check if selected ally occupied space
                        update_sitrep('Area blocked by allied piece')
                        print('move, second click allied collision BREAK')
                        break
                    if tile_dic[second_click][1]==change_player(current_player(turn)): #check if selected enemy occupied space
                        if tile_dic[second_click][0]=='Chicken':
                            tile_dic[second_click][0]='Chick'
                        for location in captured_dic[change_player(tile_dic[second_click][1])]: #update captured area picture
                            if tile_dic[location][0]=='Empty':
                                update_image(location,tile_dic[second_click][0])
                                break
                        kill_entity(tile_dic[second_click][0],tile_dic[second_click][1],second_click)
                        update_image(second_click) #update emptied area picture #unnecessary
                    update_image(second_click,tile_dic[first_click][0],tile_dic[first_click][1]) #update pictures
                    update_image(first_click)
                    move_entity(tile_dic[first_click][0],current_player(turn),first_click,second_click)
                    if tile_dic[second_click][0]=='Chick' and second_click in lair_dic[change_player(tile_dic[second_click][1])]: #check chick and evolve. second click since after move.
                        tile_dic[second_click][0]='Chicken'
                        update_image(second_click,'Chicken',tile_dic[second_click][1])
                        update_sitrep(tile_dic[second_click][1]+'Chick evolved into Chicken')
                        print('chick evolution')
                    change_turn(turn)
                    break
            elif first_click in captured_dic[current_player(turn)]:
                update_sitrep(tile_dic[first_click][1]+tile_dic[first_click][0]+' selected.')
                for i in tile_code_list:
                    print('waiting for second click')
                    button_dic[i].wait_variable(click_var)
                    second_click=click_var.get()
                    if second_click in captured_code_list: #check if selected captured space again
                        update_sitrep('Invalid location selected')
                        print('place, second click capture area selected BREAK')
                        break
                    if tile_dic[second_click][0]!='Empty': #check if selected ally or enemy occupied space
                        update_sitrep('Cannot place over other pieces')
                        print('place, second click collision error BREAK')
                        break
                    if second_click in lair_dic[change_player(current_player(turn))]: #check if selected enemy lair
                        update_sitrep('Cannot place in opponents lair')
                        print('place, second click opponent lair err BREAK')
                        break
                    update_image(second_click,tile_dic[first_click][0],current_player(turn)) #update pictures
                    update_image(first_click)
                    move_entity(tile_dic[first_click][0],current_player(turn),first_click,second_click)
                    change_turn(turn)
                    break
            else:
                raise
            break
        checkGG()
    if game_status==True:
        root.after(500, func=infinite_loop())

#menu related code
def new_game():
    global game_status, turn
    initial_board_setting()
    infinite_loop()
def end_game():
    game_status=False
    root.quit()
    root.destroy()
menu=tk.Menu(root)
_menu_game=tk.Menu(menu,tearoff=0)
_menu_game.add_command(label='New Game',command=new_game)
_menu_game.add_command(label='Quit Game',command=end_game)
_menu_game.add_command(label='Undo Last Move',command=undo_move)
menu.add_cascade(label='Game',menu=_menu_game)
root.config(menu=menu)
root.protocol('WM_DELETE_WINDOW',end_game)
root.mainloop()


#problems to fix

#quit game in menu doesn't work