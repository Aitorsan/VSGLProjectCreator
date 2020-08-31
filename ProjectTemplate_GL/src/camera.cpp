#pragma once
#include "camera.h"
#include "glm/gtc/matrix_transform.hpp"
#include <glm/gtc/matrix_inverse.hpp>
#include <GLFW/glfw3.h>
#include <iostream>
Camera::Camera()
    :Camera(0.0f, 0.0f, 0.0f, 45.0f)
{
}

Camera::Camera(float x, float y, float z, float fov)
	: CameraPos{x,y,z}
	, CameraFront{ 0, 0,-1.0f }
	, CameraUp{ 0, 1, 0 }
	, yaw{-90}
	, pitch{0.0f}
	, lastX{x}
	, lastY{y}
	,init{true}
{

}

void Camera::CheckMouseMovement(GLFWwindow& window)
{   
	
		double xpos{ 0 }, ypos{ 0 };
		glfwGetCursorPos(&window, &xpos, &ypos);
		if (!init)
		{

			float xoffset = lastX- xpos ;
			float yoffset = ypos - lastY;
			lastX = xpos;
			lastY = ypos;

			float sensitivity = 0.1f;
			xoffset *= sensitivity;
			yoffset *= sensitivity;
			

			if (glfwGetMouseButton(&window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_PRESS)
			{
				yaw += xoffset;
				pitch += yoffset;
				if (pitch > 89.0f)
					pitch = 89.0f;
				if (pitch < -89.0f)
					pitch = -89.0f;
			
					glm::vec3 direction;
					direction.x = cos(glm::radians(yaw)) * cos(glm::radians(pitch));
					direction.y = sin(glm::radians(pitch));
					direction.z = sin(glm::radians(yaw)) * cos(glm::radians(pitch));
					CameraFront = glm::normalize(direction);

					// experimental
					//need to transform xpos and ypos into word space
					int width, height;
					glfwGetWindowSize(&window, &width, &height);
					float x = (2.0f * xpos) / width - 1.0f;
					float y = 1.0f - (2.0f * ypos) / height;
					float z = 1.0f;
					glm::vec3 ray_nds = glm::vec3(x, y, z);
					glm::vec4 ray_clip = glm::vec4(ray_nds.x, ray_nds.y, -1.0, 1.0);
					glm::mat4 projection_matrix = glm::perspective(glm::radians(60.0f), (float)width / (float)(height), 0.5f, 1000.f);
					glm::vec4 ray_eye = glm::inverse(projection_matrix) * ray_clip;
					ray_eye = glm::vec4(ray_eye.x, ray_eye.y, -1.0, 0.0);

					glm::vec4 ray_wor = (glm::inverse(glm::lookAt(CameraPos, CameraPos + CameraFront, CameraUp)) * ray_eye);
					// don't forget to normalise the vector at some point
					ray_wor = glm::normalize(ray_wor);
					std::cout << '\r' << "xpos:" << ray_wor.x << ", ypos:" << ray_wor.y << ", zpos:" << ray_wor.z;
					
			
					CameraFront = glm::normalize(direction);
			        
			
			}
			
			
				
				
			
		}
		init = false;
}




void Camera::MoveFront(float elapsedTime, float velocity)
{

	CameraPos += CameraFront * velocity*elapsedTime;
}

void Camera::MoveBack(float elapsedTime, float velocity)
{
	CameraPos -= CameraFront * velocity*elapsedTime;
}

void Camera::MoveRight(float elapsedTime, float velocity)
{
	CameraPos += glm::normalize(glm::cross(CameraFront, CameraUp)) * elapsedTime*velocity;
}

void Camera::MoveLeft(float elapsedTime, float velocity)
{
	CameraPos -= glm::normalize(glm::cross(CameraFront, CameraUp)) * elapsedTime*velocity;
}

glm::mat4 Camera::GetCameraTranslationMatrix()
{
	return glm::lookAt(CameraPos, CameraPos + CameraFront, CameraUp);
}

glm::vec3& Camera::GetCameraPosition()
{
	return CameraPos;
}

glm::vec3& Camera::GetCameraFront()
{
	return CameraFront;
}

void Camera::SetCameraPosition(float x, float y, float z)
{
	CameraPos.x = x;
	CameraPos.y = y;
	CameraPos.z = z;
}
