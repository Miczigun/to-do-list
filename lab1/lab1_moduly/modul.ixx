#include <iostream>

export module modul;

void f() {
	std::cout << "funkcja f() z modul.ixx\n\n";
}

export void g() {
	std::cout << "wywolanie funkcji f() w modul.ixx:\n\t\t";
	f();
}