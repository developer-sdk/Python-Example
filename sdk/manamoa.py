# -*- coding: utf-8 -*-
import requests, zipfile, os, re
from bs4 import BeautifulSoup
from multiprocessing import Pool

minitoon_host = "https://manamoa20.net"

download_url = "https://manamoa20.net/bbs/page.php?hid=manga_detail&manga_id=2127"     # 불멸의 그대에게 

def get_list():
    headers = {'Content-Type': 'charset=utf-8'}
    r = requests.get(download_url, headers=headers)
    
    bs = BeautifulSoup(r.text, "lxml")
    div = bs.find(class_='chapter-list')

    targets = div.find_all(class_='slot')
    
    for index, target in enumerate(targets):
        infos = [ item.strip() for item in target.text.strip().split("\n") if item != ""]
        temp = infos[0]
        temp2 = [ item for item in temp.split("\t") if item.strip() != "" ]
        title = temp2[0]
        number = temp2[1]
        comment = infos[1]
        like = infos[2]
        upload_date = infos[3]
        link = target.a["href"]

        print("{0} [{1} {2}] {3}".format(index, title, number, link))
    
    print("다운받을 항목의 인덱스를 입력하세요. ")
    print("  ex) 1, 2, 4-10")
    print("      1-10")
    print("      입력없음(enter 전권 다운)")
    str_input = input("input: ")

    index_list = []
    
    if str_input != "":    
        for str_name in str_input.split(","):
            
            if(str_name.find("-") != -1):
                start = int(str_name.split('-')[0].strip())
                end = int(str_name.split('-')[1].strip())
                #index_list.extend(range(start, end+1))
                index_list = targets[start:end+1]
            else:
                index_list.append(targets[int(str_name.strip())])
    else:
        index_list = targets
    
    #print(str_input)
    return index_list

def get_img_list(html_str):
    p = re.compile("(https:....cdnwowmax.xyz..upload..[a-z0-9-]+.jpg)")
    img_list = p.findall(html_str)
    return img_list

# target 만화책을 다운로드 한다. 
def down_comic(target):
    global target_url
    target_url = minitoon_host + target.a['href']
    print(target_url)
    r = requests.get(target_url)
    
    imgs_urls = get_img_list(r.text)
    bs = BeautifulSoup(r.text, 'lxml')
    title = bs.find("meta", name='title').text.strip()
    #div = bs.find("div", class_="view-content scroll-viewer")
    
    #imgs = div.find_all('img')
    #imgs_urls = [ img['src'] for img in imgs ]
    
    print("{0} 다운로드 시작".format(title))
    
    with Pool(processes=2) as pool:
        pool.map(down_img, imgs_urls)
        
    pool.join()
    
    with zipfile.ZipFile(u"{0}.zip".format(title), 'w') as myzip:
        for file_url in imgs_urls:
            file_name = file_url.split("/")[-1]
            myzip.write(file_name)
            os.remove(file_name)
    
    print("{0} 다운로드 종료".format(title))
    

# file_url 의 이미지를 다운로드 
def down_img(file_url):
    
    file_name = file_url.split("/")[-1]
     
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0', 'Referer': target_url }

    r1 = requests.get(file_url, headers=headers)
    
    output = open(file_name,"wb")
    output.write(r1.content)
    output.close()    

if __name__ == "__main__":
    targets = get_list()
    
    for target in targets:
        down_comic(target)
