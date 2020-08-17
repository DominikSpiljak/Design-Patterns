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
    struct Animal* p = malloc((argc - 1) * sizeof(struct Animal));
  	for (int i=1; i<argc; ++i){
		mypredefinedfactory(&p[i], argv[i], "Modrobradi");
    	animalPrintGreeting(&p[i]);
    	animalPrintMenu(&p[i]); 
  	}
    free(p);
}
