# 监控内存CPU

[TOC]

# 一、使用教程

```bash
# 克隆代码
git clone https://github.com/AliGitOps/python_mem_cpu.git
cd python_mem_cpu/


# 安装包
pip3.11 install -r requirements.txt
```

```bash
# 使用之前可以更改代码中报警的阈值进行测试
sed -i '/cpu_usage/ s/> [0-9]\{1,2\}/> <你想更改的阈值 (CPU)>/' main.py 
sed -i '/memory_usage/ s/> [0-9]\{1,2\}/> <你想更改的阈值 (内存)>/' main.py 

```

```bash

python3 main.py
# 使用脚本之前在配置文件中添加自己对应的账号信息
# 没有问题之后写入crontab周期执行即可

```

