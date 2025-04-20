import sys


# print(len(sys.argv[1]))
#
#
#
# print(sys.argv[1])

if len(sys.argv[1]) < 1:
    pass
elif sys.argv[1] == "-v":
    print("version: 5")
    exit(0)
elif sys.argv[1] == "-h":
    print("用法如下:")
    print("    在 config.conf 配置文件中添加对应的 qq邮箱地址和钉钉地址(授权和、关键词)")
    exit(0)
