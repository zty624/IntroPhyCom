cmake_minimum_required(VERSION 3.22)

project(ising)

set(CMAKE_CXX_STANDARD 17)

add_executable(a
    ../ising/ising.h
    ../ising/ising.cpp
    a.cpp
)

add_executable(b
    ../ising/ising.h
    ../ising/ising.cpp
    b.cpp
)

# add_executable(b
#     ising.h
#     ising.cpp
#     b.cpp
# )