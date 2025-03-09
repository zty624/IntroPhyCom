#include<iostream>
#include<fstream>
#include<cmath>
#include<chrono>
#include "dft.h"

using namespace std;


complex<double> samples[MAX], samplescheck[MAX];

class Timer {
private:
    chrono::time_point<chrono::high_resolution_clock> start;
public:
    Timer() : start(chrono::high_resolution_clock::now()) {}
    void reset() {
        start = chrono::high_resolution_clock::now();
    }
    double elapsed() const {
        return chrono::duration<double>(chrono::high_resolution_clock::now() - start).count();
    }
};


int main() {
    Timer timer;
    double fffttimes[100], fffterrors[100];
    double ffttimes[100], ffterrors[100];
    int l_min = 5, l_max = 24;
    for (int len = l_min; len <= l_max; len++)
    {
        int n = 1 << len;
        cout << n << "\n";
        for (int i = 0; i < n; i++) {
            double re = rand() % 1000 / 1000.0;
            samples[i] = complex<double>(re, 0);
            samplescheck[i] = complex<double>(re, 0);
        }

        timer.reset();
        fftfast(samples, n, false);
        double fft_time = timer.elapsed();
        timer.reset();
        fftfast(samples, n, true);
        double ifft_time = timer.elapsed();
        fffttimes[len] = fft_time + ifft_time;
        double error = 0;
        for (int i = 0; i < n; i++) {
            error += abs(samples[i] - samplescheck[i]);
        }
        fffterrors[len] = error;

        timer.reset();
        fft(samples, n, false);
        fft_time = timer.elapsed();
        timer.reset();
        fftfast(samples, n, true);
        ifft_time = timer.elapsed();
        ffttimes[len] = fft_time + ifft_time;
        error = 0;
        for (int i = 0; i < n; i++) {
            error += abs(samples[i] - samplescheck[i]);
        }
        ffterrors[len] = error;
    }

    ofstream outfile("fft_results.txt");
    for (int len = l_min; len <= l_max; len++) {
        int n = 1 << len;
        outfile << n << "\t" << ffttimes[len] << "\t" << ffterrors[len] << "\t" << fffttimes[len] << "\t" << fffterrors[len] << "\n";
    }
    outfile.close();

    return 0;
}