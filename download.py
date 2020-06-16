import requests, re, time
import os, argparse, subprocess
from bs4 import BeautifulSoup

class Itchy:
    def __init__(self, headers, token, bundle_key, dl_path):
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Content-Type': 'text/html'
        }
        self.cookies = {
            'itchio':token
        }
        self.bundle_url = "https://itch.io/bundle/download/"+str(bundle_key)
        self.dl_path = dl_path
    def start(self):
        game_links=self.get_links()
        for x in game_links:
            x=x.strip('\n')
            self.download(x)
            time.sleep(0.75)
    def get_links(self):
        page = self.seek(wurl=self.bundle_url)
        
        num_of_pages = int(page.find('span',attrs={'class':'pager_label'}).a.text)
        self.bundle_name = page.findAll('span',attrs={'class':'object_title'})[0].text

        game_links = []
        print('Building game list... PLEASE WAIT, THIS WILL TAKE A MOMENT.')
        if not os.path.exists('game_list.txt'):
            text_file = open('game_list.txt', 'a+') 
            didnt_download = open('did_not_download.txt','a+')
            for i in range(num_of_pages):
                seek_url = (self.bundle_url+"?page="+str(i+1))
                i_page = self.seek(seek_url)
                find_list = i_page.findAll('h2', attrs={'class':'game_title'})
                for k in find_list:
                    link = k.a['href']
                    print(link)
                    if re.match(r'(https:\/\/[a-zA-Z0-9\-]+\.itch\.io\/[a-zA-Z0-9\-]+\/)download\/(.+)', link):
                        text_file.write("%s\n" % link)
                    else:
                        didnt_download.write("%s\n" % link)
                print('Completed page #'+str(i+1))
        game_links = open('game_list.txt','r')
        game_links = game_links.readlines()
        return game_links
    def seek(self, wurl):
        resp = requests.get(
            url=wurl,
            cookies=self.cookies
        )
        page = BeautifulSoup(resp.content,'html.parser')
        
        return page
    def download(self, dl):
        page = self.seek(wurl=dl)

        game_title = page.findAll('span',attrs={'class':'object_title'})[0].text
        game_title = re.sub(r"\/|\\|\"|\t|\:|\||\?|\.|\*|\'|\`|\;|\<|\>","", game_title)
        dl_list = page.findAll('a',attrs={'class':'button download_btn'})

        print('\nDownloading '+game_title)
        for z in dl_list:
            dl_id = z['data-upload_id']
            keys = re.findall(r'(https:\/\/[a-zA-Z0-9\-]+\.itch\.io\/[a-zA-Z0-9\-]+\/)download\/(.+)', dl)
            if keys:
                keys=keys[0]
                build_url = keys[0]+"file/"+str(dl_id)+"?key="+keys[1]
                url_post = requests.post(build_url, cookies=self.cookies)
                url_final = url_post.json()['url']

                dir_final = self.dl_path+"/"+self.bundle_name+'/'+game_title
                if not os.path.exists(dir_final):
                    os.makedirs(dir_final)
                # wget.download(url=url_final, out=dir_final)
                subprocess.run(f'wget {url_final} --content-disposition -nc -q --show-progress -P "{dir_final}"')
                time.sleep(0.5)

parse = argparse.ArgumentParser(description='A tool to download your itchio bundles')
parse.add_argument('--headers')
parse.add_argument('--dl_path',default='./downloads')
parse.add_argument('--token')
parse.add_argument('--bundle_key')
args = parse.parse_args()

itchio = Itchy(args.headers, args.token, args.bundle_key, args.dl_path)
itchio.start()
