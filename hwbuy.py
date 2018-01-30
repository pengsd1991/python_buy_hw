# -*- encoding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from threading import Thread


ACCOUNTS = {
        "account1":"password1"
        "account2":"password2"
    }

#MATE10 抢购地址
#BUY_URL = 'https://www.vmall.com/product/396602535.html'
#保时捷
BUY_URL = 'https://www.vmall.com/product/173840389.html'
#测试
# BUY_URL = 'https://www.vmall.com/product/144380118.html'
#登录url
LOGIN_URL = 'https://hwid1.vmall.com/CAS/portal/login.html?validated=true&themeName=red&service=https%3A%2F%2Fwww.vmall.com%2Faccount%2Facaslogin%3Furl%3Dhttps%253A%252F%252Fwww.vmall.com%252F&loginChannel=26000000&reqClientType=26&lang=zh-cn'
#登录成功手动确认URL
LOGIN_SUCCESS_CONFIRM = 'https://www.baidu.com/'
#开始自动刷新等待抢购按钮出现的时间点,提前3分钟
BEGIN_GO = '2017-11-16 10:07:10'



#进到购买页面后提交订单
def submitOrder(driver,user):
    time.sleep(1)
    while BUY_URL == driver.current_url :
        print (user+':当前页面还在商品详情！！！')
        time.sleep(3)

    while True:
        try:
            submitOrder = driver.find_element_by_link_text('提交订单')
            submitOrder.click()
            print (user+':成功提交订单')
            break
        except :
            print (user+':提交不了订单！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！')
            time.sleep(1)#到了订单提交页面提交不了订单一直等待 
            pass
    while True:
        time.sleep(3000)
        print (user+':进入睡眠3000s')
        pass

#排队中
def onQueue(driver,user):
    time.sleep(1)
    nowUrl = driver.current_url
    while True:
        try:
            tryAgain = driver.find_element_by_link_text('再试一次')
            tryAgain.click()
            print (user+':再试一次点击')
            pass
        except :
            print (user+':排队中')
            time.sleep(0.3)#排队中
            pass
        if nowUrl != driver.current_url:
            print (user+':排队页面跳转了!!!!!!!!!!!!!!')
            break
    submitOrder(driver,user)
    
#登录成功去到购买页面
def goToBuy(driver,user):
    driver.get(BUY_URL)
    print (user+'打开购买页面')
    #转换成抢购时间戳
    timeArray = time.strptime(BEGIN_GO, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    #未发现购买按钮
    no_found_bug = True
    while True:
        if time.time()>timestamp:#到了抢购时间
            try:
                buyButton = driver.find_element_by_link_text('立即申购')
                no_found_bug = False
                print (user+'立即申购按钮出现了！！！')
                #点击摩卡金
                # driver.find_element_by_xpath('//*[@id="pro-skus"]/dl[1]/div/ul/li[2]/div/a/p/span').click()
                #点击6gb+128gb
                # driver.find_element_by_xpath('//*[@id="pro-skus"]/dl[3]/div/ul/li[2]/div/a/p/span').click()
                buyButton.click()
                print (user+'立即申购')
                break
            except :    
                if no_found_bug:
                    time.sleep(0.3)
                    if BUY_URL == driver.current_url :#还在当前页面自动刷新
                        driver.get(BUY_URL)
                        pass
                    else:
                        print(user+'手动点击了申购')
                        break
                else:
                    print (user+'点击不了申购！！！！！！需要手动点击！！！！！')
                    time.sleep(0.5)
                    if BUY_URL != driver.current_url :
                        print(user+'手动点击了申购')
                        break
                    pass
        else:
            time.sleep(15)
            print (user+'睡眠15s，未到脚本开启时间：'+BEGIN_GO)
    onQueue(driver,user)

#登录商城,登陆成功后手动先访问baidu页面跳转至抢购页面
def loginMall(user,pwd):
    driver = webdriver.Chrome()
    driver.get(LOGIN_URL)
    hasLogin = False
    try:
        account = driver.find_element_by_xpath('//*[@id="login_userName"]')
        account.click()
        account.send_keys(user)
        time.sleep(1)
        password = driver.find_element_by_xpath('//*[@id="login_password"]')
        password.click()
        password.send_keys(pwd)
        print (user+'输入了账号密码，等待手动登录')
    except :    
        print (user+'账号密码不能输入')

    while True:
            time.sleep(3)
            if LOGIN_SUCCESS_CONFIRM == driver.current_url :
                print(user+'登录成功！')
                break
    goToBuy(driver,user)






if __name__ == "__main__":
    # 账号密码
    data = ACCOUNTS
    # 构建线程 
    threads = []  
    for account, pwd in data.items():  
       t = Thread(target=loginMall,args=(account,pwd,))
       threads.append(t)  
    # 启动所有线程
    for thr in threads:
        time.sleep(2)
        thr.start()