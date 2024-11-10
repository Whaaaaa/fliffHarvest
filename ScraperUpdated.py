from datetime import datetime, timedelta
import requests
from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv
import io
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

username = "nbenezra"
password = "5Zi5JQ!xwn6nDUj"
collected_data = []
collected_data2 = []

def send_error_email(error_list):
    sender_email = "benezra.noah@gmail.com"
    sender_password = "xgdu cvhq ehip gahr"
    recipient_email = "noah.benezra@solidcam.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "List of String IDs"

    ids_string = "\n".join(error_list)
    message.attach(MIMEText(ids_string, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email successfully sent to", recipient_email)
    except Exception as e:
        print("Error sending email:", e)

def setup_and_login(username, password):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get("https://dsxclient.3ds.com/psp/CRPRD/EMPLOYEE/DS_ECO/c/CRM_MENU.CRML_MODLIC.GBL?FolderPath=PORTAL_ROOT_OBJECT.CRML.CRML_MODLIC_GBL&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    username_field = driver.find_element(By.NAME, "username")
    username_field.send_keys(username)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "refuse")))

    driver.find_element(By.CLASS_NAME, "refuse").click()
    driver.find_element(By.CLASS_NAME, 'uwa-submit').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    print('Logging In...')
    WebDriverWait(driver, 10).until(EC.title_contains("My Page"))

    return driver

def search_orders(driver):
    driver.get("https://dsxclient.3ds.com/psp/CRPRD/EMPLOYEE/DS_ECO/c/CRM_MENU.CRML_ORDSRCH.GBL?FolderPath=PORTAL_ROOT_OBJECT.CRML.CRML_ORDSRCH_GBL&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder")
    WebDriverWait(driver, 50).until(EC.title_contains("Search License Key Order"))
    iframe = driver.find_element(By.ID, 'ptifrmtgtframe')
    driver.switch_to.frame(iframe)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CRML_ORDSCH_WRK_CRM_LSTDATEINF")))

    search_field = driver.find_element(By.CSS_SELECTOR, '[id="CRML_ORDSCH_WRK_CRM_LSTDATEINF"]')
    search_field.clear()
    search_field2 = driver.find_element(By.CSS_SELECTOR, '[id="CRML_ORDSCH_WRK_CRM_LSTDATESUP"]')
    search_field2.clear()

    #start_date = (datetime.now() - timedelta(days=1)).strftime('%m/%d/%Y')
    start_date= '06/27/2024'
    search_field.send_keys(start_date)
    search_field.send_keys(Keys.RETURN)

    WebDriverWait(driver, 500).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))
    table = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, 'CRML_ORDSCH_VW$scroll$0')))
    rows = table.find_elements(By.TAG_NAME, 'tr')[6:]

    row_list = [row.find_elements(By.TAG_NAME, 'td')[0].text for row in rows]
    print("Making List of All Modified License Keys: ")
    print(row_list)

    return row_list

def process_license_keys(driver, row_list, tekyaz):
    site_id_list = []

    for lko_nb in row_list:
        url = f"https://dsxclient.3ds.com/psp/CRPRD_58/EMPLOYEE/DS_ECO/c/CRM_MENU.CRML_ORD.GBL?Page=CRML_ORDFORM&Action=U&ForceSearch=Y&CRML_ORDID={lko_nb}"
        print('Searching for License Key:', lko_nb)
        driver.get(url)
        WebDriverWait(driver, 50).until(EC.title_contains("Search License Key Order"))
        iframe = driver.find_element(By.ID, 'ptifrmtgtframe')
        driver.switch_to.frame(iframe)
        site_id = driver.find_element(By.ID, 'CRML_ORD_CRML_ORDCUST$69$').text
        site_name = driver.find_element(By.ID, 'CRM_SITENAME_V2_CRM_SITENAME').text
        print('Customer Name:', site_name)

        if site_name != 'SOLIDCAM LTD':
            site_id_list.append(site_id)

    site_id_list = list(set(site_id_list))
    print('Site ID List without Duplicates:', ', '.join(site_id_list))

    return site_id_list

def process_site_ids(driver, site_id_list, tekyaz):
    error_list = []

    for site_id in site_id_list:
        print('Searching for Site ID#', site_id)
        driver.get("https://dsxclient.3ds.com/psp/CRPRD_58/EMPLOYEE/DS_ECO/c/CRM_MENU.CRM_SITESRCH.GBL")
        WebDriverWait(driver, 10).until(EC.title_contains("Search Site"))
        iframe = driver.find_element(By.ID, 'ptifrmtgtframe')
        driver.switch_to.frame(iframe)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CRM_SITESRCHWK_CRM_SITEID")))

        search_field = driver.find_element(By.CSS_SELECTOR, '[id="CRM_SITESRCHWK_CRM_SITEID"]')
        search_field.clear()
        search_field.send_keys(site_id)
        search_field.send_keys(Keys.RETURN)

        try:
            WebDriverWait(driver, 5000).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))
            customer_name = driver.find_element(By.ID, 'CRM_CUSTHEAD_VW_CRM_SITENAME$160$').text
        except (NoSuchElementException, TimeoutException):
            try:
                table = driver.find_element(By.CLASS_NAME, "PSLEVEL1GRID")
                detail_rows = table.find_elements(By.TAG_NAME, 'tr')[1:]
                for row in detail_rows:
                    site_name_int = row.find_elements(By.TAG_NAME, 'td')[1].text
                    if site_name_int == site_id:
                        row.find_elements(By.TAG_NAME, 'td')[0].find_element(By.TAG_NAME, 'a').click()
                        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))
                        break
            except (NoSuchElementException, TimeoutException):
                print('Error', site_id)
                error_list.append(site_id)
                continue

        try:
            driver.find_element(By.ID, 'ICTAB_4').click()
        except (NoSuchElementException, TimeoutException):
            print('Error', site_id)
            error_list.append(site_id)
            continue

        WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.ID, 'CRML_MODLIC_WRK_CRML_SHOW1_LBL')))
        process_license_details(driver, site_id, customer_name, tekyaz)

    return error_list

def process_license_details(driver, site_id, customer_name, tekyaz):
    deactivated_nb = driver.find_element(By.ID, "CRML_MODLIC_WRK_CRML_SHOWNB1").text
    if deactivated_nb != '0':
        driver.find_element(By.ID, "CRML_MODLIC_WRK_CRML_SHOW1").click()
        driver.find_element(By.ID, "CRML_MODLIC_WRK_CRML_BUTSRCHLIC").click()
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, 'CRML_INSTBAS_VW$scroll$0')))

        table = driver.find_element(By.ID, 'CRML_INSTBAS_VW$scroll$0')
        rows = table.find_elements(By.TAG_NAME, 'tr')[6:]

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            record = {
                "Name": cells[15].text,
                "Product__c": cells[6].text,
                "SolidWorks_Customer_ID__c": site_id,
                "Network_License__c": cells[10].text == 'SW Network',
                "Users__c": cells[11].text,
                "SeatId__c": cells[17].text,
                "Subscription_Termination_Date__c": datetime.strptime(cells[14].text, '%m/%d/%Y').date().isoformat(),
                "Term_License__c": cells[9].text == 'ALC',
                "Final_Customer_Name__c": customer_name,
                "Usage__c": cells[9].text,
                "Type__c": cells[10].text,
                "GMBH__c": tekyaz
            }
            collected_data.append(record)

    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "ICTAB_3"))).click()
    WebDriverWait(driver, 100).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))

    terminated_nb = driver.find_element(By.ID, "CRM_IB_VIEW_WRK_CRM_IB_SHOWTN3").text
    if terminated_nb != '0':
        driver.find_element(By.ID, "CRM_IB_VIEW_WRK_CRM_IB_SHOW3").click()
        driver.find_element(By.ID, "CRM_IB_COM2_WRK_IB_SEARCH_PB").click()

        table = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, 'CRM_IBDUMMY3$scroll$0')))
        rows = table.find_elements(By.TAG_NAME, 'tr')[1:]

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            record = {
                "Original_Order_Type__c": cells[15].text,
                "Subscription_End_Date__c": datetime.strptime(cells[12].text, '%b %d, %Y').date().isoformat(),
                "Subscription_start_date__c": datetime.strptime(cells[11].text, '%b %d, %Y').date().isoformat(),
                "SeatId__c": cells[8].text
            }
            collected_data2.append(record)

def authenticate_salesforce():
    sf_username = "noah.benezra@solidcam.com"
    sf_password = "MoonyMoshe35"
    sf_security_token = "SXzP8NXk1rzyJi1iNRWxxNxsC"
    sf_client_id = "3MVG9WtWSKUDG.x6iIGrpPBJuD9aAqVvgdku3fI3GyG4ysHQb2e1qmurOX5IfXmoUUo6Y22BUia_XKxdVCkB6"
    sf_client_secret = "3F3D710FE90E17F4E9F2EF0F00311AA564B2B9AD1E08CEFF16B0708CEAE59442"
    sf_instance = "https://solid.my.salesforce.com/"

    sf_auth_endpoint = f"{sf_instance}/services/oauth2/token"
    sf_auth_payload = {
        "grant_type": "password",
        "client_id": sf_client_id,
        "client_secret": sf_client_secret,
        "username": sf_username,
        "password": f"{sf_password}{sf_security_token}",
    }

    sf_auth_response = requests.post(sf_auth_endpoint, data=sf_auth_payload)
    sf_auth_response_json = sf_auth_response.json()
    sf_access_token = sf_auth_response_json.get("access_token")

    if not sf_access_token:
        print(json.dumps({"error": "Authentication failed"}))
        return None

    return sf_access_token

def upload_to_salesforce(sf_access_token, collected_data, sf_object_api_name):
    sf_instance = "https://solid.my.salesforce.com/"
    sf_object_endpoint = f"{sf_instance}/services/data/v52.0/jobs/ingest"

    sf_headers = {
        "Authorization": f"Bearer {sf_access_token}",
        "Content-Type": "application/json",
    }

    job_definition = {
        "operation": "insert",
        "object": sf_object_api_name,
        "contentType": "CSV",
        "lineEnding": "CRLF",
    }

    job_response = requests.post(sf_object_endpoint, headers=sf_headers, json=job_definition)
    job_response_json = job_response.json()
    job_id = job_response_json.get('id')

    if not job_id:
        print(json.dumps({"error": "Failed to create job"}))
        return False

    batch_url = f"{sf_instance}/services/data/v52.0/jobs/ingest/{job_id}/batches"

    csv_io = io.StringIO()
    fieldnames = list(collected_data[0].keys())

    writer = csv.DictWriter(csv_io, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(collected_data)

    csv_data = csv_io.getvalue()
    csv_io.close()

    batch_headers = {
        'Authorization': f'Bearer {sf_access_token}',
        'Content-Type': 'text/csv'
    }

    batch_response = requests.put(batch_url, headers=batch_headers, data=csv_data)

    if batch_response.status_code not in range(200, 299):
        print("Failed to upload batch")
        return False

    job_close_url = f"{sf_instance}/services/data/v52.0/jobs/ingest/{job_id}"
    job_close_response = requests.patch(job_close_url, headers=sf_headers, json={"state": "UploadComplete"})

    if job_close_response.status_code not in range(200, 299):
        print("Failed to close job")
        return False

    return True

def main(tekyaz):
    driver = setup_and_login(username, password)
    row_list = search_orders(driver)
    site_id_list = process_license_keys(driver, row_list, tekyaz)
    error_list = process_site_ids(driver, site_id_list, tekyaz)

    send_error_email(error_list)

    sf_access_token = authenticate_salesforce()
    if not sf_access_token:
        return

    success1 = upload_to_salesforce(sf_access_token, collected_data, "SolidWorks_license__c")
    success2 = upload_to_salesforce(sf_access_token, collected_data2, "Installed_Base__c")

    if success1 and success2:
        print("Data upload initiated successfully")
    else:
        print("Data upload failed")

if __name__ == "__main__":
    main(True)