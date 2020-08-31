#version 430 core
in vec3 colors;
out vec4 pixel_color;

void main()
{
  
      pixel_color = vec4(colors,1.0f);
}