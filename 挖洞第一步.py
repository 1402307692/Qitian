#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：project 
@IDE     ：PyCharm 
@Author  ：齐天
@Date    ：2023/8/26 19:09 
'''
import argparse
import base64
import csv
import datetime
import random
import re
import cv2
import requests
import time

from bs4 import BeautifulSoup




headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }

def get_beian(writer,ip):
    url = 'https://icp.chinaz.com/'+ ip
    try:
        resu = requests.get(url,headers=headers)
        soup = BeautifulSoup(resu.content.decode('utf-8'), 'html.parser')
        company_info = soup.find('ul','bor-t1s IcpMain01')
        try:
            company_name = re.findall(' id="companyName" target="_blank">(.*)</a>',str(company_info))[0]
        except:
            company_name= ''
        try:
            company_xingzhi = re.findall('<p><strong class="fl fwnone">(.*)</strong></p>',str(company_info))[0]
        except:
            company_xingzhi = ''
        print(ip,company_name,company_xingzhi)
        writer.writerow((ip,company_name,company_xingzhi))
    except Exception as e:
        print(e)
    time.sleep(random.randint(0,3))
def get_quanzhong(writer,ip):
    if 'http'in ip:
        domain = ip.split('/')[2]
    else:
        domain = ip.split('/')[0]
    url = 'https://www.aizhan.com/cha/'+domain
    print(url)
    try:
        rep = requests.get(url,headers=headers)
        soup = BeautifulSoup(rep.content.decode('utf-8'), 'html.parser')
        html_content = str(soup)
        baidu_weight = re.findall(
            r'<li>360权重：<a href="https://sorank.aizhan.com/pc/www.baidu.com/" id="360_pr" target="_blank"><img alt="(.*?)"',
            html_content)[0]
        yidong_weight = re.findall('<li>移动权重：<a href="https://baidurank.aizhan.com/mobile/www.baidu.com/" id="baidurank_mbr" target="_blank"><img alt="(.*?)"',
                                   html_content)[0]
        sll_weight= re.findall('<li>360权重：<a href="https://sorank.aizhan.com/pc/www.baidu.com/" id="360_pr" target="_blank"><img alt="(.*?)"',
                                   html_content)[0]
        shenma_weight = re.findall(
            r'<li>神马：<a href="https://smrank.aizhan.com/mobile/www.baidu.com/" id="sm_pr" target="_blank"><img alt="(.*?)"',
            html_content)[0]
        sougou_weight = re.findall(
            r'<li>搜狗：<a href="https://sogourank.aizhan.com/pc/www.baidu.com/" id="sogou_pr" target="_blank"><img alt="(.*?)"',
            html_content)[0]
        google_weight = re.findall(
            r'<li>谷歌PR：<a href="https://pr.aizhan.com/www.baidu.com/" id="google_pr" target="_blank"><img alt="(.*?)"',
            html_content)[0]

        print(domain,baidu_weight,yidong_weight,sll_weight,shenma_weight,sougou_weight,google_weight)
        writer.writerow((domain,baidu_weight,yidong_weight,sll_weight,shenma_weight,sougou_weight,google_weight))
        # print(soup.find_all('div',class_='content'))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    tubiao ='''
   ____  _ _______ _             
  / __ \(_)__   __(_)            
 | |  | |_   | |   _  __ _ _ __  
 | |  | | |  | |  | |/ _` | '_ \ 
 | |__| | |  | |  | | (_| | | | |
  \___\_\_|  |_|  |_|\__,_|_| |_|
    '''
    print(tubiao)
    parser = argparse.ArgumentParser(description="该脚本包含两个功能，一个查icp一个查权重")
    parser.add_argument('-t','--type',required=True,help='输入想要使用的功能类型,icp、weight')
    parser.add_argument('-in','--input',required=True,help='输入所要查看的文件')
    parser.add_argument('-o', '--output', help='输出位置')
    args = parser.parse_args()
    if not args.output:
        output = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.csv'
    else:
        output = args.output
    fp = open(output, 'a+', newline='', encoding='utf-8')
    writer = csv.writer(fp)
    ll = args.input
    with open(ll,'r',encoding='utf-8') as file:
        lists = file.readlines()
    lists = [line.rstrip('\n') for line in lists]
    if args.type == 'icp':
        headrow = ['domain', '公司名字', '公司性质']
        if fp.tell() == 0:
            writer.writerow(headrow)
        for l in lists:
            resu = get_beian(writer,l)
    elif args.type == 'weight':
        headrow = ['domain', '百度权重', '移动权重','360权重','神马权重','搜狗权重','谷歌权重']
        if fp.tell() == 0:
            writer.writerow(headrow)
        for l in lists:
            resu = get_quanzhong(writer,l)
    else:
        print('请重新确定所需要的类型哇,暂时只有-t weight或者icp')
    fp.close()

