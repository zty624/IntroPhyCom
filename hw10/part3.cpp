#include <iostream>
#include <vector>
#include <random>
#include <future>
#include <cmath>
#include <algorithm>
#include <chrono>

using namespace std;

double corr(const vector<int>& u, const vector<int>& v) {
    double sum = 0.0;
    for (size_t i = 0; i < u.size(); ++i) {
        sum += u[i] * v[i];
    }
    return abs(sum / u.size());
}

vector<int> add_noise(const vector<int>& v, double delta, mt19937& gen) {
    uniform_real_distribution<> dis(0.0, 1.0);
    bernoulli_distribution bern(0.5);
    vector<int> noisy_v;
    noisy_v.reserve(v.size());
    for (int vi : v) {
        if (dis(gen) < delta) {
            noisy_v.push_back(bern(gen) ? 1 : -1);
        } else {
            noisy_v.push_back(vi);
        }
    }
    return noisy_v;
}

bool metropolis(vector<int>& spin, int spin_idx, 
               const vector<vector<double>>& Js_mat, 
               double beta, mt19937& gen) {
    double sum = 0.0;
    for (size_t k = 0; k < Js_mat[spin_idx].size(); ++k) {
        sum += Js_mat[spin_idx][k] * spin[k];
    }
    double delta_E = 2 * spin[spin_idx] * sum;

    uniform_real_distribution<> prob_dis(0.0, 1.0);
    if (delta_E <= 0 || prob_dis(gen) < exp(-beta * delta_E)) {
        spin[spin_idx] *= -1;
        return true;
    }
    return false;
}

struct InitResult {
    vector<vector<double>> Js_mat;
    vector<vector<int>> sp_mat;
    vector<vector<int>> ss_mat;
};

InitResult init(int PtNum, int SpNum, double delta) {
    InitResult res;
    random_device rd;
    mt19937 gen(rd());
    bernoulli_distribution bern(0.5);

    res.sp_mat.resize(SpNum, vector<int>(PtNum));
    for (auto& row : res.sp_mat) {
        for (auto& val : row) {
            val = bern(gen) ? 1 : -1;
        }
    }
    res.Js_mat.assign(PtNum, vector<double>(PtNum, 0.0));
    for (const auto& s : res.sp_mat) {
        for (int j = 0; j < PtNum; ++j) {
            for (int k = 0; k < PtNum; ++k) {
                res.Js_mat[j][k] += s[j] * s[k];
            }
        }
    }
    for (auto& row : res.Js_mat) {
        for (auto& val : row) {
            val /= SpNum;
        }
    }
    for (int i = 0; i < PtNum; ++i) {
        res.Js_mat[i][i] = 0.0;
    }
    for (const auto& row : res.sp_mat) {
        res.ss_mat.push_back(add_noise(row, delta, gen));
    }

    return res;
}

struct Result {
    int p;
    vector<double> corrs;
};

Result simulate_p(int p, int PtNum = 2000, 
                 int num_samples = 50, int num_steps = 50000) {
    Result res;
    res.p = p;
    
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> idx_dis(0, PtNum-1);

    for (int sample = 0; sample < num_samples; ++sample) {
        auto init_data = init(PtNum, p, 0.5);
        auto& ss_mat = init_data.ss_mat;

        for (int step = 0; step < num_steps; ++step) {
            for (int j = 0; j < p; ++j) {
                int idx = idx_dis(gen);
                metropolis(ss_mat[j], idx, init_data.Js_mat, 1e5, gen);
            }
        }

        for (int i = 0; i < p; ++i) {
            res.corrs.push_back(corr(ss_mat[i], init_data.sp_mat[i]));
        }
    }
    return res;
}

int main() {
    vector<int> p_values = {200, 260, 270, 272, 274, 276, 278, 280, 290};
    vector<future<Result>> futures;

    // 启动并行任务
    for (int p : p_values) {
        futures.emplace_back(async(launch::async, [p]() { return simulate_p(p); }));
    }

    // 收集结果
    vector<Result> results;
    for (auto& f : futures) {
        results.push_back(f.get());
    }

    // 输出统计信息
    for (const auto& res : results) {
        double sum = accumulate(res.corrs.begin(), res.corrs.end(), 0.0);
        cout << "p = " << res.p << "\n";
        for (int i = 0; i < res.corrs.size(); ++i) {
            cout << res.corrs[i] << "\n";
        }
    }

    return 0;
}