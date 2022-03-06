import psycopg2

def convert_to_int(str_val):
    if str_val.text == '-':
      return 0
    return int(float(str_val.text.replace(",","")))

def connect(dbname,user,pwd,host,port):
    return psycopg2.connect(f'dbname={dbname} user={user} password={pwd} host={host} port={port}')

def persist_strike_row(conn,strike_row,updated_time,dbhost):
    strike_price = convert_to_int(strike_row[11])
   # conn = psycopg2.connect(f'dbname=postgres user=postgres password=postgres host={dbhost} port=5432')
    cursor = conn.cursor()
    query =  f'''INSERT INTO optionmetrics (strike_price,scrape_time,coi,ccoi,cvol,civ,cltp,poi,pcoi,pvol,piv,pltp) VALUES 
        ({strike_price}, '{updated_time}', {convert_to_int(strike_row[1])}, {convert_to_int(strike_row[2])}, {convert_to_int(strike_row[1])}, 
        {convert_to_int(strike_row[1])},{convert_to_int(strike_row[1])}, {convert_to_int(strike_row[1])}, {convert_to_int(strike_row[1])},
         {convert_to_int(strike_row[1])}, {convert_to_int(strike_row[1])},{convert_to_int(strike_row[1])})'''
    #print(query)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close