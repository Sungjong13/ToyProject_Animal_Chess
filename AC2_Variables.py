#not sure why I separated these but yeah

#tile_dic= {tile code: [occupying name, occupying owner]}
tile_dic={}
tile_code_list=['A1','A2','A3','B1','B2','B3','C1','C2','C3','D1','D2','D3','E1','E2','E3','E4','F1','F2','F3','F4']
board_code_list=tile_code_list[:12]
captured_code_list=tile_code_list[12:]
P1captured_code_list=captured_code_list[:4]
P2captured_code_list=captured_code_list[4:]
captured_dic={'P1':P1captured_code_list,'P2':P2captured_code_list}
lair_dic={'P2':board_code_list[:3],'P1':board_code_list[-3:]}
for i in tile_code_list:
    tile_dic[i]=['Empty','No_Owner']
N=-3;NE=-2;E=1;SE=4;S=3;SW=2;W=-1;NW=-4
P1_moveable_dir_dic={'Chick':[N],'Giraff':[N,S,E,W],'Elephant':[NE,NW,SE,SW],'Tiger':[N,S,E,W,NE,NW,SE,SW], 'Chicken':[N,S,E,W,NE,NW]}
P2_moveable_dir_dic={'Chick':[S],'Giraff':[N,S,E,W],'Elephant':[NE,NW,SE,SW],'Tiger':[N,S,E,W,NE,NW,SE,SW], 'Chicken':[N,S,E,W,SE,SW]}
moveable_dir_dic={'P1':P1_moveable_dir_dic,'P2':P2_moveable_dir_dic}
recorded_move_list=[] #1.1
# def record_move(entityname,entityowner,move_from,move_to,iskilled=False):
#     recorded_move_list.append([entityname,entityowner,move_from,move_to,iskilled])

def check_valid_move(entityname,entityowner,move_from,move_to):
    direction=list(tile_dic.keys()).index(move_to)-list(tile_dic.keys()).index(move_from)
    return direction in moveable_dir_dic[entityowner][entityname] #returns true if move is valid

def place_entity(entityname,entityowner,location):
    tile_dic[location][0]=entityname
    tile_dic[location][1]=entityowner

def move_entity(entityname,entityowner,move_from,move_to,iskilled=False):
    tile_dic[move_from][0]='Empty'
    tile_dic[move_from][1]='No_Owner'
    tile_dic[move_to][0]=entityname
    tile_dic[move_to][1]=entityowner
    recorded_move_list.append([entityname,entityowner,move_from,move_to,iskilled]) #1.1

def kill_entity(entityname,entityowner,location):
    if entityowner=='P2':
        if tile_dic['E1'][0]=='Empty':
            move_entity(entityname,entityowner,location,'E1',iskilled=True)
            tile_dic['E1'][1]='P1'
        elif tile_dic['E2'][0]=='Empty':
            move_entity(entityname,entityowner,location,'E2',iskilled=True)
            tile_dic['E2'][1]='P1'
        elif tile_dic['E3'][0]=='Empty':
            move_entity(entityname,entityowner,location,'E3',iskilled=True)
            tile_dic['E3'][1]='P1'
        else:
            move_entity(entityname,entityowner,location,'E4',iskilled=True)
            tile_dic['E4'][1]='P1'
    elif entityowner=='P1':
        if tile_dic['F1'][0]=='Empty':
            move_entity(entityname,entityowner,location,'F1',iskilled=True)
            tile_dic['F1'][1]='P2'
        elif tile_dic['F2'][0]=='Empty':
            move_entity(entityname,entityowner,location,'F2',iskilled=True)
            tile_dic['F2'][1]='P2'
        elif tile_dic['F3'][0]=='Empty':
            move_entity(entityname,entityowner,location,'F3',iskilled=True)
            tile_dic['F3'][1]='P2'
        else:
            move_entity(entityname,entityowner,location,'F4',iskilled=True)
            tile_dic['F4'][1]='P2'


