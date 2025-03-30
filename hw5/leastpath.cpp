#include <iostream>
#include <vector>
#include <cstdlib>
using namespace std;

int leastPath(int n) {
    double **heap = new double*[n];
    for (int i = 0; i < n; i++) {
        heap[i] = new double[i + 1] {0};
    }
    int **path = new int*[n - 1];
    for (int i = 0; i < n - 1; i++) {
        path[i] = new int[i + 1] {0};
    }
    for (int i = n - 1; i > 0; i--) {
        for (int j = 0; j <= i; j++) {
            heap[i][j] += (rand() % 100) / 100.0;
            if (j > 0) {
                if (heap[i][j] > heap[i][j-1]) {
                    path[i-1][j-1] = 0;
                    heap[i-1][j-1] += heap[i][j-1];
                }
                else {
                    path[i-1][j-1] = 1;
                    heap[i-1][j-1] += heap[i][j];
                }
            }
        }
    }

    int res = 0;
    for(int i = 0; i < n - 1; i++){
        res += path[i][res];
    }

    for (int i = 0; i < n - 1; i++) {
        delete[] heap[i];
        delete[] path[i];
    }
    delete[] heap[n - 1];
    delete[] heap;
    delete[] path;
    return res;
}

int main(){
    int n;
    while (cin >> n) {
        cout << leastPath(n) << endl;
    }
    return 0;
}
