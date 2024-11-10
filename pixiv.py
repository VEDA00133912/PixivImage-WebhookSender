import requests, json, os, time, random
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv

load_dotenv()
userId = os.getenv("USER_ID")
webhook_url = os.getenv("WEBHOOK_URL")
random_download = os.getenv("RANDOM", "false").lower() == "true"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Referer': "https://www.pixiv.net/",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
}

current_path = os.getcwd()

userpage = requests.get(f"https://www.pixiv.net/users/{userId}", headers=headers)
user_soup = bs(userpage.text, 'html.parser')
user_name = user_soup.find("title").text.replace(" - pixiv", "")

data = requests.get(f"https://www.pixiv.net/ajax/user/{userId}/profile/all", headers=headers).json()
if data["error"] == False:
    folder_name = f"./{user_name}"
    new_folder_path = os.path.join(current_path, folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    illusts = data["body"]["illusts"]
    keys = list(illusts.keys())

    if random_download:
        random.shuffle(keys)
        print(f"{len(keys)}の画像のランダム取得を開始します")
    else:
        print(f"{len(keys)}の画像の取得を開始します")

    for illustId in keys:
        p = 0
        
        html = requests.get(f"https://www.pixiv.net/artworks/{illustId}", headers=headers)
        if html.status_code == 429:
            print("Status 429 error.")
            time.sleep(10)
        soup = bs(html.text, "lxml")
        meta = soup.find_all("meta")[-1]
        meta_content = json.loads(meta.get("content"))
        img_url = meta_content["illust"][f"{illustId}"]["urls"]["original"]

        while True:
            img_url2 = img_url.replace("_p0", f"_p{p}")
            p += 1
            img_name = img_url2.split("/")[-1]
            img_path = os.path.join(new_folder_path, img_name)

            if os.path.exists(img_path):
                continue
            
            r = requests.get(img_url2, stream=True, headers=headers)
            if r.status_code == 200:
                print(f"ダウンロードしました {img_url2}:  {img_name}")
                try:
                    with open(img_path, "wb") as f:
                        f.write(r.content)
                    
                    files = {'file': open(img_path, 'rb')}
                    webhook_data = {
                        "content": f"{user_name}さんのイラストを取得しました"
                    }
                    response = requests.post(webhook_url, data=webhook_data, files=files)
                    if response.status_code == 204:
                    else:
                        print(f"Failed to send {img_name} to Discord.")
                
                except Exception as e:
                    print(f"Failed to download {img_name}: {e}")
            if r.status_code == 404:
                break
else:
    print("Could not find user")
