#include "ising.h"
#include <stdexcept>
#include <vector> // Ensure vector is included

Particle::Particle(int idx, cords_t boxsize)
{
    this->idx = idx;
    this->boxsize = boxsize;
    this->pos[0] = idx / boxsize[1];  // 假设boxsize[0]是行数
    this->pos[1] = idx % boxsize[1];  // boxsize[1]是列数
    this->neighbors.clear();
}

IsingParticle::IsingParticle(int idx, cords_t boxsize, IsingSpin spin)
    : Particle(idx, boxsize), spin(spin) {}


std::vector<int>* IsingParticle::getNeighbor()
{
    neighbors = std::vector<int>();
    if (neighbors.empty())
    {
        int row = pos[0];
        int col = pos[1];
        int rowp = (row + 1) % boxsize[0];
        int rowm = (row - 1 + boxsize[0]) % boxsize[0];
        int colp = (col + 1) % boxsize[1];
        int colm = (col - 1 + boxsize[1]) % boxsize[1];
        neighbors.reserve(4);
        neighbors.push_back(rowm * boxsize[1] + col);  // 上
        neighbors.push_back(rowp * boxsize[1] + col);  // 下
        neighbors.push_back(row * boxsize[1] + colm);  // 左
        neighbors.push_back(row * boxsize[1] + colp);  // 右
    }
    return &neighbors;
}

IsingLattice::IsingLattice(cords_t boxsize, IsingSpin initialSpin) : Lattice(boxsize)
{
    const int total = boxsize[0] * boxsize[1];
    particles.reserve(total);
    for (int i = 0; i < total; ++i) {
        particles.push_back(new IsingParticle(i, boxsize, initialSpin));
    }
}

IsingLattice::~IsingLattice()
{
    for (auto particle : particles)
    {
        delete particle;  // 删除每个粒子
    }
    particles.clear();  // 清空粒子向量
}

Particle* IsingLattice::operator[](size_t idx) const
{
    if (idx < 0 || idx >= particles.size()) {
        throw std::out_of_range("Index out of range");
    }
    return particles[idx];
}

spin_cnt IsingLattice::getNeighborCount(int idx) const
{
    std::vector<int>* neighbors = particles[idx]->getNeighbor();
    if (neighbors == nullptr)
    {
        throw std::runtime_error("Neighbors not initialized");
    }
    spin_cnt count = {0, 0, 0};
    for (int i = 0; i < neighbors->size(); i++)
    {
        int neighborIdx = (*neighbors)[i];
        if (neighborIdx < 0 || neighborIdx >= particles.size())
        {
            throw std::out_of_range("Neighbor index out of range");
        }
        IsingSpin spin = particles[neighborIdx]->getSpin();
        if (spin == UP)
        {
            count[0]++;
        }
        else if (spin == DOWN)
        {
            count[1]++;
        }
        else
        {
            count[2]++;
        }
    }
    return count;
}

int IsingLattice::getLocalEnergy(int idx) const
{
    if (idx < 0 || idx >= particles.size())
    {
        throw std::out_of_range("Index out of range");
    }
    std::vector<int>* neighbors = this->particles[idx]->getNeighbor();
    int energy = 0;
    int selfspin = particles[idx]->getSpin() == UP ? 1 : -1;
    for (size_t i = 0; i < neighbors->size(); i++)
    {
        int neighborIdx = (*neighbors)[i];
        if (neighborIdx < 0 || neighborIdx >= particles.size())
        {
            throw std::out_of_range("Neighbor index out of range");
        }
        int neighborspin = particles[neighborIdx]->getSpin() == UP ? 1 : -1;
        energy += selfspin * neighborspin;
    }
    return -energy;
}

int IsingLattice::getGlobalEnergy() const
{
    int energy = 0;
    for (size_t i = 0; i < particles.size(); i++)
    {
        energy += getLocalEnergy(i);
    }
    return energy / 2;  // 消除重复计数
}

int IsingLattice::getGlobalMagnetization() const
{
    int magnet = 0;
    for (size_t i = 0; i < particles.size(); i++)
    {
        magnet += particles[i]->getSpin() == UP ? 1 : -1;
    }
    return magnet;
}

void IsingLattice::printLattice(std::ostream& os) const
{
    int row = boxsize[0];
    int col = boxsize[1];
    for (int i = 0; i < row; i++)
    {
        for (int j = 0; j < col; j++)
        {
            int idx = i * col + j;
            std::cout << particles[idx]->getSpin() << " ";
        }
        std::cout << "\n";
    }
}

FrustratedParticle::FrustratedParticle(int idx, cords_t boxsize, IsingSpin spin)
    : Particle(idx, boxsize), spin(spin) 
{
    if (pos[1] % 2 == 0) {
        is_A = true;  // 偶数列为A
    } else {
        is_A = false; // 奇数列为B
    }
}

std::vector<int>* FrustratedParticle::getNeighbor()
{
    if (neighbors.empty())
    {
        int row = pos[0];
        int col = pos[1];
        neighbors.reserve(6);
        if (is_A)
        {
            neighbors.push_back(row * boxsize[1] + (col + 1) % boxsize[1]);  // 右
            neighbors.push_back(row * boxsize[1] + (col + 2) % boxsize[1]);  // 右右
            neighbors.push_back(row * boxsize[1] + (col - 1 + boxsize[1]) % boxsize[1]);  // 左
            neighbors.push_back(row * boxsize[1] + (col - 2 + boxsize[1]) % boxsize[1]);  // 左左
            neighbors.push_back((row + 1) % boxsize[0] * boxsize[1] + (col + 1) % boxsize[1]);  // 下右
            neighbors.push_back((row + 1) % boxsize[0] * boxsize[1] + (col - 1 + boxsize[1]) % boxsize[1]);  // 下左
        }
        else
        {
            neighbors.push_back(row * boxsize[1] + (col - 1 + boxsize[1]) % boxsize[1]);  // 左
            neighbors.push_back(row * boxsize[1] + (col + 1) % boxsize[1]);  // 右
            neighbors.push_back((row + 1) % boxsize[0] * boxsize[1] + col % boxsize[1]);  // 下
            neighbors.push_back((row - 1 + boxsize[0]) % boxsize[0] * boxsize[1] + col % boxsize[1]);  // 上
            neighbors.push_back((row - 1 + boxsize[0]) % boxsize[0] * boxsize[1] + (col - 1 + boxsize[1]) % boxsize[1]);  // 上左
            neighbors.push_back((row - 1 + boxsize[0]) % boxsize[0] * boxsize[1] + (col + 1) % boxsize[1]);  // 上右
        }
    }
    return &neighbors;
}

FrustratedLattice::FrustratedLattice(cords_t boxsize, IsingSpin initialSpin) : Lattice(boxsize)
{
    const int total = boxsize[0] * boxsize[1];
    particles.reserve(total);
    for (int i = 0; i < total; ++i) {
        particles.push_back(new FrustratedParticle(i, boxsize, initialSpin));
    }
}

FrustratedLattice::~FrustratedLattice()
{
    for (auto particle : particles)
    {
        delete particle;  // 删除每个粒子
    }
    particles.clear();  // 清空粒子向量
}

Particle* FrustratedLattice::operator[](size_t idx) const
{
    if (idx < 0 || idx >= particles.size()) {
        throw std::out_of_range("Index out of range");
    }
    return particles[idx];
}

spin_cnt FrustratedLattice::getNeighborCount(int idx) const
{
    std::vector<int>* neighbors = particles[idx]->getNeighbor();
    if (neighbors == nullptr)
    {
        throw std::runtime_error("Neighbors not initialized");
    }
    spin_cnt count = {0, 0, 0};
    for (int i = 0; i < neighbors->size(); i++)
    {
        int neighborIdx = (*neighbors)[i];
        if (neighborIdx < 0 || neighborIdx >= particles.size())
        {
            throw std::out_of_range("Neighbor index out of range");
        }
        IsingSpin spin = particles[neighborIdx]->getSpin();
        if (spin == UP)
        {
            count[0]++;
        }
        else if (spin == DOWN)
        {
            count[1]++;
        }
        else
        {
            count[2]++;
        }
    }
    return count;
}

int FrustratedLattice::getLocalEnergy(int idx) const
{
    if (idx < 0 || idx >= particles.size())
    {
        throw std::out_of_range("Index out of range");
    }
    std::vector<int>* neighbors = particles[idx]->getNeighbor();

    int energy = 0;
    for (int i = 0; i < neighbors->size(); i++)
    {
        int neighborIdx = (*neighbors)[i];
        if (neighborIdx < 0 || neighborIdx >= particles.size())
        {
            throw std::out_of_range("Neighbor index out of range");
        }
        energy += particles[idx]->getSpin() * particles[neighborIdx]->getSpin();
    }
    return energy;
}

int FrustratedLattice::getGlobalEnergy() const
{
    int energy = 0;
    for (size_t i = 0; i < particles.size(); i++)
    {
        energy += getLocalEnergy(i);
    }
    return energy / 2;  // 消除重复计数
}

int FrustratedLattice::getGlobalMagnetization() const
{
    int magnet = 0;
    for (size_t i = 0; i < particles.size(); i++)
    {
        magnet += particles[i]->getSpin();
    }
    return magnet;
}

void FrustratedLattice::printLattice(std::ostream& os) const
{
    int row = boxsize[0];
    int col = boxsize[1];
    for (int i = 0; i < row; i++)
    {
        for (int j = 0; j < col; j++)
        {
            int idx = i * col + j;
            std::cout << particles[idx]->getSpin() << " ";
        }
        std::cout << "\n";
    }
}