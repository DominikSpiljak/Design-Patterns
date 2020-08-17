#include <stdio.h>
#include <stdlib.h>

class B{
    public:
        virtual int prva()=0;
        virtual int druga(int)=0;
};

class D: public B{
    public:
        virtual int prva(){return 42;}
        virtual int druga(int x){return prva()+x;}
};

void call_funcs(B* pb, int x){
    
    int* ptrToPb = (int*) pb;
    long int* pbVtablePtr = (long int*) ptrToPb[0];

    int (*pfun1)() = (int (*)()) pbVtablePtr[0];
    int (*pfun2)(B*, int) = (int (*)(B*, int)) pbVtablePtr[1];
    printf("prva = %d\n", pfun1());
    printf("druga = %d\n", pfun2(pb, x));
}

int main(void){
    B* pb = new D;  
    call_funcs(pb, 100);
    return 0;
}