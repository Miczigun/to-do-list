// lab4.cpp : Ten plik zawiera funkcję „main”. W nim rozpoczyna się i kończy wykonywanie programu.
//

#include <iostream>
#include <ranges>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>

namespace rg = std::ranges;

struct Person {
    std::string imie;
    std::string nazwisko;
    int wiek;
};

int main()
{
    std::cout << "Zad1" << std::endl;
    //a
    std::vector<int> wektor{ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
    auto wynik = wektor | std::views::filter([](int n) { return n < 8; })
        | std::views::take(4);

    for (const auto& i : wynik) {
        std::cout << i << ", ";
    }
    std::cout << std::endl;
    //b
    std::vector<std::string> wektor2 = { "aaaa", "bbbc", "aa","bjkdas","shdgashdga","d","dsfsf" };
    rg::sort(wektor2, {}, [](const std::string& s) {return s.size(); });
    for (const auto& wyraz : wektor2) {
        std::cout << wyraz << ", ";
    }
    std::cout << std::endl;
    //c
    std::vector<int> wektor3{ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
    int wyznacznik = 5;
    auto itr = rg::find_if(wektor3, [&](int n) {return n > wyznacznik; });
    if (itr != wektor3.end()) {
        std::cout << "Najmniejszy element : " << *itr << std::endl;
    }
    else {
        std::cout << "Nie znaleziono elementu" << std::endl;
    }
    std::cout << "Zad2" << std::endl;
    std::ifstream input("people.txt");
    if (input) {
        std::vector<Person> ludzie;
        std::string imie;
        std::string nazwisko;
        int wiek;
        
        while (input >> imie >> nazwisko >> wiek) {
            ludzie.push_back({ imie, nazwisko, wiek });
        }

        auto ludzie_posortowani = ludzie | std::views::filter([](const Person& czlowiek) {
            return czlowiek.wiek >= 18 && czlowiek.wiek <= 25;});

        for (const Person& czlowiek : ludzie_posortowani) {
            std::cout << czlowiek.imie << " " << czlowiek.nazwisko << " " << czlowiek.wiek << std::endl;
        }

        std::cout << "Zad3" << std::endl;

        std::string haslo = "Dryksonderulo123";
        auto hashed_pass = haslo | std::views::transform([](char z) {
            if (std::isdigit(z)) {
                return static_cast<char>(z + 1);
            }
            else if (std::isalpha(z)) {
                return std::tolower(z) == 'a' ? 'z' : static_cast<char>(z - 1);
            }
            else {
                return z;
            }
            });

        std::cout << "Zaszyfrowane haslo: " << std::string{ hashed_pass.begin(), hashed_pass.end() } << std::endl;
    }

}

