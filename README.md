# opus2wav-py
opus音频转换为wav

### 前置准备
下载opus-tools：https://opus-codec.org/downloads/

将opus-tool中的`opusdec.exe`、`opus2wav.py`和你要转换的opus、ogg文件放在一个文件夹中（YOUR_FILE_PATH）。


### 开始转换
```
>>> cd [YOUR_FILE_PATH]
>>> python opus2wav.py input.opus
------------------------------------
# 转换单个文件
python opus2wav.py input.opus

# 转换整个目录
python opus2wav.py /path/to/opus/files/

# 使用通配符
python opus2wav.py *.opus

# 指定输出目录
python opus2wav.py input.opus -o output_dir
```
### 关于opus的一些背景介绍
https://aoeo.eu.org/public/articles/opus%E9%9F%B3%E9%A2%91%E8%BD%AC%E6%8D%A2%E6%95%99%E7%A8%8B.html
