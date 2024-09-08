from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Define Tutor credentials
TUTOR_ID = "ID"
TUTOR_PASSWORD = "Password"
website= "Write the Website"

def give_feedback(driver, comment):
    """
    Function to submit feedback with two 5-star ratings and a comment.
    """
    try:
        print("Starting feedback submission process...")

        # Mark student as present (uncheck "absent")
        absent_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "is_student_absent"))
        )
        absent_checkbox.click()
        print("Checked the student as present.")

        # Select 5 stars for the first rating
        first_rating = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                '#web-app-body-tag > div.modal-container.open.backdrop-shadow > div > div > div.modal-body > form > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > ul > li:nth-child(5)'
            ))
        )
        first_rating.click()
        print("Selected 5 stars for the first rating.")

        # Select 5 stars for the second rating
        second_rating = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                '#web-app-body-tag > div.modal-container.open.backdrop-shadow > div > div > div.modal-body > form > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > ul > li:nth-child(5)'
            ))
        )
        second_rating.click()
        print("Selected 5 stars for the second rating.")

        # Optionally rate homework if it exists
        try:
            homework_rating = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "i.fa-star"))
            )
            # Ensure there are five stars available
            stars = driver.find_elements(By.CSS_SELECTOR, "i.fa-star")
            if len(stars) >= 5:
                stars[4].click()  # Click the 5th star to rate 5 stars
                print("Selected 5 stars for homework rating.")
        except Exception as e:
            print(f"No homework rating found or error in homework rating: {e}")

        # Select comment from dropdown
        comment_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Comment"))
        )
        comment_dropdown.click()
        print("Clicked on the comment dropdown.")

        dropdown_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//option[. = '{comment}']"))
        )
        dropdown_option.click()
        print(f"Selected the comment option: {comment}")

        # Submit feedback
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".rounded-pill"))
        )
        submit_button.click()
        print("Submitted the feedback.")
    except Exception as e:
        print(f"Error during feedback submission: {e}")
        driver.save_screenshot('feedback_error_screenshot.png')

def get_number_of_students(driver):
    """
    Function to get the number of students displayed on the current page.
    """
    try:
        student_count_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[class*="font-normal"]'))
        ).text
        # Extract the current and total student count
        current_range, total_count = student_count_text.split(" of ")
        total_students = int(total_count)
        return total_students
    except Exception as e:
        print(f"Error retrieving number of students: {e}")
        return 0

def main():
    driver = None
    try:
        driver = webdriver.Chrome()
        print("WebDriver initialized.")

        # Navigate to the login page
        driver.get(website)
        print("Navigated to the login page.")

        # Automate login
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.NAME, "email"))
        ).send_keys(TUTOR_ID)  # Correctly format the email

        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        ).send_keys(TUTOR_PASSWORD)  # Locate the password field by name

        # Locate and click the login button
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        print("Logged in successfully.")

        # Wait for login to complete
        WebDriverWait(driver, 120).until(
            EC.url_contains("my-classes")
        )
        print("Login complete. Proceeding to feedback page.")

        # Maximize browser window
        driver.maximize_window()
        print("Browser window is now maximized.")

        # Wait for 15 seconds to allow manual filter modification
        time.sleep(15)
        print("15-second wait for manual filter modification completed.")

        # Process all students across pages
        while True:
            students = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr .classes-tutor-table__feedback .button"))
            )
            print(f"Number of students found: {len(students)}")

            # Loop through students and provide feedback
            for i, student in enumerate(students):
                # Scroll element into view
                driver.execute_script("arguments[0].scrollIntoView(true);", student)

                # Retry clicking the student button
                click_attempts = 3
                while click_attempts > 0:
                    try:
                        student.click()
                        break  # Exit loop if click is successful
                    except Exception as click_exception:
                        print(f"Click failed for student {i + 1}: {click_exception}")
                        # Try using JavaScript to click
                        driver.execute_script("arguments[0].click();", student)
                        click_attempts -= 1
                        time.sleep(1)  # Wait before retrying

                print(f"Clicked feedback button for student {i + 1}.")

                # Provide feedback for the student
                give_feedback(driver, 'متعاون')  # You can change the comment as needed
                print(f"Feedback provided for student {i + 1}.")

                # Delay between feedback submissions
                time.sleep(5)

            # Click the "Next" button if available
            try:
                # Ensure there are no obstructing elements
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.Toastify__toast-container'))
                )

                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[tooltip="Next"]'))
                )

                # Scroll the "Next" button into view and click
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                next_button.click()
                print("Clicked the 'Next' button to go to the next page.")
                time.sleep(5)  # Wait for the next page to load
            except Exception as e:
                print(f"No more pages or error navigating to next page: {e}")
                break  # Exit loop if no more pages or error occurs

            # Optionally, check number of students on the current page
            total_students = get_number_of_students(driver)
            if total_students == 0:
                print("No students found on the current page.")
                break  # Exit loop if no students are found

    finally:
        if driver:
            driver.quit()
            print("WebDriver closed.")

if __name__ == "__main__":
    main()
