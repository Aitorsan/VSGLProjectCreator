#version 430 core
out vec4 pixel_color;

in vec4 normal_color;

void main()
{

      pixel_color = normal_color;
}
