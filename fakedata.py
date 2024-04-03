import json
from faker import Faker
from decimal import Decimal

fake = Faker()

books = []

for i in range(1, 1001):
    book = {
        "model": "books_service.book",
        "pk": i,
        "fields": {
            "title": fake.sentence(nb_words=3),
            "author": fake.name(),
            "cover": fake.random_element(elements=("HARD", "SOFT")),
            "inventory": fake.random_int(min=1, max=100),
            "daily_fee": str(fake.pydecimal(left_digits=2, right_digits=2, positive=True))
        }
    }
    books.append(book)

# Зберігаємо дані у JSON файл
with open('books_data.json', 'w') as f:
    json.dump(books, f, indent=4)
