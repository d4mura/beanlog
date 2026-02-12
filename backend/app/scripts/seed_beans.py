"""Seed script: insert 45 beans across 5 roasters for Phase 0 MVP."""

import uuid

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Bean definitions per roaster (name used to look up roaster_id)
# flavor_note_slugs will be mapped to flavor_note IDs at runtime
# origin_code will be mapped to origin IDs at runtime

BEANS_BY_ROASTER = {
    "LIGHT UP COFFEE": [
        {
            "name": "エチオピア イルガチェフェ ウォッシュド",
            "name_en": "Ethiopia Yirgacheffe Washed",
            "description": "花のような華やかな香りと、レモンティーを思わせる明るい酸味。クリーンカップで後味にジャスミンの余韻が残る。",
            "description_en": "Gorgeous floral aroma with bright acidity reminiscent of lemon tea. A clean cup with a lingering jasmine finish.",
            "origin_code": "ET", "variety": "Heirloom", "process": "washed", "roast_level": "light",
            "altitude_min": 1900, "altitude_max": 2200,
            "flavor_slugs": ["citrus", "jasmine", "berry"],
            "purchase_url": "https://lightupcoffee.com/collections/all",
        },
        {
            "name": "エチオピア グジ ナチュラル",
            "name_en": "Ethiopia Guji Natural",
            "description": "完熟ブルーベリーのような甘さとワイニーな質感。ナチュラルプロセスならではの複雑なフルーツ感が魅力。",
            "description_en": "Ripe blueberry sweetness with a winey body. Complex fruit character unique to natural processing.",
            "origin_code": "ET", "variety": "Heirloom", "process": "natural", "roast_level": "light",
            "altitude_min": 1800, "altitude_max": 2100,
            "flavor_slugs": ["berry", "tropical", "winey"],
            "purchase_url": "https://lightupcoffee.com/collections/all",
        },
        {
            "name": "ケニア ニエリ AA",
            "name_en": "Kenya Nyeri AA",
            "description": "カシスやブラックカラントのような力強い酸味と、ブラウンシュガーの甘さ。ケニア特有の複雑な味わい。",
            "description_en": "Powerful acidity like cassis and blackcurrant with brown sugar sweetness. Complex flavors characteristic of Kenya.",
            "origin_code": "KE", "variety": "SL28", "process": "washed", "roast_level": "light",
            "altitude_min": 1700, "altitude_max": 1900,
            "flavor_slugs": ["berry", "citrus", "brown_sugar"],
            "purchase_url": "https://lightupcoffee.com/collections/all",
        },
        {
            "name": "コスタリカ タラス ハニー",
            "name_en": "Costa Rica Tarrazú Honey",
            "description": "はちみつのような甘みとオレンジの酸味が調和。ハニープロセスによる滑らかなボディ感。",
            "description_en": "Harmonious honey sweetness with orange acidity. Smooth body from the honey process.",
            "origin_code": "CR", "variety": "Caturra", "process": "honey", "roast_level": "light",
            "altitude_min": 1500, "altitude_max": 1800,
            "flavor_slugs": ["honey", "citrus", "stone_fruit"],
            "purchase_url": "https://lightupcoffee.com/collections/all",
        },
        {
            "name": "グアテマラ アンティグア ウォッシュド",
            "name_en": "Guatemala Antigua Washed",
            "description": "チェリーのような甘い酸味とチョコレートのコク。バランスの取れたクリーンカップ。",
            "description_en": "Sweet cherry-like acidity with chocolate depth. A well-balanced clean cup.",
            "origin_code": "GT", "variety": "Bourbon", "process": "washed", "roast_level": "light",
            "altitude_min": 1500, "altitude_max": 1700,
            "flavor_slugs": ["stone_fruit", "chocolate", "caramel"],
            "purchase_url": "https://lightupcoffee.com/collections/all",
        },
        {
            "name": "コロンビア ウイラ ウォッシュド",
            "name_en": "Colombia Huila Washed",
            "description": "プラムやピーチのような穏やかな酸味。甘みが豊かでバランスに優れた一杯。",
            "description_en": "Gentle acidity like plum and peach. Rich sweetness with excellent balance.",
            "origin_code": "CO", "variety": "Caturra", "process": "washed", "roast_level": "light",
            "altitude_min": 1600, "altitude_max": 1900,
            "flavor_slugs": ["stone_fruit", "caramel", "citrus"],
            "purchase_url": "https://lightupcoffee.com/collections/all",
        },
        {
            "name": "ルワンダ フイエ ウォッシュド",
            "name_en": "Rwanda Huye Washed",
            "description": "オレンジやアプリコットの明るい風味。紅茶のような上品な質感と長い余韻。",
            "description_en": "Bright orange and apricot flavors. Elegant tea-like body with a long finish.",
            "origin_code": "RW", "variety": "Bourbon", "process": "washed", "roast_level": "light",
            "altitude_min": 1700, "altitude_max": 2000,
            "flavor_slugs": ["citrus", "stone_fruit", "jasmine"],
            "purchase_url": "https://lightupcoffee.com/collections/all",
        },
        {
            "name": "パナマ ボケテ ゲイシャ ウォッシュド",
            "name_en": "Panama Boquete Gesha Washed",
            "description": "ジャスミンとベルガモットの華やかなアロマ。ピーチティーのような甘く繊細な風味が際立つ、極上の一杯。",
            "description_en": "Gorgeous jasmine and bergamot aroma. Exquisite cup with delicate peach tea-like sweetness.",
            "origin_code": "PA", "variety": "Gesha", "process": "washed", "roast_level": "light",
            "altitude_min": 1600, "altitude_max": 1800,
            "flavor_slugs": ["jasmine", "stone_fruit", "tropical"],
            "purchase_url": "https://lightupcoffee.com/collections/all",
        },
        {
            "name": "ホンジュラス コパン ウォッシュド",
            "name_en": "Honduras Copán Washed",
            "description": "グリーンアップルのような爽やかな酸味とキャラメルの甘み。飲みやすく日常使いにぴったり。",
            "description_en": "Refreshing green apple acidity with caramel sweetness. Easy-drinking and perfect for everyday.",
            "origin_code": "HN", "variety": "Catuai", "process": "washed", "roast_level": "light",
            "altitude_min": 1300, "altitude_max": 1600,
            "flavor_slugs": ["citrus", "caramel", "honey"],
            "purchase_url": "https://lightupcoffee.com/collections/all",
        },
    ],
    "ONIBUS COFFEE": [
        {
            "name": "エチオピア シダモ ナチュラル",
            "name_en": "Ethiopia Sidamo Natural",
            "description": "ストロベリーやラズベリーのような赤い果実の風味。甘い余韻が長く続く、ジューシーな一杯。",
            "description_en": "Red fruit flavors of strawberry and raspberry. A juicy cup with a long sweet finish.",
            "origin_code": "ET", "variety": "Heirloom", "process": "natural", "roast_level": "light",
            "altitude_min": 1800, "altitude_max": 2000,
            "flavor_slugs": ["berry", "tropical", "honey"],
            "purchase_url": "https://onibuscoffee.com/collections/coffee-beans",
        },
        {
            "name": "ケニア キリニャガ AB",
            "name_en": "Kenya Kirinyaga AB",
            "description": "グレープフルーツのような鮮烈な酸味と、黒糖のようなコク。ケニアらしいジューシーで複雑な味わい。",
            "description_en": "Vivid grapefruit acidity with dark brown sugar richness. Juicy, complex Kenyan character.",
            "origin_code": "KE", "variety": "SL34", "process": "washed", "roast_level": "light",
            "altitude_min": 1600, "altitude_max": 1800,
            "flavor_slugs": ["citrus", "brown_sugar", "berry"],
            "purchase_url": "https://onibuscoffee.com/collections/coffee-beans",
        },
        {
            "name": "コロンビア ナリーニョ ウォッシュド",
            "name_en": "Colombia Nariño Washed",
            "description": "赤りんごやカラメルのような甘さ。まろやかな口当たりとクリーンな後味が特徴。",
            "description_en": "Red apple and caramel sweetness. Smooth mouthfeel with a clean finish.",
            "origin_code": "CO", "variety": "Typica", "process": "washed", "roast_level": "medium_light",
            "altitude_min": 1800, "altitude_max": 2100,
            "flavor_slugs": ["stone_fruit", "caramel", "chocolate"],
            "purchase_url": "https://onibuscoffee.com/collections/coffee-beans",
        },
        {
            "name": "ブラジル セラード ナチュラル",
            "name_en": "Brazil Cerrado Natural",
            "description": "ナッツやチョコレートの風味に、穏やかな甘みが広がる。毎日飲みたいバランスの良い一杯。",
            "description_en": "Nutty, chocolatey flavors with gentle sweetness. A well-balanced cup for everyday enjoyment.",
            "origin_code": "BR", "variety": "Catuai", "process": "natural", "roast_level": "medium_light",
            "altitude_min": 900, "altitude_max": 1200,
            "flavor_slugs": ["almond", "chocolate", "caramel"],
            "purchase_url": "https://onibuscoffee.com/collections/coffee-beans",
        },
        {
            "name": "グアテマラ ウエウエテナンゴ ウォッシュド",
            "name_en": "Guatemala Huehuetenango Washed",
            "description": "アプリコットのような酸味とミルクチョコレートの甘さ。スムーズなボディ感が心地よい。",
            "description_en": "Apricot-like acidity with milk chocolate sweetness. Pleasantly smooth body.",
            "origin_code": "GT", "variety": "Bourbon", "process": "washed", "roast_level": "medium_light",
            "altitude_min": 1500, "altitude_max": 1800,
            "flavor_slugs": ["stone_fruit", "chocolate", "honey"],
            "purchase_url": "https://onibuscoffee.com/collections/coffee-beans",
        },
        {
            "name": "コスタリカ ウエストバレー アナエロビック",
            "name_en": "Costa Rica West Valley Anaerobic",
            "description": "マンゴーやパッションフルーツのようなトロピカル感。嫌気性発酵による独特のフレーバーが楽しめる。",
            "description_en": "Tropical notes of mango and passion fruit. Unique flavors from anaerobic fermentation.",
            "origin_code": "CR", "variety": "Caturra", "process": "anaerobic", "roast_level": "light",
            "altitude_min": 1400, "altitude_max": 1700,
            "flavor_slugs": ["tropical", "fermented", "stone_fruit"],
            "purchase_url": "https://onibuscoffee.com/collections/coffee-beans",
        },
        {
            "name": "インドネシア スマトラ マンデリン",
            "name_en": "Indonesia Sumatra Mandheling",
            "description": "アーシーでウッディな風味にハーブのニュアンス。どっしりとしたボディと長い余韻。",
            "description_en": "Earthy, woody flavors with herbal nuances. Full body with a long finish.",
            "origin_code": "ID", "variety": "Typica", "process": "washed", "roast_level": "medium",
            "altitude_min": 1100, "altitude_max": 1500,
            "flavor_slugs": ["earthy", "woody", "herbal"],
            "purchase_url": "https://onibuscoffee.com/collections/coffee-beans",
        },
        {
            "name": "ルワンダ ニャマシェケ ナチュラル",
            "name_en": "Rwanda Nyamasheke Natural",
            "description": "ピーチやプラムのような果実味と、はちみつのような甘い余韻。ナチュラルの豊かなフルーツ感。",
            "description_en": "Fruity peach and plum notes with a honey-like sweet finish. Rich fruit character from natural processing.",
            "origin_code": "RW", "variety": "Bourbon", "process": "natural", "roast_level": "light",
            "altitude_min": 1600, "altitude_max": 1900,
            "flavor_slugs": ["stone_fruit", "honey", "berry"],
            "purchase_url": "https://onibuscoffee.com/collections/coffee-beans",
        },
        {
            "name": "エチオピア イルガチェフェ ウォッシュド",
            "name_en": "Ethiopia Yirgacheffe Washed",
            "description": "レモンやベルガモットのような爽やかな酸味。フローラルなアロマとシルキーな質感。",
            "description_en": "Refreshing lemon and bergamot acidity. Floral aroma with a silky texture.",
            "origin_code": "ET", "variety": "Heirloom", "process": "washed", "roast_level": "light",
            "altitude_min": 1900, "altitude_max": 2200,
            "flavor_slugs": ["citrus", "jasmine", "stone_fruit"],
            "purchase_url": "https://onibuscoffee.com/collections/coffee-beans",
        },
    ],
    "FUGLEN COFFEE ROASTERS": [
        {
            "name": "エチオピア ゲデブ ウォッシュド",
            "name_en": "Ethiopia Gedeb Washed",
            "description": "ジャスミンティーのような華やかなアロマ。レモンとピーチの明るい酸味に、紅茶のような上品なボディ。北欧ロースト。",
            "description_en": "Gorgeous jasmine tea-like aroma. Bright lemon and peach acidity with an elegant tea-like body. Nordic roast.",
            "origin_code": "ET", "variety": "Heirloom", "process": "washed", "roast_level": "light",
            "altitude_min": 1900, "altitude_max": 2200,
            "flavor_slugs": ["jasmine", "citrus", "stone_fruit"],
            "purchase_url": "https://fuglencoffee.jp/collections/beans",
        },
        {
            "name": "ケニア ニエリ SL28",
            "name_en": "Kenya Nyeri SL28",
            "description": "ブラックカラントのような濃厚な果実味。トマトのような甘い酸味とシロップのようなボディ。",
            "description_en": "Rich blackcurrant fruit character. Tomato-like sweet acidity with a syrupy body.",
            "origin_code": "KE", "variety": "SL28", "process": "washed", "roast_level": "light",
            "altitude_min": 1700, "altitude_max": 1900,
            "flavor_slugs": ["berry", "citrus", "brown_sugar"],
            "purchase_url": "https://fuglencoffee.jp/collections/beans",
        },
        {
            "name": "コロンビア カウカ ウォッシュド",
            "name_en": "Colombia Cauca Washed",
            "description": "プラムやチェリーのような赤い果実の酸味。キャラメルの甘みが余韻に広がる、クリーンカップ。",
            "description_en": "Red fruit acidity of plum and cherry. Caramel sweetness lingers in the finish. Clean cup.",
            "origin_code": "CO", "variety": "Caturra", "process": "washed", "roast_level": "light",
            "altitude_min": 1700, "altitude_max": 2000,
            "flavor_slugs": ["stone_fruit", "caramel", "berry"],
            "purchase_url": "https://fuglencoffee.jp/collections/beans",
        },
        {
            "name": "グアテマラ ウエウエテナンゴ ブルボン",
            "name_en": "Guatemala Huehuetenango Bourbon",
            "description": "オレンジやアプリコットのフルーティな酸味。はちみつのような甘さとシルキーな口当たり。",
            "description_en": "Fruity orange and apricot acidity. Honey-like sweetness with a silky mouthfeel.",
            "origin_code": "GT", "variety": "Bourbon", "process": "washed", "roast_level": "light",
            "altitude_min": 1600, "altitude_max": 1900,
            "flavor_slugs": ["citrus", "honey", "stone_fruit"],
            "purchase_url": "https://fuglencoffee.jp/collections/beans",
        },
        {
            "name": "コスタリカ タラス ウォッシュド",
            "name_en": "Costa Rica Tarrazú Washed",
            "description": "グリーンアップルのような爽やかな酸味と、ブラウンシュガーの甘み。クリーンで飲みやすい。",
            "description_en": "Refreshing green apple acidity with brown sugar sweetness. Clean and easy-drinking.",
            "origin_code": "CR", "variety": "Catuai", "process": "washed", "roast_level": "light",
            "altitude_min": 1400, "altitude_max": 1700,
            "flavor_slugs": ["citrus", "brown_sugar", "honey"],
            "purchase_url": "https://fuglencoffee.jp/collections/beans",
        },
        {
            "name": "パナマ チリキ ゲイシャ ナチュラル",
            "name_en": "Panama Chiriquí Gesha Natural",
            "description": "ライチやマンゴーのようなトロピカルフルーツ感。ゲイシャ種のフローラルさにナチュラルの甘みが加わった逸品。",
            "description_en": "Tropical fruit notes of lychee and mango. The floral character of Gesha enhanced by natural sweetness.",
            "origin_code": "PA", "variety": "Gesha", "process": "natural", "roast_level": "light",
            "altitude_min": 1600, "altitude_max": 1900,
            "flavor_slugs": ["tropical", "jasmine", "berry"],
            "purchase_url": "https://fuglencoffee.jp/collections/beans",
        },
        {
            "name": "ルワンダ キブ レイクショア ウォッシュド",
            "name_en": "Rwanda Kivu Lakeshore Washed",
            "description": "オレンジやピーチの明るい酸味。紅茶のようなエレガントなボディとフローラルな余韻。",
            "description_en": "Bright orange and peach acidity. Elegant tea-like body with a floral finish.",
            "origin_code": "RW", "variety": "Bourbon", "process": "washed", "roast_level": "light",
            "altitude_min": 1500, "altitude_max": 1800,
            "flavor_slugs": ["citrus", "jasmine", "stone_fruit"],
            "purchase_url": "https://fuglencoffee.jp/collections/beans",
        },
        {
            "name": "エチオピア シダモ ナチュラル",
            "name_en": "Ethiopia Sidamo Natural",
            "description": "ブルーベリーやストロベリーの鮮やかなフルーツ感。ワイニーな質感と甘い余韻が特徴的。",
            "description_en": "Vivid blueberry and strawberry fruit character. Winey texture with a sweet lingering finish.",
            "origin_code": "ET", "variety": "Heirloom", "process": "natural", "roast_level": "light",
            "altitude_min": 1800, "altitude_max": 2100,
            "flavor_slugs": ["berry", "winey", "tropical"],
            "purchase_url": "https://fuglencoffee.jp/collections/beans",
        },
        {
            "name": "ブラジル モジアナ イエローブルボン",
            "name_en": "Brazil Mogiana Yellow Bourbon",
            "description": "ナッツとチョコレートの風味に、穏やかな酸味。北欧ローストで浅く焼き上げ、クリーンな甘さを引き出した一杯。",
            "description_en": "Nutty, chocolatey flavors with gentle acidity. Nordic-roasted light to bring out clean sweetness.",
            "origin_code": "BR", "variety": "Bourbon", "process": "natural", "roast_level": "light",
            "altitude_min": 1000, "altitude_max": 1300,
            "flavor_slugs": ["almond", "chocolate", "caramel"],
            "purchase_url": "https://fuglencoffee.jp/collections/beans",
        },
    ],
    "堀口珈琲": [
        {
            "name": "エチオピア イルガチェフェ G1 ウォッシュド",
            "name_en": "Ethiopia Yirgacheffe G1 Washed",
            "description": "フローラルで繊細なアロマ。レモンやベルガモットのような酸味にジャスミンの余韻。堀口珈琲が長年取り扱うイルガチェフェの定番。",
            "description_en": "Delicate floral aroma. Lemon and bergamot-like acidity with jasmine finish. A classic Yirgacheffe selection from Horiguchi Coffee.",
            "origin_code": "ET", "variety": "Heirloom", "process": "washed", "roast_level": "medium_light",
            "altitude_min": 1900, "altitude_max": 2200,
            "flavor_slugs": ["jasmine", "citrus", "berry"],
            "purchase_url": "https://kohikobo.com/collections/single-origin",
        },
        {
            "name": "グアテマラ アンティグア ラ・アゾテア農園",
            "name_en": "Guatemala Antigua La Azotea Farm",
            "description": "チョコレートとキャラメルの甘さに、オレンジのような明るい酸味。アンティグアの火山性土壌が育むバランスの良い味わい。",
            "description_en": "Chocolate and caramel sweetness with bright orange acidity. Well-balanced flavors nurtured by Antigua's volcanic soil.",
            "origin_code": "GT", "variety": "Bourbon", "process": "washed", "roast_level": "medium",
            "altitude_min": 1500, "altitude_max": 1600,
            "flavor_slugs": ["chocolate", "caramel", "citrus"],
            "purchase_url": "https://kohikobo.com/collections/single-origin",
        },
        {
            "name": "コロンビア ウイラ サン・アグスティン",
            "name_en": "Colombia Huila San Agustín",
            "description": "赤い果実とミルクチョコレートのハーモニー。バランスに優れ、温度変化で表情を変えるクラシックなコロンビア。",
            "description_en": "Harmony of red fruits and milk chocolate. Well-balanced Colombian that shows different expressions as temperature changes.",
            "origin_code": "CO", "variety": "Caturra", "process": "washed", "roast_level": "medium",
            "altitude_min": 1600, "altitude_max": 1900,
            "flavor_slugs": ["stone_fruit", "chocolate", "caramel"],
            "purchase_url": "https://kohikobo.com/collections/single-origin",
        },
        {
            "name": "ケニア エンブ AA ファクトリー",
            "name_en": "Kenya Embu AA Factory",
            "description": "カシスやグレープフルーツのような鮮烈な酸味。ケニア特有のSL品種が生み出す複雑で豊かな味わい。品種情報を詳細に管理。",
            "description_en": "Vivid cassis and grapefruit acidity. Complex, rich flavors created by Kenya's signature SL varieties. Detailed variety tracking.",
            "origin_code": "KE", "variety": "SL28, SL34", "process": "washed", "roast_level": "medium_light",
            "altitude_min": 1500, "altitude_max": 1700,
            "flavor_slugs": ["berry", "citrus", "brown_sugar"],
            "purchase_url": "https://kohikobo.com/collections/single-origin",
        },
        {
            "name": "コスタリカ タラス カネット農園 ハニー",
            "name_en": "Costa Rica Tarrazú Cannet Farm Honey",
            "description": "はちみつやアプリコットの甘い風味。ハニープロセスならではのなめらかな質感とクリーンな後味。",
            "description_en": "Sweet honey and apricot flavors. Smooth texture unique to honey processing with a clean finish.",
            "origin_code": "CR", "variety": "Catuai", "process": "honey", "roast_level": "medium",
            "altitude_min": 1400, "altitude_max": 1700,
            "flavor_slugs": ["honey", "stone_fruit", "caramel"],
            "purchase_url": "https://kohikobo.com/collections/single-origin",
        },
        {
            "name": "パナマ ボケテ エスメラルダ農園 ゲイシャ",
            "name_en": "Panama Boquete Esmeralda Farm Gesha",
            "description": "ジャスミンとベルガモットの華やかなアロマ。ピーチティーのような繊細な甘さ。世界最高峰のゲイシャ種。",
            "description_en": "Gorgeous jasmine and bergamot aroma. Delicate peach tea sweetness. World-class Gesha variety.",
            "origin_code": "PA", "variety": "Gesha", "process": "washed", "roast_level": "medium_light",
            "altitude_min": 1600, "altitude_max": 1800,
            "flavor_slugs": ["jasmine", "stone_fruit", "tropical"],
            "purchase_url": "https://kohikobo.com/collections/single-origin",
        },
        {
            "name": "ブラジル 南ミナス カルモ農園 ナチュラル",
            "name_en": "Brazil Sul de Minas Carmo Farm Natural",
            "description": "ナッツやダークチョコレートの風味に、穏やかな甘み。ブラジルらしいどっしりとしたボディ。中煎りで豆のポテンシャルを最大限に引き出す。",
            "description_en": "Nutty, dark chocolate flavors with gentle sweetness. Full body typical of Brazil. Medium roast to maximize the bean's potential.",
            "origin_code": "BR", "variety": "Catuai", "process": "natural", "roast_level": "medium",
            "altitude_min": 1000, "altitude_max": 1300,
            "flavor_slugs": ["almond", "chocolate", "brown_sugar"],
            "purchase_url": "https://kohikobo.com/collections/single-origin",
        },
        {
            "name": "ホンジュラス サンタバルバラ ウォッシュド",
            "name_en": "Honduras Santa Bárbara Washed",
            "description": "グリーンアップルのような酸味とキャラメルの甘み。クリーンで飲みやすく、コストパフォーマンスに優れた逸品。",
            "description_en": "Green apple acidity with caramel sweetness. Clean, easy-drinking with excellent value.",
            "origin_code": "HN", "variety": "Catuai", "process": "washed", "roast_level": "medium",
            "altitude_min": 1300, "altitude_max": 1600,
            "flavor_slugs": ["citrus", "caramel", "almond"],
            "purchase_url": "https://kohikobo.com/collections/single-origin",
        },
        {
            "name": "インドネシア スマトラ リントン マンデリン",
            "name_en": "Indonesia Sumatra Lintong Mandheling",
            "description": "アーシーでハーバルな風味にスパイスのニュアンス。重厚なボディと長い余韻。堀口珈琲の深煎りブレンドにも使用される豆。",
            "description_en": "Earthy, herbal flavors with spice nuances. Heavy body with a long finish. Also used in Horiguchi Coffee's dark roast blends.",
            "origin_code": "ID", "variety": "Typica", "process": "washed", "roast_level": "medium_dark",
            "altitude_min": 1100, "altitude_max": 1500,
            "flavor_slugs": ["earthy", "herbal", "cinnamon"],
            "purchase_url": "https://kohikobo.com/collections/single-origin",
        },
    ],
    "丸山珈琲": [
        {
            "name": "エチオピア イルガチェフェ コンガ G1 ウォッシュド",
            "name_en": "Ethiopia Yirgacheffe Konga G1 Washed",
            "description": "ジャスミンとベルガモットの繊細なアロマ。レモンティーのような爽やかさと花の蜜のような甘さ。COE審査員である丸山氏が厳選。",
            "description_en": "Delicate jasmine and bergamot aroma. Refreshing like lemon tea with floral honey sweetness. Carefully selected by COE judge Mr. Maruyama.",
            "origin_code": "ET", "variety": "Heirloom", "process": "washed", "roast_level": "light",
            "altitude_min": 1900, "altitude_max": 2200,
            "flavor_slugs": ["jasmine", "citrus", "honey"],
            "purchase_url": "https://www.maruyamacoffee.com/ec/products/list",
        },
        {
            "name": "グアテマラ エル・インヘルト農園 ブルボン",
            "name_en": "Guatemala El Injerto Farm Bourbon",
            "description": "チョコレートとオレンジの調和。COE常連のエル・インヘルト農園から届く、バランスに優れたグアテマラ。",
            "description_en": "Harmony of chocolate and orange. Well-balanced Guatemala from the COE-regular El Injerto Farm.",
            "origin_code": "GT", "variety": "Bourbon", "process": "washed", "roast_level": "medium_light",
            "altitude_min": 1500, "altitude_max": 1800,
            "flavor_slugs": ["chocolate", "citrus", "caramel"],
            "purchase_url": "https://www.maruyamacoffee.com/ec/products/list",
        },
        {
            "name": "コロンビア ウイラ COE入賞ロット",
            "name_en": "Colombia Huila COE Winner Lot",
            "description": "赤い果実の華やかな酸味とブラウンシュガーの甘み。カップ・オブ・エクセレンス入賞ロットの贅沢な味わい。",
            "description_en": "Gorgeous red fruit acidity with brown sugar sweetness. Luxurious Cup of Excellence winning lot.",
            "origin_code": "CO", "variety": "Caturra", "process": "washed", "roast_level": "light",
            "altitude_min": 1700, "altitude_max": 2000,
            "flavor_slugs": ["berry", "brown_sugar", "stone_fruit"],
            "purchase_url": "https://www.maruyamacoffee.com/ec/products/list",
        },
        {
            "name": "ケニア ニエリ カラツ ファクトリー AA",
            "name_en": "Kenya Nyeri Karathu Factory AA",
            "description": "カシスとグレープフルーツの鮮烈な酸味。黒糖のような甘さとシロップのようなボディ。ケニアの魅力を存分に楽しめる一杯。",
            "description_en": "Vivid cassis and grapefruit acidity. Dark brown sugar sweetness with syrupy body. A cup to fully enjoy Kenya's charm.",
            "origin_code": "KE", "variety": "SL28", "process": "washed", "roast_level": "medium_light",
            "altitude_min": 1700, "altitude_max": 1900,
            "flavor_slugs": ["berry", "citrus", "brown_sugar"],
            "purchase_url": "https://www.maruyamacoffee.com/ec/products/list",
        },
        {
            "name": "パナマ エスメラルダ農園 ゲイシャ ナチュラル",
            "name_en": "Panama Esmeralda Farm Gesha Natural",
            "description": "トロピカルフルーツとジャスミンの華やかな融合。ナチュラルプロセスによる濃厚な甘さと複雑さ。世界最高峰の逸品。",
            "description_en": "Gorgeous fusion of tropical fruit and jasmine. Rich sweetness and complexity from natural processing. A world-class gem.",
            "origin_code": "PA", "variety": "Gesha", "process": "natural", "roast_level": "light",
            "altitude_min": 1600, "altitude_max": 1800,
            "flavor_slugs": ["tropical", "jasmine", "berry", "winey"],
            "purchase_url": "https://www.maruyamacoffee.com/ec/products/list",
        },
        {
            "name": "ブラジル セラード パッセイオ農園 ナチュラル",
            "name_en": "Brazil Cerrado Passeio Farm Natural",
            "description": "ナッツとダークチョコレートの風味に、キャラメルの甘さ。どっしりとしたボディで深煎り好きにも人気。",
            "description_en": "Nutty, dark chocolate flavors with caramel sweetness. Full body popular with dark roast enthusiasts.",
            "origin_code": "BR", "variety": "Catuai", "process": "natural", "roast_level": "medium",
            "altitude_min": 900, "altitude_max": 1200,
            "flavor_slugs": ["almond", "chocolate", "caramel"],
            "purchase_url": "https://www.maruyamacoffee.com/ec/products/list",
        },
        {
            "name": "コスタリカ チリポ マイクロミル ハニー",
            "name_en": "Costa Rica Chirripó Micromill Honey",
            "description": "ピーチやマンゴーのようなトロピカルな甘さ。ハニープロセスのシルキーなボディが心地よい。",
            "description_en": "Tropical sweetness of peach and mango. Comfortable silky body from honey processing.",
            "origin_code": "CR", "variety": "Caturra", "process": "honey", "roast_level": "medium_light",
            "altitude_min": 1500, "altitude_max": 1800,
            "flavor_slugs": ["stone_fruit", "tropical", "honey"],
            "purchase_url": "https://www.maruyamacoffee.com/ec/products/list",
        },
        {
            "name": "ルワンダ フイエ ムソ ウォッシュド",
            "name_en": "Rwanda Huye Muso Washed",
            "description": "オレンジやアプリコットの明るい酸味。紅茶のような上品なボディと甘い余韻。アフリカの隠れた銘産地。",
            "description_en": "Bright orange and apricot acidity. Elegant tea-like body with a sweet finish. Africa's hidden gem origin.",
            "origin_code": "RW", "variety": "Bourbon", "process": "washed", "roast_level": "light",
            "altitude_min": 1700, "altitude_max": 2000,
            "flavor_slugs": ["citrus", "stone_fruit", "jasmine"],
            "purchase_url": "https://www.maruyamacoffee.com/ec/products/list",
        },
        {
            "name": "インドネシア スラウェシ トラジャ",
            "name_en": "Indonesia Sulawesi Toraja",
            "description": "ダークチョコレートとスパイスの風味。アーシーなニュアンスに甘い余韻。深煎りで豊かなコクを楽しめるインドネシアの銘品。",
            "description_en": "Dark chocolate and spice flavors. Earthy nuances with a sweet finish. An Indonesian classic for enjoying deep, rich flavor.",
            "origin_code": "ID", "variety": "Typica", "process": "washed", "roast_level": "medium_dark",
            "altitude_min": 1200, "altitude_max": 1500,
            "flavor_slugs": ["chocolate", "cinnamon", "earthy"],
            "purchase_url": "https://www.maruyamacoffee.com/ec/products/list",
        },
        {
            "name": "ホンジュラス コパン COE入賞ロット カーボニックマセレーション",
            "name_en": "Honduras Copán COE Lot Carbonic Maceration",
            "description": "パッションフルーツやワインのような華やかな風味。カーボニックマセレーションによる独特の発酵感とシルキーなボディ。",
            "description_en": "Gorgeous passion fruit and wine-like flavors. Unique fermentation character from carbonic maceration with a silky body.",
            "origin_code": "HN", "variety": "Catuai", "process": "carbonic_maceration", "roast_level": "light",
            "altitude_min": 1400, "altitude_max": 1700,
            "flavor_slugs": ["tropical", "winey", "fermented"],
            "purchase_url": "https://www.maruyamacoffee.com/ec/products/list",
        },
    ],
}


def main():
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Load roaster name -> id mapping
        roaster_rows = session.execute(text("SELECT id, name FROM roasters")).fetchall()
        roaster_map = {r[1]: str(r[0]) for r in roaster_rows}

        # Load origin country_code -> id mapping (region IS NULL = country-level)
        origin_rows = session.execute(
            text("SELECT id, country_code FROM origins WHERE region IS NULL")
        ).fetchall()
        origin_map = {r[1]: str(r[0]) for r in origin_rows}

        # Load flavor_note slug -> id mapping
        fn_rows = session.execute(text("SELECT id, slug FROM flavor_notes")).fetchall()
        fn_map = {r[1]: str(r[0]) for r in fn_rows}

        total = 0
        for roaster_name, beans in BEANS_BY_ROASTER.items():
            roaster_id = roaster_map.get(roaster_name)
            if not roaster_id:
                print(f"  WARNING: Roaster '{roaster_name}' not found, skipping.")
                continue

            for bean in beans:
                bean_id = str(uuid.uuid4())
                origin_id = origin_map.get(bean["origin_code"])

                session.execute(
                    text("""
                        INSERT INTO beans (id, name, name_en, description, description_en,
                                           roaster_id, origin_id, variety, process, roast_level,
                                           altitude_min, altitude_max, purchase_url)
                        VALUES (:id, :name, :name_en, :description, :description_en,
                                :roaster_id, :origin_id, :variety, :process, :roast_level,
                                :altitude_min, :altitude_max, :purchase_url)
                    """),
                    {
                        "id": bean_id,
                        "name": bean["name"],
                        "name_en": bean["name_en"],
                        "description": bean["description"],
                        "description_en": bean["description_en"],
                        "roaster_id": roaster_id,
                        "origin_id": origin_id,
                        "variety": bean["variety"],
                        "process": bean["process"],
                        "roast_level": bean["roast_level"],
                        "altitude_min": bean["altitude_min"],
                        "altitude_max": bean["altitude_max"],
                        "purchase_url": bean["purchase_url"],
                    },
                )

                # Insert bean_flavor_notes
                for slug in bean["flavor_slugs"]:
                    fn_id = fn_map.get(slug)
                    if fn_id:
                        session.execute(
                            text("""
                                INSERT INTO bean_flavor_notes (id, bean_id, flavor_note_id)
                                VALUES (:id, :bean_id, :flavor_note_id)
                            """),
                            {"id": str(uuid.uuid4()), "bean_id": bean_id, "flavor_note_id": fn_id},
                        )

                total += 1
                print(f"  [{roaster_name}] {bean['name']}")

        session.commit()
        count = session.execute(text("SELECT COUNT(*) FROM beans")).scalar()
        fn_count = session.execute(text("SELECT COUNT(*) FROM bean_flavor_notes")).scalar()
        print(f"\nDone. Total beans: {count}, bean_flavor_notes: {fn_count}")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
