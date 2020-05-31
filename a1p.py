# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import re
import socks
import socket
from stem import Signal
from stem.control import Controller


def get_domain(weburls):
    domain = weburls.replace('www.', "")
    domain = domain.split(".")
    domain = domain[0]
    return domain


def check_domain_sku_status(domain):
    x = requests.get("https://signup.microsoft.com/signup?sku=Education")
    soup = BeautifulSoup(x.text, 'html.parser')
    match = soup.find('input', id='WizardState')
    while match is None:
        controller.signal(Signal.NEWNYM)
        time.sleep(10)
        x = requests.get("https://signup.microsoft.com/signup?sku=Education")
        soup = BeautifulSoup(x.text, 'html.parser')
        match = soup.find('input', id='WizardState')
        WizardState = match["value"]
    else:
        WizardState = match["value"]
    data = {
        "StepsData.Email": "fadaw@" + domain,
        "MessageId": "GenericError",
        "BackgroundImageUrl":"",
        "SkuId": "Education",
        "Origin": "",
        "IsAdminSignup": False,
        "CurrentWedcsTag": "/Signup/CollectEmail",
        "WizardState": WizardState,
        "WizardFullViewRendered": True,
        "ShowCookiesDisclosureBanner": False,
        "X-Requested-With": "XMLHttpRequest"
    }
    x = requests.post("https://signup.microsoft.com/signup/indexinternal?sku=Education", json=data)
    if 'id="sku_314c4481-f395-4525-be8b-2ec4bb1e9d91"' in x.text:
        print("The domain: " + domain + ". Can use for A1.")
        with open("domain_A1.txt", "a") as write:
            write.write(domain + "\n")
    elif 'id="sku_e82ae690-a2d5-4d76-8d30-7c6e01e6022e"' in x.text:
        print("The domain: " + domain + ". Can use for A1P.")
        with open("domain_A1P.txt", "a") as write:
            write.write(domain + "\n")
    else:
        print("The domain: " + domain + ". Can't do anything")


def get_domain_can_register(domain):
    url = "https://whois.chinaz.com/" + domain
    x = requests.get(url)
    if "未被注册" in x.text :
        return True
    else:
        return False


def get_google_search_result():
    global count, pages
    sub_domain = ['.com', '.net', '.org']
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    x = requests.get("https://www.google.com/search?q=site:.edu&start=" + str(pages * 10), headers=header)
    bs = BeautifulSoup(x.text, 'html.parser')
    cites = bs.find_all("cite")
    while len(cites) == 0:
        time.sleep(100)
        x = requests.get("https://www.google.com/search?q=site:.edu&start=" + str(pages * 10), headers=header)
        bs = BeautifulSoup(x.text, 'html.parser')
        cites = bs.find_all("cite")
    domains = get_domain(cites)
    for domain in domains:
        for i in range(3):
            _domain = domain + sub_domain[i]
            print(_domain)
            if get_domain_can_register(_domain):
                check_domain_sku_status(_domain)
    print("Current Done: " + str(pages + 1))
    count += 1
    pages += 1


def google_map_get():
    global count
    print("Current Page: " + str(count))
    sub_domain = ['.com', '.net', '.org']
    while True:
        url = 'https://www.google.co.jp/search?tbm=map&authuser=0&hl=zh-CN&gl=jp&pb=!4m9!1m3!1d1664509.594834528!2d-98.45748168991207!3d29.91837745074451!2m0!3m2!1i1050!2i722!4f13.1!7i20!' + str(count * 20) + '!10b1!12m23!1m1!18b1!2m3!5m1!6e2!20e3!6m14!4b1!23b1!26i1!27i1!41i2!45b1!49b1!63m0!67b1!73m0!74i150000!75b1!89b1!110m0!10b1!16b1!19m4!2m3!1i360!2i120!4i8!20m57!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m42!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e3!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!9b0!22m6!1sSOvTXsy5MJaVr7wPzomWkAw%3A63!2s1i%3A0%2Ct%3A20588%2Cp%3ASOvTXsy5MJaVr7wPzomWkAw%3A63!4m1!2i20588!7e81!12e3!24m46!1m12!13m6!2b1!3b1!4b1!6i1!8b1!9b1!18m4!3b1!4b1!5b1!6b1!2b1!5m5!2b1!3b1!5b1!6b1!7b1!10m1!8e3!14m1!3b1!17b1!20m2!1e3!1e6!24b1!25b1!26b1!30m1!2b1!36b1!43b1!52b1!55b1!56m2!1b1!3b1!65m5!3m4!1m3!1m2!1i224!2i298!26m4!2m3!1i80!2i92!4i8!30m28!1m6!1m2!1i0!2i0!2m2!1i458!2i722!1m6!1m2!1i1000!2i0!2m2!1i1050!2i722!1m6!1m2!1i0!2i0!2m2!1i1050!2i20!1m6!1m2!1i0!2i702!2m2!1i1050!2i722!31b1!34m13!2b1!3b1!4b1!6b1!8m3!1b1!3b1!4b1!9b1!12b1!14b1!20b1!23b1!37m1!1e81!42b1!46m1!1e2!47m0!49m1!3b1!50m12!1m11!2m7!1u2!4z6K-E5YiG5pyA6auY!5e1!9s0ahUKEwjSzZ-H0t7pAhWWyosBHc6EBcIQ_KkBCJIGKBY!10m2!2m1!1e1!3m1!1u2!4BIAE!59BQ2dBd0Fn!65m0&q=school&tch=1&ech=1&psi=SOvTXsy5MJaVr7wPzomWkAw.1590946634884.1'
        # 上面修改成 Google Map的搜索结果网址就ojbk了
        x = requests.get(url)
        json_string = x.text.replace('/*""*/', "")
        json_string = json_string.replace('\\', "")
        matchs = re.findall(r'(https?)://(.*?)/', json_string)
        for match in matchs:
            if "google" not in match[1]:
                print(match[1])
                domain = get_domain(match[1])
                for i in range(3):
                    _domain = domain + sub_domain[i]
                    print(_domain)
                    if get_domain_can_register(_domain):
                        check_domain_sku_status(_domain)
        print("Done Page: " + str(count))
        count += 1


def run():
    google_map_get()


count = 0


run()
