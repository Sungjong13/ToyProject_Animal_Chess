import tkinter as tk
from PIL import Image, ImageTk
from AC_Variables import *
from AC_Class import *
# from threading import Thread
import glob
import os

root=tk.Tk()
root.title('Animal Chess')
root.geometry('600x700')
# root.resizable(False,False)

_animal_name_list=['Chick','Chicken','Elephant','Empty','Giraff','Tiger']
_pic_dic=dict(zip(_animal_name_list,glob.glob('image_folder/*.png')))

def get_pic(animal_name):
    return Image.open(_pic_dic[animal_name])
def flip_pic(get_pic):
    return get_pic.transpose(Image.FLIP_TOP_BOTTOM)
def animal_pic(get_pic):
    return ImageTk.PhotoImage(get_pic.resize((150,150),Image.ANTIALIAS))
def small_animal_pic(get_pic):
    return ImageTk.PhotoImage(get_pic.resize((54,54),Image.ANTIALIAS))

# def btn_select(location):
#     global clicked_btn_location
#     clicked_btn_location=location
    # print(location+'\n')
    # return location
#이 값이 input()기다리는 프로그램에 전달이 될까?
def update_sitrep(string): #updating the textbox on bottom
    sitrep.configure(state='normal')
    if sitrep.get('1.0',tk.END).count('\n')>=4:
        sitrep.delete('1.0','2.0')
    sitrep.insert(tk.END,string+'\n')
    sitrep.configure(state='disabled')

def new_game():
    global Whoturn, C1, T1, E1, G1, C2, T2, G2, E2
    Whoturn='1'
    _Pwhoturn={'1':'P1','2':'P2'}
    game_status=True

    C1=Piece('Chick','C2','P1')
    T1=Piece('Tiger','D2','P1')
    E1=Piece('Elephant','D1','P1')
    G1=Piece('Giraff','D3','P1')
    C2=Piece('Chick','B2','P2')
    T2=Piece('Tiger','A2','P2')
    E2=Piece('Elephant','A1','P2')
    G2=Piece('Giraff','A3','P2')


# game_thread=Thread(target=new_game, daemon=True)

menu=tk.Menu(root)
menu_game=tk.Menu(menu,tearoff=0)
menu_game.add_command(label='New Game',command=new_game())
# menu_game.add_command(label='New Game',command=game_thread.start())
menu_game.add_command(label='Quit Game',command=root.quit)
menu.add_cascade(label='Game',menu=menu_game)

image_dic={}
small_image_dic={}
flipped_image_dic={}
for i in _animal_name_list:
    image_dic[i]=animal_pic(get_pic(i))
for i in _animal_name_list:
    small_image_dic[i]=small_animal_pic(get_pic(i))
for i in _animal_name_list:
    flipped_image_dic[i]=animal_pic(get_pic(i).transpose(Image.FLIP_TOP_BOTTOM))

leftframe=tk.Frame(root)
leftframe.pack(side='left')
button_dic={}
x,y=[0,0]

click_var=tk.StringVar()
for location in TileNames: #making 12 board buttons
    button_dic[location]=tk.Button(leftframe,command=lambda location=location: click_var.set(location),image=image_dic['Empty'])
    # button_dic[location]=tk.Button(leftframe,command=lambda location=location: btn_select(location),image=animal_pic(get_pic('Tiger')))
    # button_dic[location].image=animal_pic(get_pic('Tiger'))
    button_dic[location].grid(row=x,column=y)
    y+=1
    if y==3:
        y=0;x+=1


textboxtitle=tk.LabelFrame(leftframe,text='Situation Report',width=460,height=70)
textboxtitle.grid(row=4,columnspan=3)
textboxtitle.grid_propagate(False)
sitrep=tk.Text(textboxtitle)
sitrep.place(width=452,height=48,)

rightframe=tk.Frame(root)
rightframe.pack(side='right',fill='both')

winningconditiontitle=tk.LabelFrame(rightframe,text='Help',width=125,height=390)
winningconditiontitle.pack(side='top')
winningconditiontitle.pack_propagate(False)
winningcondition=tk.Text(winningconditiontitle,height=390)
winningcondition.pack()
if os.path.isfile(r'C:\Users\1000d\Desktop\program projects\simple game projects\animal chess\winning_conditions.txt'):
    with open(r'C:\Users\1000d\Desktop\program projects\simple game projects\animal chess\winning_conditions.txt','r',encoding='utf8') as file:
        winningcondition.insert(tk.END,file.read())
winningcondition.configure(state='disabled')

_capturedareaframe=tk.LabelFrame(rightframe,text='Captured Pieces')
_capturedareaframe.pack(side='bottom')
_p1capturearea=tk.LabelFrame(_capturedareaframe,text='P1')
_p1capturearea.pack(side='top')
_p2capturearea=tk.LabelFrame(_capturedareaframe,text='P2')
_p2capturearea.pack(side='bottom')

# capturebutton_dic={} #making captured buttons #걍 button_dic 써도 됨
_P1_captured_areacode_list=['H1','I1','J1','K1']
_P2_captured_areacode_list=['L2','M2','N2','O2']
total_areacode_list=TileNames+_P1_captured_areacode_list+_P2_captured_areacode_list
captured_areacode_dic={'P1':_P1_captured_areacode_list,'P2':_P2_captured_areacode_list}
x,y=[0,0]
for code in _P1_captured_areacode_list:
    button_dic[code]=tk.Button(_p1capturearea,command=lambda code=code: click_var.set(code),image=small_image_dic['Empty'])
    # capturebutton_dic[code].image=small_animal_pic(get_pic('Empty'))
    button_dic[code].grid(row=x,column=y)
    x+=1
    if x==2:
        y+=1;x=0
x,y=[0,0]
for code in _P2_captured_areacode_list:
    button_dic[code]=tk.Button(_p2capturearea,command=lambda code=code: click_var.set(code),image=small_image_dic['Empty'])
    # capturebutton_dic[code].image=small_animal_pic(get_pic('Empty'))
    button_dic[code].grid(row=x,column=y)
    x+=1
    if x==2:
        y+=1;x=0

def KillCaptured():
    for livecode in captures_dic['P1']+captures_dic['P2']:
        livecode.Kill()
        if livecode.name=='Chicken':
            livecode.name='Chick'
            livecode.moveable_dir=Moveable_dir_dic[livecode.ownership]['Chick']
            # if livecode.ownership=='P1':
            #     livecode.moveable_dir=P1_Dic_moveable_dir['Chick']
            # if livecode.ownership=='P2':
            #     livecode.moveable_dir=P2_Dic_moveable_dir['Chick']

def Winner(player):
    update_sitrep('Congratulations! You Win '+player+'!')
    global game_status
    game_status=False   ###끄는거도 기능 생각해야할듯

def CheckGG():
    if T1 in captures_dic['P2']: #상대 호랑이 잡으면 승리
        Winner('Player 2')
    elif T2 in captures_dic['P1']:
        Winner('Player 1')
    if T1.location in Lair_dic['P2']:
        update_sitrep("P1 tiger in P2 lair! P1 will win if tiger isn't captured!")
        ShowMapStatus()
        turn('P2','2')
        if T1.location in Lair_dic['P2']:
            Winner('Player 1')
    elif T2.location in Lair_dic['P1']:
        update_sitrep("P2 tiger in P1 lair! P2 will win if tiger isn't captured!")
        ShowMapStatus()
        turn('P1','1')
        if T2.location in Lair_dic['P1']:
            Winner('Player 2')

def change_turn(player):
    global Whoturn
    if player=='P1':
        Whoturn='2'
    elif player=='P2':
        Whoturn='1'

def update_board(): #################################
    for instance in units_dic['P1']:
        button_dic[instance.location].configure(image=image_dic[instance.name])
        # button_dic[instance.location].image=animal_pic(get_pic(instance.name))
    for instance in units_dic['P2']:
        button_dic[instance.location].configure(image=flipped_image_dic[instance.name])
        # button_dic[instance.location].image=animal_pic(get_pic(instance.name).transpose(Image.FLIP_TOP_BOTTOM))
    occupied_location=[]
    for instance in units_dic['P1']+units_dic['P2']:
        occupied_location.append(instance.location)
    unoccupied_location=[x for x in TileNames if x not in occupied_location]
    for locatoin in unoccupied_location:
        button_dic[locatoin].configure(image=image_dic['Empty'])
    occupied_location=[]
    for instance in captures_dic['P1'] and captures_dic['P2']:
        button_dic[instance.location].configure(image=small_image_dic[instance.name])
        # button_dic[instance.location].image=small_animal_pic(get_pic(instance.name))
        occupied_location.append(instance.location)
    unoccupied_location=[x for x in captures_dic['P1']+captures_dic['P2'] if x not in occupied_location]
    # unoccupied_location=list(set(captures_dic['P1']+captures_dic['P2'])-set(occupied_location))
    for locatoin in unoccupied_location:
        button_dic[locatoin].configure(image=small_image_dic['Empty'])

def update_captured_location():
    for instance in captures_dic['P1']:
        for i in captured_areacode_dic['P1']:
            instance.location=i
    for instance in captures_dic['P2']:
        for i in captured_areacode_dic['P2']:
            instance.location=i

#input 바꾸기
#tilestatus랑 그림 동기화하기

def turn(player):
    global Whoturn
    update_sitrep('Player'+Whoturn+', your turn')
    while Whoturn==list(_Pwhoturn.keys())[list(_Pwhoturn.values()).index(player)]:
        for i in total_areacode_list:
            update_sitrep('click button')
            print('waiting first click')
            button_dic[i].wait_variable(click_var)
            first_click=click_var.get()
            print(first_click)
            if first_click in TileNames:
                if tile_dic[first_click][2]!=player: #상대꺼 선택못함
                    update_sitrep('Click your own piece')
                    continue
                else:
                    update_sitrep(tile_dic[first_click][1]+' selected. Move where?')
                    for i in total_areacode_list:
                        print('waiting second click')
                        update_sitrep('click second button')
                        button_dic[i].wait_variable(click_var)
                        second_click=click_var.get()
                        print(second_click)
                        if second_click in _P1_captured_areacode_list+_P2_captured_areacode_list:
                            update_sitrep('click a valid location to move to')
                            continue
                        try: #test invalid movement
                            Inboardtest(second_click)
                            Collisiontest(second_click,player)
                            direction=tile_dic[second_click][0]-tile_dic[first_click][0] #지정한 위치로 이동할 때 바뀌는 숫자 수치
                            Validmovetest(direction, Moveable_dir_dic[player][tile_dic[first_click][1]])
                        # except KeyError:
                        #     update_sitrep('Select a valid position')
                        #     continue
                        except OutofBoard as err:
                            update_sitrep('Invalid position, try again')
                            continue
                        except Collision as err:
                            update_sitrep('Position blocked by allied piece, try again')
                            continue
                        except WrongMove as err:
                            update_sitrep(namecode.name+' is unable to move that direction')
                            # update_sitrep(err)
                            continue
                        for namecode in units_dic[player]:
                            if namecode.location==first_click:
                                print(namecode)
                                namecode.Move(second_click)
                                change_turn(player)
                                break
                            else:
                                pass
                        break
                break
            elif first_click in _P1_captured_areacode_list+_P2_captured_areacode_list:
                if captures_dic[player]==[]: #놓을 말 있는지 확인
                    update_sitrep('No captured piece to place')
                    continue
                elif first_click in captured_areacode_dic[player]:
                    update_sitrep("Cannot select opponents piece")
                    continue
                else:
                    update_sitrep('piece selected')
                    for i in total_areacode_list:
                        update_sitrep('click second button')
                        button_dic[i].wait_variable(click_var)
                        second_click=click_var.get()
                        print(second_click)
                        try: #test invalid placement
                            Inboardtest(Whereplace)
                            Collisiontest(Whereplace, Ownership) 
                            Invadingtertest(Whereplace, Ownership)
                        except OutofBoard as err:
                            update_sitrep('Invalid position, try again')
                            continue
                        except Collision as err:
                            update_sitrep('Position blocked by allied piece, try again')
                            continue
                        except TerrErr as err:
                            update_sitrep('Cannot place in opponents lair')
                            continue
                        for namecode in captures_dic[player]:
                            if namecode.location==first_click:   ################ need to assign captured pieces locations as well
                                namecode=Piece(namecode.name, second_click, player)
                            captures_dic[player].remove(namecode)
                            change_turn(player)


# def turn(player,player_number):
#     global Whoturn
#     update_sitrep('Player'+player_number+', your turn')
#     while Whoturn==player_number:
#         Ownership=player
#         for i in total_areacode_list:
#             print('test')
#             button_dic[i].wait_variable(click_var)
#             print('test2')
#             initQ=click_var #수 선택
#             print('test3')
#             break
#         if initQ in TileNames: #이동 선택시
#             for i in total_areacode_list:
#                 button_dic[i].wait_variable(click_var)
#                 Wherepiece=click_var
#             # Wherepiece=input('Move from:')
#             try:
#                 Inboardtest(Wherepiece) #보드밖 선택못함
#             except OutofBoard as err:
#                 update_sitrep(err)
#                 continue
#             if tile_dic[Wherepiece][2]!=Ownership: #상대꺼 선택못함
#                 update_sitrep('Cannot move opponents piece')
#                 continue
#             Whichpiece=tile_dic[Wherepiece][1] #위치의 말 이름
#             update_sitrep(Ownership+' '+Whichpiece+' selected. Move where?')
#             Numberpiece=tile_dic[Wherepiece][0]
#             if all(x in list(tile_dic.values()) for x in [[Numberpiece,Whichpiece,Ownership]])!=True: #중간정검
#                 update_sitrep('Error, Piece info not found')
#                 continue
#             for i in total_areacode_list:
#                 button_dic[i].wait_variable(click_var)
#                 Moveto=click_var
#                 break
#             for namecode in units_dic[player]: #변수 이름 확인 후 이동 실행
#                 if Whichpiece==namecode.name and namecode.location==Wherepiece and namecode.ownership==Ownership:
#                     try: #test invalid movement
#                         Inboardtest(Moveto)
#                         Collisiontest(Moveto,Ownership)
#                         direction=tile_dic[Moveto][0]-tile_dic[Wherepiece][0] #지정한 위치로 이동할 때 바뀌는 숫자 수치
#                         Validmovetest(direction, namecode.moveable_dir)
#                     except OutofBoard as err:
#                         update_sitrep(err)
#                         continue
#                     except Collision as err:
#                         update_sitrep(err)
#                         continue
#                     except WrongMove as err:
#                         update_sitrep(namecode.name, end=' ')
#                         update_sitrep(err)
#                         continue
#                     namecode.Move(Moveto)
#                     change_turn(player_number)
#         elif initQ in _P1_captured_areacode_list or _P2_captured_areacode_list: #말 놓기 선택시
#             if captures_dic[player]==[]: #놓을 말 있는지 확인
#                 update_sitrep('No captured piece to place')
#                 continue
#             else:
#                 captures_names=[]
#                 # P1_captures_names=[]
#                 for i in captures_dic[player]:
#                     captures_names.append(i.name)
#                     # P1_captures_names.append(i.name)
#                 update_sitrep('Pieces available: ',captures_names)
#                 for i in total_areacode_list:
#                     button_dic[i].wait_variable(click_var)
#                     Whatpiece=click_var
#                     break
#                 # Whatpiece=input('Which piece?:')
#                 if Whatpiece not in captures_dic[player]: #없는 말 선택시
#                     update_sitrep(Whatpiece+' is not a captured piece')
#                     captures_names.clear()
#                     continue
#                 captures_names.clear()
#                 for i in total_areacode_list:
#                     button_dic[i].wait_variable(click_var)
#                     Wherepiece=click_var
#                     break
#                 # Whereplace=input('Place Where?:')
#                 try: #test invalid placement
#                     Inboardtest(Whereplace)
#                     Collisiontest(Whereplace, Ownership) 
#                     Invadingtertest(Whereplace, Ownership)
#                 except OutofBoard as err:
#                     update_sitrep(err)
#                     continue
#                 except Collision as err:
#                     update_sitrep(err)
#                     continue
#                 except TerrErr as err:
#                     update_sitrep(err)
#                     continue
#                 for namecode in captures_dic[player]:  #말 instance variable 찾아서 
#                     captures_dic[player].remove(namecode)
#                     namecode=Piece(Whatpiece, Whereplace, Ownership)
#                     change_turn(player_number)
#         else:
#             update_sitrep('Invalid command. Available commands are')
#             continue

Whoturn='1'
_Pwhoturn={'1':'P1','2':'P2'}
game_status=True

C1=Piece('Chick','C2','P1')
T1=Piece('Tiger','D2','P1')
E1=Piece('Elephant','D1','P1')
G1=Piece('Giraff','D3','P1')
C2=Piece('Chick','B2','P2')
T2=Piece('Tiger','A2','P2')
E2=Piece('Elephant','A1','P2')
G2=Piece('Giraff','A3','P2')

def game_loop():
    if game_status==True:
        update_board()
        print('board updated')
        turn(_Pwhoturn[Whoturn])
        print('turn ended')
        KillCaptured()
        print('captured killed')
        update_captured_location()
        print('captured updated')
        CheckGG()
        print('GG checked')
    elif game_status==False:
        update_sitrep('Game Over')
    root.config(menu=menu)
    root.after(100, func=game_loop())
    root.mainloop()

game_loop()


