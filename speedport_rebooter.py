import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import argparse
from time import sleep

def reboot(user,passwd,ip):
    url = "https://"+ip+"/html/login/index.html"
    usr =  user
    pwd = passwd
    driver_path = '/usr/local/bin/chromedriver'
    c_opt = Options()
    c_opt.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=driver_path,options=c_opt)
    
    browser = driver
    browser.implicitly_wait(10)
    
    try:
        print('Fetching modem web interface..')
        browser.get(url)
        sleep(1)
    except RuntimeError as e:
        return e

    print('Logging in to modem..')
    browser.find_element_by_xpath('//*[@id="details-button"]').click()
    sleep(1)
    browser.find_element_by_xpath('//*[@id="proceed-link"]').click()
    browser.find_element_by_name("username").send_keys(usr)
    browser.find_element_by_name("password").send_keys(pwd)
    browser.find_element_by_name('action').click()
    print('Logged in to modem..')
    sleep(1)
    print('Navigating to settings menu..')
    browser.find_element_by_xpath('//a[@href="../content/config/change_password.html"]').click()
    sleep(1)
    print('Navigating to problem handling menu..')
    browser.find_element_by_xpath('//a[@href="problem_handling.html"]').click()
    sleep(1)
    print('Navigating to restart menu..')
    browser.find_element_by_class_name('unfold').click()
    sleep(1)
    print('Proceeding to modem reboot..')
    browser.find_element_by_class_name('submitBtn').click()
    tc = 70
    while tc != 0:
        print('Sleeping for {} seconds until modem gets restarted..'.format(tc))
        tc -=1
        sleep(1)

    try:
        print('Try fetching modem status page..')
        browser.get("https://"+ip+"/html/login/status.html")
        sleep(1)
    except RuntimeError as e:
        return e
    
    dsldwn = '0'
    dslup = '0'
    c = 0
    while str(dsldwn) == '0' and str(dslup) == '0':
        if c >= 60 :
            browser.close()
            exit(print('Something went wrong with the reboot.You need manual to check it out,as modem is still not synced after 10 minutes'))
        print('Refreshing status page..')
        browser.refresh()
        sleep(2)
        dsldwn = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div/div[1]/div[3]/div[2]/span[1]').text
        dslup = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div/div[1]/div[4]/div[2]/span[1]').text
        if str(dslup) == '0' or str(dsldwn) == '0':
            sleep(8)
        c += 1
    else:
        print("Download synced at: {} , Upload synced at: {}".format(dsldwn,dslup))
    
    sleep(1)
    print('Restart completed succesfully.Exiting..')
    browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--username','-u',nargs="?",default='admin')
    parser.add_argument('--password','-p',nargs="?",default='admin')
    parser.add_argument('--speedport_ip',nargs="?", default='192.168.1.1')
    args = parser.parse_args()
    reboot(args.username,args.password,args.speedport_ip)
