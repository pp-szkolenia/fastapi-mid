**2. Implementacja operacji bazodanowych w psycopg2**

Zaimplementuj mechanizmy CRUD dla tabeli `users` z wykorzystaniem psycopg2.

---

**3. Implementacja operacji bazodanowych w SQLalchemy**

Zaimplementuj mechanizmy CRUD dla tabeli `tasks` z wykorzystaniem SQLAlchemy.

---

**4. Model odpowiedzi**

Zmodyfikuj kod endpointów, które odpowiadają tabeli `users`. Dodaj do nich odpowiednie modele odpowiedzi.

---

**5. Query parameters (sortowanie, filtrowanie)**

Dodaj query parameters do endpointów odpowiadającym tabeli `users` tak aby można było:
- wyciągnąć samych adminów albo samych zwykłych użytkowników (albo wszystkich)
- posortować wyciągniętych użytkowników alfabetycznie po ich nazwie
- wyciągnąć tych użytkowników, którzy mają hasło równe lub krótsze niż *x* znaków (znajdź sposób na przefiltrowanie długości tekstu)
- nie wyświetlać informacji o tym, jakie obecnie dane ma użytkownik po modyfikacji rekordu

