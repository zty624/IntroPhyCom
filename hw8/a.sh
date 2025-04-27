#!/bin/bash
# Ising simulation for homework 8.1

path=$(pwd)
output_dir="${path}/outputa"
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
    t=$2
    beta=$(echo "scale=4; 1/$t" | bc)
    iternum=$((box * box * 150000))

    echo "[$(date +%T)] Running box:${box} temp:${t} beta:${beta}"

    "${path}/build/a" "$box" 1 "$iternum" "$beta" > \
    "${output_dir}/box${box}_temp${t}.txt"
}

export -f run_simulation

parallel -j "$(nproc)" run_simulation ::: 8 16 32 ::: $(seq 1.5 0.1 3 | tr ',' '.')
echo "All simulations completed. Output saved to: ${output_dir}"