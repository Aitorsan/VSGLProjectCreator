#include <GL/glew.h>
#define GLFW_DLL
#include <GLFW/glfw3.h>
#include "../ShaderProgram/ShaderProgram.h"
#include "camera.h"
#include "utils.hpp"
#include <stdexcept>
#include <vector>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/constants.hpp>
#include <glm/gtc/noise.hpp>
#include <iostream>

std::pair<std::vector<glm::vec3>, std::vector<int>> makeWorldAxis();
void processInput(GLFWwindow* window, Camera& camera, float elapsedTime, float velocity);
std::pair<std::vector<glm::vec3>,std::vector<int>> createSphere(int stackCount, int sectorCount, float r = 1.0f);
std::vector<glm::vec3> createCircle(int rowcount,float radious = 1.0f);
glm::vec3 lightPosition{0,1,0};

std::pair<std::vector<float>, std::vector<int>> makePlane(int dimensions);
int SCR_WIDTH = 800;
int SCR_HEIGHT = 700;
//projeciton matrix can be precomputed 
constexpr float fov = 60.0f;
glm::mat4 projectionMatrix = glm::perspective(glm::radians(fov), (float)SCR_WIDTH / (float)(SCR_HEIGHT), 0.5f, 1000.f);
int DRAW_TYPE{GL_FILL};
int triangles = 10;
std::vector<float> heighMap;

Camera camera;



int main()
{
	glfwInit();

	GLFWwindow* window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "Geometries", nullptr, nullptr);
	
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

	heighMap = perlinNoise1D(triangles);

	// compile shaders
	ShaderProgram shaderProgram("Shaders/vertex.sh", "Shaders/fragment.sh");
	std::pair<std::vector<float>,std::vector<int>> sphereShape = makePlane(triangles);

	// Axis
	ShaderProgram AxisShaderProgram("Shaders/vertexAxis.sh", "Shaders/fragmentAxis.sh");

	auto axis = makeWorldAxis();
	auto scaleAxis = glm::scale(glm::mat4(),glm::vec3(100.f,100.f,100.f));

	//create Word axis
	GLuint axisVao, axisVbo,axisEbo;
	glGenVertexArrays(1, &axisVao);
	glBindVertexArray(axisVao);

	glGenBuffers(1, &axisVbo);
	glBindBuffer(GL_ARRAY_BUFFER, axisVbo);
	glBufferData(GL_ARRAY_BUFFER, axis.first.size() * sizeof(glm::vec3), axis.first.data(), GL_DYNAMIC_DRAW);
	//vertexdata
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
	
	//indices
	glGenBuffers(1, &axisEbo);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, axisEbo);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, axis.second.size() * sizeof(GLuint), axis.second.data(), GL_STATIC_DRAW);

	glBindVertexArray(0);


	//create Data
	GLuint vao,vbo,ebo;
	glGenVertexArrays(1, &vao);

	glBindVertexArray(vao);

	glGenBuffers(1, &vbo);
	glBindBuffer(GL_ARRAY_BUFFER, vbo);
	glBufferData(GL_ARRAY_BUFFER, sphereShape.first.size() * sizeof(float), sphereShape.first.data(), GL_DYNAMIC_DRAW);
	//vertexdata
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
	//normal
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
	//indices
	glGenBuffers(1, &ebo);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sphereShape.second.size() * sizeof(GLuint), nullptr, GL_STATIC_DRAW);

	glBindVertexArray(0);

	while (!glfwWindowShouldClose(window))
	{
		processInput(window, camera, 1, 0.04f);
		glClearColor(0.1, 0.1, 0, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		//--------------------------------------------------------
		
		//axis draw
		glBindVertexArray(axisVao);

		AxisShaderProgram.useProgram();
		shaderProgram.setMatrix("scale", scaleAxis);
		shaderProgram.setMatrix("projection", projectionMatrix);
		shaderProgram.setMatrix("cameraTransform", camera.GetCameraTranslationMatrix());
		shaderProgram.setVector3f("lightPosition", lightPosition);
		glLineWidth(2);
		glDrawElements(GL_LINES, axis.second.size(), GL_UNSIGNED_INT, 0);
		AxisShaderProgram.stopProgram();
		glLineWidth(1);
		glBindVertexArray(0);

	    //circle draw
		glBindVertexArray(vao);
		sphereShape = makePlane(triangles);
		glBufferData(GL_ARRAY_BUFFER, sphereShape.first.size() * sizeof(float), sphereShape.first.data(), GL_DYNAMIC_DRAW);
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, sphereShape.second.size() * sizeof(GLuint), sphereShape.second.data(), GL_STATIC_DRAW);
		shaderProgram.useProgram();
		
		shaderProgram.setMatrix("projection", projectionMatrix);
		shaderProgram.setMatrix("cameraTransform", camera.GetCameraTranslationMatrix());
		glPolygonMode(GL_FRONT_AND_BACK, DRAW_TYPE);

		glDrawElements(GL_TRIANGLES, sphereShape.second.size(), GL_UNSIGNED_INT, 0);
		shaderProgram.stopProgram();
		glBindVertexArray(0);

		//---------------------------------------------------------------------------------
		glfwSwapBuffers(window);
		glfwPollEvents();
	}

	return 0;
}


void processInput(GLFWwindow* window, Camera& camera, float elapsedTime, float velocity)
{
	camera.CheckMouseMovement(*window);

	if (glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_PRESS)
	{
		DRAW_TYPE =  GL_FILL;
	}
	if (glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_RELEASE)
	{
		DRAW_TYPE = GL_LINE;
	}

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

	if (glfwGetKey(window, GLFW_KEY_R) == GLFW_PRESS)
	{
		heighMap.clear();
		++triangles;
		if (triangles <= 0) triangles = 1;

		heighMap = perlinNoise1D(triangles);
	}

	if (glfwGetKey(window, GLFW_KEY_T) == GLFW_PRESS)
	{  
		heighMap.clear();

		--triangles;
		if (triangles <= 0) triangles = 1;
		
		 heighMap = perlinNoise1D(triangles);


		
	}
	if (glfwGetKey(window, GLFW_KEY_P) == GLFW_PRESS)
	{
		glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
	}

	if (glfwGetKey(window, GLFW_KEY_P) == GLFW_RELEASE)
	{
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
	}
}


std::pair<std::vector<glm::vec3>,std::vector<int>> createSphere( int stackCount, int  sectorCount, float r)
{
	std::vector<int> indices;
	std::vector<glm::vec3> sphere{};

	for (int i = 0; i <= stackCount;++i)
	{
		float phi = 90 - i * 180/stackCount ;

		for (int j = 0; j <= sectorCount; ++j)
		{
			float theta = j * 360/sectorCount;

			float x = r * glm::cos(glm::radians(phi)) * glm::cos(glm::radians(theta));
			float y = r * glm::cos(glm::radians(phi)) * glm::sin(glm::radians(theta));
			float z = r * glm::sin(glm::radians(phi));

			sphere.emplace_back(x, y, z);
		}
	}

	int k1, k2;
	for (int i = 0; i < stackCount; i++)
	{
		k1 = i * (sectorCount +1);                      // beginning of current stack
		k2 = i * (sectorCount + 1 ) + (sectorCount +1); // beginning of next stack
		for (int j = 0; j < sectorCount;j++,++k1,++k2)
		{
			// 2 triangles per sector excluding first and last stacks
			// k1 => k2 => k1+1	
			if (i !=0)
			{
				indices.push_back(k1);
				indices.push_back(k2);
				indices.push_back(k1 +1);
		    }
			// k1+1 => k2 => k2+1
			if (i != sectorCount -1)
			{
				indices.push_back(k1 +1);
				indices.push_back(k2);
				indices.push_back(k2 + 1);
			}
		}
	}

	return { sphere,indices };
}

//simple circle generation function
std::vector<glm::vec3> createCircle(int rowCount, float r )
{
	if (rowCount <= 0) rowCount = 1;
	std::vector<glm::vec3> circle{};
	glm::vec3 center{ 0,0,0 };
	glm::vec3 last_vertex_pos{(center.x+r), 0,0};

	for (int i = 0; i <= 360; ++i)
	{   
		float theta = i * 360 / rowCount;
		glm::vec3 circunference_point { r * glm::cos(glm::radians(theta)), r * glm::sin(glm::radians(theta)), 0};
		circle.push_back(center);
		circle.push_back(circunference_point);
		circle.push_back(last_vertex_pos);
		last_vertex_pos = circunference_point;
	}

	return circle;
}



std::pair<std::vector<float>, std::vector<int>> makePlane(int dimensions)
{
	std::vector<glm::vec3> plane;
	float xofset = 0;
	float yoffset = 0;
	for (int r = 0; r < dimensions; ++r)
	{
		for (int c = 0; c < dimensions; c++)
		{
			glm::vec3 v;
			v.x = (c - dimensions / 2);
			v.z = (r - dimensions / 2);
			float sample =  glm::perlin(glm::vec3(c / 12.f, r / 12.0f, 7.5f)) * 3;
			v.y = sample;
			xofset += 0.5;
			yoffset += 0.98;
			plane.push_back(v);

		}
	}
	std::vector<glm::vec3> normals;

	// [1,2,3,4,5,3]
	// [1,2,3,4,5,3]
	for (int i = 0; i < plane.size(); i+=3)
	{
		if (i < plane.size() - 3)
		{
			glm::vec3 first = plane[i];
			glm::vec3 second = plane[i + 1];
						
			auto normal = glm::cross( second,first);
			auto normalizedNormal = glm::normalize(normal);
			normals.push_back(normalizedNormal);
		}
		
	}

	std::vector<float> finalVertices;
	int nextNormal = 0;
	for (int i = 0; i < plane.size(); i += 3)
	{
		finalVertices.push_back(plane[i].x);
		finalVertices.push_back(plane[i].y);
		finalVertices.push_back(plane[i].z);
		if (nextNormal == normals.size())
			  --nextNormal;
		finalVertices.push_back(normals[nextNormal].x);
		finalVertices.push_back(normals[nextNormal].y);
		finalVertices.push_back(normals[nextNormal].z);
		if (i < plane.size() - 1)
		{
			finalVertices.push_back(plane[i + 1].x);
			finalVertices.push_back(plane[i + 1].y);
			finalVertices.push_back(plane[i + 1].z);
			finalVertices.push_back(normals[nextNormal].x);
			finalVertices.push_back(normals[nextNormal].y);
			finalVertices.push_back(normals[nextNormal].z);
			finalVertices.push_back(plane[i + 2].x);
			finalVertices.push_back(plane[i + 2].y);
			finalVertices.push_back(plane[i + 2].z);
			finalVertices.push_back(normals[nextNormal].x);
			finalVertices.push_back(normals[nextNormal].y);
			finalVertices.push_back(normals[nextNormal].z);
			++nextNormal;
		}
		
	}


	std::vector<int> planeIndices;

	for (int i = 0; i < dimensions-1;++i)
	{
		for (int j = 0; j < dimensions-1; ++j)
		{
			//first triangle of the square face
			planeIndices.push_back(i*dimensions + j);
			planeIndices.push_back(i*dimensions + j + dimensions);
			planeIndices.push_back(i*dimensions + j + dimensions + 1);
			//second triangle of the square face
			planeIndices.push_back(i*dimensions + j );
			planeIndices.push_back(i*dimensions + j + dimensions + 1);
			planeIndices.push_back(i*dimensions + j + 1);
		}
	}

	return { finalVertices,planeIndices };
}



std::pair<std::vector<glm::vec3>,std::vector<int>> makeWorldAxis()
{
	using namespace glm;

	std::vector<glm::vec3> axis;

	vec3 center{ 0,0,0 };
	vec3 xaxis{ 0 };
	xaxis.x = 1000;
	vec3 yaxis{};
	yaxis.y = 1000;
	vec3 zaxis{};
	zaxis.z = 1000;

	axis.push_back(center);
	axis.push_back(xaxis);
	axis.push_back(yaxis);
	axis.push_back(zaxis);

	axis.push_back(-xaxis);
	axis.push_back(-yaxis);
	axis.push_back(-zaxis);


	std::vector<int> index
	{
		0,1,0,2,0,3,
		0,4,0,5,0,6


	};

	return { axis,index };

}




void createRayCast(Camera& camera)
{

	

}