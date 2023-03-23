#include <iostream>
import modul1;
import modul2;
import modul;

void f() {
    std::cout << "funkcja f() z main.cpp\n\n";
}


int main()
{
    std::cout << "Zad1"<<std::endl;
    std::cout << potega(2,3) << std::endl;
    std::cout << "Zad 2 i 3" << std::endl;
    Kwadrat k(4);
    std::cout << "Pole kwadratu o boku 4 =" << k.pole() << std::endl;
    std::cout << "Zad4" << std::endl;
    std::cout << potega(2,-2) << std::endl;
    std::cout << "Zad5" << std::endl;

    std::cout << "wywolanie funkcji f() w main.cpp:\n\t";
    f();
    std::cout << "wywolanie funkcji g() w main.cpp:\n\t";
    g();

}

