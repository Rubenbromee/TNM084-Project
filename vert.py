VERTEX_SHADER = """
#version 330

    in vec4 position;
    out vec2 outPosition;

    void main() {
        gl_Position = position;
        outPosition = position.xy;
    }
"""