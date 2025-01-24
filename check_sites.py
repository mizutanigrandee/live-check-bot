import requests
import os

# 監視したいサイトURLのリスト
SITES = [
    "https://concert24-25.jp/s/kkt/?ima=0651",
    "https://bz-vermillion.com/",
    "https://shinee.jp/",
    "https://exo-jp.net/",
    "https://exile.jp/",
    "https://www.hoshinogen.com/",
    "https://www.nogizaka46.com/s/n46/?ima=0845",
    "https://starto.jp/s/p/artist/15",
    "https://m.tribe-m.jp/artist/index/37",
    "https://bts-official.jp/",
    "https://jsoulb.jp/",
    "https://backnumber.info/",
    "https://ygex.jp/blackpink/",
    "https://southernallstars.jp/",
    "https://niziu.com/s/n123/?ima=1717",
    "https://infinity-r.jp/",
    "https://enhypen-jp.weverse.io/",
    "https://www.seventeen-17.jp/",
    "https://txt-official.jp/",
    "https://www.straykidsjapan.com/",
    "https://mentrecording.jp/snowman/",
    "https://befirst.tokyo/",
    "https://www.sixtones.jp/",
    "https://reissuerecords.net/",
    "https://vaundy.jp/",
    "https://mrsgreenapple.com/",
    "https://www.yoasobi-music.jp/",
    "https://spitz-web.com/",
    "https://sekainoowari.jp/",
    "https://www.mrchildren.jp/",
    "https://www.aimyong.net/",
    "https://kinggnu.jp/",
    "https://higedan.com/",
    "https://www.universal-music.co.jp/ado/",
    "https://yuzu-official.com/",
    "https://www.oneokrock.com/jp/",
    "https://www.twicejapan.com/",
    "https://sudamasaki-music.com/",
    "https://fmsp.amob.jp/mob/index.php?site=F&ima=4103",
    "https://fujiikaze.com/",
    "https://dreamscometrue.com/",
    "https://tobe-official.jp/",
    "https://starto.jp/s/p/artist/41",
    "https://www.glay.co.jp/",
    "https://larc-en-ciel.com/index.php",
    "https://ovtp.jp/",
    "https://starto.jp/s/p/artist/56",
    "https://starto.jp/s/p/artist/157",
    "https://www.utadahikaru.jp/",
    "https://kobukuro.com/",
    "https://nct-jp.net/",
    "https://ini-official.com/",
    "https://da-ice.jp/",
    "https://tobe-official.jp/artists/number_i",

]

KEYWORDS = ["京セラドーム", "ヤンマースタジアム", "kyocera", "大阪城ホール"]

def check_site(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        html = resp.text
        for kw in KEYWORDS:
            if kw in html:
                return kw
        return None
    except Exception as e:
        print(f"[ERROR] {url} - {e}")
        return None

def send_slack_message(text):
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("No Slack webhook URL found in environment.")
        return

    payload = {"text": text}
    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        if resp.status_code != 200:
            print(f"Slack post failed: {resp.text}")
    except Exception as e:
        print(f"Slack post error: {e}")

if __name__ == "__main__":
    for url in SITES:
        found = check_site(url)
        if found:
            message = f"【ライブ情報検知】{url} にて '{found}' が見つかりました！"
            print(message)
            send_slack_message(message)
