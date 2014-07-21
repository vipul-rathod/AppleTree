from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

def draw():
    glutWireTeapot(0.5)
    glFlush()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(250, 250)
glutInitWindowPosition(1280,720)
glutCreateWindow("My First OGL Program")
glutDisplayFunc(draw)
glutMainLoop()