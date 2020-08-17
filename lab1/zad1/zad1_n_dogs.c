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

struct Animal* createNDogs(const char* names[], int n){
    struct Animal* a = malloc(n * sizeof(struct Animal));
    for(int i = 0; i < n; i++){
        constructDog(&a[i], names[i]);
    }
    return a;
}

void testAnimals(void){
    const char* names[] = {"Hamlet", "Ofelija", "Polonije"};

    struct Animal* p = createNDogs(names, 3);

    for(int i = 0; i < 3; i++){
        animalPrintGreeting(&p[i]);
        animalPrintMenu(&p[i]);
    }

    free(p);
}

int main(void){
    testAnimals();
    return 0;
}
