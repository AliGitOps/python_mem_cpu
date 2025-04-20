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
import configparser


class Conf:
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.f = os.path.join(self.root_path + "/config.conf")
        self.conf.read(self.f)



    def read_email(self, m, n):
        name = self.conf.get(m, n)  # 获取指定section的option值
        logger.info(f"获取指定section: {m}下的option: {n}的值为{name}")
        return name

    def read_dingtalk(self, m, n):
        name = self.conf.get(m, n)
        logger.info(f"获取指定section: {m}下的option: {n}的值为{name}")
        return name


# 钉钉告警通知
def send_dingtalk_message(message):
    # 实例化类
    dingtalk_conf = Conf()
    # 钉钉 webhook
    dingtalk_key = dingtalk_conf.read_dingtalk("dingtalk", "key")
    print(dingtalk_key)
    # 钉钉 关键词
    dingtalk_value = dingtalk_conf.read_dingtalk("dingtalk", "value")
    print(dingtalk_value)


    """发送钉钉消息"""
    # 确保消息中包含关键字
    message_with_keyword = f"{message}\n{dingtalk_value}"

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": message_with_keyword
        }
    }

    response = requests.post(dingtalk_key, json=data, headers=headers)

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
    try:
        # 实例化类
        qq_conf = Conf()
        # qq 账号
        QQ_EMAIN = qq_conf.read_email("email", "key")
        # qq密码
        QQ_KEYWORD = qq_conf.read_email("email", "value")

        con = smtplib.SMTP_SSL('smtp.qq.com', 465)

        con.login(f'{QQ_EMAIN}', f'{QQ_KEYWORD}')

        msg = MIMEMultipart()

        subject = Header(f'Python {server}', 'utf-8').encode()
        msg['Subject'] = subject

        msg['From'] = f'{QQ_EMAIN} <{QQ_EMAIN}>'

        msg['To'] = f'{QQ_EMAIN}'

        text = MIMEText(Maintext, 'plain', 'utf-8')
        msg.attach(text)

        con.sendmail(f'{QQ_EMAIN}', f'{QQ_EMAIN}', msg.as_string())

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

    if cpu_usage > 1:
        # 获取 CPU 使用情况
        alarm_text = "CPU使用率使用率告警"
        cpu_text = f"CPU使用率告警: 请及时远程服务器进行处理: {ip_address}"

        # qq报警
        main_qq(alarm_text, cpu_text)

        # 钉钉告警
        message = f"警告：服务器 {ip_address} CPU: 资源使用率不正常, 请立即排查"
        send_dingtalk_message(message)
    try:
        # 写入告警: 时间点、阈值
        file_time("/opt/cpu_dir", "cpu_file", cpu_usage)
    except FileNotFoundError:
        logger.error("请在 Linux 服务器上运行代码")




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

    if memory_usage > 1:
        alarm_text = "内存使用率使用率告警"
        mem_text = f"内存使用率告警: 请及时远程服务器进行处理: {ip_address}"

        # qq报警
        main_qq(alarm_text, mem_text)

        # 钉钉告警
        message = f"警告：服务器 {ip_address} MEM: 资源使用率不正常, 请立即排查"
        send_dingtalk_message(message)
    try:
        # 写入告警: 时间点、阈值
        file_time("/opt/mem_dir", "mem_file", memory_usage)
    except FileNotFoundError:
        logger.error("请在 Linux 服务器上运行代码")




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
    get_mem()
    get_cpu()





