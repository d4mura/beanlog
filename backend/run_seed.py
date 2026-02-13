"""Run all seed scripts with postgres:// URL fix."""
import os

db_url = os.environ.get("DATABASE_URL", "")
if db_url.startswith("postgres://"):
    os.environ["DATABASE_URL"] = db_url.replace("postgres://", "postgresql://", 1)

from app.scripts.seed import main as seed_main
from app.scripts.seed_roasters import main as seed_roasters
from app.scripts.seed_beans import main as seed_beans
from app.scripts.seed_reviews import main as seed_reviews

if __name__ == "__main__":
    seed_main()
    seed_roasters()
    seed_beans()
    seed_reviews()
    print("All seeds completed!")
