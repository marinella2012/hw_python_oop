import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        now_date = dt.date.today()
        return sum(
            record.amount
            for record in self.records
            if record.date == now_date
        )

    def get_week_stats(self):
        now_date = dt.date.today()
        week_ago = now_date - dt.timedelta(days=6)
        return sum(
            record.amount
            for record in self.records
            if week_ago <= record.date <= now_date
        )

    def get_today_balance(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE = 60.5
    EURO_RATE = 70.4

    def get_today_cash_remained(self, currency):
        today_balance = self.get_today_balance()
        if today_balance == 0:
            return 'Денег нет, держись'
        currencies = {
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
            'rub': (1, 'руб'),
        }
        cur, cur_info = currencies[currency]
        if currency not in currencies:
            return 'Валюта не поддерживается'
        today_stock_currency = round(today_balance / cur, 2)
        if today_balance > 0:
            return ('На сегодня осталось '
                   f'{today_stock_currency} {cur_info}')
        abs_today = abs(today_stock_currency)    
        return ('Денег нет, держись: твой долг - '
                f'{abs_today} {cur_info}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        delta = self.get_today_balance()
        if delta > 0:
            return (
                'Сегодня можно съесть что-нибудь ещё, '
                f'но с общей калорийностью не более {delta} кКал')
        return 'Хватит есть!'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = date
        if self.date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


if __name__ == "__main__":
    cash_calculator = CashCalculator(2400)
    r1 = Record(amount=145, comment="Безудержный шопинг")
    r2 = Record(amount=168, comment="Наполнение потребительской корзины")
    r3 = Record(amount=691, comment="Катание на такси", date="08.10.2020")
    cash_calculator.add_record(r1)
    cash_calculator.add_record(r2)
    cash_calculator.add_record(r3)
    print(cash_calculator.get_today_stats())
    print(cash_calculator.get_today_cash_remained("rub"))
    print(cash_calculator.get_today_cash_remained("usd"))
    print(cash_calculator.get_today_cash_remained("eur"))
    print(cash_calculator.get_week_stats())
    print()
    calories_calculator = CaloriesCalculator(1100)
    calories_calculator.add_record(Record(amount=500, comment="кофе"))
    calories_calculator.add_record(Record(amount=500, comment="пироженка"))
    calories_calculator.add_record(
        Record(amount=500, comment="бар", date="06.10.2020"))
    print(calories_calculator.get_calories_remained())
    print(calories_calculator.get_week_stats())
