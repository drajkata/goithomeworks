## Setup

1. **Clone the Repository:**

   - Clone this repository into a folder of choice on your local machine using the following command:

   ```
   git clone https://github.com/drajkata/goithomeworks/tree/main/Projects/AddressBook
   ```

2. **Install pipenv:**

   - Install pipenv if you haven't installed yet:
     ```
     pip install pipenv --user
     ```

3. **Setup the Application:**

   - Navigate to the project directory:
     ```
     cd AddressBook
     ```
   - Run the following command to install application with the exact version of modules, which are setted in the Pipfile.lock:
     ```
     pipenv install --deploy
     ```

4. **Run the pipenv:**

   - Start the pipenv using the following command:
     ```
     pipenv shell
     ```

5. **Run the Application:**

   - Start the Address Book application using the following command:
     ```
     pipenv run python address_book/main.py
     ```

6. **Exit pipenv:**

   - To exit pipenv use the following command:
     ```
     exit
     ```

7. **Uninstall environment:**
   - To uninstall environment of pipenv use the following command:
     ```
     pipenv --rm
     ```
   - You can verify that the operation was successful by checking if the system finds a virtual environment for this location. Use the following command:
     ```
     pipenv --where
     ```
