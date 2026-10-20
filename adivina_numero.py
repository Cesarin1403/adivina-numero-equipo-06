import random
from datetime import datetime


GAME_TITLE = "Adivina el número"
DIFFICULTIES = {
    "1": {"name": "Fácil", "minimum": 1, "maximum": 20, "attempts": 8},
    "2": {"name": "Medio", "minimum": 1, "maximum": 50, "attempts": 7},
    "3": {"name": "Difícil", "minimum": 1, "maximum": 100, "attempts": 6},
}
YES_ANSWERS = {"s", "si", "sí"}
NO_ANSWERS = {"n", "no"}


def get_player_name():
    name = input("¿Cómo te llamas? ").strip()
    if name == "":
        return "Jugador"
    return name


def show_difficulty_menu():
    print("\nSelecciona una dificultad:")
    for key, settings in DIFFICULTIES.items():
        print(
            f"{key}. {settings['name']} "
            f"({settings['minimum']}–{settings['maximum']}, "
            f"{settings['attempts']} intentos)"
        )


def choose_difficulty():
    show_difficulty_menu()

    while True:
        choice = input("Opción: ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]

        valid_options = ", ".join(DIFFICULTIES)
        print(f"Opción inválida. Elige una de estas opciones: {valid_options}.")


def read_guess(minimum, maximum):
    """Devuelve un entero dentro del rango, o None si la entrada no es válida."""
    raw_guess = input(f"Escribe un número entre {minimum} y {maximum}: ").strip()

    try:
        guess = int(raw_guess)
    except ValueError:
        print("La entrada debe ser un número entero. No cuenta como intento.")
        return None

    if guess < minimum or guess > maximum:
        print(
            f"El número debe estar entre {minimum} y {maximum}. "
            "No cuenta como intento."
        )
        return None

    return guess


def evaluate_guess(guess, secret_number):
    """Devuelve 'low', 'high' o 'correct'."""
    if guess < secret_number:
        return "low"
    if guess > secret_number:
        return "high"
    return "correct"


def calculate_score(attempts_used, maximum_attempts, won):
    if not won:
        return 0
    return (maximum_attempts - attempts_used) * 10


def show_round_result(result):
    if result["won"]:
        word = "intento" if result["attempts"] == 1 else "intentos"
        print(f"Adivinaste en {result['attempts']} {word}.")
    else:
        print(f"Se acabaron los intentos. El número era {result['secret_number']}.")


def play_round(settings):
    secret_number = random.randint(settings["minimum"], settings["maximum"])
    max_attempts = settings["attempts"]
    attempts_used = 0
    won = False

    print(
        f"\nAdivina el número entre {settings['minimum']} y "
        f"{settings['maximum']}. Tienes {max_attempts} intentos."
    )

    while attempts_used < max_attempts and not won:
        guess = read_guess(settings["minimum"], settings["maximum"])
        if guess is None:
            continue

        attempts_used += 1
        outcome = evaluate_guess(guess, secret_number)

        if outcome == "low":
            print("Muy bajo.")
        elif outcome == "high":
            print("Muy alto.")
        else:
            print("¡Correcto!")
            won = True

        if not won and attempts_used < max_attempts:
            print(f"Intentos restantes: {max_attempts - attempts_used}")

    result = {
        "won": won,
        "attempts": attempts_used,
        "score": calculate_score(attempts_used, max_attempts, won),
        "secret_number": secret_number,
    }
    show_round_result(result)
    return result


def save_score(scores, player_name, result, difficulty_name):
    record = {
        "name": player_name,
        "score": result["score"],
        "won": result["won"],
        "difficulty": difficulty_name,
        "played_at": datetime.now(),
    }
    scores.append(record)
    scores.sort(key=lambda item: item["score"], reverse=True)
    return record


def show_leaderboard(scores):
    print("\n--- Mejores resultados de esta sesión ---")
    if len(scores) == 0:
        print("Todavía no hay resultados.")
        return

    for position, result in enumerate(scores[:3], start=1):
        print(
            f"{position}. {result['name']} — {result['score']} puntos "
            f"({result['difficulty']})"
        )


def play_game(scores):
    player_name = get_player_name()
    settings = choose_difficulty()
    result = play_round(settings)
    save_score(scores, player_name, result, settings["name"])
    show_leaderboard(scores)


def ask_to_play_again():
    while True:
        answer = input("\n¿Quieres jugar otra vez? (s/n): ").strip().lower()
        if answer in YES_ANSWERS:
            return True
        if answer in NO_ANSWERS:
            return False
        print("Respuesta inválida. Escribe 's' para sí o 'n' para no.")


def main():
    print(f"=== {GAME_TITLE} ===")
    print("Adivina el número secreto y consigue la mayor puntuación.")
    scores = []

    while True:
        play_game(scores)
        if not ask_to_play_again():
            break

    print("\nGracias por jugar.")


if __name__ == "__main__":
    main()