
#coding:utf8

#更新 by Master_13
#@20180115

#更新 by 李强
#20191023
#
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

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

def main():
    print ('正在执行……')
    skiptext=["牙","齿","搬家","口腔","代金券"]
    '''
    print(sys.argv)
    print(len(sys.argv))
    dper= sys.argv[1]
    print(("your dper is:"+dper))
    '''
    #dper = 'b09038fd8610e45e2f7bc42c9a8d35fbf4a09b99dd2f82886dbc54f2e52743138f0b611aaf2cff3fad3c5e55e5bd583a62825774d8124d21fea7bdc8e7090d8a8e664f69bb32d47b5e697b545c3a9b266131dd9eb3391936783a362d9bddf5d7'
    dper = 'a6689dad4712ad41c9d660c8c3ac5c25594ca4554896f81822d7663e41fdd83c764a17f6b441e34f95b0c1ff0014a7f19c08487dbcfef72d763a355f98003e33715dca25e7c3e23a98fb655fbee0706533e5ec111c4ad87fda1641517225655d'
    
    opts = Options()
    opts.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"')
    #opts.add_argument("headless")
    driver = webdriver.Chrome(options=opts)
    time.sleep(1)
    driver.maximize_window()

    driver.get("http://s.dianping.com/event/beijing")
    driver.add_cookie({'name':'dper', 'value':dper,'path':'/'})
    driver.get("http://s.dianping.com/event/beijing")
    
    tabs=driver.find_element_by_class_name('s-fix-wrap').find_elements_by_tag_name('div')
    
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
    #print(all_event_url)
    process_category(all_event_url, driver)
              
    driver.quit()

if __name__ == '__main__':
    main()
