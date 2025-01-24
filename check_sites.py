import requests
import os
import json

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

# 検知したいキーワード
KEYWORDS = ["京セラドーム", "ヤンマースタジアム", "kyocera", ]

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
    """
    1. サイトのHTMLを取得
    2. キーワードを含む行だけ抽出
    3. 既にfound_dataに登録されていない行だけ返す
    """
    new_lines = []
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        lines = resp.text.split("\n")

        for line in lines:
            for kw in KEYWORDS:
                if kw in line:
                    # キーワードを含む行が見つかった
                    # 既に登録済みか確認
                    # (※行の長さが異常に長い場合、通知が冗長になる可能性あり)
                    if line not in found_data.get(url, []):
                        new_lines.append(line.strip())
                    break  # 一つでもヒットすれば次の行へ

    except Exception as e:
        print(f"[ERROR] {url} - {e}")
    return new_lines

if __name__ == "__main__":
    # 過去検出データを読み込み
    found_data = load_found_snippets()  # dict

    # 各サイトを巡回し、新しい行があれば通知
    for url in SITES:
        newly_found_lines = detect_new_lines(url, found_data)
        if newly_found_lines:
            # Slack通知 & found_data に追記
            for line in newly_found_lines:
                msg = f"【新ライブ情報？】\nURL: {url}\n該当行: {line}"
                print(msg)
                send_slack_message(msg)

            # 記録に追加
            if url not in found_data:
                found_data[url] = []
            found_data[url].extend(newly_found_lines)

    # 更新したfound_dataを保存
    save_found_snippets(found_data)

