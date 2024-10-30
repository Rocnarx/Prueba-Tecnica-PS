from datetime import datetime
import pandas as pd
import numpy as np
import json

products = [
    {"codigo": "JO-001", "nombre": "Chocolate Amargo", "tipo": "dulce", "valor": 500},
    {"codigo": "JO-002", "nombre": "Gomitas", "tipo": "dulce", "valor": 300},
    {"codigo": "JO-003", "nombre": "Caramelo", "tipo": "dulce", "valor": 200},
    {"codigo": "JO-004", "nombre": "Chicle Menta", "tipo": "dulce", "valor": 100},
    {"codigo": "JO-005", "nombre": "Agua Mineral", "tipo": "bebida", "valor": 1600},
    {"codigo": "JO-006", "nombre": "Papas Fritas", "tipo": "snack", "valor": 1200},
    {"codigo": "JO-007", "nombre": "Gaseosa", "tipo": "bebida", "valor": 2500},
    {"codigo": "JO-008", "nombre": "Maní Salado", "tipo": "snack", "valor": 500}
  ]
  

buyers =  [
    {
      "nombre": "José",
      "fecha": "2024-10-01",
      "compras": [
        {"codigo": "JO-001", "cantidad": 4},
        {"codigo": "JO-002", "cantidad": 1}
      ]
    },
    {
      "nombre": "Ana López",
      "fecha": "2024-10-02",
      "compras": [
        {"codigo": "JO-003", "cantidad": 10},
        {"codigo": "JO-005", "cantidad": 1}
      ]
    }
  ]

df_products = pd.DataFrame(products)

buyer_data = []
for buyer in buyers:
    for buy in buyer["compras"]:
        buyer_data.append({
            "nombre": buyer["nombre"],
            "fecha": buyer["fecha"],
            "codigo": buy["codigo"],
            "cantidad": buy["cantidad"]
        })

df_buyers = pd.DataFrame(buyer_data)
print(df_buyers)

df_buyers_transform = df_buyers
for index, row in df_buyers_transform.iterrows():
    value_product = df_products[df_products["codigo"] == row["codigo"]]["valor"].values[0]
    df_buyers_transform.loc[index, 'total'] = row["cantidad"] * value_product
    #df_buyers_transform.loc[index, 'codigo'] = df_products[df_products["codigo"] == row["codigo"]]["nombre"].values[0]
    
#df_buyers_transform.rename(columns={'codigo' : 'compra'}, inplace=True)
df_buyers_transform['fecha'] = pd.to_datetime(df_buyers_transform['fecha'])
df_buyers_transform['week'] = df_buyers_transform['fecha'].dt.isocalendar().week
weeks = df_buyers_transform['week'].unique()
print(df_buyers)

top3Week = []

for week in weeks:
    df_semana = df_buyers_transform[df_buyers_transform['week'] == week]

    buyersdf = df_semana[df_semana['nombre'].notnull()].groupby('nombre')['total'].sum().reset_index()
    buyersdf_top3 = buyersdf.sort_values(by='total', ascending=False).head(3)
    buyersdf_list = [{'nombre': row['nombre'], 'total': row['total']} for _, row in buyersdf_top3.iterrows()]

    items = df_semana.groupby('codigo')['total'].sum().reset_index()
    items_top3 = items.sort_values(by='total', ascending=False).head(3)
    items_list = [{'codigo': row['codigo'], 'total': row['total']} for _, row in items_top3.iterrows()]

    top3Week.append({
        'semana': week,
        'compradores': buyersdf_list,
        'articulos': items_list
    })

    TopDay = []
dates = df_buyers_transform['fecha'].unique()

for date in dates:
    # Eliminar datos nullos
    df_day = df_buyers_transform[df_buyers_transform['fecha'] == date].dropna(subset=['nombre', 'total'])
    
    # Verificar si existe algun datos que sean invalido
    if df_day.empty:
        continue
    
    topbuyer = df_day.groupby('nombre')['total'].sum().reset_index().sort_values(by='total', ascending=False).iloc[0]
    namebuyer = topbuyer['nombre']
    
    dfbuyers = df_day[df_day['nombre'] == namebuyer].dropna(subset=['cantidad'])
    
    df_dulces = dfbuyers.merge(df_products[df_products['tipo'] == 'dulce'], on='codigo', how='inner')
    if not df_dulces.empty:
        dulce_max = df_dulces.sort_values(by='cantidad', ascending=False).iloc[0]['nombre_y']
    else:
        dulce_max = None 
    
    TopDay.append({
        'fecha': date,
        'comprador': namebuyer,
        'dulce': dulce_max
    })

for day in TopDay:
    day['fecha'] = pd.to_datetime(day['fecha']).strftime('%Y-%m-%d')
for week in top3Week:
    week['semana'] = int(week['semana'])
resultado = [
    {'porDia': TopDay},
    {'porSemana': top3Week}
]

print(resultado)