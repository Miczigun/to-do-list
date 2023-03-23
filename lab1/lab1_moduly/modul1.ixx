export module modul1;

export double potega(int a, int n)
{
	double wynik = 1;
	if (n >= 0) {
		for (int i = 0; i < n; i++)
		{
			wynik *= a;
		}
	}
	else {
		for (int i = 0; i < n*(-1); i++)
		{
			wynik /= a;
		}
	}
	return wynik;
}