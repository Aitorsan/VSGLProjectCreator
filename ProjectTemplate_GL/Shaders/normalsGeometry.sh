#version 330 core

layout (points) in;
layout (line_strip, max_vertices = 2) out;

in vec3 norms[];
out vec4 normal_color;

uniform mat4 view;
uniform mat4 proj;

void main()
{
     gl_Position =  proj * view * gl_in[0].gl_Position;
     normal_color = vec4(norms[0],1.f);
     EmitVertex();

     vec4 pos = gl_in[0].gl_Position + vec4(norms[0],0.f);
     gl_Position =   proj * view * pos;
     normal_color = vec4(norms[0],1.f);
     EmitVertex();

     EndPrimitive();
}
