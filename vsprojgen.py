import shutil
import os
from argparse import ArgumentParser
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from PIL import Image, ImageTk

# solution file template string
solution_file = '''Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio 15
VisualStudioVersion = 15.0.28307.1082
MinimumVisualStudioVersion = 10.0.40219.1
Project("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}") = "project_name","project_name\project_name.vcxproj", "{30D10229-BE5A-42BC-AB81-A84D3935A0F1}"
EndProject
Global
	GlobalSection(SolutionConfigurationPlatforms) = preSolution
		Debug|x64 = Debug|x64
		Debug|x86 = Debug|x86
		Release|x64 = Release|x64
		Release|x86 = Release|x86
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution
		{30D10229-BE5A-42BC-AB81-A84D3935A0F1}.Debug|x64.ActiveCfg = Debug|x64
		{30D10229-BE5A-42BC-AB81-A84D3935A0F1}.Debug|x64.Build.0 = Debug|x64
		{30D10229-BE5A-42BC-AB81-A84D3935A0F1}.Debug|x86.ActiveCfg = Debug|Win32
		{30D10229-BE5A-42BC-AB81-A84D3935A0F1}.Debug|x86.Build.0 = Debug|Win32
		{30D10229-BE5A-42BC-AB81-A84D3935A0F1}.Release|x64.ActiveCfg = Release|x64
		{30D10229-BE5A-42BC-AB81-A84D3935A0F1}.Release|x64.Build.0 = Release|x64
		{30D10229-BE5A-42BC-AB81-A84D3935A0F1}.Release|x86.ActiveCfg = Release|Win32
		{30D10229-BE5A-42BC-AB81-A84D3935A0F1}.Release|x86.Build.0 = Release|Win32
	EndGlobalSection
	GlobalSection(SolutionProperties) = preSolution
		HideSolutionNode = FALSE
	EndGlobalSection
	GlobalSection(ExtensibilityGlobals) = postSolution
		SolutionGuid = {8C313ACA-C14C-4575-9F47-83AE484C6403}
	EndGlobalSection
EndGlobal'''

# visual studio project file string template
vcxproj = r'''<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" ToolsVersion="15.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup Label="ProjectConfigurations">
    <ProjectConfiguration Include="Debug|Win32">
      <Configuration>Debug</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Release|Win32">
      <Configuration>Release</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Debug|x64">
      <Configuration>Debug</Configuration>
      <Platform>x64</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Release|x64">
      <Configuration>Release</Configuration>
      <Platform>x64</Platform>
    </ProjectConfiguration>
  </ItemGroup>
  <PropertyGroup Label="Globals">
    <VCProjectVersion>15.0</VCProjectVersion>
    <ProjectGuid>{30D10229-BE5A-42BC-AB81-A84D3935A0F1}</ProjectGuid>
    <RootNamespace>project_name</RootNamespace>
    <WindowsTargetPlatformVersion>10.0.18362.0</WindowsTargetPlatformVersion>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>true</UseDebugLibraries>
    <PlatformToolset>v141</PlatformToolset>
    <CharacterSet>MultiByte</CharacterSet>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>false</UseDebugLibraries>
    <PlatformToolset>v141</PlatformToolset>
    <WholeProgramOptimization>true</WholeProgramOptimization>
    <CharacterSet>MultiByte</CharacterSet>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>true</UseDebugLibraries>
    <PlatformToolset>v141</PlatformToolset>
    <CharacterSet>MultiByte</CharacterSet>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>false</UseDebugLibraries>
    <PlatformToolset>v141</PlatformToolset>
    <WholeProgramOptimization>true</WholeProgramOptimization>
    <CharacterSet>MultiByte</CharacterSet>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />
  <ImportGroup Label="ExtensionSettings">
  </ImportGroup>
  <ImportGroup Label="Shared">
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <PropertyGroup Label="UserMacros" />
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <IntDir>$(SolutionDir)temp\</IntDir>
    <LibraryPath>C:$(ProjectDir)lib\;$(LibraryPath)</LibraryPath>
    <ExecutablePath>$(ExecutablePath)</ExecutablePath>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <IntDir>$(SolutionDir)temp\</IntDir>
    <LibraryPath>C:$(ProjectDir)lib\;$(LibraryPath)</LibraryPath>
    <ExecutablePath>$(ExecutablePath)</ExecutablePath>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
    <OutDir>$(SolutionDir)$(Configuration)\</OutDir>
    <IntDir>$(SolutionDir)temp\</IntDir>
    <LibraryPath>C:$(ProjectDir)lib\;$(LibraryPath)</LibraryPath>
    <ExecutablePath>$(ExecutablePath)</ExecutablePath>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <OutDir>$(SolutionDir)$(Configuration)\</OutDir>
    <IntDir>$(SolutionDir)temp\</IntDir>
    <LibraryPath>C:$(ProjectDir)lib;$(LibraryPath)</LibraryPath>
    <ExecutablePath>$(ExecutablePath)</ExecutablePath>
  </PropertyGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <Optimization>Disabled</Optimization>
      <SDLCheck>true</SDLCheck>
      <ConformanceMode>true</ConformanceMode>
      <AdditionalIncludeDirectories>$(ProjectDir)include\;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
      <LanguageStandard>stdcpp14</LanguageStandard>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <AdditionalLibraryDirectories>$(ProjectDir)lib\;%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>
      <AdditionalDependencies>opengl32.lib;glew32d.lib;glfw3dll.lib;%(AdditionalDependencies)</AdditionalDependencies>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <Optimization>Disabled</Optimization>
      <SDLCheck>true</SDLCheck>
      <ConformanceMode>true</ConformanceMode>
      <AdditionalIncludeDirectories>$(ProjectDir)include;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
      <LanguageStandard>stdcpp14</LanguageStandard>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <AdditionalLibraryDirectories>$(ProjectDir)lib;%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>
      <AdditionalDependencies>opengl32.lib;glew32d.lib;glfw3dll.lib;%(AdditionalDependencies)</AdditionalDependencies>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <Optimization>MaxSpeed</Optimization>
      <FunctionLevelLinking>true</FunctionLevelLinking>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <SDLCheck>true</SDLCheck>
      <ConformanceMode>true</ConformanceMode>
      <AdditionalIncludeDirectories>$(ProjectDir)include;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
      <LanguageStandard>stdcpp14</LanguageStandard>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <EnableCOMDATFolding>true</EnableCOMDATFolding>
      <OptimizeReferences>true</OptimizeReferences>
      <AdditionalLibraryDirectories>$(ProjectDir)lib;%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>
      <AdditionalDependencies>opengl32.lib;glew32d.lib;glfw3dll.lib;%(AdditionalDependencies)</AdditionalDependencies>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <Optimization>MaxSpeed</Optimization>
      <FunctionLevelLinking>true</FunctionLevelLinking>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <SDLCheck>true</SDLCheck>
      <ConformanceMode>true</ConformanceMode>
      <AdditionalIncludeDirectories>$(ProjectDir)include\;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
      <LanguageStandard>stdcpp14</LanguageStandard>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <EnableCOMDATFolding>true</EnableCOMDATFolding>
      <OptimizeReferences>true</OptimizeReferences>
      <AdditionalLibraryDirectories>$(ProjectDir)lib;%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>
      <AdditionalDependencies>opengl32.lib;glew32d.lib;glfw3dll.lib;%(AdditionalDependencies)</AdditionalDependencies>
    </Link>
  </ItemDefinitionGroup>
  <ItemGroup>
    <ClInclude Include="include\camera.h" />
    <ClInclude Include="include\GLFW\glfw3.h" />
    <ClInclude Include="include\GLFW\glfw3native.h" />
    <ClInclude Include="include\glm\common.hpp" />
    <ClInclude Include="include\glm\detail\compute_common.hpp" />
    <ClInclude Include="include\glm\detail\compute_vector_relational.hpp" />
    <ClInclude Include="include\glm\detail\qualifier.hpp" />
    <ClInclude Include="include\glm\detail\setup.hpp" />
    <ClInclude Include="include\glm\detail\type_float.hpp" />
    <ClInclude Include="include\glm\detail\type_half.hpp" />
    <ClInclude Include="include\glm\detail\type_mat2x2.hpp" />
    <ClInclude Include="include\glm\detail\type_mat2x3.hpp" />
    <ClInclude Include="include\glm\detail\type_mat2x4.hpp" />
    <ClInclude Include="include\glm\detail\type_mat3x2.hpp" />
    <ClInclude Include="include\glm\detail\type_mat3x3.hpp" />
    <ClInclude Include="include\glm\detail\type_mat3x4.hpp" />
    <ClInclude Include="include\glm\detail\type_mat4x2.hpp" />
    <ClInclude Include="include\glm\detail\type_mat4x3.hpp" />
    <ClInclude Include="include\glm\detail\type_mat4x4.hpp" />
    <ClInclude Include="include\glm\detail\type_quat.hpp" />
    <ClInclude Include="include\glm\detail\type_vec1.hpp" />
    <ClInclude Include="include\glm\detail\type_vec2.hpp" />
    <ClInclude Include="include\glm\detail\type_vec3.hpp" />
    <ClInclude Include="include\glm\detail\type_vec4.hpp" />
    <ClInclude Include="include\glm\detail\_features.hpp" />
    <ClInclude Include="include\glm\detail\_fixes.hpp" />
    <ClInclude Include="include\glm\detail\_noise.hpp" />
    <ClInclude Include="include\glm\detail\_swizzle.hpp" />
    <ClInclude Include="include\glm\detail\_swizzle_func.hpp" />
    <ClInclude Include="include\glm\detail\_vectorize.hpp" />
    <ClInclude Include="include\glm\exponential.hpp" />
    <ClInclude Include="include\glm\ext.hpp" />
    <ClInclude Include="include\glm\ext\matrix_clip_space.hpp" />
    <ClInclude Include="include\glm\ext\matrix_common.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double2x2.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double2x2_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double2x3.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double2x3_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double2x4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double2x4_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double3x2.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double3x2_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double3x3.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double3x3_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double3x4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double3x4_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double4x2.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double4x2_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double4x3.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double4x3_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double4x4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double4x4_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float2x2.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float2x2_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float2x3.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float2x3_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float2x4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float2x4_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float3x2.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float3x2_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float3x3.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float3x3_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float3x4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float3x4_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float4x2.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float4x2_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float4x3.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float4x3_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float4x4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float4x4_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_projection.hpp" />
    <ClInclude Include="include\glm\ext\matrix_relational.hpp" />
    <ClInclude Include="include\glm\ext\matrix_transform.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_common.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_double.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_double_precision.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_exponential.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_float.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_float_precision.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_geometric.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_relational.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_transform.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_trigonometric.hpp" />
    <ClInclude Include="include\glm\ext\scalar_common.hpp" />
    <ClInclude Include="include\glm\ext\scalar_constants.hpp" />
    <ClInclude Include="include\glm\ext\scalar_int_sized.hpp" />
    <ClInclude Include="include\glm\ext\scalar_relational.hpp" />
    <ClInclude Include="include\glm\ext\scalar_uint_sized.hpp" />
    <ClInclude Include="include\glm\ext\scalar_ulp.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool1.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool1_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool2.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool2_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool3.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool3_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool4.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool4_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_common.hpp" />
    <ClInclude Include="include\glm\ext\vector_double1.hpp" />
    <ClInclude Include="include\glm\ext\vector_double1_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_double2.hpp" />
    <ClInclude Include="include\glm\ext\vector_double2_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_double3.hpp" />
    <ClInclude Include="include\glm\ext\vector_double3_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_double4.hpp" />
    <ClInclude Include="include\glm\ext\vector_double4_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_float1.hpp" />
    <ClInclude Include="include\glm\ext\vector_float1_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_float2.hpp" />
    <ClInclude Include="include\glm\ext\vector_float2_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_float3.hpp" />
    <ClInclude Include="include\glm\ext\vector_float3_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_float4.hpp" />
    <ClInclude Include="include\glm\ext\vector_float4_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_int1.hpp" />
    <ClInclude Include="include\glm\ext\vector_int1_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_int2.hpp" />
    <ClInclude Include="include\glm\ext\vector_int2_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_int3.hpp" />
    <ClInclude Include="include\glm\ext\vector_int3_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_int4.hpp" />
    <ClInclude Include="include\glm\ext\vector_int4_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_relational.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint1.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint1_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint2.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint2_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint3.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint3_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint4.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint4_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_ulp.hpp" />
    <ClInclude Include="include\glm\fwd.hpp" />
    <ClInclude Include="include\glm\geometric.hpp" />
    <ClInclude Include="include\glm\glm.hpp" />
    <ClInclude Include="include\glm\gtc\bitfield.hpp" />
    <ClInclude Include="include\glm\gtc\color_space.hpp" />
    <ClInclude Include="include\glm\gtc\constants.hpp" />
    <ClInclude Include="include\glm\gtc\epsilon.hpp" />
    <ClInclude Include="include\glm\gtc\integer.hpp" />
    <ClInclude Include="include\glm\gtc\matrix_access.hpp" />
    <ClInclude Include="include\glm\gtc\matrix_integer.hpp" />
    <ClInclude Include="include\glm\gtc\matrix_inverse.hpp" />
    <ClInclude Include="include\glm\gtc\matrix_transform.hpp" />
    <ClInclude Include="include\glm\gtc\noise.hpp" />
    <ClInclude Include="include\glm\gtc\packing.hpp" />
    <ClInclude Include="include\glm\gtc\quaternion.hpp" />
    <ClInclude Include="include\glm\gtc\random.hpp" />
    <ClInclude Include="include\glm\gtc\reciprocal.hpp" />
    <ClInclude Include="include\glm\gtc\round.hpp" />
    <ClInclude Include="include\glm\gtc\type_aligned.hpp" />
    <ClInclude Include="include\glm\gtc\type_precision.hpp" />
    <ClInclude Include="include\glm\gtc\type_ptr.hpp" />
    <ClInclude Include="include\glm\gtc\ulp.hpp" />
    <ClInclude Include="include\glm\gtc\vec1.hpp" />
    <ClInclude Include="include\glm\gtx\associated_min_max.hpp" />
    <ClInclude Include="include\glm\gtx\bit.hpp" />
    <ClInclude Include="include\glm\gtx\closest_point.hpp" />
    <ClInclude Include="include\glm\gtx\color_encoding.hpp" />
    <ClInclude Include="include\glm\gtx\color_space.hpp" />
    <ClInclude Include="include\glm\gtx\color_space_YCoCg.hpp" />
    <ClInclude Include="include\glm\gtx\common.hpp" />
    <ClInclude Include="include\glm\gtx\compatibility.hpp" />
    <ClInclude Include="include\glm\gtx\component_wise.hpp" />
    <ClInclude Include="include\glm\gtx\dual_quaternion.hpp" />
    <ClInclude Include="include\glm\gtx\easing.hpp" />
    <ClInclude Include="include\glm\gtx\euler_angles.hpp" />
    <ClInclude Include="include\glm\gtx\extend.hpp" />
    <ClInclude Include="include\glm\gtx\extended_min_max.hpp" />
    <ClInclude Include="include\glm\gtx\exterior_product.hpp" />
    <ClInclude Include="include\glm\gtx\fast_exponential.hpp" />
    <ClInclude Include="include\glm\gtx\fast_square_root.hpp" />
    <ClInclude Include="include\glm\gtx\fast_trigonometry.hpp" />
    <ClInclude Include="include\glm\gtx\functions.hpp" />
    <ClInclude Include="include\glm\gtx\gradient_paint.hpp" />
    <ClInclude Include="include\glm\gtx\handed_coordinate_space.hpp" />
    <ClInclude Include="include\glm\gtx\hash.hpp" />
    <ClInclude Include="include\glm\gtx\integer.hpp" />
    <ClInclude Include="include\glm\gtx\intersect.hpp" />
    <ClInclude Include="include\glm\gtx\io.hpp" />
    <ClInclude Include="include\glm\gtx\log_base.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_cross_product.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_decompose.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_factorisation.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_interpolation.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_major_storage.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_operation.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_query.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_transform_2d.hpp" />
    <ClInclude Include="include\glm\gtx\mixed_product.hpp" />
    <ClInclude Include="include\glm\gtx\norm.hpp" />
    <ClInclude Include="include\glm\gtx\normal.hpp" />
    <ClInclude Include="include\glm\gtx\normalize_dot.hpp" />
    <ClInclude Include="include\glm\gtx\number_precision.hpp" />
    <ClInclude Include="include\glm\gtx\optimum_pow.hpp" />
    <ClInclude Include="include\glm\gtx\orthonormalize.hpp" />
    <ClInclude Include="include\glm\gtx\perpendicular.hpp" />
    <ClInclude Include="include\glm\gtx\polar_coordinates.hpp" />
    <ClInclude Include="include\glm\gtx\projection.hpp" />
    <ClInclude Include="include\glm\gtx\quaternion.hpp" />
    <ClInclude Include="include\glm\gtx\range.hpp" />
    <ClInclude Include="include\glm\gtx\raw_data.hpp" />
    <ClInclude Include="include\glm\gtx\rotate_normalized_axis.hpp" />
    <ClInclude Include="include\glm\gtx\rotate_vector.hpp" />
    <ClInclude Include="include\glm\gtx\scalar_multiplication.hpp" />
    <ClInclude Include="include\glm\gtx\scalar_relational.hpp" />
    <ClInclude Include="include\glm\gtx\spline.hpp" />
    <ClInclude Include="include\glm\gtx\std_based_type.hpp" />
    <ClInclude Include="include\glm\gtx\string_cast.hpp" />
    <ClInclude Include="include\glm\gtx\texture.hpp" />
    <ClInclude Include="include\glm\gtx\transform.hpp" />
    <ClInclude Include="include\glm\gtx\transform2.hpp" />
    <ClInclude Include="include\glm\gtx\type_aligned.hpp" />
    <ClInclude Include="include\glm\gtx\type_trait.hpp" />
    <ClInclude Include="include\glm\gtx\vector_angle.hpp" />
    <ClInclude Include="include\glm\gtx\vector_query.hpp" />
    <ClInclude Include="include\glm\gtx\vec_swizzle.hpp" />
    <ClInclude Include="include\glm\gtx\wrap.hpp" />
    <ClInclude Include="include\glm\integer.hpp" />
    <ClInclude Include="include\glm\mat2x2.hpp" />
    <ClInclude Include="include\glm\mat2x3.hpp" />
    <ClInclude Include="include\glm\mat2x4.hpp" />
    <ClInclude Include="include\glm\mat3x2.hpp" />
    <ClInclude Include="include\glm\mat3x3.hpp" />
    <ClInclude Include="include\glm\mat3x4.hpp" />
    <ClInclude Include="include\glm\mat4x2.hpp" />
    <ClInclude Include="include\glm\mat4x3.hpp" />
    <ClInclude Include="include\glm\mat4x4.hpp" />
    <ClInclude Include="include\glm\matrix.hpp" />
    <ClInclude Include="include\glm\packing.hpp" />
    <ClInclude Include="include\glm\simd\common.h" />
    <ClInclude Include="include\glm\simd\exponential.h" />
    <ClInclude Include="include\glm\simd\geometric.h" />
    <ClInclude Include="include\glm\simd\integer.h" />
    <ClInclude Include="include\glm\simd\matrix.h" />
    <ClInclude Include="include\glm\simd\packing.h" />
    <ClInclude Include="include\glm\simd\platform.h" />
    <ClInclude Include="include\glm\simd\trigonometric.h" />
    <ClInclude Include="include\glm\simd\vector_relational.h" />
    <ClInclude Include="include\glm\trigonometric.hpp" />
    <ClInclude Include="include\glm\vec2.hpp" />
    <ClInclude Include="include\glm\vec3.hpp" />
    <ClInclude Include="include\glm\vec4.hpp" />
    <ClInclude Include="include\glm\vector_relational.hpp" />
    <ClInclude Include="include\GL\eglew.h" />
    <ClInclude Include="include\GL\glew.h" />
    <ClInclude Include="include\GL\glxew.h" />
    <ClInclude Include="include\GL\wglew.h" />
    <ClInclude Include="include\stb_image.h" />
    <ClInclude Include="include\utils.hpp" />
    <ClInclude Include="ShaderProgram\ShaderProgram.h" />
  </ItemGroup>
  <ItemGroup>
    <None Include="include\glm\detail\func_common.inl" />
    <None Include="include\glm\detail\func_common_simd.inl" />
    <None Include="include\glm\detail\func_exponential.inl" />
    <None Include="include\glm\detail\func_exponential_simd.inl" />
    <None Include="include\glm\detail\func_geometric.inl" />
    <None Include="include\glm\detail\func_geometric_simd.inl" />
    <None Include="include\glm\detail\func_integer.inl" />
    <None Include="include\glm\detail\func_integer_simd.inl" />
    <None Include="include\glm\detail\func_matrix.inl" />
    <None Include="include\glm\detail\func_matrix_simd.inl" />
    <None Include="include\glm\detail\func_packing.inl" />
    <None Include="include\glm\detail\func_packing_simd.inl" />
    <None Include="include\glm\detail\func_trigonometric.inl" />
    <None Include="include\glm\detail\func_trigonometric_simd.inl" />
    <None Include="include\glm\detail\func_vector_relational.inl" />
    <None Include="include\glm\detail\func_vector_relational_simd.inl" />
    <None Include="include\glm\detail\type_half.inl" />
    <None Include="include\glm\detail\type_mat2x2.inl" />
    <None Include="include\glm\detail\type_mat2x3.inl" />
    <None Include="include\glm\detail\type_mat2x4.inl" />
    <None Include="include\glm\detail\type_mat3x2.inl" />
    <None Include="include\glm\detail\type_mat3x3.inl" />
    <None Include="include\glm\detail\type_mat3x4.inl" />
    <None Include="include\glm\detail\type_mat4x2.inl" />
    <None Include="include\glm\detail\type_mat4x3.inl" />
    <None Include="include\glm\detail\type_mat4x4.inl" />
    <None Include="include\glm\detail\type_mat4x4_simd.inl" />
    <None Include="include\glm\detail\type_quat.inl" />
    <None Include="include\glm\detail\type_quat_simd.inl" />
    <None Include="include\glm\detail\type_vec1.inl" />
    <None Include="include\glm\detail\type_vec2.inl" />
    <None Include="include\glm\detail\type_vec3.inl" />
    <None Include="include\glm\detail\type_vec4.inl" />
    <None Include="include\glm\detail\type_vec4_simd.inl" />
    <None Include="include\glm\ext\matrix_clip_space.inl" />
    <None Include="include\glm\ext\matrix_common.inl" />
    <None Include="include\glm\ext\matrix_projection.inl" />
    <None Include="include\glm\ext\matrix_relational.inl" />
    <None Include="include\glm\ext\matrix_transform.inl" />
    <None Include="include\glm\ext\quaternion_common.inl" />
    <None Include="include\glm\ext\quaternion_common_simd.inl" />
    <None Include="include\glm\ext\quaternion_exponential.inl" />
    <None Include="include\glm\ext\quaternion_geometric.inl" />
    <None Include="include\glm\ext\quaternion_relational.inl" />
    <None Include="include\glm\ext\quaternion_transform.inl" />
    <None Include="include\glm\ext\quaternion_trigonometric.inl" />
    <None Include="include\glm\ext\scalar_common.inl" />
    <None Include="include\glm\ext\scalar_constants.inl" />
    <None Include="include\glm\ext\scalar_relational.inl" />
    <None Include="include\glm\ext\scalar_ulp.inl" />
    <None Include="include\glm\ext\vector_common.inl" />
    <None Include="include\glm\ext\vector_relational.inl" />
    <None Include="include\glm\ext\vector_ulp.inl" />
    <None Include="include\glm\gtc\bitfield.inl" />
    <None Include="include\glm\gtc\color_space.inl" />
    <None Include="include\glm\gtc\constants.inl" />
    <None Include="include\glm\gtc\epsilon.inl" />
    <None Include="include\glm\gtc\integer.inl" />
    <None Include="include\glm\gtc\matrix_access.inl" />
    <None Include="include\glm\gtc\matrix_inverse.inl" />
    <None Include="include\glm\gtc\matrix_transform.inl" />
    <None Include="include\glm\gtc\noise.inl" />
    <None Include="include\glm\gtc\packing.inl" />
    <None Include="include\glm\gtc\quaternion.inl" />
    <None Include="include\glm\gtc\quaternion_simd.inl" />
    <None Include="include\glm\gtc\random.inl" />
    <None Include="include\glm\gtc\reciprocal.inl" />
    <None Include="include\glm\gtc\round.inl" />
    <None Include="include\glm\gtc\type_precision.inl" />
    <None Include="include\glm\gtc\type_ptr.inl" />
    <None Include="include\glm\gtc\ulp.inl" />
    <None Include="include\glm\gtx\associated_min_max.inl" />
    <None Include="include\glm\gtx\bit.inl" />
    <None Include="include\glm\gtx\closest_point.inl" />
    <None Include="include\glm\gtx\color_encoding.inl" />
    <None Include="include\glm\gtx\color_space.inl" />
    <None Include="include\glm\gtx\color_space_YCoCg.inl" />
    <None Include="include\glm\gtx\common.inl" />
    <None Include="include\glm\gtx\compatibility.inl" />
    <None Include="include\glm\gtx\component_wise.inl" />
    <None Include="include\glm\gtx\dual_quaternion.inl" />
    <None Include="include\glm\gtx\easing.inl" />
    <None Include="include\glm\gtx\euler_angles.inl" />
    <None Include="include\glm\gtx\extend.inl" />
    <None Include="include\glm\gtx\extended_min_max.inl" />
    <None Include="include\glm\gtx\exterior_product.inl" />
    <None Include="include\glm\gtx\fast_exponential.inl" />
    <None Include="include\glm\gtx\fast_square_root.inl" />
    <None Include="include\glm\gtx\fast_trigonometry.inl" />
    <None Include="include\glm\gtx\float_notmalize.inl" />
    <None Include="include\glm\gtx\functions.inl" />
    <None Include="include\glm\gtx\gradient_paint.inl" />
    <None Include="include\glm\gtx\handed_coordinate_space.inl" />
    <None Include="include\glm\gtx\hash.inl" />
    <None Include="include\glm\gtx\integer.inl" />
    <None Include="include\glm\gtx\intersect.inl" />
    <None Include="include\glm\gtx\io.inl" />
    <None Include="include\glm\gtx\log_base.inl" />
    <None Include="include\glm\gtx\matrix_cross_product.inl" />
    <None Include="include\glm\gtx\matrix_decompose.inl" />
    <None Include="include\glm\gtx\matrix_factorisation.inl" />
    <None Include="include\glm\gtx\matrix_interpolation.inl" />
    <None Include="include\glm\gtx\matrix_major_storage.inl" />
    <None Include="include\glm\gtx\matrix_operation.inl" />
    <None Include="include\glm\gtx\matrix_query.inl" />
    <None Include="include\glm\gtx\matrix_transform_2d.inl" />
    <None Include="include\glm\gtx\mixed_product.inl" />
    <None Include="include\glm\gtx\norm.inl" />
    <None Include="include\glm\gtx\normal.inl" />
    <None Include="include\glm\gtx\normalize_dot.inl" />
    <None Include="include\glm\gtx\number_precision.inl" />
    <None Include="include\glm\gtx\optimum_pow.inl" />
    <None Include="include\glm\gtx\orthonormalize.inl" />
    <None Include="include\glm\gtx\perpendicular.inl" />
    <None Include="include\glm\gtx\polar_coordinates.inl" />
    <None Include="include\glm\gtx\projection.inl" />
    <None Include="include\glm\gtx\quaternion.inl" />
    <None Include="include\glm\gtx\raw_data.inl" />
    <None Include="include\glm\gtx\rotate_normalized_axis.inl" />
    <None Include="include\glm\gtx\rotate_vector.inl" />
    <None Include="include\glm\gtx\scalar_relational.inl" />
    <None Include="include\glm\gtx\spline.inl" />
    <None Include="include\glm\gtx\std_based_type.inl" />
    <None Include="include\glm\gtx\string_cast.inl" />
    <None Include="include\glm\gtx\texture.inl" />
    <None Include="include\glm\gtx\transform.inl" />
    <None Include="include\glm\gtx\transform2.inl" />
    <None Include="include\glm\gtx\type_aligned.inl" />
    <None Include="include\glm\gtx\type_trait.inl" />
    <None Include="include\glm\gtx\vector_angle.inl" />
    <None Include="include\glm\gtx\vector_query.inl" />
    <None Include="include\glm\gtx\wrap.inl" />
    <None Include="lib\glew32d.dll" />
    <None Include="lib\glfw3.dll" />
    <None Include="Shaders\fragment.sh" />
    <None Include="Shaders\fragmentAxis.sh" />
    <None Include="Shaders\geometry.sh" />
    <None Include="Shaders\vertex.sh" />
    <None Include="Shaders\vertexAxis.sh" />
  </ItemGroup>
  <ItemGroup>
    <ClCompile Include="include\glm\detail\glm.cpp" />
    <ClCompile Include="ShaderProgram\ShaderProgram.cpp" />
    <ClCompile Include="src\camera.cpp" />
    <ClCompile Include="src\main.cpp" />
  </ItemGroup>
  <ItemGroup>
    <Library Include="lib\glew32d.lib" />
    <Library Include="lib\glfw3dll.lib" />
  </ItemGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
  <ImportGroup Label="ExtensionTargets">
  </ImportGroup>
</Project>'''
  
# visual studio filters file template string
vcxproj_filters = r'''<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup>
    <ClInclude Include="include\GL\eglew.h" />
    <ClInclude Include="include\GL\glew.h" />
    <ClInclude Include="include\GL\glxew.h" />
    <ClInclude Include="include\GL\wglew.h" />
    <ClInclude Include="include\GLFW\glfw3.h" />
    <ClInclude Include="include\GLFW\glfw3native.h" />
    <ClInclude Include="include\glm\detail\_features.hpp" />
    <ClInclude Include="include\glm\detail\_fixes.hpp" />
    <ClInclude Include="include\glm\detail\_noise.hpp" />
    <ClInclude Include="include\glm\detail\_swizzle.hpp" />
    <ClInclude Include="include\glm\detail\_swizzle_func.hpp" />
    <ClInclude Include="include\glm\detail\_vectorize.hpp" />
    <ClInclude Include="include\glm\detail\compute_common.hpp" />
    <ClInclude Include="include\glm\detail\compute_vector_relational.hpp" />
    <ClInclude Include="include\glm\detail\qualifier.hpp" />
    <ClInclude Include="include\glm\detail\setup.hpp" />
    <ClInclude Include="include\glm\detail\\type_float.hpp" />
    <ClInclude Include="include\glm\detail\\type_half.hpp" />
    <ClInclude Include="include\glm\detail\\type_mat2x2.hpp" />
    <ClInclude Include="include\glm\detail\\type_mat2x3.hpp" />
    <ClInclude Include="include\glm\detail\\type_mat2x4.hpp" />
    <ClInclude Include="include\glm\detail\\type_mat3x2.hpp" />
    <ClInclude Include="include\glm\detail\\type_mat3x3.hpp" />
    <ClInclude Include="include\glm\detail\\type_mat3x4.hpp" />
    <ClInclude Include="include\glm\detail\\type_mat4x2.hpp" />
    <ClInclude Include="include\glm\detail\\type_mat4x3.hpp" />
    <ClInclude Include="include\glm\detail\\type_mat4x4.hpp" />
    <ClInclude Include="include\glm\detail\\type_quat.hpp" />
    <ClInclude Include="include\glm\detail\\type_vec1.hpp" />
    <ClInclude Include="include\glm\detail\\type_vec2.hpp" />
    <ClInclude Include="include\glm\detail\\type_vec3.hpp" />
    <ClInclude Include="include\glm\detail\\type_vec4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_clip_space.hpp" />
    <ClInclude Include="include\glm\ext\matrix_common.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double2x2.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double2x2_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double2x3.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double2x3_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double2x4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double2x4_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double3x2.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double3x2_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double3x3.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double3x3_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double3x4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double3x4_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double4x2.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double4x2_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double4x3.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double4x3_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double4x4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_double4x4_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float2x2.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float2x2_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float2x3.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float2x3_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float2x4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float2x4_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float3x2.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float3x2_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float3x3.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float3x3_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float3x4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float3x4_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float4x2.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float4x2_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float4x3.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float4x3_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float4x4.hpp" />
    <ClInclude Include="include\glm\ext\matrix_float4x4_precision.hpp" />
    <ClInclude Include="include\glm\ext\matrix_projection.hpp" />
    <ClInclude Include="include\glm\ext\matrix_relational.hpp" />
    <ClInclude Include="include\glm\ext\matrix_transform.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_common.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_double.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_double_precision.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_exponential.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_float.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_float_precision.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_geometric.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_relational.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_transform.hpp" />
    <ClInclude Include="include\glm\ext\quaternion_trigonometric.hpp" />
    <ClInclude Include="include\glm\ext\scalar_common.hpp" />
    <ClInclude Include="include\glm\ext\scalar_constants.hpp" />
    <ClInclude Include="include\glm\ext\scalar_int_sized.hpp" />
    <ClInclude Include="include\glm\ext\scalar_relational.hpp" />
    <ClInclude Include="include\glm\ext\scalar_uint_sized.hpp" />
    <ClInclude Include="include\glm\ext\scalar_ulp.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool1.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool1_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool2.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool2_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool3.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool3_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool4.hpp" />
    <ClInclude Include="include\glm\ext\vector_bool4_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_common.hpp" />
    <ClInclude Include="include\glm\ext\vector_double1.hpp" />
    <ClInclude Include="include\glm\ext\vector_double1_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_double2.hpp" />
    <ClInclude Include="include\glm\ext\vector_double2_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_double3.hpp" />
    <ClInclude Include="include\glm\ext\vector_double3_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_double4.hpp" />
    <ClInclude Include="include\glm\ext\vector_double4_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_float1.hpp" />
    <ClInclude Include="include\glm\ext\vector_float1_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_float2.hpp" />
    <ClInclude Include="include\glm\ext\vector_float2_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_float3.hpp" />
    <ClInclude Include="include\glm\ext\vector_float3_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_float4.hpp" />
    <ClInclude Include="include\glm\ext\vector_float4_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_int1.hpp" />
    <ClInclude Include="include\glm\ext\vector_int1_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_int2.hpp" />
    <ClInclude Include="include\glm\ext\vector_int2_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_int3.hpp" />
    <ClInclude Include="include\glm\ext\vector_int3_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_int4.hpp" />
    <ClInclude Include="include\glm\ext\vector_int4_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_relational.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint1.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint1_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint2.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint2_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint3.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint3_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint4.hpp" />
    <ClInclude Include="include\glm\ext\vector_uint4_precision.hpp" />
    <ClInclude Include="include\glm\ext\vector_ulp.hpp" />
    <ClInclude Include="include\glm\gtc\bitfield.hpp" />
    <ClInclude Include="include\glm\gtc\color_space.hpp" />
    <ClInclude Include="include\glm\gtc\constants.hpp" />
    <ClInclude Include="include\glm\gtc\epsilon.hpp" />
    <ClInclude Include="include\glm\gtc\integer.hpp" />
    <ClInclude Include="include\glm\gtc\matrix_access.hpp" />
    <ClInclude Include="include\glm\gtc\matrix_integer.hpp" />
    <ClInclude Include="include\glm\gtc\matrix_inverse.hpp" />
    <ClInclude Include="include\glm\gtc\matrix_transform.hpp" />
    <ClInclude Include="include\glm\gtc\noise.hpp" />
    <ClInclude Include="include\glm\gtc\packing.hpp" />
    <ClInclude Include="include\glm\gtc\quaternion.hpp" />
    <ClInclude Include="include\glm\gtc\random.hpp" />
    <ClInclude Include="include\glm\gtc\reciprocal.hpp" />
    <ClInclude Include="include\glm\gtc\round.hpp" />
    <ClInclude Include="include\glm\gtc\type_aligned.hpp" />
    <ClInclude Include="include\glm\gtc\type_precision.hpp" />
    <ClInclude Include="include\glm\gtc\type_ptr.hpp" />
    <ClInclude Include="include\glm\gtc\ulp.hpp" />
    <ClInclude Include="include\glm\gtc\vec1.hpp" />
    <ClInclude Include="include\glm\gtx\associated_min_max.hpp" />
    <ClInclude Include="include\glm\gtx\bit.hpp" />
    <ClInclude Include="include\glm\gtx\closest_point.hpp" />
    <ClInclude Include="include\glm\gtx\color_encoding.hpp" />
    <ClInclude Include="include\glm\gtx\color_space.hpp" />
    <ClInclude Include="include\glm\gtx\color_space_YCoCg.hpp" />
    <ClInclude Include="include\glm\gtx\common.hpp" />
    <ClInclude Include="include\glm\gtx\compatibility.hpp" />
    <ClInclude Include="include\glm\gtx\component_wise.hpp" />
    <ClInclude Include="include\glm\gtx\dual_quaternion.hpp" />
    <ClInclude Include="include\glm\gtx\easing.hpp" />
    <ClInclude Include="include\glm\gtx\euler_angles.hpp" />
    <ClInclude Include="include\glm\gtx\extend.hpp" />
    <ClInclude Include="include\glm\gtx\extended_min_max.hpp" />
    <ClInclude Include="include\glm\gtx\exterior_product.hpp" />
    <ClInclude Include="include\glm\gtx\fast_exponential.hpp" />
    <ClInclude Include="include\glm\gtx\fast_square_root.hpp" />
    <ClInclude Include="include\glm\gtx\fast_trigonometry.hpp" />
    <ClInclude Include="include\glm\gtx\functions.hpp" />
    <ClInclude Include="include\glm\gtx\gradient_paint.hpp" />
    <ClInclude Include="include\glm\gtx\handed_coordinate_space.hpp" />
    <ClInclude Include="include\glm\gtx\hash.hpp" />
    <ClInclude Include="include\glm\gtx\integer.hpp" />
    <ClInclude Include="include\glm\gtx\intersect.hpp" />
    <ClInclude Include="include\glm\gtx\io.hpp" />
    <ClInclude Include="include\glm\gtx\log_base.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_cross_product.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_decompose.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_factorisation.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_interpolation.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_major_storage.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_operation.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_query.hpp" />
    <ClInclude Include="include\glm\gtx\matrix_transform_2d.hpp" />
    <ClInclude Include="include\glm\gtx\mixed_product.hpp" />
    <ClInclude Include="include\glm\gtx\norm.hpp" />
    <ClInclude Include="include\glm\gtx\normal.hpp" />
    <ClInclude Include="include\glm\gtx\normalize_dot.hpp" />
    <ClInclude Include="include\glm\gtx\number_precision.hpp" />
    <ClInclude Include="include\glm\gtx\optimum_pow.hpp" />
    <ClInclude Include="include\glm\gtx\orthonormalize.hpp" />
    <ClInclude Include="include\glm\gtx\perpendicular.hpp" />
    <ClInclude Include="include\glm\gtx\polar_coordinates.hpp" />
    <ClInclude Include="include\glm\gtx\projection.hpp" />
    <ClInclude Include="include\glm\gtx\quaternion.hpp" />
    <ClInclude Include="include\glm\gtx\range.hpp" />
    <ClInclude Include="include\glm\gtx\raw_data.hpp" />
    <ClInclude Include="include\glm\gtx\rotate_normalized_axis.hpp" />
    <ClInclude Include="include\glm\gtx\rotate_vector.hpp" />
    <ClInclude Include="include\glm\gtx\scalar_multiplication.hpp" />
    <ClInclude Include="include\glm\gtx\scalar_relational.hpp" />
    <ClInclude Include="include\glm\gtx\spline.hpp" />
    <ClInclude Include="include\glm\gtx\std_based_type.hpp" />
    <ClInclude Include="include\glm\gtx\string_cast.hpp" />
    <ClInclude Include="include\glm\gtx\texture.hpp" />
    <ClInclude Include="include\glm\gtx\transform.hpp" />
    <ClInclude Include="include\glm\gtx\transform2.hpp" />
    <ClInclude Include="include\glm\gtx\type_aligned.hpp" />
    <ClInclude Include="include\glm\gtx\type_trait.hpp" />
    <ClInclude Include="include\glm\gtx\vec_swizzle.hpp" />
    <ClInclude Include="include\glm\gtx\vector_angle.hpp" />
    <ClInclude Include="include\glm\gtx\vector_query.hpp" />
    <ClInclude Include="include\glm\gtx\wrap.hpp" />
    <ClInclude Include="include\glm\simd\common.h" />
    <ClInclude Include="include\glm\simd\exponential.h" />
    <ClInclude Include="include\glm\simd\geometric.h" />
    <ClInclude Include="include\glm\simd\integer.h" />
    <ClInclude Include="include\glm\simd\matrix.h" />
    <ClInclude Include="include\glm\simd\packing.h" />
    <ClInclude Include="include\glm\simd\platform.h" />
    <ClInclude Include="include\glm\simd\trigonometric.h" />
    <ClInclude Include="include\glm\simd\vector_relational.h" />
    <ClInclude Include="include\glm\common.hpp" />
    <ClInclude Include="include\glm\exponential.hpp" />
    <ClInclude Include="include\glm\ext.hpp" />
    <ClInclude Include="include\glm\\fwd.hpp" />
    <ClInclude Include="include\glm\geometric.hpp" />
    <ClInclude Include="include\glm\glm.hpp" />
    <ClInclude Include="include\glm\integer.hpp" />
    <ClInclude Include="include\glm\mat2x2.hpp" />
    <ClInclude Include="include\glm\mat2x3.hpp" />
    <ClInclude Include="include\glm\mat2x4.hpp" />
    <ClInclude Include="include\glm\mat3x2.hpp" />
    <ClInclude Include="include\glm\mat3x3.hpp" />
    <ClInclude Include="include\glm\mat3x4.hpp" />
    <ClInclude Include="include\glm\mat4x2.hpp" />
    <ClInclude Include="include\glm\mat4x3.hpp" />
    <ClInclude Include="include\glm\mat4x4.hpp" />
    <ClInclude Include="include\glm\matrix.hpp" />
    <ClInclude Include="include\glm\packing.hpp" />
    <ClInclude Include="include\glm\trigonometric.hpp" />
    <ClInclude Include="include\glm\vec2.hpp" />
    <ClInclude Include="include\glm\vec3.hpp" />
    <ClInclude Include="include\glm\vec4.hpp" />
    <ClInclude Include="include\glm\vector_relational.hpp" />
    <ClInclude Include="include\stb_image.h" />
    <ClInclude Include="ShaderProgram\ShaderProgram.h" />
    <ClInclude Include="ShaderProgram\StaticShader.h" />
    <ClInclude Include="include\camera.h" />
    <ClInclude Include="include\utils.hpp" />
  </ItemGroup>
  <ItemGroup>
    <None Include="include\glm\detail\func_common.inl" />
    <None Include="include\glm\detail\func_common_simd.inl" />
    <None Include="include\glm\detail\func_exponential.inl" />
    <None Include="include\glm\detail\func_exponential_simd.inl" />
    <None Include="include\glm\detail\func_geometric.inl" />
    <None Include="include\glm\detail\func_geometric_simd.inl" />
    <None Include="include\glm\detail\func_integer.inl" />
    <None Include="include\glm\detail\func_integer_simd.inl" />
    <None Include="include\glm\detail\func_matrix.inl" />
    <None Include="include\glm\detail\func_matrix_simd.inl" />
    <None Include="include\glm\detail\func_packing.inl" />
    <None Include="include\glm\detail\func_packing_simd.inl" />
    <None Include="include\glm\detail\func_trigonometric.inl" />
    <None Include="include\glm\detail\func_trigonometric_simd.inl" />
    <None Include="include\glm\detail\func_vector_relational.inl" />
    <None Include="include\glm\detail\func_vector_relational_simd.inl" />
    <None Include="include\glm\detail\type_half.inl" />
    <None Include="include\glm\detail\type_mat2x2.inl" />
    <None Include="include\glm\detail\type_mat2x3.inl" />
    <None Include="include\glm\detail\type_mat2x4.inl" />
    <None Include="include\glm\detail\type_mat3x2.inl" />
    <None Include="include\glm\detail\type_mat3x3.inl" />
    <None Include="include\glm\detail\type_mat3x4.inl" />
    <None Include="include\glm\detail\type_mat4x2.inl" />
    <None Include="include\glm\detail\type_mat4x3.inl" />
    <None Include="include\glm\detail\type_mat4x4.inl" />
    <None Include="include\glm\detail\type_mat4x4_simd.inl" />
    <None Include="include\glm\detail\type_quat.inl" />
    <None Include="include\glm\detail\type_quat_simd.inl" />
    <None Include="include\glm\detail\type_vec1.inl" />
    <None Include="include\glm\detail\type_vec2.inl" />
    <None Include="include\glm\detail\type_vec3.inl" />
    <None Include="include\glm\detail\type_vec4.inl" />
    <None Include="include\glm\detail\type_vec4_simd.inl" />
    <None Include="include\glm\ext\matrix_clip_space.inl" />
    <None Include="include\glm\ext\matrix_common.inl" />
    <None Include="include\glm\ext\matrix_projection.inl" />
    <None Include="include\glm\ext\matrix_relational.inl" />
    <None Include="include\glm\ext\matrix_transform.inl" />
    <None Include="include\glm\ext\quaternion_common.inl" />
    <None Include="include\glm\ext\quaternion_common_simd.inl" />
    <None Include="include\glm\ext\quaternion_exponential.inl" />
    <None Include="include\glm\ext\quaternion_geometric.inl" />
    <None Include="include\glm\ext\quaternion_relational.inl" />
    <None Include="include\glm\ext\quaternion_transform.inl" />
    <None Include="include\glm\ext\quaternion_trigonometric.inl" />
    <None Include="include\glm\ext\scalar_common.inl" />
    <None Include="include\glm\ext\scalar_constants.inl" />
    <None Include="include\glm\ext\scalar_relational.inl" />
    <None Include="include\glm\ext\scalar_ulp.inl" />
    <None Include="include\glm\ext\\vector_common.inl" />
    <None Include="include\glm\ext\\vector_relational.inl" />
    <None Include="include\glm\ext\\vector_ulp.inl" />
    <None Include="include\glm\gtc\\bitfield.inl" />
    <None Include="include\glm\gtc\color_space.inl" />
    <None Include="include\glm\gtc\constants.inl" />
    <None Include="include\glm\gtc\epsilon.inl" />
    <None Include="include\glm\gtc\integer.inl" />
    <None Include="include\glm\gtc\matrix_access.inl" />
    <None Include="include\glm\gtc\matrix_inverse.inl" />
    <None Include="include\glm\gtc\matrix_transform.inl" />
    <None Include="include\glm\gtc\\noise.inl" />
    <None Include="include\glm\gtc\packing.inl" />
    <None Include="include\glm\gtc\quaternion.inl" />
    <None Include="include\glm\gtc\quaternion_simd.inl" />
    <None Include="include\glm\gtc\random.inl" />
    <None Include="include\glm\gtc\reciprocal.inl" />
    <None Include="include\glm\gtc\round.inl" />
    <None Include="include\glm\gtc\type_precision.inl" />
    <None Include="include\glm\gtc\type_ptr.inl" />
    <None Include="include\glm\gtc\ulp.inl" />
    <None Include="include\glm\gtx\associated_min_max.inl" />
    <None Include="include\glm\gtx\bit.inl" />
    <None Include="include\glm\gtx\closest_point.inl" />
    <None Include="include\glm\gtx\color_encoding.inl" />
    <None Include="include\glm\gtx\color_space.inl" />
    <None Include="include\glm\gtx\color_space_YCoCg.inl" />
    <None Include="include\glm\gtx\common.inl" />
    <None Include="include\glm\gtx\compatibility.inl" />
    <None Include="include\glm\gtx\component_wise.inl" />
    <None Include="include\glm\gtx\dual_quaternion.inl" />
    <None Include="include\glm\gtx\easing.inl" />
    <None Include="include\glm\gtx\euler_angles.inl" />
    <None Include="include\glm\gtx\extend.inl" />
    <None Include="include\glm\gtx\extended_min_max.inl" />
    <None Include="include\glm\gtx\exterior_product.inl" />
    <None Include="include\glm\gtx\fast_exponential.inl" />
    <None Include="include\glm\gtx\fast_square_root.inl" />
    <None Include="include\glm\gtx\fast_trigonometry.inl" />
    <None Include="include\glm\gtx\float_notmalize.inl" />
    <None Include="include\glm\gtx\functions.inl" />
    <None Include="include\glm\gtx\gradient_paint.inl" />
    <None Include="include\glm\gtx\handed_coordinate_space.inl" />
    <None Include="include\glm\gtx\hash.inl" />
    <None Include="include\glm\gtx\integer.inl" />
    <None Include="include\glm\gtx\intersect.inl" />
    <None Include="include\glm\gtx\io.inl" />
    <None Include="include\glm\gtx\log_base.inl" />
    <None Include="include\glm\gtx\matrix_cross_product.inl" />
    <None Include="include\glm\gtx\matrix_decompose.inl" />
    <None Include="include\glm\gtx\matrix_factorisation.inl" />
    <None Include="include\glm\gtx\matrix_interpolation.inl" />
    <None Include="include\glm\gtx\matrix_major_storage.inl" />
    <None Include="include\glm\gtx\matrix_operation.inl" />
    <None Include="include\glm\gtx\matrix_query.inl" />
    <None Include="include\glm\gtx\matrix_transform_2d.inl" />
    <None Include="include\glm\gtx\mixed_product.inl" />
    <None Include="include\glm\gtx\norm.inl" />
    <None Include="include\glm\gtx\normal.inl" />
    <None Include="include\glm\gtx\normalize_dot.inl" />
    <None Include="include\glm\gtx\number_precision.inl" />
    <None Include="include\glm\gtx\optimum_pow.inl" />
    <None Include="include\glm\gtx\orthonormalize.inl" />
    <None Include="include\glm\gtx\perpendicular.inl" />
    <None Include="include\glm\gtx\polar_coordinates.inl" />
    <None Include="include\glm\gtx\projection.inl" />
    <None Include="include\glm\gtx\quaternion.inl" />
    <None Include="include\glm\gtx\raw_data.inl" />
    <None Include="include\glm\gtx\rotate_normalized_axis.inl" />
    <None Include="include\glm\gtx\rotate_vector.inl" />
    <None Include="include\glm\gtx\scalar_relational.inl" />
    <None Include="include\glm\gtx\spline.inl" />
    <None Include="include\glm\gtx\std_based_type.inl" />
    <None Include="include\glm\gtx\string_cast.inl" />
    <None Include="include\glm\gtx\texture.inl" />
    <None Include="include\glm\gtx\transform.inl" />
    <None Include="include\glm\gtx\transform2.inl" />
    <None Include="include\glm\gtx\type_aligned.inl" />
    <None Include="include\glm\gtx\type_trait.inl" />
    <None Include="include\glm\gtx\vector_angle.inl" />
    <None Include="include\glm\gtx\vector_query.inl" />
    <None Include="include\glm\gtx\wrap.inl" />
    <None Include="lib\glew32d.dll" />
    <None Include="lib\glfw3.dll" />
    <None Include="Shaders\fragment.sh" />
    <None Include="Shaders\geometry.sh" />
    <None Include="Shaders\vertex.sh" />
    <None Include="Shaders\fragmentAxis.sh" />
    <None Include="Shaders\vertexAxis.sh" />
  </ItemGroup>
  <ItemGroup>
    <ClCompile Include="include\glm\detail\glm.cpp" />
    <ClCompile Include="src\main.cpp" />
    <ClCompile Include="ShaderProgram\ShaderProgram.cpp" />
    <ClCompile Include="src\camera.cpp" />
  </ItemGroup>
  <ItemGroup>
    <Library Include="lib\glew32d.lib" />
    <Library Include="lib\glfw3dll.lib" />
  </ItemGroup>
</Project>'''

 # visual studio users file template string
vcxprojuser = '''<?xml version="1.0" encoding="utf-8"?>
    <Project ToolsVersion="15.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
      <PropertyGroup>
        <ShowAllFiles>true</ShowAllFiles>
      </PropertyGroup>
      <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
        <LocalDebuggerEnvironment>PATH=%PATH%;$(ProjectDir)lib</LocalDebuggerEnvironment>
        <DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>
      </PropertyGroup>
      <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
        <LocalDebuggerEnvironment>PATH=%PATH%;$(ProjectDir)lib</LocalDebuggerEnvironment>
        <DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>
      </PropertyGroup>
      <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
        <LocalDebuggerEnvironment>PATH=%PATH%;$(ProjectDir)lib</LocalDebuggerEnvironment>
        <DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>
      </PropertyGroup>
      <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
        <LocalDebuggerEnvironment>PATH=%PATH%;$(ProjectDir)lib</LocalDebuggerEnvironment>
        <DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>
      </PropertyGroup>
    </Project>'''

     
#initialize the tkinter library        
root = tk.Tk()
#main top level frame
main_frame = tk.LabelFrame(root,text="Main Frame",relief=tk.RAISED )
# create 2 subframes
subframe_1 =  tk.LabelFrame(main_frame)
subframe_2 =  tk.LabelFrame(main_frame)
#create the entry for the new project name
entry = tk.Entry(subframe_2)
# global variables
visual_studio_projects_directory = 'C:/Users/aitor/source/repos'
project_name: str = None
folder_icon = None
template_dir = os.path.join(os.getcwd(), 'ProjectTemplate_GL')
icons_dir = os.path.join(os.getcwd(),'icons')
# list of recently created projects. We create a list with the new created projects to 
# delete. The reason of that is to protect deliting existing projects that have not 
# been created in the current sesion. It could be usefull to delte projects old projects from
# the tool but this is a bit dangerous and I don't want to delete projects by accident
new_created_projects = []

# we save the directory where the script was launched because we will chande directories
# and we need to know the python scrip directory to load images or go back where we started
app_launch_dir = os.getcwd()

# create list box with a new style to avoid icon overlaping 
s = ttk.Style()
s.configure('treeStyle.Treeview', rowheight=40)
project_list_box = ttk.Treeview(subframe_1, height=4, style='treeStyle.Treeview')

#change select mode to not allow multiple selection of items
project_list_box.config(selectmode='browse')
# configure the heigh of the tree
project_list_box.config(height=10)

#callbacks
def current_selected_items_callback(event):
  item = project_list_box.selection()[0]
  entry.delete(0,"end")
  entry.insert(0, project_list_box.item(item,"text"))

def create_solution_file(project_name):
    solution_file_extension = '.sln'
    file_content = solution_file.replace('project_name',project_name)
    with open(project_name+solution_file_extension, 'w') as f:
    	f.write(file_content)


def create_project_file(project_name):
    vcxproj_file_extension = '.vcxproj'
    file_content = vcxproj.replace('project_name', project_name)
    with open(project_name+vcxproj_file_extension, 'w') as f:
        f.write(file_content)


def create_project_filters(project_name):
    vcxproj_filters_file_extension = '.vcxproj.filters'
    with open(project_name+vcxproj_filters_file_extension, 'w') as f:
        f.write(vcxproj_filters)


def create_project_user(project_name):
    vcxproj_usr_file_extension = '.vcxproj.user'
    with open(project_name+vcxproj_usr_file_extension, 'w') as f:
        f.write(vcxprojuser)

# open the created project
def open_visual_studio():
  open_project = entry.get()
  if len(open_project) == 0 :
    tk.messagebox.showerror("project not found","select a project to open!")
  else:
    project_folder = os.path.join(visual_studio_projects_directory,open_project)
    solution_file = os.path.join(project_folder,open_project+'.sln')
    os.system('"%s"'% solution_file)

#delete selected project
def delete_project():
  delete_project = entry.get()
  can_be_deleted = False
  for project in new_created_projects:
    if project == delete_project:
      can_be_deleted = True
      break
  if can_be_deleted:
    shutil.rmtree(os.path.join(visual_studio_projects_directory,delete_project))
    messagebox.showinfo("Project Deleted","open gl project: "+ project_name + " has been deleted")
    # remove item from the list from the list
    new_created_projects.remove(delete_project)
    # remove item from the tree view
    project_list_box.delete(*project_list_box.get_children())
    # update tree view
    fill_tree_view()
  else:
    messagebox.showerror("Delete Error", "you can't delete projects that \nhave not being created in this session for safety reasons!")
    

# create an openGL project with the given name
def create_project():
    global project_name 
    project_name = entry.get()
    os.chdir(visual_studio_projects_directory)
    # create solution directory in the folder where all visual studio projects are by default
    os.makedirs(os.path.join(project_name, 'Debug'))
    # cd into this directory
    os.chdir(project_name)
    # create solution file
    create_solution_file(project_name)
    # copy the template folders, files and create the project directory
    shutil.copytree(template_dir, os.path.join(os.getcwd(),project_name))
    # cd into project file
    os.chdir(project_name)
    # create all the files
    create_project_file(project_name)
    create_project_user(project_name)
    create_project_filters(project_name)
    # move the libs to ../Debug folder
    shutil.move('glew32d.dll', '../Debug')
    shutil.move('glfw3.dll', '../Debug')
    messagebox.showinfo("Prject created","open gl project:"+ project_name+ " succesfully created")
    project_list_box.delete(*project_list_box.get_children())
    fill_tree_view()
    global new_created_projects 
    new_created_projects.append(project_name)
    os.chdir(visual_studio_projects_directory)


def load_icons():
  global folder_icon
  icon_path = os.path.join(icons_dir,"ficon.png")
  photo = Image.open(icon_path)
  folder_icon = ImageTk.PhotoImage(photo)


def fill_tree_view(proj = '%!none!%'):
    for d in os.listdir(visual_studio_projects_directory):
      project_list_box.insert('','end',d, text = d,image= folder_icon )
     
        
def run_gui_app():
  root.title('VS openGl project creator ')
  root.geometry("300x600") 
  root.minsize(600,600)
  root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=os.path.join(icons_dir,"opengl.png")))
  root.resizable(True,True)
  label1 = tk.Label(subframe_1, text="vs projects list")
  label = tk.Label(subframe_2, text="Project name")
  label.grid(row = 0, column=0)
  # set tree view callbacks and fill in the tree
  project_list_box.bind('<Double-1>',current_selected_items_callback)
  fill_tree_view()
  # create buttons
  deletebutton = tk.Button(subframe_2,text="Delete", command = delete_project)
  button1 = tk.Button(subframe_2, text = "Create", command= create_project)
  button2 = tk.Button(subframe_2, text = "Open", command = open_visual_studio)
   #position elements in subrame_2
  entry.grid(row = 0, column = 2,sticky="we")
  deletebutton.grid(row=1,column=0, padx=2,pady=10,sticky="we")
  button1.grid(row= 1, column= 2,padx=2, pady=10,sticky="we")
  button2.grid(row=1,column=1,padx=1, pady=10,sticky="we")
  #positon elements in subrame_1
  label1.pack()
  project_list_box.pack(fill=tk.BOTH,expand=True,padx = 4,pady=4)

  label.grid(row=0)
  subframe_1.pack(fill=tk.BOTH,expand=True)
  subframe_2.pack(fill=tk.BOTH,expand=True)
  main_frame.pack(fill=tk.BOTH,expand=True)
  root.mainloop()


if __name__ == "__main__":
  load_icons()
  run_gui_app()
 
