#include <iostream>
#include <fstream>
#include <vector>
#include <deque>
#include <cstdlib>

using namespace std;

int n, num;

bool isLegal(const pair<int, int>& pos, const int length) {
    if (pos.first < 0 || pos.first >= n || pos.second < 0 || pos.second >= n) {
        return false;
    }
    return true;
}

vector<pair<int, int>> neighbors(const vector<pair<int, int>>& coors, const int length) {
    vector<pair<int, int>> res;
    for (auto& pos : coors) {
        vector<pair<int, int>> res_list = {
            {pos.first - 1, pos.second}, {pos.first + 1, pos.second},
            {pos.first, pos.second - 1}, {pos.first, pos.second + 1}
        };
        for (auto& i : res_list) {
            if (isLegal(i, length)) {
                res.push_back(i);
            }
        }
    }
    return res;
}

int depletion(vector<vector<int>>& dune, const pair<int, int>& init_coor) {
    int length = dune.size();
    deque<pair<int, int>> coors;
    coors.push_back(init_coor);
    int score = 0;
    while (!coors.empty()) {
        auto pos = coors.front();
        coors.pop_front();
        int row = pos.first, col = pos.second;
        if (dune[row][col] < 4) {
            continue;
        }
        dune[row][col] -= 4;
        score++;
        auto neighbor_coords = neighbors({pos}, length);
        for (auto& neighbor : neighbor_coords) {
            int r = neighbor.first, c = neighbor.second;
            dune[r][c] += 1;
        }
        coors.insert(coors.end(), neighbor_coords.begin(), neighbor_coords.end());
    }
    return score;
}

int iterate(vector<std::vector<int>>& dune) {
    int length = dune.size();
    int row = rand() % length;
    int col = rand() % length;
    dune[row][col] += 1;
    return depletion(dune, {row, col});
}


int main() {
    // srand(time(0));
    cin >> n >> num;
    vector<vector<int>> dune(n, vector<int>(n, 0));

    // output file
    fstream file;
    file.open("output.txt", ios::out);

    for (int i = 0; i < num; i++) {
        int score = iterate(dune);
        file << score << endl;
    }
    file.close();
    return 0;
}