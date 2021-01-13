#version 430 core

layout (location = 0) in vec3 positions;
layout (location = 1) in vec3 normals;

uniform mat4 view;
uniform mat4 proj;

out vec3 norms;

void main()
{

  gl_Position = vec4(positions,1.0f);
  norms = normals;
}