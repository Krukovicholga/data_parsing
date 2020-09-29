from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
driver.get('https://mail.ru')
login_form = driver.find_element_by_id('mailbox:login-input')
login_form.send_keys('study.ai_172')
passw = driver.find_element_by_id('mailbox:submit-button')
passw.send_keys(Keys.RETURN)
passw = driver.find_element_by_id('mailbox:password-input')
time.sleep(5)
passw.send_keys('NextPassword172')
passw.send_keys(Keys.RETURN)
time.sleep(7)
letters_list = []
letters = driver.find_elements_by_class_name('llc')
time.sleep(7)
first_letters_link = letters[0].get_attribute('href')
driver.get(first_letters_link)
time.sleep(10)
next_button = driver.find_element_by_class_name('button2_arrow-down')
next_button.click()
letter_info = {}
while True:
    try:
        time.sleep(5)
        letter_subj = driver.find_element_by_class_name('thread__subject')
        letter_author = driver.find_element_by_class_name('letter-contact')
        letter_date = driver.find_element_by_class_name('letter__date')
        letter_text = driver.find_element_by_class_name('letter__body').text
        letter_info['subject'] = letter_subj.text
        letter_info['author'] = letter_author.text
        letter_info['date'] = letter_date.text
        letter_info['text'] = letter_text
        letters_list.append(letter_info)
        next_button.click()
    except:
        print(letters_list[1])
        break

driver.quit()




