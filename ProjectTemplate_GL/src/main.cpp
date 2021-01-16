#include <stdexcept>
#include <vector>
#include <iostream>

#include <GL/glew.h>
#define GLFW_DLL
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/constants.hpp>
#include <glm/gtc/noise.hpp>

#include "ShaderProgram.h"
#include "camera.h"
#include "utils.hpp"

void processInput(GLFWwindow* window, Camera& camera, float elapsedTime, float velocity);

int SCR_WIDTH = 800, SCR_HEIGHT = 700;
constexpr float fov = 60.0f;
glm::mat4 projectionMatrix = glm::perspective(glm::radians(fov), (float)SCR_WIDTH / (float)(SCR_HEIGHT), 0.5f, 1000.f);


int main()
{
	glfwInit();

	GLFWwindow* window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "OpenGl", nullptr, nullptr);

	if (!window) throw std::runtime_error("could not create window");

	glfwMakeContextCurrent(window);
	glfwSwapInterval(1);
	glewExperimental = GL_TRUE;
	//init opengl context
	if (glewInit() != GLEW_OK) throw std::runtime_error("could not initalize openGl context");

	glfwSetFramebufferSizeCallback(window, [](GLFWwindow* window, int width, int height)
	{
			glfwGetFramebufferSize(window, &width, &height);
			SCR_WIDTH = width;
			SCR_HEIGHT = height;
			projectionMatrix = glm::perspective(glm::radians(fov), (float)SCR_WIDTH / (float)(SCR_HEIGHT), 0.5f, 1000.f);
			glViewport(0, 0, width, height);
   });
	glEnable(GL_DEPTH_TEST);

    //////////////////////// Program code ////////////////////////////////////


    Camera camera;

	float cube[] = {
		-0.5f, -0.5f, -0.5f,  0.0f,  0.0f, -1.0f,// -0.5,-0.5,-2.0
		 0.5f, -0.5f, -0.5f,  0.0f,  0.0f, -1.0f,
		 0.5f,  0.5f, -0.5f,  0.0f,  0.0f, -1.0f,
		 0.5f,  0.5f, -0.5f,  0.0f,  0.0f, -1.0f,
		-0.5f,  0.5f, -0.5f,  0.0f,  0.0f, -1.0f,
		-0.5f, -0.5f, -0.5f,  0.0f,  0.0f, -1.0f,

		-0.5f, -0.5f,  0.5f,  0.0f,  0.0f,  1.0f,
		 0.5f, -0.5f,  0.5f,  0.0f,  0.0f,  1.0f,
		 0.5f,  0.5f,  0.5f,  0.0f,  0.0f,  1.0f,
		 0.5f,  0.5f,  0.5f,  0.0f,  0.0f,  1.0f,
		-0.5f,  0.5f,  0.5f,  0.0f,  0.0f,  1.0f,
		-0.5f, -0.5f,  0.5f,  0.0f,  0.0f,  1.0f,

		-0.5f,  0.5f,  0.5f, -1.0f,  0.0f,  0.0f,
		-0.5f,  0.5f, -0.5f, -1.0f,  0.0f,  0.0f,
		-0.5f, -0.5f, -0.5f, -1.0f,  0.0f,  0.0f,
		-0.5f, -0.5f, -0.5f, -1.0f,  0.0f,  0.0f,
		-0.5f, -0.5f,  0.5f, -1.0f,  0.0f,  0.0f,
		-0.5f,  0.5f,  0.5f, -1.0f,  0.0f,  0.0f,

		 0.5f,  0.5f,  0.5f,  1.0f,  0.0f,  0.0f,
		 0.5f,  0.5f, -0.5f,  1.0f,  0.0f,  0.0f,
		 0.5f, -0.5f, -0.5f,  1.0f,  0.0f,  0.0f,
		 0.5f, -0.5f, -0.5f,  1.0f,  0.0f,  0.0f,
		 0.5f, -0.5f,  0.5f,  1.0f,  0.0f,  0.0f,
		 0.5f,  0.5f,  0.5f,  1.0f,  0.0f,  0.0f,

		-0.5f, -0.5f, -0.5f,  0.0f, -1.0f,  0.0f,
		 0.5f, -0.5f, -0.5f,  0.0f, -1.0f,  0.0f,
		 0.5f, -0.5f,  0.5f,  0.0f, -1.0f,  0.0f,
		 0.5f, -0.5f,  0.5f,  0.0f, -1.0f,  0.0f,
		-0.5f, -0.5f,  0.5f,  0.0f, -1.0f,  0.0f,
		-0.5f, -0.5f, -0.5f,  0.0f, -1.0f,  0.0f,

		-0.5f,  0.5f, -0.5f,  0.0f,  1.0f,  0.0f,
		 0.5f,  0.5f, -0.5f,  0.0f,  1.0f,  0.0f,
		 0.5f,  0.5f,  0.5f,  0.0f,  1.0f,  0.0f,
		 0.5f,  0.5f,  0.5f,  0.0f,  1.0f,  0.0f,
		-0.5f,  0.5f,  0.5f,  0.0f,  1.0f,  0.0f,
		-0.5f,  0.5f, -0.5f,  0.0f,  1.0f,  0.0f
	};


	// compile shaders
	ShaderProgram shaderProgram("Shaders/vertex.sh", "Shaders/fragment.sh");
	// Normals
	ShaderProgram normalShaderProgram("Shaders/normalsVertex.sh", "Shaders/normalsFragment.sh","Shaders/normalsGeometry.sh");

	//create Word axis
	GLuint vao, vbo;
	glGenVertexArrays(1, &vao);
	glBindVertexArray(vao);

	glGenBuffers(1, &vbo);
	glBindBuffer(GL_ARRAY_BUFFER, vbo);
	glBufferData(GL_ARRAY_BUFFER, sizeof(cube) , cube, GL_DYNAMIC_DRAW);
	//vertexdata
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
	//normals
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));


///////////////////////// Render Loop ////////////////////////////////////////////////////////
	while (!glfwWindowShouldClose(window))
	{
		processInput(window, camera, 1, 0.04f);
		glClearColor(0.1, 0.1, 0, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		//--------------------------------------------------------
		glm::mat4 camMatrix = camera.GetCameraTranslationMatrix();
		// draw cube
		glBindVertexArray(vao);
		shaderProgram.useProgram();
		shaderProgram.setMatrix("projection", projectionMatrix);
		shaderProgram.setMatrix("cameraTransform", camMatrix);
		glDrawArrays(GL_TRIANGLES, 0, 36);
		shaderProgram.stopProgram();
		normalShaderProgram.useProgram();
		normalShaderProgram.setMatrix("proj", projectionMatrix);
		normalShaderProgram.setMatrix("view", camMatrix);
		glDrawArrays(GL_POINTS, 0, 36);
		normalShaderProgram.stopProgram();

		//---------------------------------------------------------------------------------
		glfwSwapBuffers(window);
		glfwPollEvents();
	}

	return 0;
}


void processInput(GLFWwindow* window, Camera& camera, float elapsedTime, float velocity)
{
	camera.CheckMouseMovement(*window);

	if (glfwGetKey(window, GLFW_KEY_F) == GLFW_PRESS)
	{
		velocity += 10.5f;
	}
	if (glfwGetKey(window, GLFW_KEY_F) == GLFW_RELEASE)
	{
		if (velocity > 20.f)
			velocity -= 0.2f;
	}

	if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
	{
		glfwSetWindowShouldClose(window, true);
	}

	if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
	{
		camera.MoveFront(elapsedTime, velocity);
	}

	if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
	{
		camera.MoveBack(elapsedTime, velocity);
	}

	if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
	{
		camera.MoveLeft(elapsedTime, velocity);
	}

	if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
	{
		camera.MoveRight(elapsedTime, velocity);
	}
}
