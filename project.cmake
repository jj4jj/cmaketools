#CMake projects genearte by cmaketools 

project({{project_name}} CXX)
set({{project_name}}_VERSION {{project_version}})

#min version
cmake_minimum_required(VERSION 2.6)

# building must be in not source

string(COMPARE EQUAL "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" BUILDING_IN_SOURCE)

if(BUILDING_IN_SOURCE)
    message(FATAL_ERROR "compile dir must not be source dir , please remove 'CMakeCache.txt' in current dir , then create a building dir in which dir you can exec commands like this 'cmake <src dir>  [options]' ")
endif()

#compile option
option(DEBUG "Debug mode" 1)
option(PCH "Use precompiled headers" 0)
SET(DEBUG {{debug_mode}})

{{definations}}
SET( CMAKE_VERBOSE_MAKEFILE {{verbose}})

if(DEBUG)
    set(CMAKE_BUILD_TYPE Debug)
    add_definitions(-DDEBUG)
    message("Build in debug-mode : Yes (default)")
else()
    set(CMAKE_BUILD_TYPE Release)
    message("Build in debug-mode : No")
endif()

set(CMAKE_COMM_FLAGS "")

{%-for inc in incs %}
include_directories({{inc}})
{%-endfor%}

{%-for co in cos %}
add_compile_options("{{co}}")
{%-endfor%}

{%-for def in defs %}
add_definitions(-D{{def}})
{%-endfor%}


#debug common
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} ${CMAKE_COMM_FLAGS} -g3 -ggdb3 -Wall -Wfatal-errors -Wextra {{extra_c_flags}} -rdynamic")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}  ${CMAKE_COMM_FLAGS} -g3 -ggdb3 -Wall -Wfatal-errors -Wextra {{extra_cxx_flags}} -rdynamic")

# release mode
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} ${CMAKE_COMM_FLAGS} -g -O2 {{extra_c_flags}} -rdynamic")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} ${CMAKE_COMM_FLAGS} -g -O2 {{extra_cxx_flags}} -rdynamic")

# output dir
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# install dir
set(CMAKE_INSTALL_PREFIX {{install_dir}})

{%for unit in units%}add_subdirectory({{unit.subdir}})
{%endfor%}

{%for obj in objs%}
{%if obj.force%}
add_custom_target({{obj.name}}
    COMMAND {{obj.cmd}}
    DEPENDS {{obj.dep}})
{%else%}
add_custom_command(OUTPUT {{obj.out}}
    COMMAND {{obj.cmd}}
    DEPENDS {{obj.dep}})
{%endif%}
{%endfor%}
