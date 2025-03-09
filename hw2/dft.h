#ifndef DFT_H
#define DFT_H

#include<iostream>
#include<complex>
#include<cmath>

constexpr int MAX = 1 << 25;


void dft(std::complex<double>* x, int N, bool reverse);
void fft(std::complex<double>* x, int N, bool reverse);
void fftfast(std::complex<double>* x, int N, bool reverse);

#endif