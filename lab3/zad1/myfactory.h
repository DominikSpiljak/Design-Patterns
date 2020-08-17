typedef struct Animal* (*FUNPTR)(char const*);
void* myfactory(char const* libname, char const* ctorarg);
void* mystogfactory(char const* libname, char const* ctorarg);
void mypredefinedfactory(struct Animal*, char const* libname, char const* ctorarg);