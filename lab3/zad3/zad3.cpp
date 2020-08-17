#include <stdlib.h>
#include <stdio.h>
#include <memory>
#include <iostream>
#include <assert.h>

int main(void){
    int test_number;
    std::cout << "Input number of test:\n\t1) std::unique_ptr test\n\t2) std::shared_ptr/std::weak_ptr test\n\t";
    std::cin >> test_number;
    if (test_number == 1){
        std::cout << "Starting test 1\n";
        int* ptr = new int(5);
        std::unique_ptr<int> uptr(ptr);
        std::cout << "Initialized unique pointer uptr with int object\n";
        std::cout << "Initializing another unique pointer with the same object (this is expected to fail)\n";
        std::unique_ptr<int> uptr2(ptr);
    }
    else if (test_number == 2){
        std::cout << "Starting test 2\n";
        std::shared_ptr<int> sptr = std::make_shared<int>(5);
        std::cout << "Initialized shared pointer sptr with int object\n";
        std::weak_ptr<int> wptr {sptr};
        std::cout << "Initialized weak pointer wptr with shared pointer sptr\n";
        sptr.reset();
        std::cout << "Reset sptr\n";
        std::cout << "wptr " << (wptr.expired()?"is":"is not") << " expired, (expired is expected)\n";
    }
    return 0;
}
