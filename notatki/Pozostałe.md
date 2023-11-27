**1. Hashowanie haseł**

- Aby korzystać z hasowania haseł nalezy zainstalować `pip install passlib[bcrypt]`
- Bcrypt jest jednym z algorytmów używanych do hasowania haseł
- Z przyczyn bezpieczeństwa w bazie danych powinny znajdować się wyłącznie zahashowane hasła


**2. Uwierzytelnianie i autoryzacja**

- W celu uwierzytelnienia użytkownika należy sprawdzić poprawność jego danych logowania a następnie wygenerować token JWT, który potwierdza że został on uwierzytelniony przez serwer
- Klient przechowuje token i wysyła go razem z kolejnymi requestami. W ten sposób informuje serwer, że jest tym za kogo się podaje
- Token może wygasnąć po określonym czasie lub nie posiadać okresu ważności
- W tokenie mogą znajdować się informacje na temat uprawnień użytkownika, które posłużą do autoryzacji


**3. Middleware**

- Middleware to funkcja, która zostaje wykonana pomiędzy requestem a odpowiedzią. W swoim działaniu przypomina dekorator
- Funkcja ta powinna wykorzystywać async / await
- Middleware definiujemy dla całej aplikacji a nie pojedynczych endpointów
- Middleware'y można wydzielić do osobnego modułu
