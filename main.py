from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

@app.get("/")
def get_traffic(customer_name: str = None, ip: str = None, date_from: str = None, date_to: str = None):
    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()

    query = '''
        SELECT c.id, c.name, SUM(t.received_traffic)
        FROM traffic t
        JOIN customers c ON t.customer_id = c.id
        WHERE 1=1
    '''
    params = []

    if customer_name:
        query += ' AND c.name = ?'
        params.append(customer_name)
    if ip:
        query += ' AND t.ip = ?'
        params.append(ip)
    if date_from:
        query += ' AND t.date >= ?'
        params.append(date_from)
    if date_to:
        query += ' AND t.date <= ?'
        params.append(date_to)

    query += ' GROUP BY c.id, c.name'

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()

    if not results:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    response = []
    for row in results:
        data = {
            "customer_id": row[0],
            "customer_name": row[1],
            "total_traffic": row[2]
        }
        response.append(data)

    return response
