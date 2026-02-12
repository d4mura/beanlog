# ☕ BeanLog — プロジェクトディレクトリ構成

## 概要

BeanLog は **monorepo 構成** を採用し、Frontend・Backend・共有定義を1リポジトリで管理します。

---

## ディレクトリツリー

```
beanlog/
├── frontend/                   # Next.js（TypeScript）
│   ├── public/
│   │   ├── icons/              # PWA アイコン
│   │   ├── images/             # 静的画像
│   │   └── manifest.json       # PWA マニフェスト
│   ├── src/
│   │   ├── app/                # App Router
│   │   │   ├── [locale]/       # i18n ロケールルーティング
│   │   │   │   ├── (auth)/     # 認証関連ページ
│   │   │   │   │   ├── login/
│   │   │   │   │   └── callback/
│   │   │   │   ├── beans/      # 豆関連ページ
│   │   │   │   │   ├── [id]/
│   │   │   │   │   │   ├── page.tsx
│   │   │   │   │   │   └── review/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── roasters/   # ロースター関連ページ
│   │   │   │   │   ├── [id]/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── profile/    # マイページ
│   │   │   │   ├── search/     # 検索ページ
│   │   │   │   ├── layout.tsx
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx      # ルートレイアウト
│   │   ├── components/         # コンポーネント
│   │   │   ├── ui/             # 汎用 UI（Button, Input, Card 等）
│   │   │   ├── beans/          # 豆関連コンポーネント
│   │   │   ├── reviews/        # レビュー関連コンポーネント
│   │   │   ├── roasters/       # ロースター関連コンポーネント
│   │   │   ├── search/         # 検索関連コンポーネント
│   │   │   └── layout/         # レイアウト（Header, Footer, Nav）
│   │   ├── lib/                # ユーティリティ
│   │   │   ├── supabase/       # Supabase クライアント設定
│   │   │   ├── api/            # API クライアント関数
│   │   │   └── utils/          # 汎用ユーティリティ
│   │   ├── hooks/              # カスタムフック
│   │   ├── stores/             # Zustand ストア
│   │   ├── types/              # TypeScript 型定義
│   │   └── styles/             # グローバルスタイル
│   ├── messages/               # i18n 翻訳ファイル
│   │   ├── ja.json
│   │   └── en.json
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   └── .env.example
│
├── backend/                    # FastAPI（Python）
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI アプリケーションエントリ
│   │   ├── config.py           # 設定・環境変数読み込み
│   │   ├── dependencies.py     # DI（DB セッション、認証等）
│   │   ├── routers/            # API ルーター
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── beans.py
│   │   │   ├── reviews.py
│   │   │   ├── roasters.py
│   │   │   └── recommend.py
│   │   ├── schemas/            # Pydantic スキーマ
│   │   │   ├── __init__.py
│   │   │   ├── bean.py
│   │   │   ├── review.py
│   │   │   ├── roaster.py
│   │   │   └── user.py
│   │   ├── models/             # SQLAlchemy モデル
│   │   │   ├── __init__.py
│   │   │   ├── bean.py
│   │   │   ├── review.py
│   │   │   ├── roaster.py
│   │   │   ├── user.py
│   │   │   └── flavor_tag.py
│   │   ├── services/           # ビジネスロジック
│   │   │   ├── __init__.py
│   │   │   ├── bean_service.py
│   │   │   ├── review_service.py
│   │   │   ├── roaster_service.py
│   │   │   ├── recommend_service.py
│   │   │   └── embedding_service.py
│   │   ├── repositories/       # DB アクセス層
│   │   │   ├── __init__.py
│   │   │   ├── bean_repo.py
│   │   │   ├── review_repo.py
│   │   │   └── roaster_repo.py
│   │   └── scripts/            # CLI スクリプト
│   │       ├── seed.py
│   │       └── seed_flavor_tags.py
│   ├── alembic/                # DB マイグレーション
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   ├── tests/                  # テスト
│   │   ├── conftest.py
│   │   ├── test_beans.py
│   │   ├── test_reviews.py
│   │   └── test_recommend.py
│   ├── pyproject.toml          # Python プロジェクト設定（uv）
│   ├── .env.example
│   └── Dockerfile
│
├── shared/                     # 共有定義
│   ├── constants/
│   │   ├── flavor_tags.json    # フレーバータグマスターデータ
│   │   ├── origins.json        # 産地マスターデータ
│   │   ├── processes.json      # 精製方法マスターデータ
│   │   └── roast_levels.json   # 焙煎度マスターデータ
│   └── README.md
│
├── docker/                     # Docker 関連
│   └── init.sql                # DB 初期化 SQL
│
├── docs/                       # ドキュメント
│   ├── TECH_DESIGN.md          # 技術設計書
│   ├── DEV_SETUP.md            # 開発環境セットアップ
│   └── DIRECTORY_STRUCTURE.md  # 本ファイル
│
├── .github/                    # GitHub 設定
│   └── workflows/
│       ├── ci-frontend.yml     # Frontend CI
│       └── ci-backend.yml      # Backend CI
│
├── docker-compose.yml          # ローカル開発用 Docker Compose
├── BUSINESS_PLAN.md            # 事業計画書
├── README.md                   # プロジェクト README
├── .gitignore
└── LICENSE
```

---

## 各ディレクトリの役割

### `frontend/` — フロントエンド

Next.js 15 (App Router) + TypeScript で構築する PWA。

| ディレクトリ | 役割 |
|-------------|------|
| `src/app/` | App Router ページ定義。`[locale]` でi18nルーティング |
| `src/components/` | React コンポーネント。ドメイン別にサブディレクトリ分割 |
| `src/lib/` | Supabase クライアント、API クライアント、ユーティリティ |
| `src/hooks/` | カスタムフック（`useAuth`, `useBean`, `useReview` 等） |
| `src/stores/` | Zustand によるクライアント状態管理 |
| `src/types/` | API レスポンス型、コンポーネント Props 型等 |
| `messages/` | `next-intl` 翻訳 JSON（`ja.json`, `en.json`） |
| `public/` | 静的ファイル、PWA マニフェスト、アイコン |

### `backend/` — バックエンド API

FastAPI + SQLAlchemy で構築する REST API サーバー。

| ディレクトリ | 役割 |
|-------------|------|
| `app/routers/` | API エンドポイント定義（リソースごとに分割） |
| `app/schemas/` | Pydantic スキーマ（リクエスト/レスポンス定義） |
| `app/models/` | SQLAlchemy ORM モデル（DB テーブル定義） |
| `app/services/` | ビジネスロジック（ベクトル検索、レコメンド等） |
| `app/repositories/` | DB アクセス層（クエリ実行） |
| `app/scripts/` | シードデータ投入、バッチ処理用スクリプト |
| `alembic/` | DB マイグレーション管理 |
| `tests/` | pytest によるユニットテスト・統合テスト |

### `shared/` — 共有定義

Frontend と Backend の両方で参照するマスターデータ・定数。

| ファイル | 役割 |
|---------|------|
| `flavor_tags.json` | SCA フレーバーホイールのタグ定義（日英） |
| `origins.json` | コーヒー産地マスター（国・地域） |
| `processes.json` | 精製方法マスター（ウォッシュド、ナチュラル等） |
| `roast_levels.json` | 焙煎度マスター（ライト〜ダーク） |

> Frontend はビルド時に JSON をインポート。Backend はシードスクリプトで DB に投入。

### `docker/` — Docker 関連

ローカル開発用の Docker 設定ファイル。

### `docs/` — ドキュメント

技術設計書、開発手順書、構成図など。

### `.github/` — CI/CD

GitHub Actions ワークフロー定義。Frontend / Backend それぞれの CI パイプライン。
