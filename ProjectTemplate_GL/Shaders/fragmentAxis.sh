#version 430 core
in vec3 colors;
out vec4 pixel_color;


void main()
{
  
      pixel_color = vec4(abs(colors.x),colors.y,abs(colors.z),1.0f);
   
}