import smtplib
from bs4 import BeautifulSoup
import urllib3
import urllib
import sys
import time
from email.mime.multipart import *
from email.mime.base import *
from crontab import CronTab
from email import encoders

urllib3.disable_warnings()

def send_torrent_email():
	smtpObj=smtplib.SMTP('smtp.gmail.com',587)
	smtpObj.ehlo()
	smtpObj.starttls()
	email=''
	password=''

	smtpObj.login(email,password)

	msg=MIMEMultipart()
	msg['Subject']='Torrent links'
	msg['From']=email
	msg['To']=email

	part=MIMEBase('application','octet-stream')
	part.set_payload(open('torrents.txt','rb').read())
	encoders.encode_base64(part)

	part.add_header('Content-Disposition', 'attachment; filename="torrents.txt"')
	msg.attach(part)
	smtpObj.sendmail(email,email,msg.as_string())


f=open('torrents.txt','w')
checker_file=open('checker.txt','r')
crontab=CronTab(user='DELL')
checked_data=checker_file.read()
if checked_data.find('1') == -1:
	http=urllib3.PoolManager()

	url="https://kickass.unblockall.xyz/usearch/game%20of%20thrones/?field=time_add&sorder=desc"
	response=http.request('GET',url)
	soup=BeautifulSoup(response.data,'lxml')

	torrents=soup.find_all('a',{"title":"Download torrent file"})
	names=soup=soup.find_all('a',{"class":"link"})
	torrent_names=[]
	names_all=[]

	for torrent in torrents:
		if 's11e13' in torrent['href']:
			torrent_names.append(torrent['href'])

	for name in names:
		if 's11e13' in name.text:
			names_all.append(name.text)
	all_=dict(zip(names_all,torrent_names))

	for name,torrent in all_.items():
		file.write('Name: ',+name,'\nMagnet: '+torrent+"\n"+'*'*50+'\n')

	if len(torrent_names)>0:
		checker_file.close()
		checker_file.open('checker.txt','w')
		checker_file.write('1')

		if(len(torrent_names)>0):
			send_torrent_email()
		else:
			job=crontab.new(command='cd e:')
			job.crontab.new(command='cd E:/Programs/Python-Programs/automation')
			job.crontab.new(command='python auto_download_torrent.py')
			job.crontab.new(comment='dl')
			crontab.minute.every(15)
			job.write()
			sys.exit()

	else:
		for job in crontab:
			if job.comment=='dl':
				crontab.remove(job)
				crontab.write()
	sys.exit()


	


