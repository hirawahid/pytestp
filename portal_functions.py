import time


class portal():


    def login(self,url,driver,step_wait=0.5):
        driver.get(url + '/auth/login')
        driver.find_element_by_xpath("//div[@id='app']/main/form/div[1]/input").clear()
        driver.find_element_by_xpath("//div[@id='app']/main/form/div[1]/input").send_keys("admin")
        time.sleep(step_wait)
        driver.find_element_by_xpath("//div[@id='app']/main/form/div[2]/input").clear()
        driver.find_element_by_xpath("//div[@id='app']/main/form/div[2]/input").send_keys("admin")
        time.sleep(step_wait)
        driver.find_element_by_xpath("//div[@id='app']/main/form/button").click()
        time.sleep(step_wait)

    def goto_component_config(self,url,driver,step_wait=0.5):
        time.sleep(step_wait)
        driver.get(url + '/config')
        time.sleep(step_wait)
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/header/section[2]/ul/li/a/i').click()
        time.sleep(step_wait)
        driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/header/section[2]/ul/li/div/ul/li[1]/a/div/span').click()
        time.sleep(step_wait)
        #self.driver.find_element_by_xpath(component_xpath_in_menu).click()
        #time.sleep(step_wait)
    def to_export(self,path,driver,step_wait=0.5):
        driver.find_element_by_xpath(path).click()
        time.sleep(step_wait)


