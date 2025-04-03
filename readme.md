# 📖 **Table of contents**
    
## Backend
- 🧾 Requirements
- ⚙️ Installation
- 🚀 Startup
- 🛠 API
- 📂 Backend structure

## Frontend
- 🧾 Requirements
- ⚙️ Installation
- 🚀 Startup
- 🧪 Testing
- 📂 Frontend structure





# Backend:

## 🧾 **Requirements**

- Docker
- Python
- Pip
- ollama

## ⚙️ **Installation**

1. Install docker if you don't have it.

```bash
From www.docker.com/ 
```

2. Clone the repository:

```bash
git clone git@github.com:WalMaa/adc-quality.git
```

3. Open the cloned repository and navigate in `backend` folder

```bash
cd /backend and then to /src
```

4. Install the required libraries using the following command:

```bash
pip install -r requirements.txt
```

5. Install ollama3.1 using the following command:

```bash
ollama pull ollama3.1
```

## 🚀 **Startup**

1. Start the backend in docker

```bash
docker compose up --build --watch --renew-anon-volumes
```

## 🛠 **API**

📌 APIs endpoint for version 1.0


| Method   | Endpoint                | Description                              |
| -------- | ----------------------- | ---------------------------------------- |
| `POST`   | `/messages/user`        | Save a new user message                 |
| `POST`   | `/messages/system`      | Save a new system message               |
| `GET`    | `/messages/user`        | List all user messages                  |
| `GET`    | `/messages/system`      | List all system messages                |
| `GET`    | `/messages/user/{id}`   | Retrieve a specific user message        |
| `GET`    | `/messages/system/{id}` | Retrieve a specific system message      |
| `DELETE` | `/messages/user/{id}`   | Delete a specific user message          |
| `DELETE` | `/messages/system/{id}` | Delete a specific system message        |
| `GET`    | `/llms/`                | Get available LLMs                      |
| `POST`   | `/llms/select`          | Select an LLM                           |
| `GET`    | `/llms/selected`        | Get the currently selected LLM          |
| `GET`    | `/responses/`           | List all responses                      |
| `GET`    | `/responses/{id}`       | Retrieve a specific response            |
| `DELETE` | `/responses/{id}`       | Delete a specific response              |
| `POST`   | `/prompt`               | Send a prompt to the LLM and save result|
| `GET`    | `/`                     | Root endpoint (Hello World)             |

## 🧪 Testing

Backend tests for the FastAPI application are written using **pytest**. These tests ensure the stability and reliability of various components, such as database connections, API routes, and core application logic.

### Running Tests
To run the tests, use the following command in the project root:

```bash
pytest backend/src/tests
```

### Test Files
The test files are located in the `backend/src/tests/` directory and cover the following components:

- **`test_main.py`**: Tests the main FastAPI application, including root and prompt endpoints.
- **`test_db.py`**: Tests the database connection, collection creation, and MongoDB interaction.
- **`test_llms.py`**: Tests the integration with LLMs (Large Language Models), including model selection and initialization.
- **`test_messages.py`**: Tests the messages API routes for saving, retrieving, and deleting messages.
- **`test_responses.py`**: Tests the responses API routes for managing response data.
- **`test_repository.py`**: Tests that the `init_db()` function correctly initializes the MongoDB client, database, and collections.
- **`test_llm_implementation.py`**: Tests the core LLM functionality, including the interaction with external services and prompt handling.

Overall test coverage is **`100%`**.

### Mocking and Tools
- **Mocking**: External dependencies, such as MongoDB client connections, API calls, and LLM models, are mocked using `unittest.mock.patch` and `MagicMock` to simulate interactions without making actual network requests or database changes.
- **Database Mocking**: MongoDB operations like inserting and retrieving documents are mocked to simulate database interactions, ensuring tests can be run without requiring an actual database.
- **Test Coverage**: Coverage report is generated when running the tests.


## 📂 **Backend structure**

```
/backend/
│── /app/                       # 🌐 Application-specific routes and logic
│   ├── /routes/                # 🚀 API routes (e.g., messages, llms, responses)
│── /src/                       # 🌐 Source code
│   ├── /routes/                # 🚀 API entry points (REST endpoints)
│   │   ├── llms.py             # 🚀 LLM-related endpoints
│   │   ├── messages.py         # 🚀 Message-related endpoints
│   │   ├── responses.py        # 🚀 Response-related endpoints
│   ├── db.py                   # 🌐 Database connection handling
│   ├── llm_implementation.py   # 🤖 LLM implementation logic
│   ├── main.py                 # 🚀 Application entry point (FastAPI server)
│   ├── models.py               # 🛠 Data models (Pydantic schemas)
│   ├── repository.py           # 🗄 Database repository logic
│── docker-compose.yml          # 🐳 Docker Compose configuration
│── Dockerfile                  # 🐳 Dockerfile for building the backend image
│── requirements.txt            # 📦 Python dependencies
│── .gitignore                  # 🌐 Git ignore rules
```



# Frontend

## 🧾 **Requirements**

- Node from (https://nodejs.org/en)


## ⚙️ **Installation**

1. Install dependencies.

```bash
npm install
```

## 🚀 **Startup**

1. Run the app locally

```bash
npm run dev
```

## 🧪 Testing

Frontend tests are written using **Vitest** and **React Testing Library**. These tests ensure the reliability of components and user interactions.

### Running Tests
To run the tests, use the following command:

```bash
npm test
```

### Test Files
The test files are located in the `src/tests/` directory and cover the following components:

- **`App.test.tsx`**: Tests the main application component.
- **`AppLayout.test.tsx`**: Tests the layout component, including the header and sidebar.
- **`DropdownMenu.test.tsx`**: Tests the dropdown menu component for rendering and user interactions.
- **`PromptForm.test.tsx`**: Tests the prompt form component for input handling and form submission.
- **`ResponsePage.test.tsx`**: Tests the response page for fetching and displaying data.
- **`Sidebar.test.tsx`**: Tests the sidebar component for rendering links and handling API errors.

Overall test coverage is at the moment over 90%. 

### Mocking and Tools
- **Mocking**: API calls are mocked using `vi.fn()` to simulate server responses.
- **User Interaction**: Simulated using `@testing-library/user-event`.
- **Test Coverage**: To generate a test coverage report, run:

```bash
npm test -- --coverage
```


## 📂 **Frontend structure**

```
/frontend/
│── .gitignore                  # 🌐 Git ignore rules
│── eslint.config.js            # 🔧 ESLint configuration
│── index.html                  # 🌐 HTML entry point
│── package.json                # 📦 Project dependencies and scripts
│── tsconfig.app.json           # ⚙️ TypeScript configuration for the app
│── tsconfig.json               # ⚙️ TypeScript project references
│── tsconfig.node.json          # ⚙️ TypeScript configuration for Node
│── vite.config.ts              # ⚙️ Vite configuration
│── src/                        # 🌐 Source code
│   ├── App.css                 # 🎨 Global styles
│   ├── App.tsx                 # 🌐 Main application component
│   ├── index.css               # 🎨 Tailwind CSS configuration
│   ├── main.tsx                # 🚀 Application entry point
│   ├── ResponsePage.tsx        # 🌐 Response details page
│   ├── vite-env.d.ts           # ⚙️ Vite environment types
│   ├── components/             # 🌐 Reusable components
│   │   ├── AppLayout.tsx       # 🌐 Layout component
│   │   ├── DropDownMenu.tsx    # 🌐 Dropdown menu component
│   │   ├── prompt-form.tsx     # 🌐 Prompt form component
│   │   ├── SearchComponent.tsx # 🔍 Search bar component
│   │   ├── sidebar.tsx         # 🌐 Sidebar component
```