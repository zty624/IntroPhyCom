using LinearAlgebra
using Statistics
using Random
using Plots

corr(u, v) = abs(mean(u[:] .* v[:]))
energy(x::Vector{}, J::Matrix{}) = -0.5 * sum(x' * J * x)
add_noise(v, delta) = [(rand() < delta ? rand((-1, +1)) : vi) for vi in v]

# function metropolis!(
#     spin_idx::Int, spinset::Matrix{Int}, 
#     J_mat::Matrix{Float64}, beta::Float64
# )
#     # spinset is a SpNum * PtNum matrix, I want to update the spinset entirely
#     p = size(spinset, 1)
#     spin_vec = spinset[:, spin_idx]
#     dE_vec = 2 * spin_vec .* (J_mat[spin_idx, :] * spin_vec)
# end

function metropolis!(
    spin_idx::Int, spin::Vector{Int}, 
    J_mat::Matrix{Float64}, beta::Float64
)
    delta_E = 2 * spin[spin_idx] * sum(J_mat[spin_idx, :] .* spin) 
    if delta_E <= 0 || rand() < exp(-beta * delta_E)
        spin[spin_idx] *= -1
    end
end

function init(PtNum::Int, SpNum::Int, delta::AbstractFloat=0.0)
    Js_mat = zeros(PtNum, PtNum)         # H defined by spinset
    # Init sp_mat & Js_mat
    sp_mat = rand([-1, 1], SpNum, PtNum) # random spin pattern
    for i in 1:SpNum
        Js_mat += sp_mat[i, :] * sp_mat[i, :]'
    end
    Js_mat ./= SpNum
    Js_mat[diagind(Js_mat)] .= 0
    # Init spin set
    ss_mat = copy(sp_mat)
    for i in 1:SpNum
        ss_mat[i, :] = add_noise(ss_mat[i, :], delta)
    end
    return (Js_mat, sp_mat, ss_mat)
end

function part1()
    println("Part1")
    PtNum = 1000; SpNum = 1
    Js_mat, sp_mat, ss_mat = init(1000, 1, 1.0)
    num = 1e5
    beta = 1e5
    println("Initial corr: ", corr(ss_mat[1, :], sp_mat[1, :]))
    @views for _ in 1:num
        idx = rand(1:PtNum)
        metropolis!(idx, ss_mat[1, :], Js_mat, beta)
    end
    println("Final energy: ", energy(ss_mat[1, :], Js_mat))
    println("Final corr: ", corr(ss_mat[1, :], sp_mat[1, :]))
end

function part2()
    println("Part2")
    PtNum = 2000; SpNum = 10
    Js_mat, sp_mat, ss_mat = init(2000, 10, 0.5)
    ss_mat_copy = copy(ss_mat)
    num = 1e5
    beta = 1e5
    @views for i in 1:num
        for j in 1:SpNum
            idx = rand(1:PtNum)
            metropolis!(idx, ss_mat[j, :], Js_mat, beta)
        end
    end
    corr_vec = [corr(ss_mat[i, :], sp_mat[i, :]) for i in 1:SpNum]
    println("corr: ", corr_vec)
    println("mean: ", mean(corr_vec))
end

function part3()
    println("Part3")
    PtNum = 2000
    num_samples = 1     # ensemble mean size
    p_values = 50:50:400
    histograms = []

    for p in p_values
        corrTol = Float64[]
        for _ in 1:num_samples
            println("start p = $p")
            local Js_mat, sp_mat, ss_mat
            Js_mat, sp_mat, ss_mat = init(PtNum, p, 0.5)

            for _ in 1:5e4
                for j in 1:p
                    # from 1 to PtNum to select a idx
                    idx = rand(1:p)
                    ss_mat[j, :] = metropolis!(idx, ss_mat[j, :], Js_mat, 1e5)
                end
            end
            append!(corrTol, [corr(ss_mat[i, :], sp_mat[i, :]) for i in 1:p])
        end
        push!(histograms, histogram(corrTol, bins=20, label="p=$p", alpha=0.5))
        println("p=$p: ", mean(corrTol))
    end
    plot(histograms...)
end

part2()