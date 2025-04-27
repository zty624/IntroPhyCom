#!/bin/bash
# Ising simulation for homework 8.1

path=$(pwd)
output_dir="${path}/outputb"
mkdir -p "${path}/build" && cd "${path}/build"

if cmake "$path" && make; then
    echo "Build successful"
else
    echo "Build failed" >&2
    exit 1
fi

mkdir -p "$output_dir"
echo "Starting simulation..."

export path output_dir
run_simulation() {
    box=$1
    echo "[$(date +%T)] Running box:${box}"

    iternum=$((box * box * 1000))
    
    "${path}/build/b" "$box" 5000 "$iternum" > \
    "${output_dir}/box${box}.txt"
}

export -f run_simulation

parallel -j "$(nproc)" run_simulation ::: $(seq 8 4 32)
echo "All simulations completed. Output saved to: ${output_dir}"