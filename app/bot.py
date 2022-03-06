from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium import webdriver
import sys
from dbconn import postgres

try:
    arguments = len(sys.argv) - 1
    dbhost = "localhost" if arguments == 0 else sys.argv[1]
    seleniumhost = "localhost" if arguments == 0  else sys.argv[2]
    
    print("Remote Driver - Connecting")
    driver = webdriver.Remote(desired_capabilities=DesiredCapabilities.FIREFOX, 
                                    command_executor=f'http://{seleniumhost}:4444/wd/hub')
    print("Remote Driver - Connected")

    driver.get("https://nseindia.com/option-chain")
    sleep(5)

    strike_element = driver.find_element(By.XPATH,"//span[@id='equity_underlyingVal']").text
    updated_time_ele = driver.find_element(By.XPATH,"//span[@id='equity_timeStamp']").text
    updated_time = updated_time_ele.split(" ")[2] + ' ' + updated_time_ele.split(" ")[3]
    print("Strike element: " + strike_element)

    table_rows = driver.find_elements(By.XPATH, "//table[@id=\"optionChainTable-indices\"]/tbody/tr")

    conn = postgres.connect("postgres","postgres","postgres",dbhost,5432)
    for table_row in table_rows:
        strike_row = table_row.find_elements(By.TAG_NAME,"td")
        postgres.persist_strike_row(conn,strike_row,updated_time,dbhost)
        print(f'inserting strike: {strike_row[11]}')

finally:
    if conn is not None: conn.close()
    if driver is not None: driver.quit() 

#TODO handle exceptions to gracefully exit the browser
#TODO retry 3 times when driver.get fails

##TODO write the data to a file in addition to db
#TODO github check-in
