# 简介

+ 本项目是一个基于django的博客系统，使用django-mdeditor作为编辑器，博客使用markdown语法
+ 使用django自带的后台管理系统，可以方便的管理博客
+ 可以多用户撰写博客，但用户之间数据隔离尚未实现
+ 本项目是一个练手项目，用于学习django，本人已经部署在服务器上，可以访问[这里（以后再来更新地址）](http://www.0x0x0x0.cn:8000/)
+ 本项目的前端使用了bootstrap，后端使用了django，数据库使用了sqlite3
+ 提供了Dockerfile文件，可以方便的部署到docker容器中
+ 需要自行修改SECRET_KEY和DEBUG配置，以及ALLOWED_HOSTS配置
+ DJANGO_SUPERUSER_USERNAME和DJANGO_SUPERUSER_PASSWORD是创建超级用户的用户名和密码，默认为admin，可自行修改
+ 本项目的功能还在不断完善中，欢迎大家提出建议和意见
