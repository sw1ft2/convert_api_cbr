import requests as re
from bs4 import BeautifulSoup
import decimal
def convert(amount, cur_from, cur_to, date):
    date = str(date)
    resp = re.get(f'https://cbr.ru/scripts/XML_daily.asp?date_req={date}')
    api = resp.content
    soup = BeautifulSoup(api, 'xml')
    try:
        from_val = soup.find('CharCode', text=cur_from).find_next_sibling('Value').string # число денег
        from_nom = soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string # количество за число денег
    except AttributeError:
        from_val = '1'
        from_nom = '1'
    from_val_rep = from_val.replace(',', '.')
    from_nom_rep = from_nom.replace(',', '.')
    from_ = decimal.Decimal(from_val_rep) / decimal.Decimal(from_nom_rep) # проверка число  делем на количество

    amount_res = decimal.Decimal(from_) * decimal.Decimal(amount) # умножаем чило на количество заданных денег
    try:
        to_val = soup.find('CharCode', text=cur_to).find_next_sibling('Value').string # число денег
        to_nom = soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string # количество за число денег
    except AttributeError:
        to_val = '1'
        to_nom = '1'
    to_val_rep = to_val.replace(',', '.')
    to_nom_rep = to_nom.replace(',', '.')
    to_ = decimal.Decimal(to_val_rep) / decimal.Decimal(to_nom_rep) # проверка число  делем на количество
    result = decimal.Decimal(amount_res)/decimal.Decimal(to_)
    return  decimal.Decimal(result).quantize(decimal.Decimal('0.0001'))

print(convert('7000','RUR','USD','31.03.2020'))