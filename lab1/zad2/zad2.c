#include <stdio.h>
#include <stdlib.h>

struct v_table{
    double (*value_at)();
};

struct Unary_Function{
    int lower_bound;
    int upper_bound;
    double a;
    double b;
    struct v_table value_at_v_table;
};

void tabulate(struct Unary_Function* f){
    for(int x = f->lower_bound; x <= f->upper_bound; x++) {
        printf("f(%d)=%lf\n", x, f->value_at_v_table.value_at(f, (double)x));
      }
}

double square_value_at(struct Unary_Function* f, double x){
    return x*x;
}

double linear_value_at(struct Unary_Function* f, double x){
    return f->a * x + f->b;
}

void generate_square(struct Unary_Function* f, int lower_bound, int upper_bound){
    f->lower_bound = lower_bound;
    f->upper_bound = upper_bound;
    f->a = 0;
    f->b = 0;
    f->value_at_v_table.value_at = &square_value_at;
}

void generate_linear(struct Unary_Function* f, int lower_bound, int upper_bound, double a, double b){
    f->lower_bound = lower_bound;
    f->upper_bound = upper_bound;
    f->a = a;
    f->b = b;
    f->value_at_v_table.value_at = &linear_value_at;
}

struct Unary_Function* Square(int lower_bound, int upper_bound){
    struct Unary_Function* f = malloc(sizeof(struct Unary_Function));
    generate_square(f, lower_bound, upper_bound);
    return f;
}

struct Unary_Function* Linear(int lower_bound, int upper_bound, double a, double b){
    struct Unary_Function* f = malloc(sizeof(struct Unary_Function));
    generate_linear(f, lower_bound, upper_bound, a, b);
    return f;
}

double value_at(struct Unary_Function* f1, double x){
    return f1->value_at_v_table.value_at(x);
}

double negative_value_at(struct Unary_Function* f1, double x){
    return -(f1->value_at_v_table.value_at(x));
}

int same_functions_for_ints(struct Unary_Function *f1, struct Unary_Function *f2, double tolerance) {
        if(f1->lower_bound != f2->lower_bound) return 0;
        if(f1->upper_bound != f2->upper_bound) return 0;
        for(int x = f1->lower_bound; x <= f1->upper_bound; x++) {
            double delta = value_at(f1, x) - value_at(f2, x);
            if(delta < 0) delta = -delta;
            if(delta > tolerance) return 0;
        }
        return 1;
    };

int main(void){
    struct Unary_Function *f1 = Square(-2, 2);
    tabulate(f1);
    struct Unary_Function *f2 = Linear(-2, 2, 5, -2);
    tabulate(f2);
    printf("f1==f2: %s\n", same_functions_for_ints(f1, f2, 1E-6) ? "DA" : "NE");
    printf("neg_val f2(1) = %lf\n", negative_value_at(f2, 1.0));
    free(f1);
    free(f2);
    return 0;
}