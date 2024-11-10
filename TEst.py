from datetime import datetime, timedelta  # Import the datetime class from the datetime module
import requests
from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import csv
import io
import sys

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#e.msgbox("An error has occured! :(", "Error")
username = "nbenezra"
password = "5Zi5JQ!xwn6nDUj"
collected_data =[]
collected_data2 = []


# Open a file in write mode ('w') for stdout
#sys.stdout = open('output_log.txt', 'w')

# Open a file in write mode ('w') for stderr
#sys.stderr = open('error_log.txt', 'w')

def sendErrorEmail(errorList):
    # Your email credentials
    sender_email = "benezra.noah@gmail.com"
    sender_password = "xgdu cvhq ehip gahr"

    # Recipient email
    recipient_email = "noah.benezra@solidcam.com"

    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "List of String IDs"

    # List of IDs you want to send
    list_of_ids = errorList  # Add your IDs here
    # Convert the list of strings into a single string message
    ids_string = "\n".join(list_of_ids)

    # Attach the IDs string to the message
    message.attach(MIMEText(ids_string, "plain"))

    # Send the email
    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection with TLS
            server.login(sender_email, sender_password)  # Log in to the SMTP server
            server.sendmail(sender_email, recipient_email, message.as_string())  # Send the email
        print("Email successfully sent to", recipient_email)
    except Exception as e:
        print("Error sending email:", e)

def setup_and_login(username, password):
    """
    Sets up the browser, logs in to the website, and returns the WebDriver object.

    Parameters:
    username (str): The username for login.
    password (str): The password for login.

    Returns:
    WebDriver: The WebDriver object after logging in.
    """
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Enables headless mode

    driver = webdriver.Chrome(options=options)


    # Navigate to the login page
    driver.get("https://dsxclient.3ds.com/psp/CRPRD/EMPLOYEE/DS_ECO/c/CRM_MENU.CRML_MODLIC.GBL?FolderPath=PORTAL_ROOT_OBJECT.CRML.CRML_MODLIC_GBL&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    # Find the username and password fields and enter the credentials
    username_field = driver.find_element(By.NAME, "username")
    username_field.send_keys(username)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "refuse")))

    driver.find_element(By.CLASS_NAME, "refuse").click()
    clickContinue = driver.find_element(By.CLASS_NAME, 'uwa-submit').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)

    # Submit the login form
    password_field.send_keys(Keys.RETURN)
    print('Logging In...')

    # Wait for the page to load after login
    WebDriverWait(driver, 10).until(EC.title_contains("My Page"))

    return driver

def process_accounts():
    driver = setup_and_login(username, password)
    errorList = []
    driver.get(
        "https://dsxclient.3ds.com/psp/CRPRD/EMPLOYEE/DS_ECO/c/CRM_MENU.CRML_ORDSRCH.GBL?FolderPath=PORTAL_ROOT_OBJECT.CRML.CRML_ORDSRCH_GBL&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder")
    WebDriverWait(driver, 10).until(EC.title_contains("Search License Key Order"))
    iframe = driver.find_element(By.ID, 'ptifrmtgtframe')
    driver.switch_to.frame(iframe)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CRML_ORDSCH_WRK_CRM_LSTDATEINF")))
    LastAction_search_field = driver.find_element(By.CSS_SELECTOR, '[id="CRML_ORDSCH_WRK_CRM_LSTDATEINF"]')
    LastAction_search_field.clear()
    today = (datetime.now() - timedelta(days=1))
    print('Searching For Orders Updated Since Yesterday...')
    # Format today's date as MM/DD/YYYY
    startDate = today.strftime('%m/%d/%Y')
    # Process each account here
    # startDate= '02/05/2024'
    LastAction_search_field.send_keys(startDate)
    LastAction_search_field.send_keys(Keys.RETURN)
    WebDriverWait(driver, 500).until(
        EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))
    table = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, 'CRML_ORDSCH_VW$scroll$0')))
    table_locator = driver.find_element(By.ID, 'CRML_ORDSCH_VW$scroll$0')
    rows = table.find_elements(By.TAG_NAME, 'tr')[6:]
    rowList = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        license_serial_number = cells[0]
        rowList.append(license_serial_number.text)
        testIterator = 0
    print("Making List of All Modified License Keys: ")
    print(rowList)
    siteIdList = []

    for lkoNb in rowList:
            url = f"https://dsxclient.3ds.com/psp/CRPRD_67/EMPLOYEE/DS_ECO/c/CRM_MENU.CRML_ORD.GBL?Page=CRML_ORDFORM&Action=U&ForceSearch=Y&CRML_ORDID={lkoNb}"
            print('Searching for License Key: ' + lkoNb)
            driver.get(url)
            WebDriverWait(driver, 50).until(EC.title_contains("Search License Key Order"))
            iframe = driver.find_element(By.ID, 'ptifrmtgtframe')
            driver.switch_to.frame(iframe)
            siteId = driver.find_element(By.ID, 'CRML_ORD_CRML_ORDCUST$69$')
            siteIdText = siteId.text
            siteName = driver.find_element(By.ID, 'CRM_SITENAME_V2_CRM_SITENAME')
            siteNameText = siteName.text
            print('Customer Name: ' + siteName.text)
         #   customerName = siteName.text
            if (siteNameText != 'SOLIDCAM LTD'):
                siteIdList.append(siteIdText)
    siteIdlist_without_duplicates = list(set(siteIdList))
    print('Site ID List without Duplicates: ' + ', '.join(siteIdlist_without_duplicates))
    for siteIdIter in siteIdlist_without_duplicates:
            print('Searching for Site ID# ' + siteIdIter)
            driver.get(
                "https://dsxclient.3ds.com/psp/CRPRD/EMPLOYEE/DS_ECO/c/CRM_MENU.CRM_SITESRCH.GBL?&cmd=uninav&Rnode=LOCAL_NODE&uninavpath=Root%7bPORTAL_ROOT_OBJECT%7d.Sites%20Master%20Data%7bTIS_SITES_MD%7d.Sites%7bTIS_SITES%7d&PORTALPARAM_PTCNAV=CRM_SITESRCH_GBL&EOPP.SCNode=DS_ECO&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=TIS_SITES&EOPP.SCLabel=Sites&EOPP.SCPTfname=TIS_SITES&FolderPath=PORTAL_ROOT_OBJECT.TIS_SITES_MD.TIS_SITES.CRM_SITESRCH_GBL&IsFolder=false")
            WebDriverWait(driver, 10).until(EC.title_contains("Search Site"))
            iframe = driver.find_element(By.ID, 'ptifrmtgtframe')
            driver.switch_to.frame(iframe)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CRM_SITESRCHWK_CRM_SITEID")))
            search_field = driver.find_element(By.CSS_SELECTOR, '[id="CRM_SITESRCHWK_CRM_SITEID"]')
            search_field.clear()
            search_field.send_keys(siteIdIter)
            search_field.send_keys(Keys.RETURN)
            try:
                WebDriverWait(driver, 5000).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))
                print ("Waiting")

                wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'ICTAB_4')))
                customerName = driver.find_element(By.ID, 'CRM_CUSTHEAD_VW_CRM_SITENAME$160$').text


            except (NoSuchElementException, TimeoutException):
                try:
                    wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'win0divCRM_SITESRCH_VW$0')))
                    table= driver.find_element(By.CLASS_NAME, "PSLEVEL1GRID")
                    detailRows = table.find_elements(By.TAG_NAME, 'tr')[1:]  # Skip the header row
                    for indRow in detailRows:
                        detailCells = indRow.find_elements(By.TAG_NAME, 'td')
                        siteNameInt = detailCells[1].text
                        print('Searching for Site Name: ' ,siteNameText," Current Site Name: ", siteNameInt)
                        if siteNameInt == siteNameText:
                            print('Found Site')
                            detailCells[0].find_element(By.TAG_NAME, 'a').click()
                            WebDriverWait(driver, 10).until(
                                EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))

                            break
                except(NoSuchElementException, TimeoutException):
                    print('Error ', siteIdIter)
                    errorList.append(siteIdIter)
                    continue

            try:
                tab_locator = (By.ID, 'ICTAB_4')
                element = driver.find_element(*tab_locator)
                element.click()
            except(NoSuchElementException, TimeoutException):
                print('Error ', siteIdIter)
                errorList.append(siteIdIter)
                continue
            loaded = WebDriverWait(driver, 500).until(
                EC.presence_of_element_located((By.ID, 'CRML_MODLIC_WRK_CRML_SHOW1_LBL')))
            deactivatedNb = driver.find_element(By.ID, "CRML_MODLIC_WRK_CRML_SHOWNB1").text
            print("Deactivated Licenses: ", deactivatedNb)
            if (deactivatedNb != 0):
                driver.find_element(By.ID, "CRML_MODLIC_WRK_CRML_SHOW1").click()
                driver.find_element(By.ID, "CRML_MODLIC_WRK_CRML_BUTSRCHLIC").click()
            try:
                table = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, 'CRML_INSTBAS_VW$scroll$0')))
            except (NoSuchElementException, TimeoutException):
                continue
            table_locator = driver.find_element(By.ID, 'CRML_INSTBAS_VW$scroll$0')
            iterator = 0
            rows2 = table_locator.find_elements(By.TAG_NAME, 'tr')[6:]
            for i in range(len(rows2)):
                table = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'CRML_INSTBAS_VW$scroll$0')))
                newtable =  driver.find_element(By.ID, 'CRML_INSTBAS_VW$scroll$0')
                rows2 = table.find_elements(By.TAG_NAME, 'tr')[(6+iterator)]
                cells = rows2.find_elements(By.TAG_NAME, 'td')
                license_serial_number = cells[15].text
                print('   Serial Number ' + license_serial_number)
                productName = cells[6].text
                print('   Product Name ' + productName)
                type = cells[10].text
                networkLicense = ''
                if type == 'SW Network':
                    networkLicense = True
                print('   networkLicense ' + str(networkLicense))
                print('   type ' + type)
                quantity = cells[11].text
                print('   Quantity ' + quantity)
                usage = cells[9].text
                termLicense =''
                if usage == 'ALC':
                    termLicense = True
                print('   termLicense ' + str(termLicense))
                print('   usage ' + usage)

                start_date = cells[13].text
                print('   Start Date ' + start_date)
                formatted_date_start = datetime.strptime(start_date, "%m/%d/%Y").date()
                formatted_date_start2 = formatted_date_start.isoformat()
                termination_date = cells[14].text
                formatted_date_termination = datetime.strptime(termination_date, '%m/%d/%Y').date()
                formatted_date_formatted_date_termination2 = formatted_date_termination.isoformat()
                print('   Termination Date ' + formatted_date_formatted_date_termination2)
                onlineInstance = cells[17].text
                print('   Online Instance ' + onlineInstance)
                WebDriverWait(driver, 5000).until(
                    EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))
                wait = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ICTAB_3' )))

                collected_data.append({
                    "Name": license_serial_number,  # Replace with the actual record name
                    "Product__c": productName,  # Replace with the actual product information
                    "SolidWorks_Customer_ID__c": siteIdIter,
                    "Network_License__c": networkLicense,
                    "Users__c": quantity,
                    "SeatId__c": onlineInstance,
                   # "Subscription_start_date__c": formatted_date_start2,
                    "Subscription_Termination_Date__c": formatted_date_formatted_date_termination2,
                    "Term_License__c": termLicense,
                    "Final_Customer_Name__c" : customerName,
                    "Usage__c": usage,
                    "Type__c": type
                })
                print('New Record JSON:')
                print(collected_data)
                iterator += 1
            tab_locator2 = (By.ID, 'ICTAB_3')
            element = driver.find_element(*tab_locator2)
            element.click()
            loaded = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.ID, 'CRM_IB_VIEW_WRK_CRM_IB_SHOWTN3')))
            WebDriverWait(driver, 100).until(
                EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))
            terminatedNb = driver.find_element(By.ID, "CRM_IB_VIEW_WRK_CRM_IB_SHOWTN3").text
            WebDriverWait(driver, 100).until(
                EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))
            print("Terminated Licenses: ", terminatedNb)
            if (terminatedNb != 0):
                driver.find_element(By.ID, "CRM_IB_VIEW_WRK_CRM_IB_SHOW3").click()
                driver.find_element(By.ID, "CRM_IB_COM2_WRK_IB_SEARCH_PB").click()

            loadedTable = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.ID, 'CRM_IBDUMMY3$scroll$0')))
            table_locator = driver.find_element(By.ID, 'CRM_IBDUMMY3$scroll$0')
            innerTableLocator = table_locator.find_element(By.CLASS_NAME, 'PSLEVEL1GRID')
            rows3 = innerTableLocator.find_elements(By.TAG_NAME, 'tr')[1:]  # Skip the header row
            for licenseRow in rows3:
                formatted_date_exp2 = ''
                formatted_date_start2 = ''

                cellsToCheck = licenseRow.find_elements(By.TAG_NAME, 'td')
                renewal_termination_date = cellsToCheck[12].text
                renewal_start_date = cellsToCheck[11].text
                if cellsToCheck[12].text != 'No Support' and cellsToCheck[12].text != ' ':
                    formatted_date_exp = datetime.strptime(renewal_termination_date, '%b %d, %Y').date()
                    formatted_date_exp2 = formatted_date_exp.isoformat()
                    print('End Date ' + formatted_date_exp2)
                    formatted_date_start = datetime.strptime(renewal_start_date, '%b %d, %Y').date()
                    formatted_date_start2 = formatted_date_start.isoformat()
                    print('Start Date ' + formatted_date_start2)
                orderType = cellsToCheck[15].text
                print('Order Type ' + orderType)

                seatId = cellsToCheck[8].text
                print('Seat ID ' + seatId)
                collected_data2.append({
                     "Original_Order_Type__c" : orderType,
                     "Subscription_End_Date__c" : formatted_date_exp2,
                     "Subscription_start_date__c" : formatted_date_start2,
                     "SeatId__c" : seatId
                })
                print(collected_data2)

    sendErrorEmail(errorList)
    # Salesforce credentials (ensure to keep these secure and not expose in production code)
    sf_username = "noah.benezra@solidcam.com"
    sf_password = "MoonyMoshe35"
    sf_security_token = "SXzP8NXk1rzyJi1iNRWxxNxsC"  # Salesforce security token
    sf_client_id = "3MVG9WtWSKUDG.x6iIGrpPBJuD9aAqVvgdku3fI3GyG4ysHQb2e1qmurOX5IfXmoUUo6Y22BUia_XKxdVCkB6"
    sf_client_secret = "3F3D710FE90E17F4E9F2EF0F00311AA564B2B9AD1E08CEFF16B0708CEAE59442"
 #   sf_token = "n5fXl22G2JZsAxZTO8OjGmFQP"
    sf_instance = " https://solid.my.salesforce.com/"  # Replace with your Salesforce instance URL

    # Authenticate with Salesforce
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
    print(sf_access_token)
    if not sf_access_token:
        # Handle authentication failure
        print(json.dumps({"error": "Authentication failed"}))
        return  # Adjust based on your application's error handling logic

    # Assuming 'collected_data' is a list of dictionaries containing the data to be uploaded
    sf_object_api_name = "SolidWorks_license__c"  # Replace with your actual Salesforce Object API name
    sf_object_api_name2 = "Installed_Base__c"
    # Construct the endpoint URL for the Bulk API job creation
    sf_object_endpoint = f"{sf_instance}/services/data/v52.0/jobs/ingest"

    # Set the headers for the job creation request
    sf_headers = {
        "Authorization": f"Bearer {sf_access_token}",
        "Content-Type": "application/json",
    }

    # Create a new job for bulk data insertion
    job_definition = {
        "operation": "insert",
        "object": sf_object_api_name,
        "contentType": "CSV",
        "lineEnding": "CRLF",
    }

    # Create job
    # Create job for bulk data insertion
    job_response = requests.post(sf_object_endpoint, headers=sf_headers, json=job_definition)
    job_response_json = job_response.json()
    print(job_response_json)
    job_id = job_response_json.get('id')
    if not job_id:
        # Handle job creation failure
        print(json.dumps({"error": "Failed to create job"}))
        return  # Adjust based
    # Define the endpoint for uploading data to the job
    batch_url = f"{sf_instance}/services/data/v52.0/jobs/ingest/{job_id}/batches"

    # Convert collected_data to CSV format
    csv_io = io.StringIO()
    fieldnames = [
        "Name", "Product__c", "SolidWorks_Customer_ID__c",
        "Network_License__c", "Users__c", "SeatId__c",
        #"Subscription_start_date__c",
        "Subscription_Termination_Date__c",  "Term_License__c", "Final_Customer_Name__c", "Usage__c", "Type__c"
    ]

    # Initialize the CSV writer
    writer = csv.DictWriter(csv_io, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data rows
    for record in collected_data:
        writer.writerow(record)

    # Retrieve the CSV data as a string
    csv_data = csv_io.getvalue()
    print(csv_data)
    # Close the StringIO object
    csv_io.close()

    # Set the appropriate headers for batch data upload
    batch_headers = {
        'Authorization': f'Bearer {sf_access_token}',
        'Content-Type': 'text/csv'
    }

    # Upload the data to the job
    batch_response = requests.put(batch_url, headers=batch_headers, data=csv_data)

    if batch_response.status_code not in range(200, 299):
        # Handle batch upload failure
        print("Failed to upload batch")
        return {"error": "Failed to upload batch"}, 400

    # Close the job to start processing
    job_close_url = f"{sf_instance}/services/data/v52.0/jobs/ingest/{job_id}"
    job_close_response = requests.patch(job_close_url, headers=sf_headers, json={"state": "UploadComplete"})

    if job_close_response.status_code not in range(200, 299):
        # Handle job close failure
        print("Failed to close job")
        return {"error": "Failed to close job"}, 400

    # If everything went well
    print("Data upload initiated successfully")
    print(json.dumps({"message": "Data upload initiated successfully"}))

    job_definition2 = {
        "operation": "insert",
        "object": sf_object_api_name2,
        "contentType": "CSV",
        "lineEnding": "CRLF",
    }

    # Create job
    # Create job for bulk data insertion
    job_response2 = requests.post(sf_object_endpoint, headers=sf_headers, json=job_definition2)
    job_response_json2 = job_response2.json()
    print(job_response_json2)
    job_id2 = job_response_json2.get('id')
    if not job_id2:
        # Handle job creation failure
        print(json.dumps({"error": "Failed to create job"}))
        return  # Adjust based
    # Define the endpoint for uploading data to the job
    batch_url2 = f"{sf_instance}/services/data/v52.0/jobs/ingest/{job_id2}/batches"


    csv_io2 = io.StringIO()
    fieldnames = [
        "Original_Order_Type__c", "Subscription_End_Date__c", "Subscription_start_date__c", "SeatId__c"
    ]

    # Initialize the CSV writer
    writer2 = csv.DictWriter(csv_io2, fieldnames=fieldnames)

    # Write the header row
    writer2.writeheader()

    # Write the data rows
    for record2 in collected_data2:
        writer2.writerow(record2)

    # Retrieve the CSV data as a string
    csv_data2 = csv_io2.getvalue()
    print(csv_data2)
    # Close the StringIO object
    csv_io2.close()

    # Upload the data to the job
    batch_response2 = requests.put(batch_url2, headers=batch_headers, data=csv_data2)

    if batch_response2.status_code not in range(200, 299):
        # Handle batch upload failure
        print("Failed to upload batch")
        return {"error": "Failed to upload batch"}, 400

    # Close the job to start processing
    job_close_url2 = f"{sf_instance}/services/data/v52.0/jobs/ingest/{job_id2}"
    job_close_response2 = requests.patch(job_close_url2, headers=sf_headers, json={"state": "UploadComplete"})

    if job_close_response2.status_code not in range(200, 299):
        # Handle job close failure
        print("Failed to close job")
        return {"error": "Failed to close job"}, 400

    print("Data upload initiated successfully")
    print(json.dumps({"message": "Data upload initiated successfully"}))


process_accounts()
