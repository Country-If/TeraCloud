- [TeraCloud Management Platform](#teracloud-management-platform)
    - [Environment](#environment)
    - [Requirements](#requirements)

# TeraCloud Management Platform

## Environment

- OS: Windows
- Python: 3.8.13

## Requirements

- Selenium

    ```
    pip3 install selenium
    ```


- WebDriver

    - Chrome Driver

      使用的是Chrome Driver，版本为
      114.0.5735.90，路径设为[ChromeDriver/chromedriver.exe](Driver/Chrome/chromedriver.exe)，
      可根据实际情况下载对应版本的Chrome Driver。

        - 查看chrome版本号

          [chrome://settings/help](chrome://settings/help)
        - 下载对应版本的chrome driver

          [http://chromedriver.storage.googleapis.com/index.html](http://chromedriver.storage.googleapis.com/index.html)

    - Firefox

      firefox version: 118.0 driver: v0.34

      download url: [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)

    - Edge

      edge version: 118.0.2088.17
      > https://msedgewebdriverstorage.z22.web.core.windows.net/?prefix=118.0.2088.17/ (prefix为版本号)

      download url:
      [https://msedgewebdriverstorage.z22.web.core.windows.net](https://msedgewebdriverstorage.z22.web.core.windows.net)


- PyQt5

  ```
  pip3 install PyQt5
  pip3 install PyQt5-tools    # for qt designer
  ```

  see details: [PyQt5安装以及使用教程合集(2022)-知乎](https://zhuanlan.zhihu.com/p/162866700)


- func_timeout

  ```
  pip3 install func_timeout
  ```

## Release

- pyinstaller打包

  ```
  pip3 install pyinstaller    # 安装pyinstaller
  pyinstaller -F -w --distpath dist/exe src/main.py   # -F: 打包成单个exe文件，-w: 不显示cmd窗口 --distpath: 打包后的exe文件存放路径
  ```

- ISSUES

    - 打包后的exe启动时弹出chormedriver.exe窗口

      解决方法：本人修改了service.py文件，路径为：`D:\Software\anaconda3\envs\py3.8\Lib\site-packages\selenium\webdriver\common\service.py`

      参考：[解决python+selenuim运行时隐藏ChromeDriver窗口-CSDN](https://blog.csdn.net/ZDK_001/article/details/124431431)

- Reference

  > [搭建python+selenium环境,搭建谷歌浏览器,火狐浏览器,edge浏览器](https://blog.csdn.net/wangyao__1997/article/details/130784743)
