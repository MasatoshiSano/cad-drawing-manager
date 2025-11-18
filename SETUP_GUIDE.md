# CAD図面管理システム - 別PCでのセットアップ手順

このドキュメントでは、別のPCでこのアプリケーションを動作させるための手順を説明します。

## 前提条件

- Python 3.11以上
- Node.js 18以上
- Poetry（Pythonパッケージ管理）
- AWS Bedrockへのアクセス権限

## セットアップ手順

### 1. リポジトリのクローンまたはコピー

```bash
# Gitリポジトリからクローンする場合
git clone <repository-url>
cd cad-drawing-manager

# または、既存のプロジェクトをコピーする場合
# プロジェクトフォルダ全体をコピー
```

### 2. 環境変数の設定

プロジェクトルートに`.env`ファイルを作成または編集します：

```bash
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
MODEL_ID=anthropic.claude-sonnet-4-20250514
```

**重要**: AWS認証情報は、別PCでも同じものを使用するか、新しい認証情報を設定してください。

### 3. バックエンドのセットアップ

```bash
cd backend

# Poetryがインストールされていない場合
pip install poetry

# 依存関係をインストール
poetry install

# データベースを初期化（重要！）
poetry run python init_db.py
```

**重要**: `init_db.py`を実行すると、以下のテーブルが作成されます：
- drawings（図面）
- extracted_fields（抽出フィールド）
- balloons（風船情報）
- revisions（改訂履歴）
- tags（タグ）
- edit_history（編集履歴）
- locks（編集ロック）

### 4. フロントエンドのセットアップ

```bash
cd frontend

# 依存関係をインストール
npm install

# Playwrightのブラウザをインストール（テスト用、オプション）
npx playwright install
```

### 5. ストレージディレクトリの確認

プロジェクトルートに`storage`ディレクトリが存在することを確認してください：

```
storage/
├── drawings/      # PDFファイル保存先（空でOK）
├── thumbnails/    # サムネイル保存先（空でOK）
├── logs/          # ログファイル保存先（空でOK）
└── database.db    # SQLiteデータベース（init_db.pyで作成）
```

存在しない場合は、`init_db.py`が自動的に作成します。

### 6. サーバーの起動

#### バックエンドサーバー（ターミナル1）

```bash
cd backend
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### フロントエンドサーバー（ターミナル2）

```bash
cd frontend
npm run dev
```

### 7. アクセス確認

ブラウザで以下のURLにアクセス：

- **フロントエンド**: http://localhost:5173
- **バックエンドAPI**: http://localhost:8000
- **APIドキュメント**: http://localhost:8000/docs

## 既存データの移行（オプション）

既存のPCからデータを移行する場合：

### データベースの移行

1. 既存PCの`storage/database.db`を新しいPCの`storage/`にコピー
2. 既存PCの`storage/drawings/`内のPDFファイルを新しいPCの`storage/drawings/`にコピー
3. 既存PCの`storage/thumbnails/`内のサムネイルを新しいPCの`storage/thumbnails/`にコピー

**注意**: データベースとファイルのパスが一致していることを確認してください。

### サムネイルの再生成（推奨）

データベースを移行した後、サムネイルを再生成することを推奨します：

```bash
cd backend
poetry run python regenerate_thumbnails.py
```

## トラブルシューティング

### データベースエラーが発生する場合

```bash
cd backend
poetry run python init_db.py
```

これでデータベースが初期化され、すべてのテーブルが作成されます。

### ポートが既に使用されている場合

バックエンドのポートを変更する場合：

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

フロントエンドのポートを変更する場合、`frontend/vite.config.ts`を編集してください。

### AWS認証エラーが発生する場合

`.env`ファイルの認証情報が正しいか確認してください。また、AWS CLIで認証情報を確認できます：

```bash
aws sts get-caller-identity
```

## 注意事項

1. **データベースの初期化**: 新しいPCでは必ず`init_db.py`を実行してデータベースを初期化してください。
2. **ストレージディレクトリ**: `storage/`ディレクトリはプロジェクトルートに作成されます。
3. **ファイルパス**: WindowsとLinux/Macでパス区切り文字が異なるため、パスの問題が発生する可能性があります。
4. **ポート番号**: デフォルトではバックエンド8000、フロントエンド5173を使用します。必要に応じて変更してください。

## 次のステップ

セットアップが完了したら、以下を確認してください：

1. サーバーが正常に起動しているか
2. ブラウザでアプリケーションにアクセスできるか
3. PDFファイルをアップロードできるか
4. AI解析が正常に動作するか

問題が発生した場合は、ログファイル（`storage/logs/`）を確認してください。

