# Turniej wiedzy
# Gra sprawdzająca wiedzę ogólną, odczytująca dane ze zwykłego pliku tekstowego
# 146

import sys
import pickle


def otworz_dat(file_name, mode):
    """Otwórz zamarynowany plik"""
    try:
        the_file_dat = open(file_name, mode)
    except IOError as e:
        print("Nie można otworzyć pliku", file_name, "Program zostanie zakończony.\n", e)
        input("\n\nAby zakończyć program, naciśnij klawisz Enter.")
        sys.exit()
    else:
        return the_file_dat


def open_file(file_name, mode):
    """Otwórz plik."""
    try:
        the_file = open(file_name, mode)
    except IOError as e:
        print("Nie można otworzyć pliku", file_name, "Program zostanie zakończony.\n", e)
        input("\n\nAby zakończyć program, naciśnij klawisz Enter.")
        sys.exit()
    else:
        return the_file


def next_line(the_file):
    """Zwróć kolejny wiersz pliku kwiz po sformatowaniu go."""
    line = the_file.readline()
    line = line.replace("/", "\n")
    return line


def next_block(the_file):
    """Zwróć kolejny blok danych z pliku kwiz."""
    category = next_line(the_file)
    
    question = next_line(the_file)
    
    answers = []
    for i in range(4):
        answers.append(next_line(the_file))
        
    correct = next_line(the_file)
    if correct:
        correct = correct[0]
        
    explanation = next_line(the_file)

    plusscore = next_line(the_file) 

    return category, question, answers, correct, explanation, plusscore


def welcome(title):
    """Przywitaj gracza i pobierz jego nazwę."""
    print("\t\t Witaj w turnieju wiedzy!\n")
    print("\t\t", title, "\n")


def best_scores():
    """Pokaż tabele wyników"""
    global score
    wybor = None
    while wybor != "0":
        print(
            """
        0 - zakończ
        1 - wyświetl najlepsze wyniki
        2 - dodaj swój wynik
        3 - wyczyść najlepsze wyniki
            """)
        wybor = input("Wybieram: ")
        if wybor == "0":
            print("Do widzenia")
        elif wybor == "1":
            print("IMIE\t WYNIK")
            plik = otworz_dat("najlepszewyniki.dat", "rb")
            scores = pickle.load(plik)
            for entry in scores:
                scorea, name = entry
                print(name, "\t", scorea)
            plik.close()
        elif wybor == "2":
            name = input("Podaj imię: ")
            entry = (score, name)
            scores.append(entry)
            scores.sort(reverse=True)
            scores = scores[:5]  # zachowaj tylko 5 najlepszych wyników
            plik = otworz_dat("najlepszewyniki.dat", "wb")
            pickle.dump(scores, plik)
            plik.close()
        elif wybor == "3":
            scores = []
            plik = otworz_dat("najlepszewyniki.dat", "wb")
            pickle.dump(scores, plik)
            plik.close()
        else:
            print("Nieznana opcja")


def main():
    global score
    trivia_file = open_file("kwiz.txt", "r")
    title = next_line(trivia_file)
    welcome(title)
    score = 0

    # pobierz pierwszy blok
    category, question, answers, correct, explanation, plusscore = next_block(trivia_file)
    while plusscore:
        # zadaj pytanie
        print(category)
        print(question)
        print("Za to pytanie dostaniesz", plusscore, "punktów")
        for i in range(4):
            print("\t", i + 1, "-", answers[i])

        # uzyskaj odpowiedź
        answer = input("Jaka jest Twoja odpowiedź?: ")

        # sprawdź odpowiedź
        if answer == correct:
            print("\nOdpowiedź prawidłowa!", end=" ")
            score += int(plusscore)
        else:
            print("\nOdpowiedź niepoprawna.", end=" ")
        print(explanation)
        print("Wynik:", score, "\n\n")

        # pobierz kolejny blok
        category, question, answers, correct, explanation, plusscore = next_block(trivia_file)

    trivia_file.close()

    print("To było ostatnie pytanie!")
    print("Twój końcowy wynik wynosi", score)
    best_scores()

main()  
input("\n\nAby zakończyć program, naciśnij klawisz Enter.")
