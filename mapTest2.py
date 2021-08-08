import glfw
import sys
import os
from OpenGL.GL import*
from PIL import Image


def display(window):
    maplist = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
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


    glBegin(GL_QUADS)
    glTexCoord2d(0.0,1.0)#画像左下
    glVertex2d(0.0,32)
    glTexCoord2d(0.0,0.0)#画像左上
    glVertex2d(0.0,0.0)
    glTexCoord2d(1.0,0.0)#画像右上
    glVertex2d(32,0.0)
    glTexCoord2d(1.0,1.0)#画像右下
    glVertex2d(32, 32)
    
    glEnd()

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
    map1_path = os.path.join(os.path.dirname(__file__), u"data\\TowaruIcon.png")
    img = Image.open(map1_path,'r')
    w,h = img.size
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,w,h,0,GL_RGBA,GL_UNSIGNED_BYTE,img.tobytes())

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
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)


    while not glfw.window_should_close(window):
        glfw.wait_events()
        err = glGetError()
        if err != GL_NO_ERROR:
            print(err)

    window_refresh(window)
    glfw.terminate()

if __name__=="__main__":
    main()




