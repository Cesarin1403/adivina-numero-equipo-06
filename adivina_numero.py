import random
from datetime import datetime


GAME_TITLE = "Adivina el número"
DEFAULT_PLAYER_NAME = "Jugador"
LEADERBOARD_SIZE = 3
POINTS_PER_REMAINING_ATTEMPT = 10
YES_ANSWERS = {"s", "si", "sí"}
NO_ANSWERS = {"n", "no"}
DIFFICULTIES = {
    "1": {"name": "Fácil", "minimum": 1, "maximum": 20, "attempts": 8},
    "2": {"name": "Medio", "minimum": 1, "maximum": 50, "attempts": 7},
    "3": {"name": "Difícil", "minimum": 1, "maximum": 100, "attempts": 6},
}


def get_player_name():
    name = input("¿Cómo te llamas? ").strip()
    if name == "":
        return DEFAULT_PLAYER_NAME
    return name


def show_difficulty_menu():
    print("\nSelecciona una dificultad:")
    for option, settings in DIFFICULTIES.items():
        print(
            f"{option}. {settings['name']} "
            f"({settings['minimum']}–{settings['maximum']}, "
            f"{settings['attempts']} intentos)"
        )


def choose_difficulty():
    show_difficulty_menu()
    valid_options = ", ".join(DIFFICULTIES)
    while True:
        choice = input("Opción: ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print(f"Opción inválida. Escribe una de estas opciones: {valid_options}.")


def parse_guess(raw_guess, minimum, maximum):
    try:
        guess = int(raw_guess)
    except ValueError:
        return None, "La entrada debe ser un número entero."

    if guess < minimum or guess > maximum:
        return None, f"El número debe estar entre {minimum} y {maximum}."

    return guess, None


def read_valid_guess(minimum, maximum):
    while True:
        raw_guess = input(f"Escribe un número entre {minimum} y {maximum}: ").strip()
        guess, error_message = parse_guess(raw_guess, minimum, maximum)
        if error_message is None:
            return guess
        print(f"{error_message} Este intento no cuenta.")


def get_hint(guess, secret_number):
    if guess < secret_number:
        return "Muy bajo."
    return "Muy alto."


def calculate_score(attempts_used, maximum_attempts, won):
    if not won:
        return 0
    remaining_attempts = maximum_attempts - attempts_used
    return max(remaining_attempts, 0) * POINTS_PER_REMAINING_ATTEMPT


def play_round(settings):
    secret_number = random.randint(settings["minimum"], settings["maximum"])
    maximum_attempts = settings["attempts"]
    attempts_used = 0
    won = False

    print(
        f"\nAdivina el número entre {settings['minimum']} y "
        f"{settings['maximum']}. Tienes {maximum_attempts} intentos."
    )

    while attempts_used < maximum_attempts and not won:
        guess = read_valid_guess(settings["minimum"], settings["maximum"])
        attempts_used += 1

        if guess == secret_number:
            print("¡Correcto!")
            won = True
        else:
            remaining_attempts = maximum_attempts - attempts_used
            print(f"{get_hint(guess, secret_number)} Te quedan {remaining_attempts} intentos.")

    if won:
        print(f"Adivinaste en {attempts_used} intentos.")
    else:
        print(f"Se acabaron los intentos. El número era {secret_number}.")

    return {
        "won": won,
        "attempts": attempts_used,
        "score": calculate_score(attempts_used, maximum_attempts, won),
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

    for position, record in enumerate(scores[:LEADERBOARD_SIZE], start=1):
        print(
            f"{position}. {record['name']} — {record['score']} puntos "
            f"({record['difficulty']})"
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
        print("Respuesta inválida. Escribe 's' o 'n'.")


def main():
    print(f"=== {GAME_TITLE} ===")
    print("Adivina el número secreto y consigue la mayor puntuación.")
    scores = []

    try:
        while True:
            play_game(scores)
            if not ask_to_play_again():
                break
    except (KeyboardInterrupt, EOFError):
        print("\n\nJuego interrumpido.")
        return

    print("\nGracias por jugar.")


if __name__ == "__main__":
    main()