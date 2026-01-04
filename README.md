# 截屏 OCR 翻译工具 基于DeepSeek API

基于tesseract OCR + DeepSeek API 作为翻译接口的中英互译翻译工具



## 功能简介

---

- 全局快捷键截图（默认 Ctrl + D）
- 鼠标框选屏幕区域
- Tesseract OCR 文字识别
- 以 DeepSeek API 进行中英互译

## 注意

> [!WARNING]
> 
> 项目大部分基于AI生成，首次运行会生成config.json配置文件
>
> 目录下字体为抖音美好体，禁止商用！项目仅供学习！
>
> 目前没做多屏适配，截屏翻译仅会选择主屏幕，快捷键中设置需要自己输入快捷键名称 例如 "ctrl+l" 整体是半成品但还算够用
>
> API需要去DeepSeek官网购买，鉴于价格良心充一点够几个月，地址：https://platform.deepseek.com
>
> 本地需安装Tesseract OCR，地址：https://github.com/tesseract-ocr/tesseract

## 运行环境

---

Python 3.8 及以上（推荐 3.9 / 3.10）



## 依赖安装

---

安装命令：

~~~
pip install -r requirements.txt
~~~

一键指令：

~~~
pip install requests pytesseract Pillow PyQt5 keyboard
~~~



## Tesseract OCR

---

默认安装路径示例：

~~~
C:\Program Files\Tesseract-OCR\tesseract.exe
~~~

如无法识别，可在代码中手动指定路径：

~~~
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
~~~



## DeepSeek API 配置

---

默认接口地址：

https://api.deepseek.com/v1/chat/completions

首次运行后，在程序设置中填写：

- API Key
- API URL（默认即可）
- Model（默认 deepseek-chat）
- 全局快捷键

配置文件会保存为：

~~~
config.json
~~~



## 使用方法

---

启动程序：

~~~
python main.py
~~~

运行中会常驻托盘，翻译后窗口会自行弹出
