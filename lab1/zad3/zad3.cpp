#include <stdio.h>
#include <stdlib.h>

class CoolClass{
    public:
        virtual void set(int x){x_=x;};
        virtual int get(){return x_;};
    private:
        int x_;
};

class PlainOldClass{
    public:
        void set(int x){x_=x;};
        int get(){return x_;};
    private:
        int x_;
};

int main(void){
    printf("Size of CoolClass: %d\nSize of PlainOldClass: %d\n", sizeof(CoolClass), sizeof(PlainOldClass));
    return 0;
}