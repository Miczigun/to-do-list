export module modul2;
import modul1;

export struct Kwadrat {
	int bok;
	Kwadrat(int _bok) :bok(_bok) {};

	int pole() {
		return potega(bok, 2);
	}
};