**1. Hashowanie haseł**

Usuń wszystkie rekordy z tabeli `users` a następnie dodaj kilku nowych użytkowników. Zapamiętaj ich hasła, ponieważ nie będzie możliwości ich ponownego odczytania.


**2. Uwierzytelnianie i autoryzacja**

Umieść wartości stałych `SECRET_KEY`, `ALGORITHM` oraz `ACCESS_TOKEN_EXPIRE_MINUTES` w zmiennych środowiskowych w pliku .env, skąd zostaną wczytane i użyte.

Następnie dodaj mechanizm autoryzacji tak aby:
- tylko admin mógł wykonywać żądania `GET` na użytkownikach
- modyfikacji lub usunięcia użytkownika mógł dokonać wyłącznie admin lub sam ten użytkownik

W tym celu do modelu danych w tokenie należy dodać informację o tym, czy użytkownik jest adminem.


**3. Middleware**

Dodaj middleware, który będzie logował wszystkie wykonane operacje i zapisywał do pliku .json (udającego nierelacyjną bazę danych). Informacje, które powinny być zapisywane to:
- URL endpointa
- metoda HTTP
- znacznik czasu
- kod odpowiedzi
