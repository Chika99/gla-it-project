# First Run

1. 创建虚拟环境`python3 -m venv <path>`
2. 激活虚拟环境
    - Linux/Mac `source <path>/bin/activate`
    - Windows `<path>\Scripts\activate.bat` or `<path>\Scripts\Activate.ps1`

# Update

1. 更新依赖`pip install -r requirements.txt`

2. 模型修改创建迁移`init=true python manage.py makemigrations`
    - ***init=true*** 必须传入
3. 应用迁移`init=true python manage.py migrate`
    - ***init=true*** 必须传入
4. 开启服务`django-admin runserver`
    - 如果无法运行，检查`DJANGO_SETTINGS_MODULE`环境变量
        - Linux/Mac `export DJANGO_SETTINGS_MODULE=auction.settings`
        - Windows `set DJANGO_SETTINGS_MODULE=auction.settings`
        - 或启动时指定 `django-admin runserver --settings=auction.settings`