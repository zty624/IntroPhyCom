#include <iostream>
#include <fstream>
#include <cstdlib>
#include <chrono>
#include <vector>
#include <array>
#include <cmath>

using namespace std;
// cords_t: 
// index: x, y, (0 for a, 1 for b)
using cords_t = array<int, 3>;
// lattice_t: 3D array, x, y -> value: -1 or 1, down or up
// pair.first: a; pair.second: b
using lattice_t = vector<vector<pair<int, int>>>;

// return a random number between min and max with step
inline int randint(int min, int max, int step = 1)
{
    return min + (rand() % ((max - min) / step + 1)) * step;
}

// return the value stored in the lattice_t by x, y, p form
inline int getValue(const lattice_t& lattice, int x, int y, int p)
{
    if (p == 0)
    {
        return lattice[x][y].first;
    }
    else if (p == 1)
    {
        return lattice[x][y].second;
    }
    else
    {
        cerr << "Error: p is not 0 or 1" << endl;
        exit(1);
    }
}

// return the value stored in the lattice_t by cords_t form
int getValue(const lattice_t& lattice, const cords_t& cord_t)
{
    return getValue(lattice, cord_t[0], cord_t[1], cord_t[2]);
}

// for a direction return the cords_t of the neighbor
cords_t getswapNeighbor(const cords_t& cord, int direction, int Boxsize)
{
    int x = cord[0];
    int y = cord[1];
    if (direction == 0)
    {
        return {x, y, 1};
    }
    else if (direction == 1)
    {
        return {(x - 1 + Boxsize) % Boxsize, y, 1};
    }
    else if (direction == 2)
    {
        return {(x - 1 + Boxsize) % Boxsize, (y - 1 + Boxsize) % Boxsize, 1};
    }
    else if (direction == 3)
    {
        return {x, (y - 1 + Boxsize) % Boxsize, 1};
    }
    else
    {
        cerr << "Error: direction is not 0-3" << endl;
        exit(1);
    }
}

// print lattice on the screen
void printLattice(const lattice_t& lattice, ostream& io = cout)
{
    int Boxsize = lattice.size();
    for (int i = 0; i < Boxsize; i++)
    {
        for (int j = 0; j < Boxsize; j++)
        {
            if (lattice[i][j].first == 1)
            {
                io << "+ ";
            }
            else 
            {
                io << "- ";
            }
            if (lattice[i][j].second == 1)
            {
                io << "+ ";
            }
            else 
            {
                io << "- ";
            }
        }
        io << "\n";
    }
}

// return the function of x, y, p for a lattice points
// p = 0 for lattice[x][y].first, p = 1 for lattice[x][y].second
vector<cords_t> getNeighbor(int x, int y, int p, int Boxsize)
{
    vector<cords_t> res = {};
    res.reserve(6); 
    if (p == 0)
    {
        res.push_back({x, y, 1});
        res.push_back({(x - 1 + Boxsize) % Boxsize, y, 1});
        res.push_back({(x - 1 + Boxsize) % Boxsize, (y - 1 + Boxsize) % Boxsize, 1});
        res.push_back({x, (y - 1 + Boxsize) % Boxsize, 1});
        res.push_back({(x - 1 + Boxsize) % Boxsize, y, 0});
        res.push_back({(x + 1) % Boxsize, y, 0});
    }
    else 
    {
        res.push_back({x, y, 0});
        res.push_back({x, (y + 1) % Boxsize, 0});
        res.push_back({(x + 1) % Boxsize, (y + 1) % Boxsize, 0});
        res.push_back({(x + 1) % Boxsize, y, 0});
        res.push_back({x, (y - 1 + Boxsize) % Boxsize, 1});
        res.push_back({x, (y + 1) % Boxsize, 1});
    };
    return res;
}

// swap two spins on the lattice
void swapSpin(lattice_t& lattice, cords_t cord, cords_t cord2)
{
    if (cord[2] == 0 && cord2[2] == 1)
    {
        swap(lattice[cord[0]][cord[1]].first, lattice[cord2[0]][cord2[1]].second);
    }
    else if (cord[2] == 0 && cord2[2] == 0)
    {
        swap(lattice[cord[0]][cord[1]].first, lattice[cord2[0]][cord2[1]].first);
    }
    else if (cord[2] == 1 && cord2[2] == 0)
    {
        swap(lattice[cord[0]][cord[1]].second, lattice[cord2[0]][cord2[1]].first);
    }
    else if (cord[2] == 1 && cord2[2] == 1)
    {
        swap(lattice[cord[0]][cord[1]].second, lattice[cord2[0]][cord2[1]].second);
    }
    else
    {
        cerr << "Error: p is not 0 or 1" << endl;
        exit(1);
    }
}

// get the local energy around the lattice[x][y][p]
int getLocalEnergy(const lattice_t& lattice, const cords_t& cord)
{
    int Boxsize = lattice.size();
    vector<cords_t> neighbors = getNeighbor(cord[0], cord[1], cord[2], Boxsize);
    int energy = 0;
    int selfEnergy = getValue(lattice, cord);
    for (auto& neighbor : neighbors)
    {
        energy += getValue(lattice, neighbor) * selfEnergy;
    }
    return energy;
}

int getGlobalEnergy(const lattice_t& lattice)
{
    int Boxsize = lattice.size();
    int energy = 0;
    for (int i = 0; i < Boxsize; i++)
    {
        for (int j = 0; j < Boxsize; j++)
        {
            energy += getLocalEnergy(lattice, {i, j, 0});
            energy += getLocalEnergy(lattice, {i, j, 1});
        }
    }
    return energy;
}

int getsum(const lattice_t& lattice)
{
    int Boxsize = lattice.size();
    int sum = 0;
    for (int i = 0; i < Boxsize; i++)
    {
        for (int j = 0; j < Boxsize; j++)
        {
            sum += getValue(lattice, {i, j, 0});
            sum += getValue(lattice, {i, j, 1});
        }
    }
    return sum;
}

// for a random given lattice point, give a random neighbor and conduct the Metropolis Algorithm.
// beta: the probability of the spin flip while deltaE > 0
void markovTransfer(lattice_t& lattice, int x, int y, int p, double beta, double temp=1.0)
{
    int Boxsize = lattice.size();
    int direction = randint(0, 3);
    cords_t swapNeighbor = getswapNeighbor({x, y, p}, direction, Boxsize);

    // calculate energy and decision logic
    int energyOld = 0, energyNew = 0;
    energyOld += getLocalEnergy(lattice, {x, y, p});
    energyOld += getLocalEnergy(lattice, swapNeighbor);
    swapSpin(lattice, {x, y, p}, swapNeighbor);
    energyNew += getLocalEnergy(lattice, {x, y, p});
    energyNew += getLocalEnergy(lattice, swapNeighbor);

    int deltaE = energyNew - energyOld;
    double prob = exp(-beta * deltaE / temp);
    double randNum = static_cast<double>(rand()) / RAND_MAX;
    if (randNum > prob)
    {
        swapSpin(lattice, {x, y, p}, swapNeighbor);
    }
}

int main(int argc, char* argv[])
{
    int boxsize;
    int numsize;
    int iteratenum;
    double beta;
    int noise;
    if (argc != 6)
    {
        cerr << "Usage: " << argv[0] << " [Boxsize] [Numsize] [Iteratenum] [beta] [noise]" << endl;
        cin >> boxsize >> numsize >> iteratenum >> beta >> noise;
    }
    else
    {
        boxsize     = atoi(argv[1]);
        numsize     = atoi(argv[2]);
        iteratenum  = atoi(argv[3]);
        beta     = atof(argv[4]);
        noise       = atoi(argv[5]);
    }

    vector<lattice_t> lattice_ensemble (numsize,        // create lattice ensemble
        lattice_t(boxsize, vector<pair<int, int>>(boxsize, {1, -1})));
    int minE = getGlobalEnergy(lattice_ensemble[0]);
    vector<int> lattice_E (numsize, 0);              // create reach minE flags list

    // printLattice(lattice_ensemble[0]);
    cout << "Minimun Energy: " << minE << endl;

    // initial disturb the lattice
    for (int i = 0; i < numsize; i++)
    {
        for (int j = 0; j < noise; j++)
        {
            int x = randint(0, boxsize - 1);
            int y = randint(0, boxsize - 1);
            auto swapNeighbor = getswapNeighbor({x, y, 0}, randint(0, 3), boxsize);
            swapSpin(lattice_ensemble[i], {x, y, 0}, swapNeighbor);
        }
    }
    cout << "Initial disturb done!" << endl;

    auto start = chrono::high_resolution_clock::now();
    int processNum = 0;
    for (int i = 0; i < iteratenum; i++)
    {
        for (int j = 0; j < numsize; j++)
        {
            int x = randint(0, boxsize - 1);
            int y = randint(0, boxsize - 1);
            markovTransfer(lattice_ensemble[j], x, y, 0, beta);
        }
        // flush a process bar
        if (i * 100 / iteratenum > processNum)
        {
            processNum = i * 100 / iteratenum;
            cout << "\r" << "Process: " << processNum << "%";
            cout.flush();
        }
    }
    cout << "\n";
    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
    cout << "Time taken: " << duration.count() / 1000.0 << " seconds" << endl;

    // print the final state of the lattice ensemble
    string filename = "lattice_" + to_string(boxsize) + "_" + to_string(numsize) + "_"
                    + to_string(iteratenum) + "_" + to_string(beta) + ".txt";
    fstream io(filename, ios::out);
    if (!io)
    {
        cerr << "Error: Cannot open file " << filename << endl;
        return 1;
    }
    for (int i = 0; i < numsize; i++)
    {
        int energy = getGlobalEnergy(lattice_ensemble[i]);
        if (energy <= minE)
        {
            printLattice(lattice_ensemble[i], io);
            io << energy << "\n\n";
        }
        if (energy < minE)
        {
            cout << "Found a new minimum energy: " << energy << endl;
            printLattice(lattice_ensemble[i]);
        }
        if (getsum(lattice_ensemble[i]) != 0)
        {
            cout << "Found error at " << i << endl;
        }
    }
    io.close();
    return 0;
}