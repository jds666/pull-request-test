from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()

try:
    # 打开GitHub主页
    driver.get('https://github.com')

    # 等待GitHub主页加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'js-header-search'))
    )

    # 执行一些基本操作，例如点击登录按钮
    login_link = driver.find_element(By.LINK_TEXT, 'Sign in')
    login_link.click()

    # 等待登录页面加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'login_field'))
    )

    # 这里可以添加输入用户名和密码的代码，但出于安全原因，这里省略

    # 执行搜索操作，例如搜索'python'
    search_input = driver.find_element(By.ID, 'js-header-search')
    search_input.send_keys('python')
    search_input.send_keys(Keys.RETURN)

    # 等待搜索结果页面加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'repo-list-item'))
    )

    # 验证搜索结果中至少有一个项目
    repositories = driver.find_elements(By.CLASS_NAME, 'repo-list-item')
    assert len(repositories) > 0, "No repositories found for 'python'"

    # 打印测试结果
    print(f"Test passed: Found {len(repositories)} repositories for 'python'.")

except (NoSuchElementException, TimeoutException) as e:
    # 异常判定：如果发生异常，记录并报告
    print(f"Test failed: {e}")

finally:
    # 关闭浏览器
    driver.quit()

# 测试脚本结束
print("Test script finished.")