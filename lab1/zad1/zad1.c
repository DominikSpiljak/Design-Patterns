#include <stdlib.h>
#include <stdio.h>

struct greet_v_table{
    const char* (*greet)();
};
struct menu_v_table{
    const char* (*menu)();
};

struct Animal{
    char const* name;
    struct greet_v_table greet_table;
    struct menu_v_table menu_table;
};

char const* dogGreet(void){
  return "vau!";
}

char const* dogMenu(void){
  return "kuhanu govedinu";
}

char const* catGreet(void){
  return "mijau!";
}

char const* catMenu(void){
  return "konzerviranu tunjevinu";
}

void constructDog(struct Animal* a, char const* name){
    a->name = name;
    a->greet_table.greet = &dogGreet;
    a->menu_table.menu = &dogMenu;
}

void constructCat(struct Animal* a, char const* name){
    a->name = name;
    a->greet_table.greet = &catGreet;
    a->menu_table.menu = &catMenu;
}

struct Animal* createDog(char const* name){
    struct Animal* a = (struct Animal*) malloc(sizeof(struct Animal));
    constructDog(a, name);
    return a;
}

struct Animal* createCat(char const* name){
    struct Animal* a = (struct Animal*) malloc(sizeof(struct Animal));
    constructCat(a, name);
    return a;
}

void animalPrintGreeting(struct Animal *a){
    printf("%s pozdravlja: %s \n", a->name, a->greet_table.greet());
}

void animalPrintMenu(struct Animal *a){
    printf("%s voli %s \n", a->name, a->menu_table.menu());
}

void testAnimals(void){
    struct Animal* p1=createDog("Hamlet");
    struct Animal* p2=createCat("Ofelija");
    struct Animal* p3=createDog("Polonije");

    animalPrintGreeting(p1);
    animalPrintGreeting(p2);
    animalPrintGreeting(p3);

    animalPrintMenu(p1);
    animalPrintMenu(p2);
    animalPrintMenu(p3);

    free(p1); free(p2); free(p3);
}

int main(void){
    testAnimals();
    return 0;
}
