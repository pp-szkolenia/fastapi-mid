**1. Hello world**

- Aplikacja to obiekt klasy `FastAPI`
- Uruchamiamy ją w terminalu poprzez `uvicorn`
- Endpoint to kombinacja methody HTTP oraz ścieżki, którą nalezy zarequestować, żeby go wywołać

---

**2. Ścieżki i routing**

- Routing to mapowanie requestowanego adresu do wykonywanej operacji
- Definiując ścieżki poszczególnych endpointów, określamy w jaki sposób można wywoływać dane funkcje API
- Metoda `GET` jest używana do pobierania zasobów z bazy danych

---

**3. Metoda POST, request body**

- Postman jako klient HTTP (zwłaszcza dla metod innych niż `GET`)
- W celu stworzenia nowego zasobu używamy metody `POST`
- Możemy przesłać dane do serwera w postaci request body
- Obecnie nie mamy kontroli nad modelem body w requeście

---

**4. Pydantic, request body model**

- Pydantic BaseModel jest mechanizmem kontroli modelu request body 
- Od Pythona 3.10 zamiast `typing.Optional[]` można używać notacji z `|`
- Utworzona klasa powinna być użyta w type annotation
- Metoda `model_dump()` zamienia body na słownik
- Warto nadawać zasobom numery id w celu ich identyfikacji

---

**5. Pobranie konkretnego zasobu (path parameter)**

- W celu pobrania konkretnego zasobu korzystamy z path parameter
- Dla path parameters należy stosować type annotation
- Logika znalezienia właściwego zasobu musi zostać zaimplementowana przez nas

---

**6. HTTPException i błąd 404**

- W przypadku niewłaściwego requestu, możemy podnieść wyjątek HTTPException
- Należy zdefiniować kod błędu oraz wiadomość w formacie JSON

---

**7. JSONResponse zamiast słownika, domyślny status_code**

- Zamiast zwracać słownik, możemy zwrócić obiekt JSONResponse, który posiada customizowalny status_code
- To, jaki kod odpowiedzi nadamy zależy od nas, ale powinniśmy używać ich zgodnie z przeznaczeniem
- Możemy zdefiniować domyślny status_code endpointa poprzez modyfikację dekoratora przy nim
- Stworzenie nowego zasobu powinno zwracać kod `201`

---

**8. Metoda DELETE, odpowiedź 204**

- Aby usunąć zasób używamy metody `DELETE`
- Możemy zwrócić odpowiedź bez treści w formacie JSON. Kodem odpowiedzi powinno być `204`

---

**9. Metoda PUT**

- Aby zmodyfikować zasób używamy metody `PUT`
- Po modyfikacji należy zwrócić kod `200`

---

**10. Struktura projektu - app.main:app, modele do osobnego pliku**

- Zaleca się trzymać cały kod źródłowy w folderze `src/`, a pliki związane z API w podfolderze `app/`. Główna część aplikacji powinna znajdować się w pliku `main.py`
- Modele pydantica warto trzymać w osobnym pliku dla większego porządku

---

**11. Struktura projektu - podział endpointów na osobne pliki**

- Endpointy można trzymać w osobnych plikach, podzielonych np. na podstawie zasobów, do których się one odnoszą. Służy do tego klasa `APIRouter`
- Funkcje pomocnicze również warto przechowywać w oddzielnych plikach

---

**12. Automatyczna dokumentacja (/docs, /redoc)**

- W celu wygenerowania dokumentacji w formacie swagger wywołujemy endpoint `GET /docs`
- W celu wygenerowania dokumentacji w formacie redoc wywołujemy endpoint `GET /redoc`
- Wygląd dokumentacji można customizować
