#### bidong-v2 （壁咚后台）大版本项目

##### 项目结构

- server.py 运行server文件
- settings.py 项目settings文件
- tools.py 从marshmallow和docstrings 生成swagger doc的工具脚本
- bidong/ 项目源码目录
  - common/ 项目一些工具代码
  - core/ 请求和数据库session的一些封装，也包括一些API通用组件
  - service/ 项目逻辑层
  - task/ celery task，处理一些耗时的操作
  - storage/
    - cache.py 处理缓存相关逻辑
    - models.py 项目数据库表models
  - view/ tornado handlers
    - platform/ 平台handlers
    - project / 项目handlers
  - router 路由配置
    - platform/ 平台
    - project /项目
- conf/ 项目配置示例
  - etc/bidong.yaml 项目配置
  - supervisord/ 项目supervisor配置示例
  - nginx/ 项目nginx配置示例
- docs/ 项目文档
  - database/ 项目数据库sql文件夹
  - api/ 项目swagger 文档
  - mpdocs.py 平台swagger 生成配置
  - pndocs.py 项目swagger 生成配置
- tests/ 项目测试用例文件夹

##### 运行

运行项目管理后台服务:
```
python server.py --serve=project --port=PORT
```

运行平台管理后台服务:
```
python server.py --serve=platform --port=PORT
```

运行celery-task-worker

```
celery -A bidong.task worker -l info
```

##### 开发测试

1. preparation
   1. 数据库版本为 Mariadb 10.0以上，创建数据库
   2. 将 docs/database/bidongv2.sql 数据导入数据库
   3. 初始化一些配置（可选），如导入用户自定义属性 (docs/database/dyncol.sql)
   4. 将项目配置conf/etc/bidong.,yaml copy 到配置文件目录，并对配置做相应的修改，生产环境可以将配置文件copy 到/etc/目录而无需做任何修改，开发机则需要在环境变量中配置 CONF_PATH ，值为配置文件路径
2. 测试

```

python -W error -m unittest tests/xxxx/test_xxxx.py -v
py -W error -m unittest discover -s tests/view/platform -p "test_*.py"
py -W error -m unittest discover -s tests/view/project -p "test_*.py"
```
