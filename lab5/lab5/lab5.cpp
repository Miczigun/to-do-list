#include <iostream>
#include <thread>
#include <vector>
#include <algorithm>
#include <future>
#include <numeric>

void watek1() {
    std::cout << "to jest pierwszy watek" << std::endl;
}

void watek2(int liczba1, int liczba2) {
    std::cout << "to jest drugi watek" << liczba1 + liczba2 << std::endl;
}
int dodaj(int x, int y) {
    return x + y;
}
int suma(std::vector<int>& wektor) {
    return std::accumulate(wektor.begin(), wektor.end(), 0);
}
double srednia( std::vector<int>& wektor) {
    double wynik = suma(wektor);
    return wynik / static_cast<double>(wektor.size());
}

int maks( std::vector<int>& wektor) {
    return *std::max_element(wektor.begin(), wektor.end());
}

int main()
{
    std::cout << "Zad1" << std::endl;
    std::thread w1(watek1);
    std::future<void> f2 = std::async(std::launch::async, watek2, 10, 20);
    w1.join();
    f2.wait();

    std::cout << "Zad2" << std::endl;
    std::packaged_task<int(int, int)> zadanie(dodaj);
    std::future<int> wynik = zadanie.get_future();
    std::thread  w2(std::move(zadanie), 10, 20);
    w2.join();
    std::cout << "Wynik obliczen" << wynik.get() << std::endl;

    std::cout << "Zad3" << std::endl;
    std::vector<int> wektor{ 1, 2, 3, 4, 5, 6, 7, 8 };
    std::promise<int> suma_promise;
    std::promise<double> srednia_promise;
    std::promise<int> maksimum_promise;

    std::future<int> suma_future = suma_promise.get_future();
    std::future<double> srednia_future = srednia_promise.get_future();
    std::future<int> maksimum_future = maksimum_promise.get_future();

    std::async(std::launch::async, [&wektor, &suma_promise]() {
        int sum = suma(wektor);
        suma_promise.set_value(sum);
        });

    std::async(std::launch::async, [&wektor, &srednia_promise]() {
        int srd = srednia(wektor);
        srednia_promise.set_value(srd);
        });

    std::async(std::launch::async, [&wektor, &maksimum_promise]() {
        int maksiking = maks(wektor);
        maksimum_promise.set_value(maksiking);
        });

    std::cout << "suma :" << suma_future.get() << std::endl;
    std::cout << "srednia :" << srednia_future.get() << std::endl;
    std::cout << "maksimum :" << maksimum_future.get() << std::endl;

    return 0;
}

