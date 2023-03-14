# 中石化项目运行小贴士

## 运行前端项目
```
npm run build(可选)
npm run dev
```
请在`prophet-frontend\src\views\clustering.vue`中做出如下修改：
使用`CTRL+F`进行关键词搜索,将`webp`替换为`jpeg`,否则将看不到聚类模型在前端的更新。


## 运行后端项目
   1 在`prophet-backend\common\common.py `下修改`DATABASE_PATH `变量，将其修改为数据存放目录的绝对路径
   2 启动机器的mongodb服务
   3 在项目根目录使用terminal运行如下指令： 
 `python manage.py runserver 0.0.0.0:8000`

 ## 项目结构  
 ```
 |   db.sqlite3 ## 存放产量数据的mongodb数据库
|   demo_actual.jpeg
|   demo_sum.jpeg
|   dump_data.json
|   manage.py  ## django项目入口文件
|   README.md
|   test.py
|   三个样本.xlsx
|   数据单元.xlsx
|
+---backend ##Django框架相关文件
|   |   .DS_Store
|   |   admin.py
|   |   apps.py
|   |   config.py
|   |   models.py
|   |   tests.py
|   |   urls.py
|   |   util.py
|   |   views.py
|   |   __init__.py
|   |
|   +---migrations
|   |       __init__.py
|   |
|
+---common ##导入数据的相关操作
|   |   common.py
|   |
|
+---data
|   |   1023.py
|   |   dataset.json ##存放从mongodb读取的数据，项目实际上是从这里读取数据的
|   |   data_imputation.py ##数据缺失值处理
|   |   json_viewer.py     ##对json文件进行解析
|   |   smoothprocessing.py ##平滑处理
|   |
|   +---datasets
|   |       三个样本.xlsx
|   |
|
+---model
|   |   change_point.py ##检测prophet算法的变点
|   |   k_means_platform.py ##k_means聚类算法
|   |   Model.py  ##模型的基类
|   |   pred.py   ##所有预测模型的具体实现
|   |   util.py   ##一些工具函数，比如说归一化，计算拟合误差等等
|   |
|   +---myGM
|   |   |   curve_partition.py ##灰度模型的产量曲线分段
|   |   |   gm_fit_and_predict.py ##利用灰度模型进行产量拟合和预测
|   |   |   GM_implementation.py ##对Hubbert 旋回中涉及到的具体参数利用GM(1,1)模型进行拟合和预测
|   |   |   __init__.py
|   |   |
|   |
|   +---mySVD
|   |       singular_value_decompsition.py ##利用奇异值分解进行探究
|   |       __init__.py
|   |
|   +---sum
|   |   |   sum_partition.py ##利用最小误差直方图进行产量分段和分段拟合
|   |   |   __init__.py
|   |   |
|   |
|
+---static ##存放一些供前端展示的图片
|       clustering.jpeg
|       clustering.webp
|       demo_actual.jpeg
|       demo_sum.jpeg
|
 ```

## 一些遇到的比较棘手的问题
1 prophet模型由于其依赖的prophet库在我的windows系统下与visual c++有兼容性冲突 我尝试进行解决 但至今未果 后续我们可能会打包到docker上运行项目 师妹遇到任何问题可以来找我哈
2  聚类模型进行展示时可能会出现中文乱码的问题 我这边已经解决 但我们的设备环境不同 可能师妹的设备没有对应的中文字体 


