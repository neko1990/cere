#include <stdlib.h>
#include <stdio.h>

void dump();
void* load();

int a[10] = {0,1,2,3,4,5,6,7,8,9};

void initialize(int * a, int n) {
    int i;
    for (i=0; i<n; i++) {
        a[i] = i;
    }
}

int codelet(int *a, int n) {
    int sum = 0;
    int i;
    for (i=0; i<n; i++) {
        sum += a[i];
    }

    return sum;
}

int main(int argc, char* argv[]) {

    int mode = 0;
    int n = sizeof(a)/sizeof(int);
    int sum;

    if (argc != 2) {
        printf("usage: %s 0/1/2 # 0 (normal) 1 (dump) 2 (replay)\n", argv[0]); 
        exit(1);
    } else {
        mode = atoi(argv[1]);
    }
    
    initialize(a, n);

    if (mode == 1) {
        // Dump mode
        dump("mainloop", 2, a, &n);
    } 

    if (mode == 2) {
        // Replay mode
        void * args[2];
        load("mainloop", 2, args);
        sum = codelet((int*)args[0], *((int*)args[1]));
    } else {
        sum = codelet(a, n);
    }

    printf("Checksum = %d\n", sum);
    return 0;
}
