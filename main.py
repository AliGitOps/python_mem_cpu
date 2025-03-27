import sys
import time
import psutil
import os
import smtplib
import socket
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from loguru import logger


# 钉钉告警通知
def send_dingtalk_message(message):


    """
    使用 dingtalk.config 配置文件存放 钉钉的 token 和 关键词
    配置文件用法:
    https://oapi.dingtalk.com/robot/send?access_token=<你的token>
    <你的机器人关键词>
    """
    with open("dingtalk.config", "r") as dingtalk:
        DINGTALK_WEBHOOK_URL = dingtalk.readline().strip()
        KEYWORD = dingtalk.readline().strip()



    """发送钉钉消息"""
    # 确保消息中包含关键字
    message_with_keyword = f"{message}\n{KEYWORD}"

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": message_with_keyword
        }
    }

    response = requests.post(DINGTALK_WEBHOOK_URL, json=data, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        result = response.json()
        if result.get('errcode') == 0:
            print("消息发送成功")
        else:
            logger.error(f"消息发送失败，原因: {result}")
    else:
        logger.error(f"HTTP请求失败，状态码: {response.status_code}")



def main_qq(server, Maintext):
    """
        使用 email.txt 配置文件存放 qq 账号 和 关键词
        配置文件用法:
        <qq账号>
        <你的机器人关键词>
        """
    with open("email.config", "r") as qq:
        QQ_EMAIN = qq.readline().strip()
        QQ_KEYWORD = qq.readline().strip()
    try:
        con = smtplib.SMTP_SSL('smtp.qq.com', 465)

        con.login(f'{QQ_EMAIN}', f'{QQ_KEYWORD}')

        msg = MIMEMultipart()

        subject = Header(f'Python {server}', 'utf-8').encode()
        msg['Subject'] = subject

        msg['From'] = f'{QQ_EMAIN}@qq.com <{QQ_EMAIN}@qq.com>'

        msg['To'] = f'{QQ_EMAIN}@qq.com'

        text = MIMEText(Maintext, 'plain', 'utf-8')
        msg.attach(text)

        con.sendmail('2516786946@qq.com', '2516786946@qq.com', msg.as_string())

        con.quit()
    except smtplib.SMTPServerDisconnected:
        logger.error("QQ账户或者密码不正确")


# cpu
# 判断
# 写入文件
# 邮箱通知
def get_cpu():
    # 获取运行脚本的 IP 地址
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    cpu_usage = psutil.cpu_percent(interval=1)

    if cpu_usage > 75:
        alarm_text = "CPU使用率使用率告警"
        cpu_text = f"CPU使用率告警: 请及时远程服务器进行处理: {ip_address}"

        # 获取 CPU 使用情况
        main_qq(alarm_text, cpu_text)

        # 写入告警: 时间点、阈值
        file_time("/opt/cpu_dir", "cpu_file", cpu_usage)


        # 钉钉告警
        message = f"警告：服务器 {ip_address} CPU: 资源使用率不正常, 请立即排查"
        send_dingtalk_message(message)


# 内存
# 判断
# 写入文件
# 邮箱通知
def get_mem():
    # 获取运行脚本的 IP 地址
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # 获取 内存 使用情况
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent

    if memory_usage > 75:
        alarm_text = "内存使用率使用率告警"
        mem_text = f"内存使用率告警: 请及时远程服务器进行处理: {ip_address}"

        main_qq(alarm_text, mem_text)

        # 写入告警: 时间点、阈值
        file_time("/opt/mem_dir", "mem_file", memory_usage)

        # 钉钉告警
        message = f"警告：服务器 {ip_address} MEM: 资源使用率不正常, 请立即排查"
        send_dingtalk_message(message)



def file_time(create_dir, file_name, cm):
    # 定义监控到达阈值时的当时阈值写入文件目录
    # 初始化目录, 如果目录不存在则新建
    if not os.path.exists(create_dir):
        os.mkdir(create_dir)

    # 定义时间格式: 20250316-165055
    current_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
    with open(f"{create_dir}/{file_name}", "a+") as f:
        f.write(f"{current_time}:  {cm}\n")
        f.close()



if __name__ == "__main__":

    try:
        location_var = sys.argv[1]
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
    except Exception as e:
        get_mem()
        get_cpu()
