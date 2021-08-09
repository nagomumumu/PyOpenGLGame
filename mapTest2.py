import glfw
import sys
import os
from OpenGL.GL import*
from PIL import Image
texID = []

class maps():
    def drawMap():
        maplist = [ [0,1,0,0,0],
                    [0,1,0,0,0],
                    [0,1,1,1,0],
                    [0,0,0,1,0],
                    [0,0,0,1,0] ]
        
        #0から4
        for i in range(5):
            for j in range(5):
                if maplist[i][j]==0:
                    glBindTexture(GL_TEXTURE_2D, 1)
                else:
                    glBindTexture(GL_TEXTURE_2D, 2)
                glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)   
                glBegin(GL_QUADS)
                glTexCoord2d(0.0,1.0)#画像左下
                glVertex2d(0.0+j*32,32+i*32)
                glTexCoord2d(0.0,0.0)#画像左上
                glVertex2d(0.0+j*32,0.0+i*32)
                glTexCoord2d(1.0,0.0)#画像右上
                glVertex2d(32+j*32,0.0+i*32)
                glTexCoord2d(1.0,1.0)#画像右下
                glVertex2d(32+j*32, 32+i*32)
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

    #test
    """
    glColor3d(1.0, 1.0, 1.0)
    glLineWidth(3.0)

    glBegin(GL_LINES)
    glVertex2d(0.0, 0.0)
    glVertex2d(32, 32)
    glVertex2d(32, 0.0)
    glVertex2d(0.0, 32)
    glEnd()"""
    #testend

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
    

def load_texture():
    map0_path = os.path.join(os.path.dirname(__file__), u"data\\kusa.png")
    map1_path = os.path.join(os.path.dirname(__file__), u"data\\tile.png")
    img0 = Image.open(map0_path,'r')
    img1 = Image.open(map1_path,'r')
    texID=glGenTextures(2)
    w = 64
    h = 64
    
    
    print(texID[0])
    print(texID[1])
    #テクスチャの生成と文字列変換
    glBindTexture(GL_TEXTURE_2D, 1)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,w,h,0,GL_RGBA,GL_UNSIGNED_BYTE,img0.tobytes())
    glBindTexture(GL_TEXTURE_2D, 2)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,w,h,0,GL_RGBA,GL_UNSIGNED_BYTE,img1.tobytes())
    

def main():
    if not glfw.init():
        raise RuntimeError('Could not initialize GLFW3')

    window = glfw.create_window(800,800,'mapTest',None,None)

    if not window:
        glfw.terminate()
        raise RuntimeError('Could not create window')

    glfw.set_window_refresh_callback(window,window_refresh)
    glfw.make_context_current(window)

    
    load_texture()
    init(window)
    

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




