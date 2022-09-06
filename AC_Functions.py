#Function 모은 파일

from AC_Variables import *
from AC_Class import *

def ShowMapStatus(): #Map Display function
    test=[]
    for i in DicTile:
        test.append(f'{i}={DicTile[i][2]} {DicTile[i][1]}')
    for i in range(len(test)):        
        if i in [2,5,8,11]:
            print(test[i]+'\n')
        else:
            print(test[i]+',',end='\t')    

def KillCaptured():
    for livecode in P1_captures+P2_captures:
        livecode.Kill()
        if livecode.name=='닭':
            livecode.name='병아리'
            if livecode.ownership=='P1':
                livecode.moveable_dir=P1_Dic_moveable_dir['병아리']
            if livecode.ownership=='P2':
                livecode.moveable_dir=P2_Dic_moveable_dir['병아리']


def Winner(player):
    print('Congratulations! You Win '+player+'!')
    global game_status
    game_status=False

def CheckGG():
    if T1 in P2_captures: #상대 호랑이 잡으면 승리
        Winner('Player 2')
    elif T2 in P1_captures:
        Winner('Player 1')
    if T1.location in P2_Area:
        print("P1 tiger in P2 lair! P1 will win if tiger isn't captured!")
        ShowMapStatus()
        P2turn()
        if T1.location in P2_Area:
            Winner('Player 1')
    elif T2.location in P1_Area:
        print("P2 tiger in P1 lair! P2 will win if tiger isn't captured!")
        ShowMapStatus()
        P1turn()
        if T2.location in P1_Area:
            Winner('Player 2')

def P1turn():
    global Whoturn
    print('Player 1, your turn')
    while Whoturn==1:
        Ownership='P1'
        initQ=input('Move or Place:') #수 선택
        if initQ=='Move' or initQ=='move': #이동 선택시
            Wherepiece=input('Move from:')
            try:
                Inboardtest(Wherepiece) #보드밖 선택못함
            except OutofBoard as err:
                print(err)
                continue
            if DicTile[Wherepiece][2]!=Ownership: #상대꺼 선택못함
                print('Cannot move opponents piece')
                continue
            Whichpiece=DicTile[Wherepiece][1] #위치의 말 이름
            print(Ownership+' '+Whichpiece+' selected')
            Numberpiece=DicTile[Wherepiece][0]
            if all(x in list(DicTile.values()) for x in [[Numberpiece,Whichpiece,Ownership]])!=True: #중간정검
                print('Error, Piece info not found')
                continue
            Moveto=input('Move to:')
            for namecode in P1_Units: #변수 이름 확인 후 이동 실행
                if Whichpiece==namecode.name and namecode.location==Wherepiece and namecode.ownership==Ownership:
                    try: #test invalid movement
                        Inboardtest(Moveto)
                        Collisiontest(Moveto,Ownership)
                        direction=DicTile[Moveto][0]-DicTile[Wherepiece][0] #지정한 위치로 이동할 때 바뀌는 숫자 수치
                        Validmovetest(direction, namecode.moveable_dir)
                    except OutofBoard as err:
                        print(err)
                        continue
                    except Collision as err:
                        print(err)
                        continue
                    except WrongMove as err:
                        print(namecode.name, end=' ')
                        print(err)
                        continue
                    namecode.Move(Moveto)
                    Whoturn=2
        elif initQ=='Place' or initQ=='place': #말 놓기 선택시
            if P1_captures==[]: #놓을 말 있는지 확인
                print('No captured piece to place')
                continue
            else:
                P1_captures_names=[]
                for i in P1_captures:
                    P1_captures_names.append(i.name)
                print('Pieces available: ',P1_captures_names)
                Whatpiece=input('Which piece?:')
                if Whatpiece not in P1_captures_names: #없는 말 선택시
                    print(Whatpiece+' is not a captured piece')
                    P1_captures_names.clear()
                    continue
                P1_captures_names.clear()
                Whereplace=input('Place Where?:')
                try: #test invalid placement
                    Inboardtest(Whereplace)
                    Collisiontest(Whereplace, Ownership) 
                    Invadingtertest(Whereplace, Ownership)
                except OutofBoard as err:
                    print(err)
                    continue
                except Collision as err:
                    print(err)
                    continue
                except TerrErr as err:
                    print(err)
                    continue
                for namecode in P1_captures:  #말 instance variable 찾아서 
                    P1_captures.remove(namecode)
                    namecode=Piece(Whatpiece, Whereplace, Ownership)
                    Whoturn=2
        else:
            print('Invalid command. Available commands are')
            continue

def P2turn(): #same code as P1turn, only P2. 이거도 줄일 수 있었을듯.
    global Whoturn
    print('Player 2, your turn')
    while Whoturn==2:
        Ownership='P2'
        initQ=input('Move or Place:') #수 선택
        if initQ=='Move' or initQ=='move': #이동 선택시
            Wherepiece=input('Move from:')
            try:
                Inboardtest(Wherepiece) #보드밖 선택못함
            except OutofBoard as err:
                print(err)
                continue
            if DicTile[Wherepiece][2]!=Ownership: #상대꺼 선택못함
                print('Cannot move opponents piece or empty space')
                continue
            Whichpiece=DicTile[Wherepiece][1] #위치의 말 이름
            print(Ownership+' '+Whichpiece+' selected')
            Numberpiece=DicTile[Wherepiece][0]
            if all(x in list(DicTile.values()) for x in [[Numberpiece,Whichpiece,Ownership]])!=True: #중간정검
                print('Error, Piece info not found')
                continue
            Moveto=input('Move to:')
            for namecode in P2_Units: #변수 이름 확인 후 이동 실행
                if Whichpiece==namecode.name and namecode.location==Wherepiece and namecode.ownership==Ownership:
                    try: #test invalid movement
                        Inboardtest(Moveto)
                        Collisiontest(Moveto,Ownership)
                        direction=DicTile[Moveto][0]-DicTile[Wherepiece][0] #지정한 위치로 이동할 때 바뀌는 숫자 수치
                        Validmovetest(direction, namecode.moveable_dir)
                    except OutofBoard as err:
                        print(err)
                        continue
                    except Collision as err:
                        print(err)
                        continue
                    except WrongMove as err:
                        print(namecode.name, end=' ')
                        print(err)
                        continue
                    namecode.Move(Moveto)
                    Whoturn=1
        elif initQ=='Place' or initQ=='place': #말 놓기 선택시
            if P2_captures==[]: #놓을 말 있는지 확인
                print('No captured piece to place')
                continue
            else:
                P2_captures_names=[]
                for i in P2_captures:
                    P2_captures_names.append(i.name)
                print('Pieces available: ',P2_captures_names)
                Whatpiece=input('Which piece?:')
                if Whatpiece not in P2_captures_names: #없는 말 선택시
                    print(Whatpiece+' is not a captured piece')
                    P2_captures_names.clear()
                    continue
                P2_captures_names.clear()
                Whereplace=input('Place Where?:')
                try: #test invalid placement
                    Inboardtest(Whereplace)
                    Collisiontest(Whereplace, Ownership) 
                    Invadingtertest(Whereplace, Ownership)
                except OutofBoard as err:
                    print(err)
                    continue
                except Collision as err:
                    print(err)
                    continue
                except TerrErr as err:
                    print(err)
                    continue
                for namecode in P2_captures:  #말 instance variable 찾아서 
                    P2_captures.remove(namecode)
                    namecode=Piece(Whatpiece, Whereplace, Ownership)
                    Whoturn=1
        else:
            print('Invalid command. Available commands are')
            continue

Whoturn=1
game_status=True

print('Animal Chess\n')
C1=Piece('병아리','C2','P1')
T1=Piece('호랑이','D2','P1')
E1=Piece('코끼리','D1','P1')
G1=Piece('기린','D3','P1')
C2=Piece('병아리','B2','P2')
T2=Piece('호랑이','A2','P2')
E2=Piece('코끼리','A1','P2')
G2=Piece('기린','A3','P2')

while game_status==True:
    ShowMapStatus()
    P1turn()
    KillCaptured()
    CheckGG()
    if game_status==True:
        ShowMapStatus()
        P2turn()
        KillCaptured()
        CheckGG()
print('Game Over')