"""
Reto Integrador: Tragamonedas
Conceptos: clase y constructor, métodos, herencia, polimorfismo y encapsulación.
Ejecutar con:  python tragamonedas.py
"""
import random


# ---------------------------------------------------------------
# PARTES 1, 2, 3 y 5: Clase base
# ---------------------------------------------------------------
class Tragamonedas:
    def __init__(self, nombre, creditos):
        self.nombre = nombre
        self._creditos = creditos            # protegido por convención (Parte 5)
        self._creditos_iniciales = creditos
        self._total_apostado = 0
        self._total_ganado = 0
        self._jugadas = 0
        self.simbolos = ["🍒", "🔔", "💎", "🍀", "⭐", "7️⃣"]

    # --- Lectura de datos protegidos (solo lectura desde fuera) ---
    @property
    def creditos(self):
        return self._creditos

    @property
    def creditos_iniciales(self):
        return self._creditos_iniciales

    @property
    def total_apostado(self):
        return self._total_apostado

    @property
    def total_ganado(self):
        return self._total_ganado

    @property
    def jugadas(self):
        return self._jugadas

    @property
    def neto(self):
        return self._total_ganado - self._total_apostado

    @property
    def sin_creditos(self):
        return self._creditos <= 0

    # --- Parte 1B ---
    def mostrar(self):
        print(f"🎰 {self.nombre} — Créditos: S/ {self._creditos}")

    # --- Parte 2 ---
    def girar(self):
        resultado = [random.choice(self.simbolos) for _ in range(3)]
        print("[ " + "  ".join(resultado) + " ]")
        return resultado

    # --- Parte 3: reglas de premio (se sobrescribe en las hijas) ---
    def calcular_premio(self, apuesta, resultado):
        """Devuelve (premio, mensaje)."""
        distintos = len(set(resultado))
        if distintos == 1:
            return apuesta * 10, "🎉 ¡JACKPOT! Tres iguales"
        if distintos == 2:
            return apuesta * 2, "✨ ¡Dos iguales!"
        return 0, "😢 Perdiste"

    def jugar(self, apuesta):
        """Devuelve el premio ganado, o None si la jugada no fue válida."""
        if apuesta <= 0:
            print("⚠️  La apuesta debe ser mayor que 0.")
            return None
        if apuesta > self._creditos:
            print("⚠️  No tienes créditos suficientes.")
            return None

        self._creditos -= apuesta
        self._total_apostado += apuesta
        self._jugadas += 1

        resultado = self.girar()
        premio, mensaje = self.calcular_premio(apuesta, resultado)

        self._creditos += premio
        self._total_ganado += premio

        if premio > 0:
            print(f"{mensaje} Ganaste S/ {premio}")
        else:
            print(f"{mensaje} S/ {apuesta}")
        return premio

    def estadisticas(self):
        signo = "+" if self.neto >= 0 else "-"
        print(f"  {self.nombre:<15} jugadas: {self._jugadas:<3} "
              f"apostado: S/ {self._total_apostado:<5} "
              f"ganado: S/ {self._total_ganado:<5} "
              f"neto: {signo}S/ {abs(self.neto)}")


# ---------------------------------------------------------------
# PARTE 4: Herencia — máquinas con símbolos propios
# ---------------------------------------------------------------
class TragamonedasFrutas(Tragamonedas):
    def __init__(self, nombre, creditos):
        super().__init__(nombre, creditos)
        self.simbolos = ["🍒", "🍋", "🍊"]


class TragamonedasClasico(Tragamonedas):
    def __init__(self, nombre, creditos):
        super().__init__(nombre, creditos)
        self.simbolos = ["7️⃣", "💎", "🔔"]


# Parte 4B: máquina propia con reglas distintas (polimorfismo)
class TragamonedasMundial(Tragamonedas):
    def __init__(self, nombre, creditos):
        super().__init__(nombre, creditos)
        self.simbolos = ["🇵🇪", "🇦🇷", "🇫🇷", "🇧🇷"]

    def calcular_premio(self, apuesta, resultado):
        distintos = len(set(resultado))
        peruanos = resultado.count("🇵🇪")

        if distintos == 1 and peruanos == 3:
            return apuesta * 25, "🇵🇪 ¡GOOOL DEL PERÚ! Tres banderas peruanas x25"
        if distintos == 1:
            return apuesta * 15, "🏆 ¡Tres iguales! x15"
        if distintos == 2:
            if peruanos > 0:
                return apuesta * 2 + apuesta, "🇵🇪 ¡Dos iguales + bono por Perú!"
            return apuesta * 2, "✨ ¡Dos iguales!"
        return 0, "😢 Perdiste"


# ---------------------------------------------------------------
# PARTE 3B: Bucle de juego de una máquina
# ---------------------------------------------------------------
def pedir_entero(texto):
    while True:
        try:
            return int(input(texto))
        except ValueError:
            print("⚠️  Ingresa un número entero.")


def bucle_de_juego(maquina):
    while True:
        print()
        maquina.mostrar()

        if maquina.sin_creditos:
            print("😵 Te quedaste sin créditos. Fin del juego en esta máquina.")
            return

        apuesta = pedir_entero("¿Cuánto apuestas? (0 para salir): ")
        if apuesta == 0:
            print(f"💰 Saliste con S/ {maquina.creditos}. ¡Vuelve pronto!")
            return

        maquina.jugar(apuesta)


# ---------------------------------------------------------------
# PARTE 5B: Sistema multi-máquina
# ---------------------------------------------------------------
def mostrar_menu(maquinas):
    print("\n🎰 CASINO ROYALE 🎰\n")
    for i, m in enumerate(maquinas, start=1):
        estado = "SIN CRÉDITOS" if m.sin_creditos else f"S/ {m.creditos}"
        print(f"{i}. {m.nombre} ({estado})")
    n = len(maquinas)
    print(f"{n + 1}. Mostrar estadísticas de todas")
    print(f"{n + 2}. Salir\n")


def mostrar_estadisticas(maquinas):
    print("\n📊 ESTADÍSTICAS")
    for m in maquinas:
        m.estadisticas()


def resumen_final(maquinas):
    inicial = sum(m.creditos_iniciales for m in maquinas)
    final = sum(m.creditos for m in maquinas)
    apostado = sum(m.total_apostado for m in maquinas)
    ganado = sum(m.total_ganado for m in maquinas)

    print("\n🏁 RESUMEN GENERAL DEL CASINO")
    mostrar_estadisticas(maquinas)
    print(f"\n  Total apostado: S/ {apostado}")
    print(f"  Total ganado:   S/ {ganado}")
    print(f"  Empezaste con S/ {inicial} y terminas con S/ {final}.")
    print("\n¡Gracias por jugar, vuelve pronto! 🎰")


def main():
    maquinas = [
        TragamonedasFrutas("La Frutal", 200),
        TragamonedasClasico("La Clásica", 300),
        TragamonedasMundial("Mundial 2026", 150),
    ]
    n = len(maquinas)

    while True:
        mostrar_menu(maquinas)
        opcion = pedir_entero("Elige una opción: ")

        if 1 <= opcion <= n:
            maquina = maquinas[opcion - 1]
            if maquina.sin_creditos:
                print("⚠️  Esa máquina está SIN CRÉDITOS. Elige otra.")
            else:
                bucle_de_juego(maquina)
        elif opcion == n + 1:
            mostrar_estadisticas(maquinas)
        elif opcion == n + 2:
            resumen_final(maquinas)
            break
        else:
            print("⚠️  Opción no válida.")


if __name__ == "__main__":
    main()