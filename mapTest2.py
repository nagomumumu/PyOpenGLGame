import glfw
import sys
import os
from OpenGL.GL import*
from PIL import Image
window_width = 800
window_height = 800


def keyboard(window, key, scancode, action, mods):
    if key == glfw.KEY_UP:
        maps.map_offset_h = maps.map_offset_h+5
    if key == glfw.KEY_DOWN:
        maps.map_offset_h = maps.map_offset_h-5
    if key == glfw.KEY_RIGHT:
        maps.map_offset_w = maps.map_offset_w-5
    if key == glfw.KEY_LEFT:
        maps.map_offset_w = maps.map_offset_w+5
    
    window_refresh(window)

class maps():
    map_offset_w = 0
    map_offset_h = 0

    def drawMap():
        mc_size = 128
        maplist = [ [0,1,0,0,0,0,0],
                    [0,1,0,0,0,0,0],
                    [0,1,1,1,0,0,0],
                    [0,0,0,1,0,0,0],
                    [0,0,0,1,0,0,0],
                    [0,0,0,1,0,0,0],
                    [0,0,0,1,0,0,0] ]
        
        #0から4
        for i in range(7):
            for j in range(7):
                if maplist[i][j]==0:
                    glBindTexture(GL_TEXTURE_2D, texture.texID[0])
                else:
                    glBindTexture(GL_TEXTURE_2D, texture.texID[1])
                glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)   
                glBegin(GL_QUADS)
                glTexCoord2d(0.0,1.0)#画像左下
                glVertex3d(0.0+j*mc_size+maps.map_offset_w,mc_size+i*mc_size+maps.map_offset_h,0.0)
                glTexCoord2d(0.0,0.0)#画像左上
                glVertex3d(0.0+j*mc_size+maps.map_offset_w,0.0+i*mc_size+maps.map_offset_h,0.0)
                glTexCoord2d(1.0,0.0)#画像右上
                glVertex3d(mc_size+j*mc_size+maps.map_offset_w,0.0+i*mc_size+maps.map_offset_h,0.0)
                glTexCoord2d(1.0,1.0)#画像右下
                glVertex3d(mc_size+j*mc_size+maps.map_offset_w, mc_size+i*mc_size+maps.map_offset_h,0.0)
                glEnd()
            
class player():

    def drawPlayer():
        glBindTexture(GL_TEXTURE_2D, texture.texID[2])
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)   
        glBegin(GL_QUADS)
        glTexCoord2d(0.0,1.0)#画像左下
        glVertex3d(window_width/2-64,window_height/2-64+128,1.0)
        glTexCoord2d(0.0,0.0)#画像左上
        glVertex3d(window_width/2-64,window_height/2-64+0.0,1.0)
        glTexCoord2d(1.0,0.0)#画像右上
        glVertex3d(window_width/2-64+128,window_height/2-64+0.0,1.0)
        glTexCoord2d(1.0,1.0)#画像右下
        glVertex3d(window_width/2-64+128,window_height/2-64+128,1.0)
        glEnd()

def display(window):
    glClear(GL_COLOR_BUFFER_BIT)

    #描画範囲の設定と原点の設定
    viewport = (GLint * 4)()
    glGetIntegerv(GL_VIEWPORT, viewport)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-0.5,viewport[2] - 0.5,viewport[3] - 0.5, -0.5, -1.0, 1.0)


    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)

    glEnable(GL_TEXTURE_2D)

    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    maps.drawMap()
    player.drawPlayer()

    glGenerateMipmap(GL_TEXTURE_2D)
    glDisable(GL_TEXTURE_2D)

    glDisable(GL_BLEND)

    glfw.swap_buffers(window)
    glFlush()


def init(window):
    glClearColor(0.0,0.0,1.0,1.0)
    display(window)

def window_refresh(window):
    display(window)
    
class texture():
    texID = []
    def load_texture():
        map0_path = os.path.join(os.path.dirname(__file__), u"data\\kusa.png")
        map1_path = os.path.join(os.path.dirname(__file__), u"data\\tile.png")
        player_path = os.path.join(os.path.dirname(__file__), u"data\\neko.png")

        img0 = Image.open(map0_path,'r')
        img1 = Image.open(map1_path,'r')
        img2 = Image.open(player_path,'r')
        texture.texID=glGenTextures(3)
        w = 64
        h = 64
        
        #テクスチャの生成と文字列変換
        glBindTexture(GL_TEXTURE_2D, texture.texID[0])
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,w,h,0,GL_RGBA,GL_UNSIGNED_BYTE,img0.tobytes())
        glBindTexture(GL_TEXTURE_2D, texture.texID[1])
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,w,h,0,GL_RGBA,GL_UNSIGNED_BYTE,img1.tobytes())
        glBindTexture(GL_TEXTURE_2D, texture.texID[2])
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,w,h,0,GL_RGBA,GL_UNSIGNED_BYTE,img2.tobytes())
        
class phase_ctrl():
    gamephase = 0
    def phase_change(number):
        gamephase = number

def main():
    if not glfw.init():
        raise RuntimeError('Could not initialize GLFW3')

    window = glfw.create_window(window_width,window_height,'mapTest',None,None)

    if not window:
        glfw.terminate()
        raise RuntimeError('Could not create window')

    glfw.set_window_refresh_callback(window,window_refresh)
    glfw.make_context_current(window)

    
    texture.load_texture()
    init(window)
    glfw.set_key_callback(window, keyboard)

    #ゲームループ
    while not glfw.window_should_close(window):
        glfw.wait_events()
        err = glGetError()
        if err != GL_NO_ERROR:
            print(err)

    window_refresh(window)
    glfw.terminate()

if __name__=="__main__":
    main()




