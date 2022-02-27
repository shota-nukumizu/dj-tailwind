# Django Single Page Application for Tailwind CSS

DjangoとTailwind CSSで開発したSPA。構造は非常にシンプル。

**正直に言って、Tailwind CSSでのフロントエンド開発が一番難しかった。**

# 完成デモ

▼タスクを追加したり削除したりする。

![](demo.png)

▼完了済みのタスクには色がつく。

![](demo2.png)


# 環境構築

まずは以下のコマンドを入力してDjangoのプロジェクトを出力させる。

```
pip install django
django-admin startproject backend .
django-admin startapp todo
```

`backend/settings.py`の定数`INSTALLED_APPS`に`todo`を追加。

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo',
]
```

ディレクトリ構造をはっきりさせるため、定数`TEMPLATES`のディレクトリにあるキー`'DIRS'`の値に`BASE_DIR / 'templates'`と書く。

この際、`templates`フォルダを新しく作成する。


```py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], #追加
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

# データベース作成

`todo/models.py`

```py
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=100)　# タイトル：タスクの名前
    is_done = models.BooleanField(default=False) # 終了したかどうかの確認。二択になるのでTrueとFalseで表現する。
```

以下のコマンドを入力してデータベースを作成する。デフォルトは`db.sqlite3`。

```powershell
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser #管理サイトにアクセスするためのusernameとpasswordを指定する
```

# テンプレート作成

`templates`ディレクトリに新規で`todos.html`を作成。以下のプログラムをコピペする。

`templates/todos.html`

```html
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tailwind Todo</title>

    <style>
        .htmx-swapping {
            opacity: 0;
            transition: opacity 1s ease-out;
        }
    </style>
</head>

<body class="bg-sky-500">
    <nav class="flex items-center justify-between px-4 py-6 text-center bg-gradient-to-r from-cyan-500 to-sky-500">
        <a href="/" class="text-2xl text-white">Tailwind Todo</a>
    </nav>

    <div class="w-4/5 my-6 mx-auto p-2 lg:p-10 bg-white rounded-xl">
        <form
            class="flex mb-6 space-x-4"
            hx-post="/add-todo/"
            hx-target="#todos"
            hx-swaps="afterend"
        >
            <input type="text" name="title" class="title flex-1 px-4 py-3 bg-gray-200 rounded-xl"
                placeholder="The Title">

            <button class="p-3 rounded-xl text-white bg-cyan-500 hover:bg-cyan-600">+</button>
        </form>

        <div class="flex py-3 rounded-xl bg-gray-100">
            <div class="w-4/5">
                <p class="px-6 text-xs font-medium text-gray-500 uppercase">Title</p>
            </div>

            <div class="hidden md:block w-1/5 px-6 text-right">
                <div class="text-xs font-medium text-gray-500 uppercase">Actions</div>
            </div>
        </div>

        <div class="divide-y divide-gray-200" id="todos">
            {% for todo in todos %}
                {% include 'partials/todo.html' %}
            {% endfor %}
        </div>
    </div>
</body>

<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/htmx.org@1.6.1"></script>
<script>
    document.body.addEventListener('htmx:configRequest', (event) => {
        event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}'
    })

    document.body.addEventListener('htmx:afterRequest', (event) => {
        document.querySelector('input.title').value = ''
    })
</script>
</html>
```

この際、CDN経由でTailwindとhtmxをインストールする

htmxを有効化するために、`templates/todos.html`の`<scripts>`タグに以下のプログラムを書く。

**この際、プログラムそのものは短いので一つのファイルに簡潔にまとめる。別でJSファイルを作らない。**

```js
document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}'
})

document.body.addEventListener('htmx:afterRequest', (event) => {
    document.querySelector('input.title').value = ''
})
```

# 開発環境

* Django 4.0
* Tailwind CSS
* htmx 0.6.1