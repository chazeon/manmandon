# manmandon

Universal interface for batch manga downloading.

基于 Playwright 的通用漫画下载器框架。

## 支持的站点 / supported websites

站点支持可自行扩充

- 漫画柜 / 看漫画 （manhuagui）
- 拷贝漫画（copymanga）

## 用法 / usage

### 安装

本程序依赖于 Python 3。保证 Python 安装完毕后，下载后进入包含 `setup.py` 文件的
目录，执行以下命令使用 `pip` 进行安装

```bash
pip install -U .
```

安装浏览器

```bash
playwright install chromium
```

### 开始下载

如果 PATH 变量正确设置，可在工作目录中执行以下命令下载。

```bash
mmdon https://xxxx.com/xxxx/xxxx
```