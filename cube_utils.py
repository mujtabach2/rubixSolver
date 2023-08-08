import cv2
import numpy as np
import colorama
from variables import state, sign_conv, color, stickers, textPoints


font = cv2.FONT_HERSHEY_SIMPLEX

def detectColor(h,s,v):
    # print(h,s,v)
    if  h >= 84 and v >= 120 and v <= 239 and s >= 169:
        return 'red'
    elif h > 1  and h <= 13 and s >= 122: # good 
        return 'orange'
    elif h <= 37 and h>=13 and s >= 116  and v > 92:
        return 'yellow'
    elif h>=35 and h<= 66 and v >= 131 and s <= 189 and v<= 186:  # good
        return 'green'
    elif h <= 123  and h>=79 : # good 
        return 'blue'
    elif h <= 92 and s<=90 and v<=212:
        return 'white'

    return 'white'

def turn(side):
    main=state[side]
    front=state['front']
    left=state['left']
    right=state['right']
    up=state['up']
    down=state['down']
    back=state['back']
    
    if side=='front':
        left[2],left[5],left[8],up[6],up[7],up[8],right[0],right[3],right[6],down[0],down[1],down[2]=down[0],down[1],down[2],left[8],left[5],left[2],up[6],up[7],up[8],right[6],right[3],right[0] 
    elif side=='up':
        left[0],left[1],left[2],back[0],back[1],back[2],right[0],right[1],right[2],front[0],front[1],front[2]=front[0],front[1],front[2],left[0],left[1],left[2],back[0],back[1],back[2],right[0],right[1],right[2]
    elif side=='down':
        left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8]=back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8],left[6],left[7],left[8]
    elif side=='back':
        left[0],left[3],left[6],up[0],up[1],up[2],right[2],right[5],right[8],down[6],down[7],down[8]=up[2],up[1],up[0],right[2],right[5],right[8],down[8],down[7],down[6],left[0],left[3],left[6] 
    elif side=='left':
        front[0],front[3],front[6],down[0],down[3],down[6],back[2],back[5],back[8],up[0],up[3],up[6]=up[0],up[3],up[6],front[0],front[3],front[6],down[6],down[3],down[0],back[8],back[5],back[2]
    elif side=='right':
        front[2],front[5],front[8],down[2],down[5],down[8],back[0],back[3],back[6],up[2],up[5],up[8]=down[2],down[5],down[8],back[6],back[3],back[0],up[8],up[5],up[2],front[2],front[5],front[8]

    main[0],main[1],main[2],main[3],main[4],main[5],main[6],main[7],main[8]=main[6],main[3],main[0],main[7],main[4],main[1],main[8],main[5],main[2]

def revturn(side):
    main=state[side]
    front=state['front']
    left=state['left']
    right=state['right']
    up=state['up']
    down=state['down']
    back=state['back']
    
    if side=='front':
        left[2],left[5],left[8],up[6],up[7],up[8],right[0],right[3],right[6],down[0],down[1],down[2]=up[8],up[7],up[6],right[0],right[3],right[6],down[2],down[1],down[0],left[2],left[5],left[8]
    elif side=='up':
        left[0],left[1],left[2],back[0],back[1],back[2],right[0],right[1],right[2],front[0],front[1],front[2]=back[0],back[1],back[2],right[0],right[1],right[2],front[0],front[1],front[2],left[0],left[1],left[2]
    elif side=='down':
        left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8]=front[6],front[7],front[8],left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8]
    elif side=='back':
        left[0],left[3],left[6],up[0],up[1],up[2],right[2],right[5],right[8],down[6],down[7],down[8]=down[6],down[7],down[8],left[6],left[3],left[0],up[0],up[1],up[2],right[8],right[5],right[2] 
    elif side=='left':
        front[0],front[3],front[6],down[0],down[3],down[6],back[2],back[5],back[8],up[0],up[3],up[6]=down[0],down[3],down[6],back[8],back[5],back[2],up[0],up[3],up[6],front[0],front[3],front[6]
    elif side=='right':
        front[2],front[5],front[8],down[2],down[5],down[8],back[0],back[3],back[6],up[2],up[5],up[8]=up[2],up[5],up[8],front[2],front[5],front[8],down[8],down[5],down[2],back[6],back[3],back[0]

    main[0],main[1],main[2],main[3],main[4],main[5],main[6],main[7],main[8]=main[2],main[5],main[8],main[1],main[4],main[7],main[0],main[3],main[6]


def drawStickers(frame,stickers,name):
        for x,y in stickers[name]:
            cv2.rectangle(frame, (x,y), (x+30, y+30), (255,255,255), 2)



def previewSticker(frame,stickers):
        stick=['front','back','left','right','up','down']
        for name in stick:
            for x,y in stickers[name]:
                cv2.rectangle(frame, (x,y), (x+40, y+40), (255,255,255), 2)

def stickerText(frame,stickers, preview):
        stick=['front','back','left','right','up','down']
        for name in stick:
            for x,y in stickers[name]:
                sym,x1,y1=textPoints[name][0][0],textPoints[name][0][1],textPoints[name][0][2]
                cv2.putText(preview, sym, (x1,y1), font,1,(0, 0, 0), 1, cv2.LINE_AA)  
                sym,col,x1,y1=textPoints[name][1][0],textPoints[name][1][1],textPoints[name][1][2],textPoints[name][1][3]             
                cv2.putText(preview, sym, (x1,y1), font,0.5,col, 1, cv2.LINE_AA)  

def colorSticker(frame,stickers,sides):    
    for side,colors in sides.items():
        num=0
        for x,y in stickers[side]:
            cv2.rectangle(frame,(x,y),(x+40,y+40),color[colors[num]],-1)
            num+=1
            
def process(operation,preview,solution):
    replace={
                "F":[turn,'front'],
                "F2":[turn,'front','front'],
                "F'":[revturn,'front'],
                "U":[turn,'up'],
                "U2":[turn,'up','up'],
                "U'":[revturn,'up'],
                "L":[turn,'left'],
                "L2":[turn,'left','left'],
                "L'":[revturn,'left'],
                "R":[turn,'right'],
                "R2":[turn,'right','right'],
                "R'":[revturn,'right'],
                "D":[turn,'down'],
                "D2":[turn,'down','down'],
                "D'":[revturn,'down'],
                "B":[turn,'back'],
                "B2":[turn,'back','back'],
                "B'":[revturn,'back']           
    }    
    a=0
    for i in operation:
        for j in range(len(replace[i])-1):
            replace[i][0](replace[i][j+1])
        cv2.putText(preview, i, (700,a+50), font,1,(0,255,0), 1, cv2.LINE_AA)  
        colorSticker(preview,stickers,state)
        solution.append(preview)
        cv2.imshow('solution',preview)
        cv2.waitKey()
        cv2.putText(preview, i, (700,50), font,1,(0,0,0), 1, cv2.LINE_AA) 
    
