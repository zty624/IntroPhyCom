#ifndef ISING_H
#define ISING_H

#include <iostream>
#include <array>
#include <vector>

using cords_t = std::array<int, 2>;
// spin_cnt: return count of UP, DOWN, UNKNOWN
using spin_cnt = std::array<int, 3>;

enum IsingSpin { UP = 1, DOWN = -1, UNKNOWN = 0 };

class Particle {
public:
    int idx;                // The unique ID of the particle in a lattice
    cords_t boxsize;        // The size of the lattice
    cords_t pos;            // The position of the particle in the lattice
    std::vector<int> neighbors;  // The idx of the neighboring particles
    Particle(int idx, cords_t boxsize);
    Particle() = default;
    ~Particle() = default;
    
    virtual std::vector<int>* getNeighbor() = 0;
    virtual IsingSpin getSpin() const = 0;
    virtual void setSpin(int s) = 0;
};

class IsingParticle : public Particle {
public:
    IsingSpin spin;
    
    IsingParticle(int idx, cords_t boxsize, IsingSpin spin = UP);
    IsingParticle() = default;
    ~IsingParticle() = default;
    std::vector<int>* getNeighbor() override;
    IsingSpin getSpin() const override { return spin; };
    void setSpin(int s) override {
        spin = static_cast<IsingSpin>(s);
    };
};

class FrustratedParticle : public Particle {
public:
    IsingSpin spin;

    // extra bool flag is_A to show if the lattice is A or B
    bool is_A = false;

    FrustratedParticle(int idx, cords_t boxsize, IsingSpin spin = UP);
    FrustratedParticle() = default;
    ~FrustratedParticle() = default;
    std::vector<int>* getNeighbor() override;
    IsingSpin getSpin() const override { return spin; }
    void setSpin(int s) override {
        spin = static_cast<IsingSpin>(s);
    };
};

class Lattice {
public:
    cords_t boxsize;

    Lattice(cords_t boxsize) : boxsize(boxsize) {};
    Lattice() = default;
    virtual ~Lattice() = default;

    virtual Particle* operator[](size_t idx) const = 0;
    virtual spin_cnt getNeighborCount(int idx) const = 0;
    virtual int getLocalEnergy(int idx) const = 0;
    virtual int getGlobalEnergy() const = 0;
    virtual int getGlobalMagnetization() const = 0;
    virtual void printLattice(std::ostream& os = std::cout) const = 0;
};

class IsingLattice : public Lattice {
public:
    std::vector<IsingParticle*> particles;

    IsingLattice(cords_t boxsize, IsingSpin initialSpin = UP);
    IsingLattice(const IsingLattice& other): Lattice(other.boxsize) {
        for (const auto& particle : other.particles) {
            particles.push_back(new IsingParticle(*particle));
        }
    };
    ~IsingLattice() override;
    Particle* operator[](size_t idx) const override;
    spin_cnt getNeighborCount(int idx) const override;
    int getLocalEnergy(int idx) const override;
    int getGlobalEnergy() const override;
    int getGlobalMagnetization() const override;
    void printLattice(std::ostream& os = std::cout) const override;
};

class FrustratedLattice : public Lattice {
public:
    std::vector<FrustratedParticle*> particles;

    FrustratedLattice(cords_t boxsize, IsingSpin initialSpin = UP);
    ~FrustratedLattice() override;
    Particle* operator[](size_t idx) const override;
    spin_cnt getNeighborCount(int idx) const override;
    int getLocalEnergy(int idx) const override;
    int getGlobalEnergy() const override;
    int getGlobalMagnetization() const override;
    void printLattice(std::ostream& os = std::cout) const override;
};

#endif