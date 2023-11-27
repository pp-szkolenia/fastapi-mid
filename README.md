# FastAPI – szkolenie


## Uruchamianie
Aby uruchomić API, należy wykonać w terminalu komendę

`python -m uvicorn app.main:app --reload`

gdzie `app.main` to ścieżka do głównego pliku a `app` to obiekt reprezentujący aplikację.


## Użyte biblioteki
- `fastapi`
- `uvicorn`
- `SQLAlchemy`
- `psycopg2-binary`
- `python-dotenv`
- `passlib[bcrypt]`
- `python-jose[cryptography]`


## Spis treści
### 1. Wprowadzenie
1. Idea aplikacji webowej
2. Protokół HTTP (klient, serwer, zasób, request, response)
3. Endpoint, URL, URI
4. Przykłady API oraz jak się z nimi komunikujemy
5. Przegląd narzędzi (terminal, Postman, JSON viewer)
6. Czym jest REST API
7. Format JSON
8. Type annotation w Pythonie
9. Omówienie projektu

### 2. FastAPI
1. Hello world
2. Ścieżki i routing
3. Metoda POST, request body
4. Pydantic, request body model
5. Pobranie konkretnego zasobu (path parameter)
6. HTTPException i błąd 404
7. JSONResponse zamiast słownika, domyślny `status_code`
8. Metoda DELETE, odpowiedź 204
9. Metoda PUT
10. Struktura projektu - `app.main:app`, modele do osobnego pliku
11. Struktura projektu - podział endpointów na osobne pliki
12. Automatyczna dokumentacja (`/docs`, `/redoc`)

###  3. Bazy danych
1. SQL (postgres), pgAdmin
2. Konfiguracja bazy dla projektu
3. Psycopg2
4. Przechowywanie sekretów
5. SQLAlchemy (ORM)

### 4. CRUD
1. Omówienie poszczególnych liter
2. Implementacja operacji bazodanowych w psycopg2
3. Implementacja operacji bazodanowych w SQLalchemy
4. Model odpowiedzi
5. Query parameters (sortowanie, filtrowanie)

### 5. Pozostałe zagadnienia
1. Hashowanie haseł
2. Uwierzytelnianie i autoryzacja
3. Middleware
4. Frontend aplikacji
