# -*- coding: utf-8 -*-
import requests, zipfile, os, re, sys
from bs4 import BeautifulSoup
from multiprocessing import Pool

minitoon_host = "https://manamoa52.net"

download_url = "https://manamoa52.net/bbs/page.php?hid=manga_detail&manga_id=2127" # 고블린 슬레이어 
#download_url = "https://manamoa25.net/bbs/page.php?hid=manga_detail&manga_id=2111" # 고블린 슬레이어-이어원
#download_url = "https://manamoa25.net/bbs/page.php?hid=manga_detail&manga_id=2110" # 고블린 슬레이어-브랜뉴데이 
#download_url = "https://manamoa25.net/bbs/page.php?hid=manga_detail&manga_id=1640" # 피와 재의 여왕 
#download_url = "https://manamoa25.net/bbs/page.php?hid=manga_detail&manga_id=1140" # 자중 안 하는 전 용사의 강하고 즐거운 뉴 게임 
#download_url = "https://manamoa52.net/bbs/page.php?hid=manga_detail&manga_id=161" # 던전밥 
#download_url = "https://manamoa25.net/bbs/page.php?hid=manga_detail&manga_id=3226" # 마스터키튼 

def get_list():
    headers = {'Content-Type': 'charset=utf-8', "authority": "manamoa20.net", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
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


def get_img_list(html_str, img_list_str):
    
    str_var_img = "var " + img_list_str
    str_start = html_str.index(str_var_img)
    str_end = html_str.find("\n", html_str.index(str_var_img))
    str_img_list = html_str[str_start:str_end]
    
    img_list = str_img_list[str_img_list.index("[") + 1:str_img_list.index("]")].split(",")
    img_list = [ img[1:-1].replace("\/", "/") for img in img_list ]
    
    #if len(img_list) == 0:
    #    print(html_str)
    #    print(img_list)
    #    sys.exit(0)
    
    if len(img_list) == 1 and img_list[0] == '':
        del img_list[0]
    
    return img_list


# target 만화책을 다운로드 한다. 
def down_comic(target):
    global target_url
    target_url = minitoon_host + target.a['href']
    r = requests.get(target_url)
    html_str = r.text
    
    imgs_urls1 = get_img_list(html_str, "img_list")
    imgs_urls2 = get_img_list(html_str, "img_list1")
    
    if len(imgs_urls1) == 0 and len(imgs_urls2) == 0:
        print(html_str)
        print(imgs_urls1)
        print(imgs_urls2)
        sys.exit(1)
        
    if len(imgs_urls1) != 0:
        imgs_urls = imgs_urls1
    elif len(imgs_urls2) != 0:
        imgs_urls = imgs_urls2
    else:
        imgs_urls = imgs_urls1
    
    bs = BeautifulSoup(html_str, 'lxml')
    title = bs.find("meta", attrs = {"name":"title"})["content"].strip()
    
    print("="*30)
    print(title)
    print(imgs_urls1)
    print(imgs_urls2)
    print("="*30)
    
    print("{0} 다운로드 시작".format(title))
    
    with Pool(processes=8) as pool:
        pool.map(down_img, imgs_urls)
        
    pool.join()
    
    with zipfile.ZipFile(u"{0}.zip".format(title), 'w') as myzip:
        print("  압축시작")
        for index, file_url in enumerate(imgs_urls):
            file_url = file_url.replace("\/", "/")
            origin_file_name = file_url.split("/")[-1]

            file_url = file_url.replace("\/", "/")
            new_file_name = "{0}-{2}.{1}".format(index, file_url.split(".")[-1], title)
            
            print("    {0} to {1} 변경 및 압축".format(origin_file_name, new_file_name))
            
            os.rename(origin_file_name, new_file_name)
            myzip.write(new_file_name)
            os.remove(new_file_name)
        
        print("  압축종료")
        
    print("{0} 다운로드 종료".format(title))


# file_url 의 이미지를 다운로드 
def down_img(file_url):
    
    print('  {0}: {1}'.format('이미지 파일 다운로드', file_url))
    
    file_url = file_url.replace("\/", "/")
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
