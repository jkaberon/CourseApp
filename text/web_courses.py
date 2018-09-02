from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import smtplib
import sys

def everything():
	url="https://apps.uillinois.edu/selfservice/"
	subject=sys.argv[1]
	course=sys.argv[2]
	sections=[s.strip() for s in sys.argv[3].split(',')]
	netID=sys.argv[4]
	password=sys.argv[5]
	
	browser=webdriver.Chrome()
	browser.get(url)
	link1=browser.find_element_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_ctl06_pnlTemplatedContent']/div/div/div[2]/a") #change here
	link1.click()
	box=browser.find_element_by_id("netid")
	box.send_keys(netID)
	browser.find_element_by_id("easpass").send_keys(password)
	browser.find_element_by_name("BTN_LOGIN").click()
	
	try:
		browser.find_element_by_link_text("Registration & Records").click()
	except NoSuchElementException:
		send_text("NetID/password incorrect, please try again")
		return
	
	browser.find_element_by_link_text("Classic Registration").click()
	browser.find_element_by_link_text("Look-up or Select Classes").click()
	browser.find_element_by_partial_link_text("I Agree").click()
	browser.find_elements_by_tag_name("option")[1].click()
	browser.find_element_by_xpath("/html/body/div[3]/form/input[2]").click()
	browser.find_element_by_xpath("//*[@value='%s']" %subject).click()
	browser.find_element_by_xpath("/html/body/div[3]/form/input[17]").click()
	
	result=None
	t=0
	while True:   #go back and forth between course listings, section listings
		if result is None:
			body=browser.find_element_by_xpath("/html/body/div[3]/table[2]/tbody")
			choices=body.find_elements_by_tag_name("tr")
			result=binary_search(choices,course,2,len(choices)-1)
			if result == "course doesn't exist":
				send_text("Course doesn't exist, please try again")
				break
		else:
			body=browser.find_element_by_xpath("/html/body/div[3]/table[2]/tbody")
			choices=body.find_elements_by_tag_name("tr")
			if t > 72000:
				send_text("Your request has timed out. Try again if you like")
				break
		
		choices[result].find_element_by_name("SUB_BTN").click() 
		bod=browser.find_element_by_xpath("/html/body/div[3]/form/table/tbody")
		rows=bod.find_elements_by_tag_name("tr")
		finished=True #becomes false if section has openings
		
		for s in sections:
			res=b_search_2(rows,s,2,len(rows)-1)
			if res == "section doesn't exist":
				send_text("Section doesn't exist, please try again")
				return
			elem=rows[res].find_element_by_tag_name("td")
			try:
				elem.find_element_by_tag_name("input")
			except NoSuchElementException:
				continue
			finished=False
			break
		
		if not finished:
			send_text("Spot is open in %s %s" %(subject,course))
			break
		time.sleep(30)
		t+=30
		browser.back()

def binary_search(c,course,start,end):
    if start>end:
        return "course doesn't exist"
    mid=int((start+end)/2)
    elem=c[mid].find_element_by_tag_name("td")
    num=elem.get_attribute('innerHTML')
    
    if num == course:
        return mid
    elif int(num)<int(course):
        return binary_search(c,course,mid+1,end)
    else:
        return binary_search(c,course,start,mid-1)

def b_search_2(c,section,start,end):
    if start>end:
        return "section doesn't exist"
    mid=int((start+end)/2)
    elem=c[mid].find_elements_by_tag_name("td")[4]
    sec=elem.get_attribute('innerHTML')
    if sec == "&nbsp;":
        elem=c[mid-1].find_elements_by_tag_name("td")[4]
        sec=elem.get_attribute('innerHTML')
		
    if sec==section:
        return mid
    elif sec<section:
        return b_search_2(c,section,mid+1,end)
    else:
        return b_search_2(c,section,start,mid-1)
		
def send_text(msg):
	email=sys.argv[6]
	Epassword=sys.argv[7]
	phone=sys.argv[8]
	provider = sys.argv[9]
	p_map = {'AllTel':'text.wireless.alltel.com','AT&T':'txt.att.net',
			 'Boost':'myboostmobile.com','Cricket':'sms.mycricket.com',
			 'Sprint':'messaging.sprintpcs.com','T':'tmomail.net',
			 'US':'email.uscc.net','Verizon':'vtext.com','Virgin':'vmobl.com'}
	server=smtplib.SMTP("smtp.gmail.com",587)
	server.starttls()
	server.login(email,Epassword)
	server.sendmail(email,"%s@%s" % (phone,p_map[provider]), msg)
	server.quit()
		
if __name__ == "__main__":
	everything()
