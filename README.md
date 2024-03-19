# hknweb

Welcome! This is the *in-progress website redesign* for the [IEEE-Eta Kappa Nu (HKN)](https://hkn.ieee.org/) [University of California, Berkeley Mu Chapter](https://dev-hkn.eecs.berkeley.edu/), built with [Django](https://www.djangoproject.com/), [Django REST framework](https://www.django-rest-framework.org/), and [Vue.js](https://vuejs.org/).

## Setup and Development

1. **Fork and Clone the Repository:** Go to [https://github.com/compserv/hknweb](https://github.com/compserv/hknweb) and click on the "Fork" button in the top left corner to fork the repository to your GitHub account. Clone the repository to your local machine.

2. **Install Python 3.9 and Poetry:** Ensure you have Python 3.9 installed on your system. You can download it from [python.org](https://www.python.org/downloads/). Then, install [Pipx](https://pipx.pypa.io/stable/installation/) if not already installed. Finally, install Poetry:

    ```sh
    pipx install poetry
    ```

3. **Install Dependencies:** Navigate to the cloned repository directory (`hknweb`) in your terminal and run the following command to install project dependencies using Poetry:

    ```sh
    poetry install
    ```

4. **Activate Virtual Environment:** Run the following command to activate the virtual environment created by Poetry:

    ```sh
    poetry shell
    ```

5. **Apply Migrations:** Apply all database changes using the following command:

    ```sh
    python manage.py migrate
    ```

6. **Run the Server:** Finally, run the development server using the following command:

    ```sh
    python manage.py runserver
    ```

    You should now be able to access the website locally at `http://localhost:8000`.

    In order to access the admin interface, run

    ```sh
    python manage.py createsuperuser
    ```

Complete the following prompts to create a local admin user, which can then be used to access the admin interface by logging in at `http://localhost:8000/admin`.

## Deployment

The deployment pipeline pulls from `compserv/master` to OCF servers using `fabfile.py`.

```sh
# Activate our dev environment
poetry shell

# Depending on your ssh setup, this may or may not work for you:
HKNWEB_MODE="prod" fab deploy

# If your SSH key to the apphost requires a password to unlock:
HKNWEB_MODE="prod" fab --prompt-for-passphrase deploy

# If you have no SSH key to the apphost, and require password authentication:
HKNWEB_MODE="prod" fab --prompt-for-login-password deploy
```

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as per the terms of the license.
