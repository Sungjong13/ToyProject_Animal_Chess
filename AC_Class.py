#Class 모아둔 파일

from AC_Variables import *

class OutofBoard(Exception):
    def __str__(self):
        return 'Invalid position, try again'
class TerrErr(Exception):
    def __str__(self):
        return 'Cannot place in opponents lair'
class Collision(Exception):
    def __str__(self):
        return 'Position blocked by allied piece, try again'
class WrongMove(Exception):
    def __str__(self):
        return 'is unable to move that direction'
class InvalidPieceName(Exception):
    def __str__(self):
        return 'is not a valid piece name'

def change_ownership(ownership):
    if ownership=='P1':
        return 'P2'
    if ownership=='P2':
        return 'P1'
def Inboardtest(location):
    if location in TileNames:
        pass
    else:
        raise OutofBoard
def Invadingtertest(location,ownership):
    if location in Lair_dic[change_ownership(ownership)]:
        raise TerrErr
def Collisiontest(location,ownership):
    if tile_dic[location][2]==ownership:
        raise Collision
    else:
        pass
def Validmovetest(direction,moveable_dir):
    if direction in moveable_dir:
        pass
    else:
        raise WrongMove

class Piece:
    def __init__(self,name,location,ownership,alive=True):
        self.name=name
        self.location=location
        self.alive=alive
        self.ownership=ownership

        tile_dic[self.location][1]=self.name
        tile_dic[self.location][2]=self.ownership
        # update_sitrep(self.ownership+self.name+' was placed at '+self.location)

        self.moveable_dir=Moveable_dir_dic[ownership][self.name] #P2 invert direction
        # if ownership=='P1': #P2 invert direction
        #     self.moveable_dir=P1_Dic_moveable_dir[self.name]
        # elif ownership=='P2':
        #     self.moveable_dir=P2_Dic_moveable_dir[self.name]
        # else:
        #     print('Ownership Code Error')
        #     raise
        
        units_dic[self.ownership].append(self) #instance name 기록
        # if self.ownership=='P1': #instance name 기록
        #     P1_Units.append(self)
        # elif self.ownership=='P2':
        #     P2_Units.append(self)

    def Move(self,NewLocation):
        OldLocation=self.location
        # update_sitrep(self.ownership+self.name+' piece moved from '+OldLocation+' to '+NewLocation)
        if tile_dic[NewLocation][2]==change_ownership(self.ownership):
        # if tile_dic[NewLocation][2]!=tile_dic[OldLocation][2] and tile_dic[NewLocation][2]!='N/A': #상대 말인지 확인. 보드랑 비교해서
            EnemyName=tile_dic[NewLocation][1]
            EnemyOwnership=tile_dic[NewLocation][2]
            EnemyLocation=NewLocation
            for namecode in units_dic[EnemyOwnership]:
            # if EnemyOwnership=='P1': #상대 말 확인 후 instance 포획. instance parameter랑 비교해서
            #     for namecode in P1_Units:
                if namecode.name==EnemyName and namecode.ownership==EnemyOwnership and namecode.location==EnemyLocation:
                    captures_dic[change_ownership(EnemyOwnership)].append(namecode)
                    units_dic[EnemyOwnership].remove(namecode)
                    # P2_captures.append(namecode)
                    # P1_Units.remove(namecode)
                    # update_sitrep(self.name+' captured '+EnemyName+' at '+NewLocation)
            # elif EnemyOwnership=='P2':
            #     for namecode in P2_Units:
            #         if namecode.name==EnemyName and namecode.ownership==EnemyOwnership and namecode.location==EnemyLocation:
            #             P1_captures.append(namecode)
            #             P2_Units.remove(namecode)
            #             print(self.name+' captured '+EnemyName+' at '+NewLocation)
                else:
                    print('Enemy ownership varification error while capturing')
                    # update_sitrep('Enemy Ownership Varification Error While Capturing')
                    raise
        else:
            tile_dic[self.location][1]='empty'
            tile_dic[self.location][2]='N/A' #있던 자리 비우기
            self.location=NewLocation
            tile_dic[self.location][1]=self.name
            tile_dic[self.location][2]=self.ownership #새 자리 채우기
            if self.name=='Chick': #병아리 닭 변신
                if self.location in Lair_dic[change_ownership(self.ownership)]: 
                # if self.ownership=='P1' and self.location in P2_Area:
                    self.name='Chicken'
                    self.moveable_dir=Moveable_dir_dic[self.ownership]['Chicken']
                    # self.moveable_dir=P1_Dic_moveable_dir['Chicken']
                    tile_dic[self.location][1]=self.name
                    # update_sitrep(str(self.ownership)+'병아리 turned into 닭')
                # elif self.ownership=='P2' and self.location in P1_Area:
                #     self.name='Chicken'
                #     self.moveable_dir=P2_Dic_moveable_dir['Chicken']
                #     tile_dic[self.location][1]=self.name
                #     print('P2병아리 turned into 닭')                    

    def Kill(self,alive=False):
        self.alive=alive
        if self.alive==False:
            self.location='null_location'
            self.ownership='null_ownership'
