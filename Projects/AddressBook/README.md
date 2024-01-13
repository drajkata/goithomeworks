## Stage 1 - Setup pipenv

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

## Stage 2 - Setup docker

Please, firstly run above instructions to activate virtual environment with pipenv. Then go through instructions below.

1. **Creating an image**

- To create an image use the following command:

  ```
  docker build . -t drajkata/hm_address_book
  ```

  You can name your image in a different way for example my_app or with flag -t [your_profile_in_docker_hub]/[name_of_your_up].

- To check your images use the following command:
  ```
  docker image ls
  ```

2. **Creating an container**

- To create a container use the following command:

  ```
  docker run -itd -p 3000:5000 drajkata/hm_address_book
  ```

  You can set other port than 3000.

- To check your container ID use the following command:
  ```
  docker container ls
  ```

2. **Run the application in the container**

- To run the app in the container use the following command:

  ```
  docker exec -it [container_id] /bin/bash
  ```

  Use bin/bash or bin/sh - it depends on your system, which command is correct.

- To exit from your application use the following command:
  ```
  exit
  ```

## Example of use

**Example of restarting the program from the beginning**

![Docker_example](https://github.com/drajkata/goithomeworks/tree/main/Projects/AddressBook/Docker_example.png)
