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
git clone git@github.com:donhamalainen/6GVisible.git
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


## 📂 **Backend structure**

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

## 📂 **Frontend structure**

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


