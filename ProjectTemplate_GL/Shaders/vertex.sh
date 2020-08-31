#version 430 core

layout ( location = 0) in vec3 positions;
layout (location = 1) in vec3 normals;
out vec3 colors;

uniform mat4 cameraTransform;
uniform mat4 projection;
uniform vec3 lightPosition;

void main()
{
     
	 
  gl_Position =  projection * cameraTransform * vec4(positions,1.0f);

  colors = normals;
	
}