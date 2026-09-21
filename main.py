from pathlib import Path
from random import uniform
from time import monotonic, sleep

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


DELAY_FILE = Path(__file__).with_name("delayrange.txt")


def get_delay_range() -> tuple[float, float]:
    try:
        lines = DELAY_FILE.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise ValueError(
            "delayrange.txt skal ligge ved siden af main.py"
        ) from exc

    values = [
        line.strip()
        for line in lines
        if line.strip() and not line.startswith("#")
    ]

    if not values:
        raise ValueError("delayrange.txt indeholder ingen forsinkelse.")

    try:
        start_text, end_text = values[0].split(",", maxsplit=1)
        start = float(start_text.strip())
        end = float(end_text.strip())
    except ValueError as exc:
        raise ValueError(
            "Brug formatet 0.06,0.10 i delayrange.txt"
        ) from exc

    if start < 0 or end < start:
        raise ValueError("Forsinkelsesintervallet er ugyldigt.")

    return start, end


def get_active_word(driver: webdriver.Chrome) -> str | None:
    return driver.execute_script("""
        const word = document.querySelector(".word.active");

        if (!word) {
            return null;
        }

        return Array.from(word.querySelectorAll("letter"))
            .map(letter => letter.textContent)
            .join("") || word.textContent.trim();
    """)


def test_is_running(driver: webdriver.Chrome) -> bool:
    return bool(driver.execute_script("""
        return document.querySelector(".word.active");
    """))


def send_character(
    driver: webdriver.Chrome,
    character: str,
) -> None:
    ActionChains(driver).key_down(character).key_up(character).perform()


def send_space(driver: webdriver.Chrome) -> None:
    ActionChains(driver).key_down(Keys.SPACE).key_up(Keys.SPACE).perform()


def wait_for_next_word(
    driver: webdriver.Chrome,
    previous_element,
    timeout: float = 1.5,
) -> bool:
    try:
        WebDriverWait(driver, timeout).until(
            lambda browser: browser.execute_script(
                """
                const previous = arguments[0];
                const current = document.querySelector(".word.active");

                return !current || current !== previous;
                """,
                previous_element,
            )
        )
        return True
    except WebDriverException:
        return False


def type_test(driver: webdriver.Chrome, mode: str) -> None:
    start_delay, end_delay = get_delay_range()

    print("Klik på lokalhost-testen. Starter om 3 sekunder...")
    sleep(3)

    first_word = get_active_word(driver)

    if not first_word:
        print("Ingen aktiv test fundet. Start testen i Chrome først.")
        return

    written_words = 0
    started_at = monotonic()

    while True:
        active_elements = driver.find_elements(By.CSS_SELECTOR, ".word.active")

        if not active_elements:
            break

        active_element = active_elements[0]
        word = get_active_word(driver)

        if not word:
            break

        print(f"Skriver: {word}")

        for character in word:
            send_character(driver, character)

            if mode == "random":
                sleep(uniform(start_delay, end_delay))
            elif mode == "static":
                sleep(start_delay)
            else:
                # En meget lille pause forhindrer Chrome i at tabe tegn.
                sleep(0.005)

        send_space(driver)
        written_words += 1

        # Vent på, at Monkeytype rent faktisk har godkendt mellemrummet
        # og flyttet markøren til næste ord.
        if not wait_for_next_word(driver, active_element):
            sleep(0.05)

        if not test_is_running(driver):
            break

    duration = monotonic() - started_at
    print(
        f"Færdig! Skrev {written_words} ord på {duration:.1f} sekunder."
    )


def show_visible_words(driver: webdriver.Chrome) -> None:
    words = driver.execute_script("""
        return Array.from(document.querySelectorAll(".word"))
            .map(word => word.textContent.trim())
            .filter(Boolean);
    """)

    print(f"Fandt {len(words)} ord.")
    print(" ".join(words))


def main() -> None:
    print("MONKEYHACK")
    print("Åbner Google Chrome...")

    driver = webdriver.Chrome()

    try:
        driver.get("https://monkeytype.com/login")
        input("Log ind, og tryk Enter her, når du er klar...")

        driver.get("https://monkeytype.com")

        WebDriverWait(driver, 15).until(
            lambda browser: browser.find_element(By.TAG_NAME, "body")
        )

        while True:
            print(
                "\nMONKEYHACK"
                "\n[1] Vis fundne ord"
                "\n[2] Skriv med tilfældig forsinkelse"
                "\n[3] Skriv med fast forsinkelse"
                "\n[4] Skriv hurtigt"
                "\n[9] Afslut"
            )

            choice = input("\nVælg en funktion: ").strip()

            try:
                if choice == "1":
                    show_visible_words(driver)
                elif choice == "2":
                    type_test(driver, "random")
                elif choice == "3":
                    type_test(driver, "static")
                elif choice == "4":
                    type_test(driver, "fast")
                elif choice == "9":
                    break
                else:
                    print("Ugyldigt valg.")

            except ValueError as exc:
                print(f"Fejl: {exc}")

            except WebDriverException as exc:
                print(f"Chrome-fejl: {exc.msg}")
                break

    finally:
        driver.quit()
        print("Chrome er lukket.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgrammet blev afbrudt.")
