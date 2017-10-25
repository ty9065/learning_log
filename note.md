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
       
---

## 让用户能够输入数据
   创建基于表单的页面的方法几乎与前面创建网页一样：定义一个URL，编写一个视图函数并编写一个模板。  
   一个主要差别是，需要导入包含表单的模块forms.py。  
   在models.py所在的目录下创建forms.py文件，编写如下代码：  
   ```py
   from django import forms
   from .models import Topic

   class TopicForm(forms.ModelForm):
       class Meta:
           model = Topic
           fields = ['text']
           labels = {'text':''}
   ```

## 让用户拥有自己的数据
1. 使用@login_required 限制访问
	* view.py中导入：`from django.contrib.auth.decorators import login_required`  
	  并在需要限制的方法前添加：`@login_required`
	* 如果用户未登录，就重定向到登录页面  
	  在settings.py末尾添加如下代码：`LOGIN_URL = '/users/login/'`

2. 将数据关联到用户：添加外键
   * models.py中导入：`from django.contrib.auth.models import User`  
     Topic类中添加外键：`user = models.ForeignKey(User)`
   * 迁移数据库  
     * 修改models.py
     * 执行命令：`python manage.py makemigrations app_name`
     * 再执行命令：`python manage.py migrate`

3. 只允许用户访问自己的主题
   * 修改views.py中的topics()：
     ```py
     topics = Topic.objects.order_by('date_added')
     改为：
     topics = Topic.objects.filter(user=request.user).order_by('date_added')
     ```

4. 保护用户的主题（防止直接通过网址访问其他用户的主题）
   * views.py中导入：`from django.http import Http404`  
     topic()中添加：
     ```py
     if topic.user != request.user:
         raise Http404
     ```

5. 将新主题关联到当前用户
   * 修改views.py中的new_topic()：
     ```py
   	 form.save()
     改为：
     new_topic = form.save(commit=False)
     new_topic.user = request.user
     new_topic.save()
     ```
   
---

## 其他笔记 
     
* 模板标签{% url 'learning_logs:index' %} 生成一个URL  
  learning_logs 是一个命名空间，而index 是该命名空间中一个名称独特的URL模式。

* return HttpResponseRedirect(reverse('learning_logs:index'))
	* reverse 接收 url 中的 name 作为第一个参数
	* learning_logs--主项目文件夹urls的namespace
	* index-------------app文件夹urls的name

* render(request, template_name, context)  
  作用---把context的内容，加载进templates中定义的文件, 并通过浏览器渲染呈现  
  参数讲解：  
    * request：固定参数。  
    * template_name：templates 中定义的文件，要注意路径名。  
                       比如'templates\polls\index.html'，参数就要写‘polls\index.html’  
    * context：要传入文件中用于渲染呈现的数据, 默认是字典格式

**注销的三种方式**：  
1. url直接定向，不需要编写视图函数views.py  
	app文件夹下的urls.py：
	```py
	from django.conf.urls import url
	from django.contrib.auth.views import logout

	urlpatterns = [
	    url(r'^logout/$', logout, {'template_name': 'learning_logs/index.html'}, name='logout'),
	]
	```

2. HttpResponseRedirect(reverse())  
	app文件夹下的urls.py：
	```py
	from django.conf.urls import url

	from . import views

	urlpatterns = [
	    url(r'^logout/$', views.logout_view, name='logout'),
	]
	```
	app文件夹下的views.py：
	```py
	from __future__ import unicode_literals

	from django.shortcuts import render
	from django.http import HttpResponseRedirect
	from django.urls import reverse

	from django.contrib.auth import logout

	def logout_view(request):
	    logout(request)
	    return HttpResponseRedirect(reverse('learning_logs:index'))
	```

3. render()  
	将方法二中的视图函数views.py中的：
	```py
	return HttpResponseRedirect(reverse('learning_logs:index'))
	改为：
	return render(request, 'learning_logs/index.html')
	```
