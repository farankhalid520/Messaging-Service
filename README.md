# Flask Messaging Service with MySQL Database

This project is a Flask-based messaging service connected to a MySQL database. The service allows sending, fetching and deleting messages and stores the message data in the database via REST API.

---

## Prerequisites

Ensure you have the following installed on your system:
- Python 3.7 or higher
- Git
- Virtual Environment support (`venv` comes pre-installed with Python 3.3+)
- Flask and required dependencies (installed via `requirements.txt`)

---

## Setup Instructions

Follow these steps to clone the repository, set up the environment, and run the application:

### 1. Clone the Repository
git clone https://github.com/farankhalid520/Messaging-Service

### 2. Navigate to the Project Directory
cd Messaging-Service

### 3. Create a Virtual Environment
python -m venv venv

### 4. Activate the Virtual Environment
venv\Scripts\activate

### 5. Install Dependencies
pip install -r requirements.txt

### 6. Create connection on any local MySQL client
I used MySQL Workbench

### 7. Create Database in MySQL client
Run this query:
CREATE DATABASE message_service;

### 8. Update credentials in .env file
Update this string with your username, password and database name:
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost/database_name"
e.g.
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root123@localhost/message_service"

### 9. Initialize the Database and Run Migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

### 10. Run the Application
python run.py

This starts the Flask development server, allowing you to access the messaging service application locally. By default, it runs on http://127.0.0.1:5000/

---

## API Testing Guide

This guide provides instructions for testing the messaging service API endpoints using a client like Postman.

### 1. **Submit a Message to a Recipient (POST)**

**Endpoint**:  
`http://127.0.0.1:5000/api/v1/messages/send`

**Request**:  
- **Method**: `POST`  
- **Headers**:  
  - `Content-Type: application/json`
- **Body (JSON)**:  

  ```json
  {
    "recipient": "OSTTRA",
    "content": "My first message"
  }

 **Description**:
 This endpoint allows you to send a message to a specific recipient.

 ![image alt](https://github.com/farankhalid520/Messaging-Service/blob/7377c22767b2782d05f0f2d4028d8a9a58be1064/screenshots/POST%20Message.png)

### 2. **Fetch Messages by Status (GET)**

**Endpoint**:  
`http://127.0.0.1:5000/api/v1/messages/status?status=[read/unread]`

**Request**:  
- **Method**: `GET`  
- **Parameters**:  
  - `status` (required):  
    - `read`  
    - `unread`

**Description**:  
This endpoint allows you to retrieve messages based on their read/unread status. Use the `status` query parameter to specify whether you want to fetch messages that are marked as `read` or `unread`.

**Example Request**:  
- To fetch unread messages:  
  `GET http://127.0.0.1:5000/api/v1/messages/status?status=unread`
  
- To fetch read messages:  
  `GET http://127.0.0.1:5000/api/v1/messages/status?status=read`
  
**Response**:  
- The response will return a list of messages filtered by the specified status.
![image alt](https://github.com/farankhalid520/Messaging-Service/blob/7377c22767b2782d05f0f2d4028d8a9a58be1064/screenshots/GET%20read.png)

![image alt](https://github.com/farankhalid520/Messaging-Service/blob/7377c22767b2782d05f0f2d4028d8a9a58be1064/screenshots/GET%20unread.png)

### 3. **Delete a Single Message (DEL)**

**Endpoint**:  
`http://127.0.0.1:5000/api/v1/messages/delete/[id]`

**Request**:  
- **Method**: `DELETE`  
- **Parameters**:  
  - `id` (required): The unique identifier of the message to be deleted.

**Description**:  
This endpoint allows you to delete a single message from the database using its unique `id`.

**Example Request**:  
- To delete a message with ID 1:  
  `DELETE http://127.0.0.1:5000/api/v1/messages/delete/1`

**Response**:  
- A success message indicating that the message has been deleted, or an error message if the message ID does not exist.

 ![image alt](https://github.com/farankhalid520/Messaging-Service/blob/7377c22767b2782d05f0f2d4028d8a9a58be1064/screenshots/DEL%20one.png)
 
### 4. **Delete Multiple Messages (DEL)**

**Endpoint**:  
`http://127.0.0.1:5000/api/v1/messages/delete/range?start_id=[id]&stop_id=[id]`

**Request**:  
- **Method**: `DELETE`  
- **Parameters**:  
  - `start_id`: The starting ID of the range of messages to be deleted.
  - `stop_id` : The ending ID of the range of messages to be deleted.

**Description**:  
This endpoint allows you to delete multiple messages from the database within a specific range of IDs (inclusive).

**Example Request**:  
- To delete messages between IDs 1 and 5:  
  `DELETE http://127.0.0.1:5000/api/v1/messages/delete/range?start_id=1&stop_id=5`
  

**Response**:  
- If messages are deleted successfully, you will receive a success message indicating the number of deleted messages.
  
  Example response for successful deletion:
  ```json
  {
    "message": "5 messages deleted between IDs 1 and 5"
  }

 - If the specified range does not contain any existing messages, you will receive a message like this:

   Example response when no messages are deleted:
   ```json
   {
     "message": "0 messages deleted between IDs 10 and 14"
   }

 ![image alt](https://github.com/farankhalid520/Messaging-Service/blob/7377c22767b2782d05f0f2d4028d8a9a58be1064/screenshots/DEL%20multiple.png)   


### 5. **Fetch Messages (Including Previously Fetched) Ordered by Time and Index (GET)**

**Endpoint**:  
`http://127.0.0.1:5000/api/v1/messages/all?start=[id]&stop=[id]`

**Request**:  
- **Method**: `GET`  
- **Parameters**:  
  - `start`: The starting ID of the range of messages to be fetched.
  - `stop` : The ending ID of the range of messages to be fetched.

**Description**:  
This endpoint retrieves messages between the specified `start_id` and `stop_id`, ordered by time (oldest to newest) and index. This allows you to fetch previously fetched messages in the desired range.

**Example Request**:  
- To fetch messages between IDs 1 and 5:  
  `GET http://127.0.0.1:5000/api/v1/messages/all?start=1&stop=5`

**Response**:  
- If messages are retrieved successfully, you will receive a response containing the list of messages ordered by time (oldest to newest) else if the range specified does not exist an empty response [] will be returned.

  Example response:
  ```json
  {
    "messages": [
      {
        "id": 1,
        "recipient": "OSTTRA",
        "content": "My first message",
        "status": "unread",
        "timestamp": "2025-01-15T15:30:00"
      },
      {
        "id": 2,
        "recipient": "Faran",
        "content": "Another message",
        "status": "read",
        "timestamp": "2025-01-15T15:35:00"
      }
    ]
  }

![image alt](https://github.com/farankhalid520/Messaging-Service/blob/7377c22767b2782d05f0f2d4028d8a9a58be1064/screenshots/GET%20multiple.png) 

  ---

## Assumptions

1. **Recipient**:  
   The `recipient` field in each message represents the username within the messaging service. Each recipient corresponds to a unique user who can receive messages sent via the service.

2. **Message Status**:  
   Upon initial submission, all messages are stored in the database with a status of `unread`. The status of a message is updated to `read` only after it is fetched using the API endpoint described in Step 2 of the API Testing Guide.

3. **Message Ordering**:  
   When fetching messages using the API endpoint in Step 5 of the API Testing Guide, the messages are returned in chronological order, from the oldest to the newest based on the timestamp associated with each message.

4. **Message ID**:  
   The `id` field is a unique identifier assigned to each message in the database. It is used to reference and manipulate specific messages within the system (e.g., deleting a single message or fetching messages within a specific range).

