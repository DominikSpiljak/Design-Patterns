#include <iostream>
#include <assert.h>
#include <stdlib.h>
#include <list>

struct Point{
    int x; int y;
};
class Shape{
    public:
        virtual void draw() = 0;
        virtual void move(int x, int y) = 0;
};
class Circle : public Shape{
    public:
        double radius_;
        Point center_;

        virtual void draw(){
            std::cerr <<"in drawCircle\n";
        }
        virtual void move(int x, int y){
            center_.x += x;
            center_.y += y;
            std::cout <<"Translated a circle by ("<< x << ", " << y << ")\n";
        }
};
class Square : public Shape{
    public:
        double side_;
        Point center_;
        
        virtual void draw(){
            std::cerr <<"in drawSquare\n";
        }
        virtual void move(int x, int y){
            center_.x += x;
            center_.y += y;
             std::cout <<"Translated a square by ("<< x << ", " << y << ")\n";
        }
};
class Rhomb : public Shape{
    public:
        double side_;
        Point center_;
        Point points_[4];
        virtual void draw(){
            std::cerr <<"in drawRhomb\n";
        }
        virtual void move(int x, int y){
            center_.x += x;
            center_.y += y;
            for(int i = 0; i < 4; i++){
                points_[i].x += x;
                points_[i].y += y;
            }
            std::cout <<"Translated a rhomb by ("<< x << ", " << y << ")\n";
        }
};
void drawShapes(const std::list<Shape*>& fig){
    std::list<Shape*>::const_iterator  it;
    for(it=fig.begin(); it!=fig.end(); it++){
        (*it)->draw();
    }
}
void moveShapes(const std::list<Shape*>& fig, int x, int y){
    std::list<Shape*>::const_iterator it;
    for(it=fig.begin(); it!=fig.end(); it++){
        (*it)->move(x, y);
    }
}
int main(){
    std::list<Shape*> shapes;
    shapes.push_back((Shape*)new Circle);
    shapes.push_back((Shape*)new Square);
    shapes.push_back((Shape*)new Square);
    shapes.push_back((Shape*)new Circle);
    shapes.push_back((Shape*)new Rhomb);

    drawShapes(shapes);
    moveShapes(shapes, 1, 1);
}