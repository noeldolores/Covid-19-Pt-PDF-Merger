#!/usr/bin/env python3
from __future__ import print_function

import requests
import re
from pathlib import Path
import PyPDF2

import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes

def scrape_html():
  url = 'https://www.fda.gov/emergency-preparedness-and-response/coronavirus-disease-2019-covid-19/pfizer-biontech-covid-19-vaccine'
  page = requests.get(url)
  html = page.content.decode('utf-8')
  regex = r"Pfizer-BioNTech COVID-19 Vaccine EUA Letter of Authorization reissued (\d+-\d+-\d+)"
 
  matches = re.findall(regex, html)

  global live_date
  live_date = matches[0]

  if new_version_check(live_date):
    download_PfizerEUA()
    combine_pdfs()
    send_email()
  
def new_version_check(live_date):
  filename = Path('local_version_date.txt')
  filename.touch(exist_ok=True)

  with open(filename, 'r+') as f:
    lines = f.readline()
    if len(lines) > 0:
      local_date = lines
      if local_date != live_date:
        with open(filename, 'w') as f:
          f.truncate(0)
          f.write(live_date)
        return True
      else:
        print("File Not Updated")
    else:
      with open(filename, 'w') as f:
        f.truncate(0)
        f.write(live_date)
      return True

def download_PfizerEUA():
  url = 'https://www.fda.gov/media/144414/download'
  r = requests.get(url, allow_redirects=True)
  open('PfizerEUA.pdf', 'wb').write(r.content)

def combine_pdfs():
  p1 = open('PfizerEUA.pdf', 'rb')
  p2 = open('vsafe.pdf', 'rb')

  p1_reader = PyPDF2.PdfFileReader(p1)
  p2_reader = PyPDF2.PdfFileReader(p2)

  writer = PyPDF2.PdfFileWriter()

  for pageNum in range(p1_reader.numPages):
    pageObj = p1_reader.getPage(pageNum)
    writer.addPage(pageObj)
  for pageNum in range(p2_reader.numPages):
    pageObj = p2_reader.getPage(pageNum)
    writer.addPage(pageObj)

  p3 = open('PfizerEUA_VSafe.pdf', 'wb')
  writer.write(p3)

  p1.close()
  p2.close()
  p3.close()

  print("File Updated to {}".format(live_date))

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)
 
    cred = None
 
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
 
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)
 
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()
 
        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
 
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def send_email():
  CLIENT_SECRET_FILE = 'client_secret.json'
  API_NAME = 'gmail',
  API_VERSION = 'v1'
  SCOPES = ['https://mail.google.com/']
  
  service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
  
  file_attachments = ['PfizerEUA_VSafe.pdf']
  
  emailMsg = 'One file attached'
  
  # create email message
  mimeMessage = MIMEMultipart()
  mimeMessage['to'] = 'noel.dolores2@gmail.com'
  mimeMessage['subject'] = 'Updated Pfizer EUA - VSafe PDF [{}]'.format(live_date)
  mimeMessage.attach(MIMEText(emailMsg, 'plain'))
  
  # Attach files
  for attachment in file_attachments:
      content_type, encoding = mimetypes.guess_type(attachment)
      main_type, sub_type = content_type.split('/', 1)
      file_name = os.path.basename(attachment)
  
      f = open(attachment, 'rb')
  
      myFile = MIMEBase(main_type, sub_type)
      myFile.set_payload(f.read())
      myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
      encoders.encode_base64(myFile)
  
      f.close()
  
      mimeMessage.attach(myFile)
  
  raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
  
  service.users().messages().send(
      userId='me',
      body={'raw': raw_string}).execute()
      
  print("Email successfully sent!")
scrape_html()