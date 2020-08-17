#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include "myfactory.h"


typedef struct Animal* (*FUNPTR)(char const*);
typedef void (*PFUNPTR)(struct Animal*, char const*);

void *myfactory(char const* libname, char const* ctorarg) {
	void *file_handle;
	char *error;
	FUNPTR create;

	file_handle = dlopen(libname, RTLD_LAZY);


	create = (FUNPTR)dlsym(file_handle, "create");

	return create(ctorarg);
}

void *mystogfactory(char const* libname, char const* ctorarg) {
	void *file_handle;
	char *error;
	FUNPTR create_on_stog;

	file_handle = dlopen(libname, RTLD_LAZY);

	create_on_stog = (FUNPTR)dlsym(file_handle, "create_on_stog");

	return create_on_stog(ctorarg);
}

void mypredefinedfactory(struct Animal* a, char const* libname, char const* ctorarg) {
	void *file_handle;
	char *error;
	PFUNPTR create_on_predefined_mem;

	file_handle = dlopen(libname, RTLD_LAZY);

	create_on_predefined_mem = (PFUNPTR)dlsym(file_handle, "create_on_predefined_mem");

	create_on_predefined_mem(a, ctorarg);
}