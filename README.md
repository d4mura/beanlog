# ☕ BeanLog

コーヒー豆のレビュー＆発見プラットフォーム

## 技術スタック

| レイヤー | 技術 |
|---------|------|
| Frontend | Next.js 15, TypeScript, Tailwind CSS 4, next-intl |
| Backend | FastAPI, SQLAlchemy, Alembic |
| Database | PostgreSQL 17 + pgvector |
| Auth | Supabase Auth |
| Search | pgvector (コサイン類似度) |

## ローカル開発

### 前提条件

- Node.js 22.x / pnpm 9.x
- Python 3.12+ / uv 0.5+
- Docker / Docker Compose

### セットアップ

```bash
# 1. DB起動
docker compose up -d

# 2. Backend
cd backend
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run python -m app.scripts.seed
uv run uvicorn app.main:app --reload --port 8000

# 3. Frontend
cd frontend
cp .env.example .env.local
pnpm install
pnpm dev
```

### アクセス

| サービス | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

## プロジェクト構成

```
beanlog/
├── frontend/    # Next.js (TypeScript)
├── backend/     # FastAPI (Python)
├── shared/      # 共有定数・マスターデータ
├── docker/      # Docker関連
└── docs/        # ドキュメント
```

詳細は [docs/DIRECTORY_STRUCTURE.md](docs/DIRECTORY_STRUCTURE.md) を参照。
