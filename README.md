# manmandon

Universal interface for batch manga downloading.

基于 Selenium 的通用漫画下载器框架。

## 支持的站点 / supported websites

站点支持可自行扩充

- 漫画柜 / 看漫画 （manhuagui）
- 动漫之家 （dmzj）
- 拷贝漫画（copymanga）

## 用法 / usage

### 安装

本程序依赖于 Python 3。保证 Python 安装完毕后，下载后进入包含 `setup.py` 文件的
目录，执行以下命令使用 `pip` 进行安装

```bash
pip install -U .
```

### 准备

1. 建立工作目录，比如随源代码附带的 `example`，首先去下载 Chrome Driver
   （同样兼容 Microsoft Edge）。
2. 准备 `providers`
3. 准备 [TOML][1] 格式的配置文件 `config.toml`，该文件中的字段将覆盖默认配置文件
   [`default.toml`](default.toml)。

[1]: https://toml.io/en/

### 开始下载

如果 PATH 变量正确设置，可在工作目录中执行以下命令下载。

```bash
mmdon -c config.toml https://xxxx.com/xxxx/xxxx
```