import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker


from models import create_tables, Publisher, Shop, Book, Stock, Sale


login = 'postgres'
password = 'postgres'
base = 'postgres'
host = 'localhost:5432'
database = 'postgresql'

DSN = f'{database}://{login}:{password}@{host}/{base}'
engine = sqlalchemy.create_engine(DSN)


Session = sessionmaker(bind=engine)
session = Session()

def open_file():
    with open('test_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def request(name_publisher):

    quer = session.query(Book.title, Shop.name_shop, Sale.date_sale, Sale.price).select_from(Shop).\
    join(Stock, Stock.id_shop == Shop.id).\
    join(Book, Book.id == Stock.id_book).\
    join(Publisher, Publisher.id == Book.id_publisher).\
    join(Sale, Sale.id_stock == Stock.id)

    if name_publisher.isdigit():
        queru = quer.filter(Publisher.id == name_publisher).all()

    else:
        queru = quer.filter(Publisher.name == name_publisher).all()

    for title, name_shop, date_sale, price in queru:  
        print(f'{title}, {name_shop}, {date_sale}, {price}')
       




if __name__ == '__main__':
    create_tables(engine)
    open_file()
    name_publisher = input('Введите издателя: ')
    request(name_publisher)    
