#변수 모아둔 파일

TileNames=['A1','A2','A3','B1','B2','B3','C1','C2','C3','D1','D2','D3']
NumberLabels=range(1,13)
tile_dic={}
for i in range(12):
    tile_dic[TileNames[i]]=[NumberLabels[i],'empty','N/A'] 
    #key,value=A1,[1,'empty','N/A']. 
    # piece name will replace 'empty' str
    # piece ownership will replace 'N/A' str
# print(list(tile_dic.keys())[0]) #get first tilename 'A1'
# print(tile_dic['B1'][0])  #get numberlabel for specific tile
# print(tile_dic['B1'][1])  #get occupancy for specific tile

P1_Area=['D1','D2','D3']
P2_Area=['A1','A2','A3'] 
Lair_dic={'P1':P1_Area,'P2':P2_Area}#각자의 진영
P1_Units=[]
P2_Units=[]
units_dic={'P1':P1_Units,'P2':P2_Units} #각자 살아있는 유닛 instance 보관용
P1_captures=[]
P2_captures=[]
captures_dic={'P1':P1_captures,'P2':P2_captures} #각자 잡은 유닛 instance 보관함
N=-3;NE=-2;E=1;SE=4;S=3;SW=2;W=-1;NW=-4 #direction. maybe should've made dictionary as well? Initially was trying to make user input these values
P1_Dic_moveable_dir={'Chick':[N],'Giraff':[N,S,E,W],'Elephant':[NE,NW,SE,SW],'Tiger':[N,S,E,W,NE,NW,SE,SW], 'Chicken':[N,S,E,W,NE,NW]}
P2_Dic_moveable_dir={'Chick':[S],'Giraff':[N,S,E,W],'Elephant':[NE,NW,SE,SW],'Tiger':[N,S,E,W,NE,NW,SE,SW], 'Chicken':[N,S,E,W,SE,SW]}
Moveable_dir_dic={'P1':P1_Dic_moveable_dir,'P2':P2_Dic_moveable_dir}