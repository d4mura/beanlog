"""Seed script: insert 5 roasters for Phase 0 MVP."""

import uuid

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config import settings

ROASTERS = [
    {
        "name": "LIGHT UP COFFEE",
        "name_en": "LIGHT UP COFFEE",
        "description": "2014年創業。「コーヒーの美味しさで、日常を照らす」をコンセプトに、産地のテロワールを活かした浅煎りのスペシャルティコーヒーを提供。吉祥寺と下北沢に店舗を構え、シングルオリジンの個性を最大限に引き出すロースティングで知られる。自社で産地を訪問し、ダイレクトトレードにも積極的に取り組んでいる。",
        "description_en": "Founded in 2014. Under the concept of 'Illuminating daily life with great coffee,' LIGHT UP COFFEE offers light-roasted specialty coffee that highlights the terroir of each origin. With shops in Kichijoji and Shimokitazawa, they are known for roasting that maximizes the individuality of single origins. They actively engage in direct trade, visiting origins themselves.",
        "location": "東京都武蔵野市吉祥寺本町4-13-15",
        "prefecture": "東京都",
        "website_url": "https://lightupcoffee.com",
        "instagram_url": "https://www.instagram.com/lightupcoffee/",
    },
    {
        "name": "ONIBUS COFFEE",
        "name_en": "ONIBUS COFFEE",
        "description": "2012年創業。店名はポルトガル語で「公共バス」を意味し、コーヒーが人と人をつなぐ乗り物であるというビジョンを持つ。中目黒・奥沢・八雲に店舗を展開。浅煎りから中煎りを中心に、産地の個性を尊重したロースティングを行う。坂尾篤史氏が代表を務め、東京のサードウェーブコーヒーシーンを牽引してきた存在。",
        "description_en": "Founded in 2012. The name means 'public bus' in Portuguese, embodying the vision that coffee is a vehicle connecting people. With locations in Nakameguro, Okusawa, and Yakumo, they focus on light to medium roasts that respect each origin's character. Led by Atsushi Sakao, ONIBUS has been a driving force in Tokyo's third-wave coffee scene.",
        "location": "東京都目黒区上目黒2-14-1",
        "prefecture": "東京都",
        "website_url": "https://onibuscoffee.com",
        "instagram_url": "https://www.instagram.com/onibuscoffee/",
    },
    {
        "name": "FUGLEN COFFEE ROASTERS",
        "name_en": "FUGLEN COFFEE ROASTERS",
        "description": "ノルウェー・オスロ発のコーヒーロースター。2012年に東京・渋谷の富ヶ谷に日本1号店をオープン。北欧スタイルの浅煎りロースティングを特徴とし、フルーティで明るい酸味のコーヒーを提供。ヴィンテージ家具に囲まれた店内はカフェ＆バーとしても人気。日本でのスペシャルティコーヒー文化の発展に大きく貢献している。",
        "description_en": "A coffee roaster originating from Oslo, Norway. Opened their first Japan location in Tomigaya, Shibuya in 2012. Known for Nordic-style light roasting, they offer fruity coffees with bright acidity. The interior, surrounded by vintage furniture, is also popular as a cafe and bar. Fuglen has significantly contributed to the development of specialty coffee culture in Japan.",
        "location": "東京都渋谷区富ヶ谷1-16-11",
        "prefecture": "東京都",
        "website_url": "https://fuglencoffee.jp",
        "instagram_url": "https://www.instagram.com/fuglentokyo/",
    },
    {
        "name": "堀口珈琲",
        "name_en": "Horiguchi Coffee",
        "description": "1990年創業の老舗スペシャルティコーヒー専門店。堀口俊英氏が設立し、日本におけるスペシャルティコーヒーの先駆者的存在。世田谷・千歳船橋を拠点に、品種・農園・精製方法にこだわった高品質な豆を提供。特に中米・アフリカ産のシングルオリジンの品揃えが豊富で、各豆の詳細なトレーサビリティ情報を公開している。ブレンドの技術にも定評がある。",
        "description_en": "An established specialty coffee shop founded in 1990. Established by Toshihide Horiguchi, it is a pioneer of specialty coffee in Japan. Based in Chitosefunabashi, Setagaya, they offer high-quality beans with detailed attention to variety, farm, and processing method. Particularly known for their extensive selection of single origins from Central America and Africa, with full traceability information. Their blending expertise is also highly regarded.",
        "location": "東京都世田谷区船橋1-12-15",
        "prefecture": "東京都",
        "website_url": "https://kohikobo.com",
        "instagram_url": "https://www.instagram.com/horiguchicoffee/",
    },
    {
        "name": "丸山珈琲",
        "name_en": "Maruyama Coffee",
        "description": "1991年創業。長野県軽井沢を拠点とするスペシャルティコーヒーの名店。代表の丸山健太郎氏はCOE（カップ・オブ・エクセレンス）国際審査員を務め、世界中の優れたコーヒーを直接買い付ける。軽井沢本店のほか、東京・名古屋にも展開。浅煎りから深煎りまで幅広い焙煎度をカバーし、COE入賞ロットなど希少な豆も多数取り扱う。日本のスペシャルティコーヒー業界を代表するロースターの一つ。",
        "description_en": "Founded in 1991. A renowned specialty coffee roaster based in Karuizawa, Nagano. Founder Kentaro Maruyama serves as a Cup of Excellence (COE) international judge, directly sourcing outstanding coffees from around the world. Beyond the Karuizawa flagship, they have locations in Tokyo and Nagoya. Covering a wide range of roast levels from light to dark, they handle many rare lots including COE winners. One of Japan's most representative specialty coffee roasters.",
        "location": "長野県北佐久郡軽井沢町軽井沢1154-10",
        "prefecture": "長野県",
        "website_url": "https://www.maruyamacoffee.com",
        "instagram_url": "https://www.instagram.com/maruyamacoffee/",
    },
]


def main():
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for r in ROASTERS:
            # Check if already exists
            existing = session.execute(
                text("SELECT id FROM roasters WHERE name = :name"),
                {"name": r["name"]},
            ).first()
            if existing:
                print(f"  Roaster '{r['name']}' already exists, skipping.")
                continue

            rid = str(uuid.uuid4())
            session.execute(
                text("""
                    INSERT INTO roasters (id, name, name_en, description, description_en,
                                          location, prefecture, website_url, instagram_url)
                    VALUES (:id, :name, :name_en, :description, :description_en,
                            :location, :prefecture, :website_url, :instagram_url)
                """),
                {"id": rid, **r},
            )
            print(f"  Inserted roaster: {r['name']} ({rid})")
        session.commit()
        count = session.execute(text("SELECT COUNT(*) FROM roasters")).scalar()
        print(f"Done. Total roasters: {count}")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
