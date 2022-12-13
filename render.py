from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np
import vert
import frag
from audio import load, play
import time
 
VERTEX_SHADER = vert.VERTEX_SHADER
FRAGMENT_SHADER = frag.FRAGMENT_SHADER
 
shaderProgram = None
IBO = None
windowSize = 500
a_list = None
df_list = None
ampLocation = None
freqLocation = None
firstUpdate = True
i_t = None
a_list_len = None
df_list_len = None

# Intitialization, runs once at the start of the program
def init():
    global shaderProgram
    global a_list
    global df_list
    global ampLocation
    global freqLocation
    global a_list_len
    global df_list_len

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

    a_list, df_list = load() # Load amplitude and frequency data for each time frame from sound file
    ampLocation = glGetUniformLocation(shaderProgram, 'amp') # Get shader location for the amplitude variable
    freqLocation = glGetUniformLocation(shaderProgram, 'freq') # Get shader location for the frequency variable
    # Calculate list lengths once to reduce calculations in frame update function
    a_list_len = len(a_list) 
    df_list_len = len(df_list)

    glutTimerFunc(12, updateData, 0) # Loop data update function every 12 ms

def updateData(_):
    global firstUpdate # To check for first frame update and set initial time
    global ampLocation
    global freqLocation
    global i_t # Initial time, the time it takes to set up window etc.
    global a_list_len
    global df_list_len

    # Don't check null lists
    if a_list == None or df_list == None:
        return

    # Set initial time it took to set up window etc.
    # Play sound at the beginning of rendering
    if firstUpdate:
        i_t = glutGet(GLUT_ELAPSED_TIME)
        play("song.wav")
        time.sleep(0.2)
        firstUpdate = False

    c_t = glutGet(GLUT_ELAPSED_TIME) # Get current time
    t = c_t - i_t # Get current time offset by the execution time of setting up the window

    t_i = round(t / 12) # Get amplitude and frequency index for current time
    if t_i >= a_list_len or t_i >= df_list_len:
        return


    a = a_list[t_i] # Get amplitude for current time
    df = df_list[t_i] # Get dominating frequency for current time

    # Update uniforms
    glUniform1f(ampLocation, a)
    glUniform1f(freqLocation, df)

    glutPostRedisplay() # Refresh window with new data
    glutTimerFunc(12, updateData, 0) # Loop every 12 ms

def render():
    global shaderProgram
    global IBO

    glClearColor(0, 0, 0, 1) # Specify the color that the buffer be set to when it clears (black in this case)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear the color and the depth buffer using the clear color
 
    glUseProgram(shaderProgram) # Use the compiled shader program in the rendering
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, IBO, 3 * np.uint32(0).nbytes) # Draw polygons
   
    glutSwapBuffers() # Swap to next frame
 
def main():
    glutInit([]) # Initialize context
    glutInitWindowSize(windowSize, windowSize) # Set initial window size
    glutCreateWindow("TNM084 Project") # Create window
    init() # Call setup of shaders, vertices, indicies etc.
    glutDisplayFunc(render) # Set display function
    glutMainLoop() # Start program
    
if __name__ == '__main__':
    main()