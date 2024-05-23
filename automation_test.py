import random
import string
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time


# Function to generate a random email address
def generate_random_email():
    random_digits = ''.join(random.choices(string.digits, k=4))
    return f"test{random_digits}@example.com"


# Function to take a screenshot
def take_screenshot(driver, step_name):
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    screenshot_name = os.path.join(screenshots_dir, f"{step_name}.png")
    driver.save_screenshot(screenshot_name)
    print(f"Screenshot taken for step: {step_name}")


# Function to log steps
def log_step(step):
    print(f"Step: {step}")


# Initialize the Chrome driver using ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

# 1 & 2 --> Launch browser and navigate to URL
driver.get("http://automationexercise.com")
log_step("Launched browser and navigated to URL")

# 3 --> Verify that home page is visible successfully
assert "Automation Exercise" in driver.title
log_step("Verified that home page is visible successfully")
take_screenshot(driver, "home_page_visible")

time.sleep(2)

# 4 --> Add products to the cart
products = driver.find_elements(By.CLASS_NAME, 'productinfo')
for product in products[:3]:  # Adding first 3 products to cart
    product.find_element(By.TAG_NAME, 'a').click()

    # Wait for the 'Continue Shopping' button to be clickable
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Continue Shopping']"))
    )

    # Use JavaScript to click the 'Continue Shopping' button if interactable exception occurs
    try:
        continue_button.click()
    except selenium.common.exceptions.ElementNotInteractableException:
        driver.execute_script("arguments[0].click();", continue_button)

    time.sleep(1)

time.sleep(2)
log_step("Added products to the cart")
take_screenshot(driver, "products_added_to_cart")

# 5 --> Click the 'Cart' button
driver.find_element(By.XPATH, '//a[contains(@href, "/view_cart")]').click()
log_step("Clicked the 'Cart' button")
time.sleep(2)

# 6 --> Verify that cart page is displayed
shopping_cart_text = driver.page_source
assert "Shopping Cart" in shopping_cart_text
log_step("Verified that cart page is displayed")
take_screenshot(driver, "cart_page_displayed")

time.sleep(1)

# 7 --> Click Proceed To Checkout
driver.find_element(By.CLASS_NAME, 'check_out').click()
log_step("Clicked Proceed To Checkout")
time.sleep(1)

# 8 --> Click the 'Register / Login' button
driver.find_element(By.XPATH, " //u[normalize-space()='Register / Login']").click()
log_step("Clicked the 'Register / Login' button")
time.sleep(1)

# 9 --> Fill all details in Sign up and create an account
driver.find_element(By.XPATH, "//input[@placeholder='Name']").send_keys('Demo')

# Generate a random email
random_email = generate_random_email()
print(f"Generated random email: {random_email}")

driver.find_element(By.XPATH, "//input[@data-qa='signup-email']").send_keys(random_email)
driver.find_element(By.XPATH, "//button[normalize-space()='Signup']").click()
time.sleep(2)

# Fill remaining details

'''
    Account Information
'''
driver.find_element(By.ID, 'id_gender1').click()
driver.find_element(By.XPATH, "//input[@id='password']").send_keys('password123')
driver.find_element(By.XPATH, "//select[@id='days']").send_keys('1')
driver.find_element(By.XPATH, "//select[@id='months']").send_keys('January')
driver.find_element(By.XPATH, "//select[@id='years']").send_keys('2003')
driver.find_element(By.XPATH, "//input[@id='newsletter']").click()
driver.find_element(By.XPATH, "//input[@id='optin']").click()

'''
    Address Information
'''
driver.find_element(By.XPATH, "//input[@id='first_name']").send_keys('AnotherDemo')
driver.find_element(By.XPATH, "//input[@id='last_name']").send_keys('User')
driver.find_element(By.XPATH, "//input[@id='address1']").send_keys('123 Washington DC')
driver.find_element(By.XPATH, "//select[@id='country']").send_keys('United States')
driver.find_element(By.XPATH, "//input[@id='state']").send_keys('California')
driver.find_element(By.XPATH, "//input[@id='city']").send_keys('Test City')
driver.find_element(By.XPATH, "//input[@id='zipcode']").send_keys('123456')
driver.find_element(By.XPATH, "//input[@id='mobile_number']").send_keys('1234567890')
time.sleep(2)
driver.find_element(By.XPATH, '//button[contains(text(), "Create Account")]').click()

# 10 --> Verify 'ACCOUNT CREATED!' and click 'Continue'
assert "Account Created!" in driver.page_source
log_step("Verified 'ACCOUNT CREATED!' and clicked 'Continue'")
take_screenshot(driver, "account_created")

driver.find_element(By.XPATH, "//a[normalize-space()='Continue']").click()

# 11 --> Verify 'Logged in as username' at top
assert "Demo" in driver.page_source
log_step("Verified 'Logged in as username' at top")
take_screenshot(driver, "logged_in_as_username")

# 12 --> Click the 'Cart' button
driver.find_element(By.XPATH, '//a[contains(@href, "/view_cart")]').click()
log_step("Clicked the 'Cart' button")
time.sleep(1)

# 13 --> Click the 'Proceed To Checkout' button
driver.find_element(By.CLASS_NAME, 'check_out').click()
log_step("Clicked the 'Proceed To Checkout' button")

# 14 --> Verify Address Details and Review Your Order
assert "Address Details" in driver.page_source
assert "Review Your Order" in driver.page_source
log_step("Verified Address Details and Review Your Order")
take_screenshot(driver, "address_and_review")

time.sleep(1)

# 15 --> Enter the description in comment text area and click 'Place Order'
driver.find_element(By.NAME, 'message').send_keys('Please deliver between 9 AM and 5 PM.')
driver.find_element(By.XPATH, "//a[normalize-space()='Place Order']").click()
log_step("Entered the description in comment text area and clicked 'Place Order'")
time.sleep(1)

# 16 --> Enter payment details
driver.find_element(By.NAME, 'name_on_card').send_keys('Demo User')
driver.find_element(By.NAME, 'card_number').send_keys('4222222222')
driver.find_element(By.NAME, 'cvc').send_keys('123')
driver.find_element(By.NAME, 'expiry_month').send_keys('12')
driver.find_element(By.NAME, 'expiry_year').send_keys('2025')
time.sleep(1)
log_step("Entered payment details")

# 17 --> Click the 'Pay and Confirm Order' button
driver.find_element(By.XPATH, '//button[contains(text(), "Pay and Confirm Order")]').click()
log_step("Clicked the 'Pay and Confirm Order' button")

# 18 --> Verify the success message
assert "Congratulations! Your order has been confirmed!" in driver.page_source
log_step("Verified the success message")
take_screenshot(driver, "order_success")

# Close the browser
driver.quit()
log_step("Closed the browser")
