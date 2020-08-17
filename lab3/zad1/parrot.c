#include <stdlib.h>
#include <malloc.h>

typedef struct Animal* (*FUNPTR)(char const*);
typedef char const* (*PTRFUN)();

struct Parrot {
	PTRFUN *vtable;
	char const* name;
};

char const* parrotGreet(void){
  	return "Sto mu gromova!";
}
char const* parrotMenu(void){
  	return "brazilske orahe.";
}

char const* parrotName(void* this){
    return ((struct Parrot*)this)->name;
}

PTRFUN ParrotVtable[3] = {
    (PTRFUN) parrotName,
    (PTRFUN) parrotGreet,
    (PTRFUN) parrotMenu
};

void* create(char const* name){
    struct Parrot* parrot = malloc(sizeof(struct Parrot));
    parrot->name = name;
    parrot->vtable = ParrotVtable;
    return parrot;
}

struct Parrot* create_on_stog(char const* name){
	struct Parrot* parrot = alloca(sizeof(struct Parrot));
    parrot->name = name;
    parrot->vtable = ParrotVtable;
    return parrot;
}

void create_on_predefined_mem(struct Animal* parrot, char const* name){
    ((struct Parrot *)parrot)->name = name;
    ((struct Parrot *)parrot)->vtable = ParrotVtable;
}