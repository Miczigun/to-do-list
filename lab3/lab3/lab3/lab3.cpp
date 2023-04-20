// lab3.cpp : Ten plik zawiera funkcję „main”. W nim rozpoczyna się i kończy wykonywanie programu.
//
#include <iostream>
#include <filesystem>
#include <string>

namespace fs = std::filesystem;

void zadanie2() {
    fs::path p1("jakis");
    fs::path p2("jakis2");
    if (!fs::exists(p2)) {
        fs::create_directory(p2);
    }
    for (const auto& it: fs::directory_iterator(p1))
    {
        fs::path var(it);
        fs::copy(it, p2 / var.filename(), fs::copy_options::overwrite_existing);
    }
}

void zadanie3() {
    fs::path p3("jakis2");
    for (const auto& it : fs::directory_iterator(p3))
    {
        fs::path var1(it);
        std::cout << fs::absolute(var1) << std::endl;
    }
}

void zadanie4() {
    int kb = 64 * 1024;
    fs::path p4("jakis2");
    fs::directory_entry ostatni;
    for (const auto& it : fs::directory_iterator(p4))
    {
        ostatni = it;
    }
    fs::path p5(ostatni);
    fs::path p6((p5.parent_path()).parent_path() / p5.filename());
    fs::copy(p5, p6, fs::copy_options::overwrite_existing);
    fs::resize_file(p6, kb);
    std::cout << "Rozmiar pliku w bajtach:" << fs::file_size(p6) << std::endl;
    fs::remove(p6);
}

void zadanie5() {
    fs::path p7("jakis2");
    int n = 2;
    for (const auto& it : fs::directory_iterator(p7))
    {
        fs::path varp = it.path();
        std::string plik_nazwa = std::to_string(n) + varp.extension().string();
        fs::path nowa_sciezka = varp.parent_path() / plik_nazwa;
        std::cout << varp << " " << nowa_sciezka << std::endl;
        fs::rename(it, nowa_sciezka);
        n += 2;
    }
}

int main()
{
    std::cout << "zad2" << std::endl;
    zadanie2();
    std::cout << "zad3" << std::endl;
    zadanie3();
    std::cout << "zad4" << std::endl;
    zadanie4();
    std::cout << "zad5" << std::endl;
    zadanie5();
    
}

