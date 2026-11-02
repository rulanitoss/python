#include <iostream>

using namespace std;

int main ()
{
    int base, expoente;
    int resultado=1;

    cout << "Diga a base: ";
    cin >> base;
    cout <<"Diga o expoente: ";
    cin >> expoente;

    while (expoente >0) {
        resultado = resultado * base;
        expoente--;
    }

    cout << "Resultado: " << resultado;


  return 0;
}
