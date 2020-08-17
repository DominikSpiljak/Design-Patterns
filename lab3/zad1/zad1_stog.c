#include "myfactory.h"
#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

struct Animal{
    PTRFUN* vtable;
};

/* 
Template:
PTRFUN AnimalVTable[3] = {
  	(PTRFUN)getName,
	(PTRFUN)animalGreet,
	(PTRFUN)animalMenu
};
*/

void animalPrintGreeting(struct Animal *a){
    printf("%s pozdravlja: %s \n", a->vtable[0](a), a->vtable[1]());
}

void animalPrintMenu(struct Animal *a){
    printf("%s voli %s \n", a->vtable[0](a), a->vtable[2]());
}


int main(int argc, char *argv[]){
  	for (int i=1; i<argc; ++i){
		struct Animal* p = mystogfactory(argv[i], "Modrobradi");
		if (!p){
      		printf("Creation of plug-in object %s failed.\n", argv[i]);
      		continue;
    	}

    	animalPrintGreeting(p);
    	animalPrintMenu(p);
    	free(p); 
  	}
}
