# First Run

1. 创建虚拟环境`python3 -m venv <path>`
2. 激活虚拟环境
   - Linux/Mac `source <path>/bin/activate`
   - Windows `<path>\Scripts\activate.bat` or `<path>\Scripts\Activate.ps1`

# Update

1. 拉取最新版本`git pull`
2. 更新依赖`pip install -r requirements.txt`
3. 模型修改创建迁移`python manage.py makemigrations`
4. 应用迁移`python manage.py migrate --run-syncdb`
5. 填充数据库`python population_script.py`
   - 注意上步结束后保证添加参数`--run-syncdb` 保证已创建数据库
6. 开启服务`django-admin runserver`
   - 如果无法运行，检查`DJANGO_SETTINGS_MODULE`环境变量
     - Linux/Mac `export DJANGO_SETTINGS_MODULE=auction.settings`
     - Windows `set DJANGO_SETTINGS_MODULE=auction.settings`
     - 或启动时指定 `django-admin runserver --settings=auction.settings`
   - 如果提示找不到 auction 模块，尝试`python manage.py runserver`
7. Populating script with example data `python population_script.py`
