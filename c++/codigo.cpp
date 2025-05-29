#include <iostream>
#include <string>
#include <vector>
#include <random>
#include <algorithm>

using namespace std;

class Pokemon {
private:
    string nombre;
    string tipo;
    int hp;
    int maxHp;
    int ataque;
    int defensa;
    vector<string> movimientos;

public:
    Pokemon(string n, string t, int h, int a, int d, vector<string> mov) 
        : nombre(n), tipo(t), hp(h), maxHp(h), ataque(a), defensa(d), movimientos(mov) {}
    
    string getNombre() const { return nombre; }
    string getTipo() const { return tipo; }
    int getHp() const { return hp; }
    int getMaxHp() const { return maxHp; }
    bool estaVivo() const { return hp > 0; }
    
    void mostrarEstado() const {
        cout << nombre << " (" << tipo << ") - HP: " << hp << "/" << maxHp << endl;
    }
    
    void mostrarMovimientos() const {
        cout << "Movimientos de " << nombre << ":" << endl;
        for (int i = 0; i < movimientos.size(); i++) {
            cout << (i + 1) << ". " << movimientos[i] << endl;
        }
    }
    
    int atacar(const string& movimiento) {
        // Daño base + variación aleatoria
        random_device rd;
        mt19937 gen(rd());
        uniform_int_distribution<> dis(80, 120);
        
        int multiplicador = dis(gen);
        int danio = (ataque * multiplicador) / 100;
        
        cout << nombre << " usa " << movimiento << "!" << endl;
        return danio;
    }
    
    void recibirDanio(int danio, int ataqueEnemigo) {
        // Calcular daño con defensa
        int danioFinal = max(1, danio - defensa/2);
        hp -= danioFinal;
        if (hp < 0) hp = 0;
        
        cout << nombre << " recibe " << danioFinal << " puntos de daño!" << endl;
        if (hp == 0) {
            cout << nombre << " se ha debilitado!" << endl;
        }
    }
    
    string getMovimiento(int indice) const {
        if (indice >= 0 && indice < movimientos.size()) {
            return movimientos[indice];
        }
        return movimientos[0];
    }
    
    int getNumMovimientos() const {
        return movimientos.size();
    }
};

class Jugador {
private:
    string nombre;
    vector<Pokemon> equipo;
    int pokemonActivo;

public:
    Jugador(string n) : nombre(n), pokemonActivo(0) {}
    
    void agregarPokemon(const Pokemon& p) {
        equipo.push_back(p);
    }
    
    string getNombre() const { return nombre; }
    
    Pokemon& getPokemonActivo() {
        return equipo[pokemonActivo];
    }
    
    bool tienePokemonVivos() const {
        for (const auto& pokemon : equipo) {
            if (pokemon.estaVivo()) {
                return true;
            }
        }
        return false;
    }
    
    void mostrarEquipo() const {
        cout << "\nEquipo de " << nombre << ":" << endl;
        for (int i = 0; i < equipo.size(); i++) {
            cout << (i + 1) << ". ";
            equipo[i].mostrarEstado();
        }
    }
    
    bool cambiarPokemon() {
        cout << "\n¿Quieres cambiar de Pokemon? (s/n): ";
        char respuesta;
        cin >> respuesta;
        
        if (respuesta == 's' || respuesta == 'S') {
            mostrarEquipo();
            cout << "Selecciona un Pokemon (1-" << equipo.size() << "): ";
            int seleccion;
            cin >> seleccion;
            seleccion--;
            
            if (seleccion >= 0 && seleccion < equipo.size() && equipo[seleccion].estaVivo()) {
                pokemonActivo = seleccion;
                cout << "¡Adelante, " << equipo[pokemonActivo].getNombre() << "!" << endl;
                return true;
            }
        }
        return false;
    }
    
    void seleccionarSiguientePokemon() {
        mostrarEquipo();
        cout << nombre << ", selecciona tu siguiente Pokemon (1-" << equipo.size() << "): ";
        int seleccion;
        cin >> seleccion;
        seleccion--;
        
        while (seleccion < 0 || seleccion >= equipo.size() || !equipo[seleccion].estaVivo()) {
            cout << "Selección inválida. Elige un Pokemon vivo: ";
            cin >> seleccion;
            seleccion--;
        }
        
        pokemonActivo = seleccion;
        cout << "¡Adelante, " << equipo[pokemonActivo].getNombre() << "!" << endl;
    }
};

void inicializarPokemon(vector<Pokemon>& pokemonDisponibles) {
    pokemonDisponibles.push_back(Pokemon("Pikachu", "Electrico", 100, 45, 30, {"Impactrueno", "Ataque Rapido", "Rayo", "Trueno"}));
    pokemonDisponibles.push_back(Pokemon("Charizard", "Fuego", 120, 55, 35, {"Lanzallamas", "Garra Dragon", "Vuelo", "Llamarada"}));
    pokemonDisponibles.push_back(Pokemon("Blastoise", "Agua", 130, 50, 40, {"Hidrobomba", "Burbuja", "Surf", "Pulso Agua"}));
    pokemonDisponibles.push_back(Pokemon("Venusaur", "Planta", 125, 48, 38, {"Hoja Afilada", "Latigo Cepa", "Rayo Solar", "Bomba Germen"}));
    pokemonDisponibles.push_back(Pokemon("Gengar", "Fantasma", 110, 52, 32, {"Bola Sombra", "Lametazo", "Pesadilla", "Puño Sombra"}));
    pokemonDisponibles.push_back(Pokemon("Machamp", "Lucha", 140, 60, 45, {"Puño Dinamico", "Golpe Karate", "Fuerza", "Sumision"}));
    pokemonDisponibles.push_back(Pokemon("Alakazam", "Psiquico", 95, 58, 28, {"Psicorrayo", "Confusion", "Psiquico", "Teletransporte"}));
    pokemonDisponibles.push_back(Pokemon("Gyarados", "Agua", 150, 62, 42, {"Hidrobomba", "Mordisco", "Dragon Rage", "Hiperrayo"}));
}

void seleccionarEquipo(Jugador& jugador, const vector<Pokemon>& pokemonDisponibles) {
    cout << "\n" << jugador.getNombre() << ", selecciona 3 Pokemon para tu equipo:" << endl;
    
    for (int i = 0; i < pokemonDisponibles.size(); i++) {
        cout << (i + 1) << ". " << pokemonDisponibles[i].getNombre() 
             << " (" << pokemonDisponibles[i].getTipo() << ") - HP: " 
             << pokemonDisponibles[i].getMaxHp() << endl;
    }
    
    for (int i = 0; i < 3; i++) {
        cout << "\nSelecciona Pokemon #" << (i + 1) << " (1-" << pokemonDisponibles.size() << "): ";
        int seleccion;
        cin >> seleccion;
        seleccion--;
        
        while (seleccion < 0 || seleccion >= pokemonDisponibles.size()) {
            cout << "Selección inválida. Intenta de nuevo: ";
            cin >> seleccion;
            seleccion--;
        }
        
        jugador.agregarPokemon(pokemonDisponibles[seleccion]);
        cout << "¡" << pokemonDisponibles[seleccion].getNombre() << " se ha unido a tu equipo!" << endl;
    }
}

void batalla(Jugador& jugador1, Jugador& jugador2) {
    cout << "\n¡¡¡COMIENZA LA BATALLA!!!" << endl;
    cout << "¡Adelante, " << jugador1.getPokemonActivo().getNombre() << "!" << endl;
    cout << "¡Adelante, " << jugador2.getPokemonActivo().getNombre() << "!" << endl;
    
    while (jugador1.tienePokemonVivos() && jugador2.tienePokemonVivos()) {
        cout << "\n" << string(50, '=') << endl;
        cout << "ESTADO ACTUAL:" << endl;
        jugador1.getPokemonActivo().mostrarEstado();
        jugador2.getPokemonActivo().mostrarEstado();
        cout << string(50, '=') << endl;
        
        // Turno del Jugador 1
        if (jugador1.getPokemonActivo().estaVivo()) {
            cout << "\nTurno de " << jugador1.getNombre() << endl;
            
            if (!jugador1.cambiarPokemon()) {
                jugador1.getPokemonActivo().mostrarMovimientos();
                cout << "Selecciona un movimiento (1-" << jugador1.getPokemonActivo().getNumMovimientos() << "): ";
                int movimiento;
                cin >> movimiento;
                movimiento--;
                
                if (movimiento >= 0 && movimiento < jugador1.getPokemonActivo().getNumMovimientos()) {
                    string nombreMovimiento = jugador1.getPokemonActivo().getMovimiento(movimiento);
                    int danio = jugador1.getPokemonActivo().atacar(nombreMovimiento);
                    jugador2.getPokemonActivo().recibirDanio(danio, jugador1.getPokemonActivo().getMaxHp());
                }
            }
        }
        
        // Verificar si el Pokemon del jugador 2 se debilitó
        if (!jugador2.getPokemonActivo().estaVivo() && jugador2.tienePokemonVivos()) {
            jugador2.seleccionarSiguientePokemon();
        }
        
        // Turno del Jugador 2
        if (jugador2.getPokemonActivo().estaVivo() && jugador1.tienePokemonVivos()) {
            cout << "\nTurno de " << jugador2.getNombre() << endl;
            
            if (!jugador2.cambiarPokemon()) {
                jugador2.getPokemonActivo().mostrarMovimientos();
                cout << "Selecciona un movimiento (1-" << jugador2.getPokemonActivo().getNumMovimientos() << "): ";
                int movimiento;
                cin >> movimiento;
                movimiento--;
                
                if (movimiento >= 0 && movimiento < jugador2.getPokemonActivo().getNumMovimientos()) {
                    string nombreMovimiento = jugador2.getPokemonActivo().getMovimiento(movimiento);
                    int danio = jugador2.getPokemonActivo().atacar(nombreMovimiento);
                    jugador1.getPokemonActivo().recibirDanio(danio, jugador2.getPokemonActivo().getMaxHp());
                }
            }
        }
        
        // Verificar si el Pokemon del jugador 1 se debilitó
        if (!jugador1.getPokemonActivo().estaVivo() && jugador1.tienePokemonVivos()) {
            jugador1.seleccionarSiguientePokemon();
        }
    }
    
    // Determinar ganador
    cout << "\n" << string(50, '=') << endl;
    if (jugador1.tienePokemonVivos()) {
        cout << "¡¡¡" << jugador1.getNombre() << " ES EL GANADOR!!!" << endl;
    } else {
        cout << "¡¡¡" << jugador2.getNombre() << " ES EL GANADOR!!!" << endl;
    }
    cout << string(50, '=') << endl;
}

int main() {
    cout << "🔥 ¡BIENVENIDOS AL SIMULADOR DE BATALLAS POKEMON! 🔥" << endl;
    cout << string(60, '=') << endl;
    
    vector<Pokemon> pokemonDisponibles;
    inicializarPokemon(pokemonDisponibles);
    
    cout << "\nIngresa el nombre del Jugador 1: ";
    string nombre1;
    cin >> nombre1;
    Jugador jugador1(nombre1);
    
    cout << "Ingresa el nombre del Jugador 2: ";
    string nombre2;
    cin >> nombre2;
    Jugador jugador2(nombre2);
    
    seleccionarEquipo(jugador1, pokemonDisponibles);
    seleccionarEquipo(jugador2, pokemonDisponibles);
    
    batalla(jugador1, jugador2);
    
    cout << "\n¡Gracias por jugar!" << endl;
    return 0;
}
