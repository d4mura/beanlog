"""Seed script: insert sample users and reviews for Phase 0 MVP."""

import random
import uuid

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config import settings

random.seed(42)  # Reproducible

SAMPLE_USERS = [
    {"username": "coffee_taro", "email": "taro@example.com", "preferred_language": "ja"},
    {"username": "latte_hanako", "email": "hanako@example.com", "preferred_language": "ja"},
    {"username": "drip_master", "email": "drip@example.com", "preferred_language": "ja"},
    {"username": "bean_hunter", "email": "hunter@example.com", "preferred_language": "en"},
    {"username": "espresso_yuki", "email": "yuki@example.com", "preferred_language": "ja"},
    {"username": "aeropress_ken", "email": "ken@example.com", "preferred_language": "ja"},
    {"username": "siphon_lover", "email": "siphon@example.com", "preferred_language": "ja"},
    {"username": "nordic_roast_fan", "email": "nordic@example.com", "preferred_language": "en"},
]

BREW_METHODS = ["pour_over", "espresso", "french_press", "aeropress", "siphon", "cold_brew"]

# Comments templates (will be randomly selected and varied)
COMMENTS_JA = {
    "excellent": [
        "素晴らしい一杯！フレーバーノートの通り、{notes}の風味がしっかり感じられます。",
        "今まで飲んだ中でもトップクラス。{notes}のバランスが絶妙です。",
        "このロースターの中でも特にお気に入り。{notes}が際立っていて何度もリピートしたくなる。",
        "産地の個性がしっかり出ている。{notes}の風味が心地よく、毎朝飲みたい。",
    ],
    "good": [
        "とても美味しい。{notes}の風味が楽しめます。日常使いにもぴったり。",
        "{notes}のニュアンスがあり、飲みやすくて好みの味。リピート確定。",
        "バランスが良くて飲みやすい。{notes}がほんのり感じられて心地よい。",
        "期待通りの味わい。{notes}が感じられ、コスパも良い。",
    ],
    "average": [
        "悪くないけど、もう少し{notes}の個性がほしかった。好みが分かれるかも。",
        "普通に美味しいけど、特別感は少ない。{notes}はやや控えめ。",
        "{notes}の風味はあるものの、全体的にやや単調な印象。",
    ],
}


def generate_rating():
    """Generate realistic rating distribution (skewed toward 3.5-4.5)."""
    r = random.gauss(4.0, 0.5)
    r = max(3.0, min(5.0, r))
    return round(r * 2) / 2  # Round to 0.5 increments


def pick_comment(rating, flavor_note_names):
    notes_str = "・".join(flavor_note_names[:2]) if flavor_note_names else "コーヒー"
    if rating >= 4.5:
        template = random.choice(COMMENTS_JA["excellent"])
    elif rating >= 3.5:
        template = random.choice(COMMENTS_JA["good"])
    else:
        template = random.choice(COMMENTS_JA["average"])
    return template.format(notes=notes_str)


def main():
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 1. Create sample users
        user_ids = []
        for u in SAMPLE_USERS:
            existing = session.execute(
                text("SELECT id FROM users WHERE username = :username"),
                {"username": u["username"]},
            ).first()
            if existing:
                user_ids.append(str(existing[0]))
                print(f"  User '{u['username']}' already exists.")
                continue
            uid = str(uuid.uuid4())
            session.execute(
                text("""
                    INSERT INTO users (id, username, email, preferred_language)
                    VALUES (:id, :username, :email, :preferred_language)
                """),
                {"id": uid, **u},
            )
            user_ids.append(uid)
            print(f"  Created user: {u['username']}")
        session.commit()

        # Also include the dev user
        dev_user = session.execute(
            text("SELECT id FROM users WHERE username = 'dev_user'")
        ).first()
        if dev_user:
            user_ids.append(str(dev_user[0]))

        # 2. Load all beans
        bean_rows = session.execute(
            text("""
                SELECT b.id, b.name, b.roaster_id
                FROM beans b
                WHERE b.deleted_at IS NULL
                ORDER BY b.created_at
            """)
        ).fetchall()

        # 3. Load flavor notes per bean
        bean_fn_map = {}  # bean_id -> list of (fn_id, fn_name)
        fn_rows = session.execute(
            text("""
                SELECT bfn.bean_id, fn.id, fn.name
                FROM bean_flavor_notes bfn
                JOIN flavor_notes fn ON fn.id = bfn.flavor_note_id
            """)
        ).fetchall()
        for r in fn_rows:
            bean_fn_map.setdefault(str(r[0]), []).append((str(r[1]), r[2]))

        # 4. Create reviews
        total_reviews = 0
        total_rfn = 0
        used_pairs = set()  # track (bean_id, user_id) uniqueness

        for bean_row in bean_rows:
            bean_id = str(bean_row[0])
            bean_name = bean_row[1]
            fn_list = bean_fn_map.get(bean_id, [])

            # 2-5 reviews per bean
            num_reviews = random.randint(2, 5)
            reviewers = random.sample(user_ids, min(num_reviews, len(user_ids)))

            for user_id in reviewers:
                pair = (bean_id, user_id)
                if pair in used_pairs:
                    continue
                used_pairs.add(pair)

                rating = generate_rating()
                brew_method = random.choice(BREW_METHODS)
                fn_names = [fn[1] for fn in fn_list]
                comment = pick_comment(rating, fn_names)

                review_id = str(uuid.uuid4())
                session.execute(
                    text("""
                        INSERT INTO reviews (id, bean_id, user_id, rating, brew_method, comment)
                        VALUES (:id, :bean_id, :user_id, :rating, :brew_method, :comment)
                    """),
                    {
                        "id": review_id,
                        "bean_id": bean_id,
                        "user_id": user_id,
                        "rating": rating,
                        "brew_method": brew_method,
                        "comment": comment,
                    },
                )
                total_reviews += 1

                # Add 1-3 flavor notes to the review
                if fn_list:
                    review_fn_count = min(random.randint(1, 3), len(fn_list))
                    selected_fns = random.sample(fn_list, review_fn_count)
                    for fn_id, _ in selected_fns:
                        session.execute(
                            text("""
                                INSERT INTO review_flavor_notes (id, review_id, flavor_note_id)
                                VALUES (:id, :review_id, :flavor_note_id)
                            """),
                            {"id": str(uuid.uuid4()), "review_id": review_id, "flavor_note_id": fn_id},
                        )
                        total_rfn += 1

        session.commit()

        # 5. Verify counts
        review_count = session.execute(text("SELECT COUNT(*) FROM reviews")).scalar()
        rfn_count = session.execute(text("SELECT COUNT(*) FROM review_flavor_notes")).scalar()
        user_count = session.execute(text("SELECT COUNT(*) FROM users")).scalar()

        # 6. Check if trigger updated avg_rating
        sample = session.execute(
            text("SELECT id, name, avg_rating, review_count FROM beans WHERE review_count > 0 LIMIT 3")
        ).fetchall()

        print(f"\nDone.")
        print(f"  Users: {user_count}")
        print(f"  Reviews: {review_count}")
        print(f"  Review flavor notes: {rfn_count}")
        print(f"\nSample bean ratings (trigger check):")
        for s in sample:
            print(f"  {s[1]}: avg_rating={s[2]}, review_count={s[3]}")

        if not sample:
            # Trigger might not exist, manually update
            print("\nNo auto-updated ratings found. Updating manually...")
            session.execute(
                text("""
                    UPDATE beans SET
                        avg_rating = sub.avg_r,
                        review_count = sub.cnt
                    FROM (
                        SELECT bean_id,
                               ROUND(AVG(rating), 1) as avg_r,
                               COUNT(*) as cnt
                        FROM reviews
                        WHERE deleted_at IS NULL
                        GROUP BY bean_id
                    ) sub
                    WHERE beans.id = sub.bean_id
                """)
            )
            session.commit()
            sample2 = session.execute(
                text("SELECT name, avg_rating, review_count FROM beans WHERE review_count > 0 LIMIT 3")
            ).fetchall()
            for s in sample2:
                print(f"  {s[0]}: avg_rating={s[1]}, review_count={s[2]}")

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
