import http.client
import pandas as pd
import dash
from dash import dcc, html

# Загружаем данные из NocoDB API
def load_data():
    # Укажи свой API токен
    api_token = "O1RmgUMHz73SXi7Tmbilnu7-lqY3Bc4ZA4FqYhhK"

    # Укажи идентификаторы таблицы и представления
    table_id = "mhk38g2tng1cv63"  # Замени на ID своей таблицы
    view_id = "vwukd5wkscz37nmj"  # Замени на ID своего представления

    # Создаём соединение с NocoDB
    conn = http.client.HTTPSConnection("app.nocodb.com")
    headers = { 'xc-token': api_token }

    # Формируем URL для запроса данных
    url = f"/api/v2/tables/{table_id}/records?offset=0&limit=25&where=&viewId={view_id}"

    try:
        # Отправляем GET-запрос
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()

        # Проверяем статус ответа
        if res.status == 200:
            # Читаем данные
            data = res.read()
            json_data = data.decode("utf-8")

            # Преобразуем JSON в DataFrame
            import json
            data_dict = json.loads(json_data)
            return pd.DataFrame(data_dict["list"])  # Данные находятся в ключе "list"
        else:
            print(f"Ошибка: {res.status} - {res.reason}")
            return pd.DataFrame()
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Создаём Dash-приложение
app = dash.Dash(__name__)

# Загружаем данные сразу при запуске
df = load_data()

# Лейаут приложения
app.layout = html.Div([
    html.H1("Items Table from NocoDB"),
    dcc.Link('Go to NocoDB', href='https://app.nocodb.com'),
    html.Br(),
    # Отображаем таблицу сразу
    html.Table(
        # Заголовок таблицы
        [html.Tr([html.Th(col) for col in df.columns])] +
        # Данные таблицы
        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))]
    ) if not df.empty else html.Div("No data available.")
])

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True, port=8050)