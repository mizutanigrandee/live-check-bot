import requests
import os
import json

# URL → アーティスト名 の辞書
ARTIST_MAP = {
    "https://concert24-25.jp/s/kkt/?ima=0651": "キンキキッズ",
    "https://bz-vermillion.com/": "B'z",
    "https://shinee.jp/": "SHINee",
    "https://exo-jp.net/": "EXO",
    "https://exile.jp/": "EXILE",
    "https://www.hoshinogen.com/": "星野源",
    "https://www.nogizaka46.com/s/n46/?ima=0845": "乃木坂46",
    "https://starto.jp/s/p/artist/15": "ヘイセイジャンプ",
    "https://m.tribe-m.jp/artist/index/37": "ジェネレーションズ",
    "https://bts-official.jp/": "BTS",
    "https://jsoulb.jp/": "三代目JSOULBROTHERS",
    "https://backnumber.info/": "バックナンバー",
    "https://ygex.jp/blackpink/": "BLACKPINK",
    "https://southernallstars.jp/": "サザンオールスターズ",
    "https://niziu.com/s/n123/?ima=1717": "NiziU",
    "https://infinity-r.jp/": "∞(スーパーエイト?)",
    "https://enhypen-jp.weverse.io/": "ENHYPEN",
    "https://www.seventeen-17.jp/posts/information": "SEVENTEEN",
    "https://txt-official.jp/": "TXT",
    "https://www.straykidsjapan.com/": "Stray Kids",
    "https://mentrecording.jp/snowman/": "Snow Man",
    "https://befirst.tokyo/news/": "BE:FIRST",
    "https://www.sixtones.jp/": "SixTONES",
    "https://reissuerecords.net/": "米津玄師",
    "https://vaundy.jp/": "Vaundy",
    "https://mrsgreenapple.com/": "Mrs.GREEN APPLE",
    "https://www.yoasobi-music.jp/": "YOASOBI",
    "https://spitz-web.com/": "スピッツ",
    "https://sekainoowari.jp/": "SEKAI NO OWARI",
    "https://www.mrchildren.jp/": "Mr.Children",
    "https://www.aimyong.net/": "あいみょん",
    "https://kinggnu.jp/": "King Gnu",
    "https://higedan.com/": "Official髭男dism",
    "https://www.universal-music.co.jp/ado/": "Ado",
    "https://yuzu-official.com/": "ゆず",
    "https://www.oneokrock.com/jp/news": "ONE OK ROCK",
    "https://www.twicejapan.com/": "TWICE",
    "https://sudamasaki-music.com/": "菅田将暉",
    "https://fmsp.amob.jp/mob/index.php?site=F&ima=4103": "福山雅治",
    "https://fujiikaze.com/": "藤井風",
    "https://dreamscometrue.com/": "DREAMS COME TRUE",
    "https://tobe-official.jp/news": "TOBE",
    "https://starto.jp/s/p/artist/41": "King & Prince",
    "https://www.glay.co.jp/": "GLAY",
    "https://larc-en-ciel.com/index.php": "L'Arc～en～Ciel",
    "https://ovtp.jp/": "タイムレス(?不明)",
    "https://starto.jp/s/p/artist/56": "なにわ男子",
    "https://starto.jp/s/p/artist/157": "Aグループ(?不明)",
    "https://www.utadahikaru.jp/": "宇多田ヒカル",
    "https://kobukuro.com/": "コブクロ",
    "https://nct-jp.net/": "NCT",
    "https://ini-official.com/": "INI",
    "https://da-ice.jp/": "Da-iCE",
    "https://tobe-official.jp/artists/number_i": "NUMBER I",
    "https://starto.jp/?ima=4916": "旧ジャニーズ"
}

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
    "https://befirst.tokyo/news/",
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
    "https://www.oneokrock.com/jp/news",
    "https://www.twicejapan.com/",
    "https://sudamasaki-music.com/",
    "https://fmsp.amob.jp/mob/index.php?site=F&ima=4103",
    "https://fujiikaze.com/",
    "https://dreamscometrue.com/",
    "https://tobe-official.jp/news",
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
    "https://starto.jp/?ima=4916",
]

# 検知したいキーワード
KEYWORDS = ["京セラドーム", "ヤンマースタジアム", "大阪","kyocera","osaka"]

def load_found_snippets():
    """
    過去に検出した行情報を found_snippets.json から読み込む。
    ファイルが無い or 壊れている時は空のデータを返す。
    形式: {
      "URL": [
        "検出済みの行1",
        "検出済みの行2",
        ...
      ],
      ...
    }
    """
    try:
        with open("found_snippets.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_found_snippets(data):
    """
    found_snippets.json に書き込む
    """
    with open("found_snippets.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

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

def detect_new_lines(url, found_data):
    new_keywords = []
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        lines = resp.text.split("\n")

        for line in lines:
            line_lower = line.lower()
            for kw in KEYWORDS:
                if kw.lower() in line_lower:
                    # すでにfound_data[url]にkwがあればスキップ
                    already_found = found_data.get(url, [])
                    if kw not in already_found:
                        new_keywords.append(kw)
                    # break or not break is optional 
    except Exception as e:
        print(f"[ERROR] {url} - {e}")
    return new_keywords

if __name__ == "__main__":
    found_data = load_found_snippets()

    for url in SITES:
        newly_found_keywords = detect_new_lines(url, found_data)

        if newly_found_keywords:
            # ARTIST_MAPからアーティスト名を取得
            artist_name = ARTIST_MAP.get(url, "アーティスト不明")

            for kw in newly_found_keywords:
                # アーティスト名を含めてメッセージを作成
                msg = (
                    f"【新ライブ情報】\n"
                    f"アーティスト: {artist_name}\n"
                    f"URL: {url}\n"
                    f"キーワード: {kw}"
                )
                print(msg)
                send_slack_message(msg)

            # 追加保存
            if url not in found_data:
                found_data[url] = []
            found_data[url].extend(newly_found_keywords)

    save_found_snippets(found_data)
