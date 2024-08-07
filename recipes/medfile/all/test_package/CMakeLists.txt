cmake_minimum_required(VERSION 3.15)
project(MedfileTest CXX)

find_package(medfile CONFIG REQUIRED)

add_executable(test src/test.cpp)
target_link_libraries(test medfile::medfile)
