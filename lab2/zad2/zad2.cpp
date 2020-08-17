#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <vector> 
#include <list>

template <typename Iterator, typename Predicate>
Iterator mymax(Iterator first, Iterator last, Predicate pred){
    Iterator max = first;
    while (first!=last) {
        if (pred(*first, *max) > 0){
            max = first;
        }
        ++first;
    }
    return max;
}

int gt_int(int first, int second){
    return first - second;
}
int gt_char(char first, char second){
    return first - second;
}
int gt_string(const char * first, const char * second){
    return strcmp(first, second);
}

int main(){
    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    char arr_char[]="Suncana strana ulice";
    const char* arr_str[] = {
    "Gle", "malu", "vocku", "poslije", "kise",
    "Puna", "je", "kapi", "pa", "ih", "njise"
    };
    std::vector<int> arr_vector{ 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    std::list<const char*> arr_list{
    "Gle", "malu", "vocku", "poslije", "kise",
    "Puna", "je", "kapi", "pa", "ih", "njise"};

    const int* maxint = mymax( &arr_int[0], &arr_int[sizeof(arr_int)/sizeof(*arr_int)], gt_int);
    const char* maxchar = mymax( &arr_char[0], &arr_char[sizeof(arr_char)/sizeof(*arr_char)], gt_char);
    const char** maxstr = mymax( &arr_str[0], &arr_str[sizeof(arr_str)/sizeof(*arr_str)], gt_string);
    std::vector<int>::iterator maxvec = mymax(arr_vector.begin(), arr_vector.end(), gt_int);
    std::list<const char*>::iterator maxlist = mymax(arr_list.begin(), arr_list.end(), gt_string);

    std::cout <<*maxint <<"\n";
    std::cout <<*maxchar <<"\n";
    std::cout <<*maxstr <<"\n";
    std::cout <<*maxvec <<"\n";
    std::cout <<*maxlist <<"\n";
}