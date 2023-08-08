import cv2
import numpy as np
import kociemba as Cube
import time
import colorama
import plotly.graph_objects as go
from cube_utils import detectColor, drawStickers, \
                        previewSticker, stickerText, colorSticker, process
from variables import stickers, textPoints, color, state, sign_conv

colorama.init()
import colorama

colorama.init()

print(colorama.Fore.CYAN + """
 __________     ___.   .__           _________________  .__                      
\______   \__ _\_ |__ |__|__  ___  /   _____/\_____  \ |  |___  __ ___________  
 |       _/  |  \ __ \|  \  \/  /  \_____  \  /   |   \|  |\  \/ // __ \_  __ \ 
 |    |   \  |  / \_\ \  |>    <   /        \/    |    \  |_\   /\  ___/|  | \/ 
 |____|_  /____/|___  /__/__/\_ \ /_______  /\_______  /____/\_/  \___  >__|    
        \/          \/         \/         \/         \/               \/        
""" + colorama.Fore.RESET)

time.sleep(2)
print("")
print("")
print(f"{MAGENTA}Please refer preview window for which side you have scanned and which color should be in centre on each side. ")




check_state=[]
solution=[]
solved=False

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cv2.namedWindow('frame')



def solve(state):
    raw=''
    for i in state:
        for j in state[i]:
            raw+=sign_conv[j]
    print("answer:",Cube.solve(raw))
    return Cube.solve(raw)


# import plotly.graph_objects as go
# def draw_3d_cube(state):
#     colors = {
#         'white': 'white',
#         'yellow': 'yellow',
#         'green': 'green',
#         'blue': 'blue',
#         'red': 'red',
#         'orange': 'orange'
#     }

#     # Define the coordinates of the cube vertices
#     vertices = []
#     for x in range(3):
#         for y in range(3):
#             for z in range(3):
#                 vertices.append((x, y, z))

#     # Define the cube edges
#     edges = []
#     for x in range(3):
#         for y in range(3):
#             for z in range(2):
#                 edges.append((x * 3 + y + z * 9, x * 3 + y + (z + 1) * 9))
#                 edges.append((x * 3 + y * 3 + z * 9, x * 3 + y * 3 + 1 + z * 9))
#                 edges.append((x * 3 + y * 3 + 1 + z * 9, x * 3 + y * 3 + 2 + z * 9))

#     fig = go.Figure()

#     # Plot the cube edges
#     for edge in edges:
#         x = [vertices[edge[0]][0], vertices[edge[1]][0]]
#         y = [vertices[edge[0]][1], vertices[edge[1]][1]]
#         z = [vertices[edge[0]][2], vertices[edge[1]][2]]
#         fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color='black')))

#     # Set the colors for each face based on the state dictionary
#     faces = ['front', 'back', 'left', 'right', 'up', 'down']
#     for face in faces:
#         x = [vertices[i][0] for i in state[face]]
#         y = [vertices[i][1] for i in state[face]]
#         z = [vertices[i][2] for i in state[face]]
#         color = colors[state[face][4]]
#         fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.8, color=color))

#     # Set the plot layout and view
#     fig.update_layout(scene=dict(
#         xaxis=dict(range=[-0.5, 2.5]),
#         yaxis=dict(range=[-0.5, 2.5]),
#         zaxis=dict(range=[-0.5, 2.5]),
#         aspectmode='cube',
#         camera=dict(eye=dict(x=1.2, y=1.2, z=1.2))
#     ))

#     # Show the 3D plot
#     fig.show()



if __name__=='__main__':

    preview = np.zeros((700,800,3), np.uint8)
    while True:
        hsv=[]
        current_state=[]
        ret,img=cap.read()
        # img=cv2.flip(img,1)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = np.zeros(frame.shape, dtype=np.uint8)   

        drawStickers(img,stickers,'main')
        drawStickers(img,stickers,'current')
        previewSticker(preview,stickers)
        colorSticker(preview,stickers,state)
        stickerText(preview,stickers,preview)

        for i in range(9):
            hsv.append(frame[stickers['main'][i][1]+50][stickers['main'][i][0]+50])
        
        a=0
        for x,y in stickers['current']:
            color_name=detectColor(hsv[a][0],hsv[a][1],hsv[a][2])
            cv2.rectangle(img,(x,y),(x+30,y+30),color[color_name],-1)
            a+=1
            current_state.append(color_name)
        
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        elif k ==ord('u'):
            state['up']=current_state
            check_state.append('u')
        elif k ==ord('r'):
            check_state.append('r')
            state['right']=current_state
        elif k ==ord('l'):
            check_state.append('l')
            state['left']=current_state
        elif k ==ord('d'):
            check_state.append('d')
            state['down']=current_state       
        elif k ==ord('f'):
            check_state.append('f')
            state['front']=current_state       
        elif k ==ord('b'):
            check_state.append('b')
            state['back']=current_state       
        elif k == ord('\r'):
            # process(["R","R'"])
            if len(set(check_state))==6:    
                try:
                    solved=solve(state)
                    if solved:
                        operation=solved.split(' ')
                        process(operation,preview,solution)
                except:
                    print("")
            else:
                print("all side are not scanned check other window for finding which left to be scanned?")
                print("left to scan:",6-len(set(check_state)))
  
        cv2.imshow('preview',preview)
        cv2.imshow('frame', img)


    cv2.destroyAllWindows()