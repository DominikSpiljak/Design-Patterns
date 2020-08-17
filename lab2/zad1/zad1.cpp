#include <iostream>
#include <stdlib.h>
#include <string.h>

const void* mymax(void *base, size_t nitems, size_t size, int (*compar)(const void *, const void*)){
    void* max;
    for(size_t i=0; i < nitems * size; i += size){
        void* obj = (base + i);
        if (i == 0){
            max = obj;
        }
        else{
            if(compar(obj, max) > 0){
                max = obj;
            }
        }
    }
    return max;
}
int gt_int(const void * first, const void * second){
    return *(int *)first - *(int *)second;
}
int gt_char(const void * first, const void * second){
    return *(char*)first - *(char*)second;
}
int gt_string(const void * first, const void * second){
    return strcmp(*(char**)first, *(char**)second);
}
int main(){
    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    char arr_char[]="Suncana strana ulice";
    const char* arr_str[] = {
    "Gle", "malu", "vocku", "poslije", "kise",
    "Puna", "je", "kapi", "pa", "ih", "njise"
    };
    std::cout << "Max: " << *(const int *)mymax(arr_int, sizeof(arr_int)/sizeof(arr_int[0]), sizeof(int), gt_int) << "\n";
    std::cout << "Max: " << *(const char *)mymax(arr_char, sizeof(arr_char)/sizeof(arr_char[0]), sizeof(char), gt_char) << "\n";
    std::cout << "Max: " << *(const char**)mymax(arr_str, sizeof(arr_str)/sizeof(arr_str[0]), sizeof(char*), gt_string) << "\n";
}
