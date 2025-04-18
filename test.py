import sys
location_var = sys.argv[1]
if not location_var:
    pass

if location_var == "-h":
    """
        钉钉使用方法
    """
    print("用法如下:")
    print("    钉钉: 在 dingtalk.config 配置文件中添加 钉钉的 第一行添加钉钉的 token, 第二行添加关键词比如")
    print("        https://oapi.dingtalk.com/robot/send?access_token=xxx")
    print("        Python")
    """
        QQ使用方法
    """
    print("    QQ: 在 email.config 配置文件中添加 QQ的 第一行添加QQ的 账号, 第二行添加授权码比如")
    print("        25167869xx")
    print("        tkdqhaxmryqqxxx")
    exit(0)


if not location_var:
    pass