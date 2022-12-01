from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np
import vert
import frag
 
VERTEX_SHADER = vert.VERTEX_SHADER
FRAGMENT_SHADER = frag.FRAGMENT_SHADER
 
shaderProgram = None
IBO = None
windowSize = 500

# Intitialization, runs once at the start of the program
def init():
    global shaderProgram
 
    vertexShader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentShader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)
 
    vertices = [
        # Vertices for bottom right triangle
        -1.0, 1.0, 0.0,
        1.0, 1.0, 0.0,
        1.0, -1.0, 0.0,

        # Vertices for top left triangle
        -1.0, -1.0, 0.0, 
        1.0, -1.0, 0.0, 
        1.0, 1.0, 0.0
    ] 
    vertices = np.array(vertices, dtype=np.float32)
    VBO = glGenBuffers(1) # Create one vertex buffer object
    # GL_ARRAY_BUFFER represents vertex attributes
    glBindBuffer(GL_ARRAY_BUFFER, VBO) # The intent is to use the buffer object for vertex attribute data
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW) # Creates and initializes the vertex buffer object's data store

    # Create index buffer object to draw two triangles using the verticies
    indicies = [ 
        0, 1, 2,  # Bottom right triangle
        0, 2, 3 # Top left triangle 
    ]
    indicies = np.array(indicies, dtype=np.uint32)
    IBO = glGenBuffers(1) # Index buffer object
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO) # The intent is to use the buffer object for index attribute data
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indicies.nbytes, indicies, GL_STATIC_DRAW) # Creates and initializes the index buffer object's data store


    position = glGetAttribLocation(shaderProgram, 'position') # Queries the (shader?) program for the variable named position
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None) # Specifies that the position data in the vertex shader should have three float components vec3f
    glEnableVertexAttribArray(position) # Enable the generic vertex attribute array
 
# Render loop, runs once per frame
def render():
    global shaderProgram
    global IBO
    t = glutGet(GLUT_ELAPSED_TIME)
    if (t % 12 == 0): # Every 12 ms
        # Send dominating frequency and average amplitude of sound buffer frame to fragment shader
        


    glClearColor(0, 0, 0, 1) # Specify the color that the buffer be set to when it clears (black in this case)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear the color and the depth buffer using the clear color
 
    glUseProgram(shaderProgram) # Use the compiled shader program in the rendering
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, IBO, 3 * np.uint32(0).nbytes)
   
    glUseProgram(0)
    glutSwapBuffers()
 
 
def main():
    glutInit([])
    glutInitWindowSize(windowSize, windowSize)
    glutCreateWindow("TNM084 Project")
    init()
    glutDisplayFunc(render)
    glutMainLoop()
 
 
if __name__ == '__main__':
    main()