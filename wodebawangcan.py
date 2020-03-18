#coding:utf8
'''
整体思路：
1.获取常居地的霸王餐链接
2.以此访问链接并点击进行报名
3.访问一个热门城市，查看是否有天天抽奖。如果有，进行4；如果没有，重新进行3。直至访问完所有热门城市
4.获取天天抽奖的所有链接
5.如果城市不是目的地，需要更改常居地
6.依次进行天天抽奖活动的点击

未来需要的功能：
1.进行免费化妆品的抽奖
2.进行霸王餐的秒杀活动
'''
#更新 by Master_13
#@20180115

#更新 by 李强
#20191023
#
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
'''
函数功能：根据得到的活动网址，进行确认报名
输入：活动url的字典，浏览器
输出：无，直接返回
'''
def process_category(all_event_url,driver):
    total=len(all_event_url)
    print(("开始报名"+str(total)+"个活动..."))
    cnt=0
    no=0
    for url in all_event_url:
        driver.get(url[0])
        no+=1
        try:
            big_btn=driver.find_element_by_class_name("big-btn")
            if big_btn.text.find('取消报名')!=-1 or big_btn.text.find('已报名')!=-1:
                continue
            big_btn.click()

            try:    #同意黄金替补
                time.sleep(1)
                sel=Select(driver.find_element_by_class_name("J_applyExtendInfo"))
                sel.select_by_index(1)                
            except:
                pass

            time.sleep(2)
            try:
                fendian = driver.find_element_by_class_name('J_branch')
                if fendian:
                    s1 = Select(fendian)
                    s1.select_by_index(1)
                    #print(s1)
                time.sleep(1)
            except:
                pass
            time.sleep(1)
            
            ok=driver.find_element_by_id("J_pop_ok")
            ok.click()
            cnt+=1
            print(str(cnt)+" success:"+url[1])
        except Exception as e:
            print(str(no)+' failed:'+url[1])
            print(format(e))
        time.sleep(1)
    return
'''
函数功能：启动chrome,并登录
输入：可以更改为输入dper
输出：drive对象
'''
def driver_start():
    print ('正在执行……')
    
    '''
    print(sys.argv)
    print(len(sys.argv))
    dper= sys.argv[1]
    print(("your dper is:"+dper))
    '''
    #dper= 'a6689dad4712ad41c9d660c8c3ac5c250638b8fb41c5bdb880d326ee4080dcdbbf97c855cbea499a36205d9753e2e8c106fb57895ed71b12fb2f915fed62f23a62abaaad6d77e1673eb00b22b33e9285c2fe28bd067fb9c7f9f66bd6ad791bd0'
    dper = 'ae5be7dc54e0942997b87c6802b86392339fda8c7f53c2a587002a8c681e894511e7b8035130f6b9988416040d2129dd1841c0e272e2fc6bb0a310725e59a8aa15065f4e5ac72de4d59470b1266fed749b701320be292f57486dac19f023b7d6'
    opts = Options()
    opts.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"')
    driver = webdriver.Chrome(options=opts)
    time.sleep(1)
    driver.maximize_window()

    driver.get("http://s.dianping.com/event/beijing")
    driver.add_cookie({'name':'dper', 'value':dper,'path':'/'})
    driver.get("http://s.dianping.com/event/beijing")
    return driver
    
'''
函数功能：获取霸王餐活动的全部网址和标题
输入：浏览器对象
输出：网址和标题组成的字典
'''
def get_bawangcan_url(driver):
    
    tabs=driver.find_element_by_class_name('s-fix-wrap').find_elements_by_tag_name('div')
    skiptext=["牙","齿","搬家","口腔"]
    
    all_event_url=[]
    for tab in tabs:
        if tab.text.find('全部')!=-1:
            continue
        if tab.text.find('美食')!=-1: # or tab.text.find(u'玩乐')!=-1 or tab.text.find(u'酒旅')!=-1 or tab.text.find(u'生活服务')!=-1:
            tab.click()
            try:
                while(1): #点击查看更多
                    more=driver.find_element_by_class_name("load-more")
                    more.click()
                    time.sleep(2)
            except:
                pass
            time.sleep(1)
            elements=driver.find_element_by_class_name("activity-lists").find_elements_by_tag_name('li')
            for e in elements:
                a = e.find_element_by_tag_name("a")
                event_url= a.get_attribute("href")
                title=e.find_element_by_tag_name("h4")
                for s in skiptext:
                    if s in title.text:
                        continue
                all_event_url.append((str(event_url),title.text))                    
    print(all_event_url)              
    return all_event_url
'''
函数功能：改变当前登录用户的常居地
输入：浏览器对象，将常居地更换为ciy的ciy
输出：无
'''
def change_home(driver,city):
    changjudi = driver.find_element_by_id("J_user_city")
    changjudi.send_keys(city)
    big_btn=driver.find_element_by_class_name("btn-txt J_submit")
    big_btn.click()
    print('改变了常居地')
    return
'''
函数功能：与process_category类似，对得到的天天抽奖链接进行点击
需要当前页面处在城市页面，紧跟在ttcj_url后面
输入：浏览器对象，天天抽奖链接字典
输出：无
'''
#进行更改常居地时，需要验证滑块，验证滑块会显示操作异常
def click_ttcj_url(driver,all_event_url):
    total=len(all_event_url)
    print(("开始报名"+str(total)+"个活动..."))
    # http://www.dianping.com/member/myinfo/setup/basic
    # 需要确定当前活动所在城市，在上面个人信息的url中更改常居地
    cnt=0
    no=0
    for url in all_event_url:
        driver.get(url[0])
        no+=1
        try:
            print('开始点击立即抽')
            big_btn=driver.find_element_by_class_name("big-btn")
            print(big_btn.text.find('立即抽'))
            if big_btn.text.find('取消报名')!=-1 or big_btn.text.find('已报名')!=-1:
                continue           
            big_btn.click()
            print('点击了立即抽')
            time.sleep(2)
            try:
                shezhi = driver.find_element_by_class_name('doorsill-list')
                a = shezhi.find_element_by_tag_name("a")
                event_url= a.get_attribute("href")
                print(event_url)
                driver.get(event_url)
                time.sleep(2)
                changehome(driver,'上海')
                
            except:
                print('改变常居地出错')
                pass
            time.sleep(1)

            try:    #同意黄金替补
                time.sleep(1)
                sel=Select(driver.find_element_by_class_name("J_applyExtendInfo"))
                sel.select_by_index(1)                
            except:
                pass

            time.sleep(2)
            try:
                fendian = driver.find_element_by_class_name('J_branch')
                if fendian:
                    s1 = Select(fendian)
                    s1.select_by_index(1)
                    #print(s1)
                time.sleep(1)
            except:
                pass
            time.sleep(1)
            
            ok=driver.find_element_by_id("J_pop_ok")
            ok.click()
            cnt+=1
            print(str(cnt)+" success:"+url[1])
        except Exception as e:
            print(str(no)+' failed:'+url[1])
            print(format(e))
        time.sleep(1)
    return
'''
函数功能：获取url页面的天天抽奖url
输入：浏览器对象drive;当前城市活动的url
输出：如果有天天抽奖，返回所有的天天抽奖活动字典，如果没有抽奖，返回null
'''
def ttcj_url(driver,url):
    skiptext=["牙","齿","搬家","口腔"]
    driver.get(url)
    #time.sleep(1)
    tabs=driver.find_element_by_class_name('s-fix-wrap').find_elements_by_tag_name('div')
    #print(tabs)
    all_event_url=[]
    for tab in tabs:
        if tab.text.find('全部')!=-1:
            continue
        
        if tab.text.find('天天抽奖')==0: # or tab.text.find(u'玩乐')!=-1 or tab.text.find(u'酒旅')!=-1 or tab.text.find(u'生活服务')!=-1:
            print("找到了天天抽奖")
            tab.click()
            try:
                while(1): #点击查看更多
                    more=driver.find_element_by_class_name("load-more")
                    more.click()
                    time.sleep(2)
            except:
                pass
            time.sleep(1)
            try:
                elements=driver.find_element_by_class_name("activity-lists").find_elements_by_tag_name('li')
                #print(elements)
                for e in elements:
                    a = e.find_element_by_tag_name("a")
                    event_url= a.get_attribute("href")
                    title=e.find_element_by_tag_name("h4")
                    for s in skiptext:
                        if s in title.text:
                            continue
                    all_event_url.append((str(event_url),title.text))
                #print(all_event_url) 
            except:
                print("当前城市天天抽奖无内容")
                pass
    return all_event_url
    
if __name__ == '__main__':
    driver = driver_start()
    city = '广州'
    #change_home(driver,city)
    guangzhou = "http://s.dianping.com/event/shanghai"
    ttcjurl = ttcj_url(driver,guangzhou)
    print(ttcjurl)
    click_ttcj_url(driver,ttcjurl)
    #all_event_url = get_bawangcan_url(driver)
    #process_category(all_event_url, driver)
    #driver.quit()
