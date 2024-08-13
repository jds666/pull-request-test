# -*- coding: utf-8 -*-
# Author: Jin Duosi
# @Time: 2024/8/11 15:46
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GitHubLoginTestCase(unittest.TestCase):

    def setUp(self):
        # 初始化WebDriver
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)  # 测试完成后关闭浏览器

    def test_login(self):
        # 1.打开GitHub主页
        self.browser.get('https://github.com')

        # 2.等待登录按钮加载完成
        try:
            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Sign in'))
            )
        except TimeoutException:
            self.fail("登录按钮未在预期时间内加载")

        # 3.点击登录按钮
        login_button = self.browser.find_element(By.LINK_TEXT, 'Sign in')
        login_button.click()

        # 4.等待登录表单加载完成
        try:
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.ID, 'login_field'))
            )
        except TimeoutException:
            self.fail("登录表单未在预期时间内加载")

        # 5.填写用户名和密码
        username_input = self.browser.find_element(By.ID, 'login_field')
        password_input = self.browser.find_element(By.ID, 'password')
        username_input.send_keys('1111111111@qq.com')  # 替换为你的GitHub用户名
        password_input.send_keys('11111111111')  # 替换为你的GitHub密码

        # 6.点击登录按钮
        login_submit_button = self.browser.find_element(By.XPATH, '//input[@value="Sign in"]')
        login_submit_button.click()

        # 7.等待首页加载完成或出现预期元素
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'application-main'))
            )
        except TimeoutException:
            self.fail("首页或预期元素未在预期时间内加载")

        # 8.验证登录是否成功
        welcome_message = self.browser.find_element(By.CLASS_NAME, 'AppHeader-globalBar-end')
        self.assertIsNotNone(welcome_message, "登录失败，未找到欢迎信息")


    def test_github_search(self):
        # 测试搜索功能
        # 1.打开GitHub首页
        self.browser.get('https://github.com/')

        try:
            # 2.点击搜索框
            search_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[1]/div[1]/header/div/div[2]/div/div/qbsearch-input/div[1]/button'))
            )
            search_button.click()
            print("搜索框按钮已点击")

            # 等待搜索框可输入
            search_input = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="query-builder-test"]'))  # 假设的XPath，根据实际情况调整
            )

            # 3.输入搜索关键字并提交
            search_input.send_keys('python')
            search_input.send_keys(Keys.RETURN)

        except ElementNotInteractableException as e:
            print("元素不可交互: ", e)
        # 4.等待搜索结果加载完成
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/main/react-app/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/span')))
        except TimeoutException:
            self.fail("搜索结果未在预期时间内加载")

        # 5.验证搜索结果是否包含关键字
        search_results = self.browser.find_elements(By.XPATH, '//div[@class="Box-sc-g0xbh4-0 bDcVHV"]/div/div/h3/div/div[2]/a/span')
        self.assertTrue(any(keyword.text.lower().endswith('python') for keyword in search_results),
                           "搜索结果中未找到包含关键字'python'的项目")

        # 6.点击其中一个搜索结果
        first_result = search_results[0]
        first_result.click()

        # 7.验证是否成功进入项目页面
        self.assertIn('python', self.browser.current_url)
        self.assertIn('github.com', self.browser.current_url)



    def tearDown(self):
        # 测试结束后的清理工作
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)