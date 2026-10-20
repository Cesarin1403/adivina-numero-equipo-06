import random
from datetime import datetime


GAME_TITLE = "Adivina el número"
DIFFICULTIES = {
    "1": {"name": "Fácil", "minimum": 1, "maximum": 20, "attempts": 8},
    "2": {"name": "Medio", "minimum": 1, "maximum": 50, "attempts": 7},
    "3": {"name": "Difícil", "minimum": 1, "maximum": 100, "attempts": 6},
}


def get_player_name():
    name = input("¿Cómo te llamas? ").strip()
    if name == "":
        return "Jugador"
    return name


def choose_difficulty():
    print("\nSelecciona una dificultad:")
    print("1. Fácil (1–20, 8 intentos)")
    print("2. Medio (1–50, 7 intentos)")
    print("3. Difícil (1–100, 6 intentos)")

    choice = input("Opción: ").lower()
    if choice in DIFFICULTIES:
        return DIFFICULTIES[choice]

    print("Opción inválida. Se usará la dificultad Fácil.")
    return DIFFICULTIES["2"]


def read_guess(minimum, maximum):
    raw_guess = input(f"Escribe un número entre {minimum} y {maximum}: ").strip()
    if raw_guess.isdigit():
        return int(raw_guess)

    print("La entrada debe ser un número entero.")
    return None


def calculate_score(attempts_used, maximum_attempts, won):
    if won is False:
        return 0

    points = (maximum_attempts - attempts_used) * 10
    if points < 0:
        points = 0
    return points


def play_round(settings):
    secret_number = random.randint(settings["minimum"], settings["maximum"])
    attempts_used = 0
    guess = None
    won = False

    print(
        f"\nAdivina el número entre {settings['minimum']} y "
        f"{settings['maximum']}. Tienes {settings['attempts']} intentos."
    )

    while attempts_used <= settings["attempts"] and won is False:
        guess = read_guess(settings["minimum"], settings["maximum"])
        attempts_used += 1

        if guess is None:
            continue
        elif guess < settings["minimum"]:
            print("El número es menor que el rango permitido.")
        elif guess > settings["maximum"]:
            print("El número es mayor que el rango permitido.")
        elif guess < secret_number:
            print("Muy bajo.")
        elif guess > secret_number:
            print("Muy alto.")
        else:
            print("¡Correcto!")
            won = True

    if won:
        print(f"Adivinaste en {attempts_used} intentos.")
    else:
        print(f"Se acabaron los intentos. El número era {secret_number}.")

    score = calculate_score(attempts_used, settings["attempts"], won)
    return {
        "won": won,
        "attempts": attempts_used,
        "score": score,
        "secret_number": secret_number,
    }


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
    answer = input("\n¿Quieres jugar otra vez? (s/n): ").lower()
    if answer == "s" or answer == "si" or answer == "sí":
        return True
    return False


def main():
    print(f"=== {GAME_TITLE} ===")
    print("Adivina el número secreto y consigue la mayor puntuación.")
    scores = []

    while True:
        play_game(scores)
        if ask_to_play_again() is False:
            break

    print("\nGracias por jugar.")


main()
