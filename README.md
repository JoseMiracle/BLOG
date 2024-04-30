# Blogging Platform API

Welcome to the  Blogging Platform API! This project provides a powerful RESTful API for creating, managing, and interacting with captivating blog content. Whether you're a seasoned blogger or just starting your journey, this API has all the features you need to create an engaging blogging experience.

## Features

- **CRUD Operations**: Seamlessly create, read, update, and delete blog posts with ease.
- **Comments**: Foster engaging discussions by allowing users to leave comments on blog posts.
- **Search Functionality**: Easily find relevant blog posts using the powerful search feature.
- **Pagination**: Enhance performance and user experience with built-in pagination.
- **User Authentication**: Ensure security and privacy with user authentication for authorized access.

## Getting Started

### Running with Docker Compose

1. **Clone the Repository**:

    ```bash
    git clone  https://github.com/JoseMiracle/BLOG.git
    ```

2. **Navigate to the Project Directory**:

    ```bash
    cd BLOG
    ```

3. **Configure Docker Compose**:

    Open the `docker-compose.yml` file and make any necessary adjustments to match your environment, such as ports or environment variables.

4. **Run Docker Compose**:

    ```bash
    docker-compose up
    ```

5. **Explore the API**:

    Once Docker Compose has finished setting up the environment, you can access the API endpoints using tools like Postman or curl at `http://localhost:8000`.

### Running with Default Django Method

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/JoseMiracle/BLOG.git
    ```

2. **Navigate to the Project Directory**:

    ```bash
    cd BLOG
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply Migrations**:

    ```bash
    python manage.py migrate
    ```

5. **Run the Development Server**:

    ```bash
    python manage.py runserver
    ```

6. **Explore the API**:

    Access the API endpoints using tools like Postman or curl at `http://localhost:8000`.
    
    USE THE POSTMAN DOCS: `https://documenter.getpostman.com/view/28107778/2sA3Bt3pyn`


## Authentication

Authentication in this application is based on JSON Web Tokens (JWT). To access protected endpoints, include the JWT token in the `Authorization` header as follows:

```http
Authorization: Bearer <jwt-token>
```

To obtain a JWT token, send a `POST` request to the `/api/accounts/sign-in/` endpoint with valid user credentials. The response will include an access token and a refresh token. Access tokens are short-lived and can be used for authentication, while refresh tokens can be used to obtain new access tokens.


# SECTION 1
    To run the programs in the SECTION_1 folder, follow these steps:
    
    - Navigate to the SECTION_1 directory in your terminal or command prompt.
    
    - Type python file_name.py and press Enter to execute the program.

## Acknowledgments

Special thanks to SkillsForge for giving me the task, I have been able to learn new things.
