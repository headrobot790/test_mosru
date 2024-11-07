## FastAPI simple parser news

Programm parse news from site mos.ru and return news in JSON format by API.

### Implemented Commands

* `make app` - up application and database
* `make down` - down application and database
* `make app-logs` - follow the logs in app container
* `make app-shell` - go to contenerized interactive shell (bash)
* `make storage` - up storage container
* `make storage-down` - down storage container
* `make prepare_network_and_migration` - prepare network and apply init migration
 
## ️Requires

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/) for use Makefile

## 🛠️ Install and run

1. **Clone the repository:**
   ```bash
   git clone git@github.com:headrobot790/test_mosru.git
   cd test_DIT
   
2. Install poetry
    ```bash
    pip install poetry
   
3. and all required packages
   ```bash
   poetry install   

4. edit `.env` file with you data or use defaults

5. create Docker network
   ```bash
   docker network create backend
   
6. 🚀build and run containers with `make` command
   ```bash
   make app
   make storage
   
- or

6. 🚀run containers manually and make migrations
   ```bash
   docker compose -p mosru -f docker_compose/app.yaml --env-file .env up --build -d
   docker compose -p mosrudb -f docker_compose/storage.yaml --env-file .env up --build -d
   alembic revision --autogenerate -m 'Initial migration'
   alembic upgrade head

7. 🌍Open API documentation in your browser
   ```bash
   http://127.0.0.1:8000/docs/api
   ```

ENJOY ❤️
