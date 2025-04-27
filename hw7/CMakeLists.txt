cmake_minimum_required(VERSION 3.22)

project(ising)

set(CMAKE_CXX_STANDARD 17)

add_executable(dfs
    ../ising/ising.h
    ../ising/ising.cpp
    dfs.cpp
)

add_executable(rand
    rand.cpp
)