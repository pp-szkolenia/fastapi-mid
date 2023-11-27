**1. Omówienie poszczególnych liter**

- CREATE – tworzenie zasobów (zapytanie INSERT, metoda POST)
- READ – odczyt zasobów (zapytanie SELECT, metoda GET)
- UPDATE – modyfikacja zasobów (zapytanie UPDATE, metoda PUT)
- DELETE – usuwanie zasobów (zapytanie DELETE, metoda DELETE)

---

**2. Implementacja operacji bazodanowych w psycopg2**

- Tworzymy połączenie oraz kursor
- Wykonujemy zapytanie (z możliwością zwrócenia przez bazę dodawanego/modyfikowanego zasobu)
- Zamykamy połączenie oraz kursor
- Formatowanie parametryczne zapobiega SQL injection

---

**3. Implementacja operacji bazodanowych w SQLalchemy**

- Operacje CRUD wykonywane są na obiektach a ORM mapuje je na SQL

---


**4. Model odpowiedzi**

- Aby dodać mechanizm kontroli poprawności schematu odpowiedzi używamy modelu odpowiedzi
- Model odpowiedzi nie powinien być używany kiedy zwracamy obiekt typu `Response` albo `JSONResponse`
- Model odpowiedzi powinien dokładnie odpowiadać strukturze zwracanego JSONa

---

**5. Query parameters (sortowanie, filtrowanie)**

- Query parameters są używane zazwyczaj do sortowania oraz filtrowania danych
- Można ich używać także do innych zastosowań, np. jako informacja o tym, w jaki sposób zwrócić odpowiedź
- Można łączyć path parameters razem z query parameters

---
