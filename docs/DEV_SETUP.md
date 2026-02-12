# ☕ BeanLog — 開発環境セットアップ手順書

## 1. 必要なツール・バージョン一覧

| ツール | バージョン | 用途 |
|--------|-----------|------|
| Node.js | 22.x LTS | Frontend ランタイム |
| pnpm | 9.x | パッケージマネージャー（Frontend） |
| Python | 3.12+ | Backend ランタイム |
| uv | 0.5+ | Python パッケージマネージャー |
| Docker | 27.x+ | ローカル DB |
| Docker Compose | 2.x+ | コンテナオーケストレーション |
| Git | 2.x+ | バージョン管理 |
| Supabase CLI | 2.x | ローカル Supabase（任意） |

---

## 2. ローカル開発環境の構築手順

### 2.1 リポジトリのクローン

```bash
git clone https://github.com/your-org/beanlog.git
cd beanlog
```

### 2.2 Frontend セットアップ

```bash
cd frontend

# 依存関係インストール
pnpm install

# 環境変数の設定
cp .env.example .env.local
# .env.local を編集（後述の環境変数一覧を参照）

# 開発サーバー起動
pnpm dev
```

### 2.3 Backend セットアップ

```bash
cd backend

# Python 仮想環境の作成と依存関係インストール
uv sync

# 環境変数の設定
cp .env.example .env
# .env を編集（後述の環境変数一覧を参照）

# DBマイグレーション
uv run alembic upgrade head

# 開発サーバー起動
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2.4 ローカルDB起動（Docker Compose）

```bash
# プロジェクトルートで実行
docker compose up -d

# DB接続確認
docker compose exec db psql -U beanlog -d beanlog -c "SELECT 1;"

# pgvector 拡張確認
docker compose exec db psql -U beanlog -d beanlog -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

---

## 3. Docker Compose 構成

### docker-compose.yml

```yaml
services:
  db:
    image: pgvector/pgvector:pg17
    container_name: beanlog-db
    environment:
      POSTGRES_USER: beanlog
      POSTGRES_PASSWORD: beanlog_dev
      POSTGRES_DB: beanlog
    ports:
      - "5432:5432"
    volumes:
      - beanlog_pgdata:/var/lib/postgresql/data
      - ./docker/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U beanlog"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Supabase CLI を使う場合はこちらを使用
  # supabase:
  #   image: supabase/postgres
  #   ...

volumes:
  beanlog_pgdata:
```

### docker/init.sql

```sql
-- pgvector 拡張の有効化
CREATE EXTENSION IF NOT EXISTS vector;

-- 日本語全文検索用（必要に応じて）
-- CREATE EXTENSION IF NOT EXISTS pgroonga;
```

---

## 4. 環境変数一覧

### 4.1 Frontend（`frontend/.env.local`）

| 変数名 | 説明 | 例 |
|--------|------|-----|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase プロジェクト URL | `https://xxx.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase 匿名キー | `eyJ...` |
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `NEXT_PUBLIC_APP_URL` | フロントエンド URL | `http://localhost:3000` |
| `NEXT_PUBLIC_DEFAULT_LOCALE` | デフォルトロケール | `ja` |

### 4.2 Backend（`backend/.env`）

| 変数名 | 説明 | 例 |
|--------|------|-----|
| `DATABASE_URL` | PostgreSQL 接続文字列 | `postgresql://beanlog:beanlog_dev@localhost:5432/beanlog` |
| `SUPABASE_URL` | Supabase プロジェクト URL | `https://xxx.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase サービスロールキー | `eyJ...` |
| `SUPABASE_JWT_SECRET` | JWT 検証シークレット | `your-jwt-secret` |
| `CORS_ORIGINS` | 許可するオリジン（カンマ区切り） | `http://localhost:3000` |
| `EMBEDDING_MODEL` | sentence-transformers モデル名 | `all-MiniLM-L6-v2` |
| `ENVIRONMENT` | 環境識別子 | `development` |
| `LOG_LEVEL` | ログレベル | `DEBUG` |

---

## 5. 開発サーバー起動手順

### 5.1 全サービス一括起動

```bash
# 1. DB 起動
docker compose up -d

# 2. Backend 起動（別ターミナル）
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. Frontend 起動（別ターミナル）
cd frontend
pnpm dev
```

### 5.2 アクセス先

| サービス | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API ドキュメント（Swagger） | http://localhost:8000/docs |
| API ドキュメント（ReDoc） | http://localhost:8000/redoc |

### 5.3 よく使うコマンド

```bash
# --- Frontend ---
pnpm dev              # 開発サーバー起動
pnpm build            # プロダクションビルド
pnpm lint             # ESLint 実行
pnpm type-check       # TypeScript 型チェック

# --- Backend ---
uv run uvicorn app.main:app --reload    # 開発サーバー起動
uv run pytest                           # テスト実行
uv run alembic upgrade head             # マイグレーション適用
uv run alembic revision --autogenerate -m "description"  # マイグレーション生成
uv run ruff check .                     # Lint
uv run ruff format .                    # Format

# --- Docker ---
docker compose up -d      # DB起動
docker compose down        # DB停止
docker compose logs -f db  # DBログ確認
```

---

## 6. Supabase ローカル開発（任意）

Supabase CLI を使えば Auth を含むフルスタックをローカルで動かせます。

```bash
# Supabase CLI インストール
brew install supabase/tap/supabase  # macOS
# または
npx supabase init

# ローカル Supabase 起動
npx supabase start

# 出力される URL とキーを .env に設定
# API URL:   http://127.0.0.1:54321
# anon key:  eyJ...
# service_role key: eyJ...
```

> ⚠️ ローカル Supabase を使う場合は Docker Compose の `db` サービスは不要です。

---

## 7. 初期データ投入

```bash
cd backend

# シードデータ投入（フレーバータグ + サンプル豆データ）
uv run python -m app.scripts.seed

# フレーバータグのみ投入
uv run python -m app.scripts.seed_flavor_tags
```

---

## 8. トラブルシューティング

| 問題 | 解決方法 |
|------|---------|
| DB 接続エラー | `docker compose ps` で DB が起動しているか確認 |
| pgvector が使えない | `CREATE EXTENSION IF NOT EXISTS vector;` を実行 |
| JWT 検証エラー | `.env` の `SUPABASE_JWT_SECRET` が正しいか確認 |
| CORS エラー | Backend の `CORS_ORIGINS` に Frontend の URL が含まれているか確認 |
| sentence-transformers が遅い | 初回起動時にモデルダウンロードが走る（約100MB） |
| pnpm install が失敗 | Node.js のバージョンが 22.x か確認（`node -v`） |
