#include <iostream>
#include <cmath>

#include "../ising/ising.h"

using namespace std;

int L;
int minEcount = 0; // count of minimum energy

bool judge(int selfspin, spin_cnt count)
{
    switch (selfspin)
    {
    case UP:
        if (count[0] <= 2)
            return true;
        else
            return false;
    case DOWN:
        if (count[1] <= 2)
            return true;
        else
            return false;
    }
}

// dfs recursion core to find the ground state.
// which satisfies that any triangle has 2 up and 1 down or 2 down and 1 up
void dfs(FrustratedLattice& lattice, int idx, int depth, int& best_energy)
{
    if (depth == lattice.boxsize[0] * lattice.boxsize[1])
    {
        int energy = lattice.getGlobalEnergy();
        if (energy <= best_energy)
        {
            lattice.printLattice();
            cout << energy << endl;
            minEcount++;
        }
        return;
    }
    // Try to set the spin of the current particle to UP
    lattice[idx]->setSpin(UP);
    // Check if the current state is valid (local energy < 0)
    if (judge(UP, lattice.getNeighborCount(idx)))
    {
        // Continue to the next particle
        dfs(lattice, idx + 1, depth + 1, best_energy);
    }
    // Try to set the spin of the current particle to DOWN
    lattice[idx]->setSpin(DOWN);
    // Check if the current state is valid (local energy < 0)
    if (judge(DOWN, lattice.getNeighborCount(idx)))
    {
        // Continue to the next particle
        dfs(lattice, idx + 1, depth + 1, best_energy);
    }
    // Backtrack: reset the spin of the current particle
    lattice[idx]->setSpin(UNKNOWN);
    return;
}

int main(int argc, char* argv[])
{
    if (argc == 2)
    {
        L = atoi(argv[1]);
    }
    else
    {
        cout << "Usage: " << argv[0] << " <L>\n";
        cin >> L;
    }
    cords_t boxsize{L, 2 * L};
    FrustratedLattice lattice(boxsize, UNKNOWN);

    int best_energy = - 2 * L * L;

    dfs(lattice, 0, 0, best_energy);

    cout << "\nMinimum energy count: " << minEcount << "\n";
    
    return 0;
}