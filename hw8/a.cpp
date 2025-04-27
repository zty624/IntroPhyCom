#include <iostream>
#include <random>

#include "../ising/ising.h"

using namespace std;

random_device rd;
mt19937 gen{rd()};

int uniform_int(int min, int max)
{
    uniform_int_distribution<> dist(min, max);
    return dist(gen);
}

double uniform_real(double min = 0.0, double max = 1.0)
{
    uniform_real_distribution<> dist(min, max);
    return dist(gen);
}

bool bernoulli(double p = 0.5)
{
    bernoulli_distribution dist(p);
    return dist(gen);
}

vector<IsingLattice>& init_ensemble(vector<IsingLattice>& ensemble, int boxsize, int num_ensembles) {
    ensemble.reserve(num_ensembles);
    for (int i = 0; i < num_ensembles; ++i) {
        ensemble.push_back(IsingLattice({boxsize, boxsize}));
        for (int j = 0; j < boxsize * boxsize; ++j) {
            IsingSpin spin = bernoulli() ? UP : DOWN;
            ensemble[i].particles[j]->spin = spin;
        }
    }
    return ensemble;
}

// Metropolis algorithm
// return 1 while flip is rejected, return 0 while flip is accepted
int mortecarlo(IsingLattice& lattice, cords_t boxsize, double beta)
{
    const int total_particles = boxsize[0] * boxsize[1];
    const int particle_idx = uniform_int(0, total_particles - 1);
    const int localE = lattice.getLocalEnergy(particle_idx);
    const int deltaE = -2 * localE;
    if (deltaE > 0 && uniform_real() > exp(-beta * deltaE)) {
        return 1; // Reject the move
    }
    auto& particle = *lattice.particles[particle_idx];
    particle.setSpin(particle.getSpin() == UP ? DOWN : UP);
    return 0;
}

int main(int argc, char* argv[]) {
    int boxsize, num_ensembles, total_steps;
    double beta;
    if (argc == 5) {
        boxsize = atoi(argv[1]);
        num_ensembles = atoi(argv[2]);
        total_steps = atoi(argv[3]);
        beta = atof(argv[4]);
    } else {
        cout << "Usage: " << argv[0] << " <boxsize> <num_ensembles> <total_steps> <beta>\n";
        cin >> boxsize >> num_ensembles >> total_steps >> beta;
    }

    cords_t dimensions{boxsize, boxsize};
    // const int sample_interval = 2;
    // const int max_samples = 500000;
    const int sample_interval = 10;
    const int max_samples = 100;
    const int warmup_steps = total_steps - sample_interval * max_samples - 1;

    vector<IsingLattice> ensemble;
    init_ensemble(ensemble, boxsize, num_ensembles);

    long long m_mean = 0, e_mean = 0, m2_mean = 0, e2_mean = 0;

    for (auto& lattice : ensemble) {
        int steps_count = 0;
        int samples_count = 0;
        while (steps_count < total_steps) {
            mortecarlo(lattice, dimensions, beta);
            steps_count++;
            // 采样数据
            if (steps_count > warmup_steps && 
                steps_count % sample_interval == 0 &&
                samples_count < max_samples) {

                // get energy and magnetization
                const int energy = lattice.getGlobalEnergy();
                const int magnet = lattice.getGlobalMagnetization();
                m_mean += magnet;
                e_mean += energy;
                m2_mean += magnet * magnet;
                e2_mean += energy * energy;
                cout << samples_count 
                     << " " << steps_count
                     << " " << boxsize
                     << " " << energy 
                     << " " << magnet
                     << "\n";

                // 输出自旋
                // for (int row = 0; row < boxsize; ++row) {
                //     for (int col = 0; col < boxsize; ++col) {
                //         const auto& p = dynamic_cast<IsingParticle&>(
                //             *lattice[row * boxsize + col]);
                //         cout << (p.spin == UP ? "1" : "-1") << " ";
                //     }
                //     cout << "\n";
                // }
                // cout << "\n";
                ++samples_count;
            }
        }
    }
    // calculate mean values
    m_mean /= (num_ensembles * max_samples);
    e_mean /= (num_ensembles * max_samples);

    bool check = 1 == UP;
    
    cout << check << true;


    return 0;
}