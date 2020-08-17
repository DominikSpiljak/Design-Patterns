#include <stdlib.h>
#include <malloc.h>

typedef struct Animal* (*FUNPTR)(char const*);
typedef char const* (*PTRFUN)();

struct Tiger {
	PTRFUN *vtable;
	char const* name;
};

char const* tigerGreet(void){
	return "Mijau!";
}
char const* tigerMenu(void){
	return "mlako mlijeko.";
}

char const* tigerName(void* this){
    return ((struct Tiger*)this)->name;
}

PTRFUN TigerVtable[3] = {
    (PTRFUN) tigerName,
    (PTRFUN) tigerGreet,
    (PTRFUN) tigerMenu
};

void* create(char const* name){
    struct Tiger* tiger = malloc(sizeof(struct Tiger));
    tiger->name = name;
    tiger->vtable = TigerVtable;
    return tiger;
}

struct Tiger* create_on_stog(char const* name){
    struct Tiger* tiger = alloca(sizeof(struct Tiger));
    tiger->name = name;
    tiger->vtable = TigerVtable;
    return tiger;
}

void create_on_predefined_mem(struct Animal* tiger, char const* name){
    ((struct Tiger *)tiger)->name = name;
    ((struct Tiger *)tiger)->vtable = TigerVtable;
}