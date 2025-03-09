#include <iostream>
#include <complex>
#include <cmath>
#include "complex.h"

constexpr int MAX = 1 << 25;
constexpr double PI = 3.14159265358979323846;

std::complex<double> tmp[MAX];
int index[MAX];

void dft(std::complex<double>* x, int N, bool reverse)
{
    std::complex<double>* res = new std::complex<double>[N];
    int sign = reverse ? -1 : 1;
    for (int i = 0; i < N; i++)
    {
        res[i] = std::complex<double> (0, 0);
        for (int j = 0; j < N; j++)
        {
            res[i] += x[j] * std::complex<double> (cos(2 * sign * PI * i * j / N), sin(2 * sign * PI * i * j / N));
        }
        res[i] /= sqrt(N);
    }
    for (int i = 0; i < N; i++) x[i] = res[i];
    delete[] res;
};

void fft(std::complex<double>* x, int N, bool reverse=false)
{
    if (N == 1)
    {
        return;
    }
    int sign = reverse ? -1 : 1; 
    for (int i = 0; i < N; i++) 
    {
        tmp[i] = x[i];
    }
    for (int i = 0; i < N; i++)
    {
        if (i & 1) x[N / 2 + i / 2] = tmp[i];
        else x[i / 2] = tmp[i];
    }
    std::complex<double>* l_ptr = x, *r_ptr = x + N / 2;
    fft(l_ptr, N / 2, reverse);
    fft(r_ptr, N / 2, reverse);
    std::complex<double> cur(1, 0), step(cos(2 * sign * PI / N), sin(2 * sign * PI / N));
    for (int i = 0; i < N / 2; i++)
    {
        tmp[i] = l_ptr[i] + cur * r_ptr[i];
        tmp[i + N / 2] = l_ptr[i] - cur * r_ptr[i];
        cur *= step;
    }
    for (int i = 0; i < N; i++) x[i] = tmp[i];
}

void fftfast(std::complex<double>* x, int N, bool reverse=false)
{
    int sign = reverse ? -1 : 1;
    // swap index
    for (int i = 1; i < N; i++)
    {
        index[i] = index[i >> 1] >> 1 | ((i & 1) * N / 2);
    }
    for (int i = 0; i < N; i++)
    {
        tmp[i] = x[index[i]];
    }
    // fft
    for (int bin = 2; bin <= N; bin <<= 1)
    {
        std::complex<double> wi_0(std::cos(2 * PI / bin), std::sin(2 * sign * PI / bin));

        for (int step = 0; step < N; step += bin)
        {
            std::complex<double> w(1, 0);
            for (int i = step; i < step + bin / 2; i++)
            {
                std::complex<double> j0 = tmp[i + bin / 2] * w, k0 = tmp[i];
                tmp[i] += j0;
                tmp[i + bin / 2] = k0 - j0;
                w *= wi_0;
            }
        }
    }
    for (int i = 0; i < N; i++)
    {
        x[i] = tmp[i] / std::sqrt(N);
    }
}