1. 建立项目
* 首先创建并激活虚拟环境，然后安装django（与flask步骤一样）
* 创建项目：`django-admin.py startproject learning_log .`，其中`learning_log`为项目名
* 创建数据库：`python manage.py migrate`
* 查看项目并运行服务器：`python manage.py runserver`

2. 创建应用程序
* 保持终端窗口运行runserver，再打开一个终端窗口（command + N），切换到managy.py所在的目录，激活虚拟环境，再执行：`python manage.py startapp learning_logs`，其中`learning_logs`为app名
* 定义模型：打开models.py，添加类，如Topic、Entry
* 激活模型：
    * 打开settings.py，将app名`'learning_logs',`添加至INSTALLED_APPS中
    * 对app调用makemigrations：`python manage.py makemigrations learning_logs`
    * 让Django迁移项目：`python manage.py migrate`
* Django管理网站
    * 创建超级用户：`python manage.py createsuperuser`
    * 向管理网站注册模型：打开与model.py同目录下的admin.py，输入以下代码：
      ```py
      from learning_logs.models import Topic, Entry
      admin.site.register(Topic)
      admin.site.register(Entry)
      ```
      接下来就可以通过超级用户访问管理网站：http://localhost:8000/admin/

* Django shell：
  ```py
  python manage.py shell                      #进入python shell
  >>> from learning_logs.models import Topic  #导入模型Topic
  >>> topics = Topic.objects.all()            #获取模型Topic的所有实例，返回的是列表
  >>> for topic in topics:                    #遍历列表打印实例id和实例
  ...   print topic.id, topic
  ... 
  >>> t= Topic.objects.get(id=1)              #通过id获取具体实例
  >>> t.text                                  #查看实例属性
  >>> t.date_added
  >>> t.entry_set.all()                       #通过外键关系获取数据，格式：模型小写名称_set
  ```
3. 创建网页
* 映射URL
  * 打开项目主文件夹learning_log中的urls.py，添加：  
  `url(r'', include('learning_logs.urls', namespace='learning_logs')),`
  * 在app文件夹learning_logs中创建另一个urls.py文件：
    ```py
    from django.conf.urls import url
    from . import views

    urlpatterns = [
        url(r'^$', views.index, name='index')
    ]
    ```

* 编写视图
  * 打开learning_logs中的view.py，添加方法：
    ```py
    def index(request):
        return render(request, 'learning_logs/index.html')
    ``` 

* 编写模版
  * 在learning_logs下创建目录和文件：`learning_logs/templates/learning_logs/index.html`，并添加代码。  
    接下来访问 http://localhost:8000/ 时，显示的即为index.html页面。
