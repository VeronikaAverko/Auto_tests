import requests
import pytest

# Настройки
BASE_URL = "https://ru.yougile.com"
BEARER_TOKEN = "nmHwtlh1zfhVYa2wdjS+vGJKjErc6vosW7w6TECPMHEA593pIeDgnduYo6yj7iJh"
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}

# ---- Авторизация ----
def test_auth_examples():
    # Получить список компаний
    auth_data = {
        "login": "www.wwwerovika@mail.ru",
        "password": "3898960aaa",
        "name": "A111"
    }
    response = requests.post(
        f"{BASE_URL}/api-v2/auth/companies",
        headers={"Content-Type": "application/json"},
        json=auth_data
    )
    assert response.status_code in [200, 201], f"Ошибка авторизации: {response.text}"
    company_id = response.json()["content"][0]["id"]

    # Создать ключ
    key_data = {
        "login": "www.wwwerovika@mail.ru",
        "password": "3898960aaa",
        "companyId": company_id
    }
    response = requests.post(
        f"{BASE_URL}/api-v2/auth/keys/get",
        headers={"Content-Type": "application/json"},
        json=key_data
    )
    assert response.status_code in [200, 201], f"Ошибка создания ключа: {response.text}"

    # Проверка формата ответа и получение ключа
    response_json = response.json()
    assert isinstance(response_json, list), "Ответ API должен быть списком"
    assert len(response_json) > 0, "Список ответов не должен быть пустым"
    assert "key" in response_json[0], "В первом элементе списка должен быть ключ 'key'"

    api_key = response_json[0]["key"]

# ---- Задачи ----
def test_task_operations():
    # Создать задачу
    task_data = {
        "title": "Купить товар",
        "columnId": "94307f8a-0409-4511-9b0d-30f2c663c160"
    }
    response = requests.post(
        f"{BASE_URL}/api-v2/tasks",
        headers=HEADERS,
        json=task_data
    )
    assert response.status_code == 201, f"Ошибка создания задачи: {response.text}"
    new_task_id = response.json()["id"]

    # Получить список задач
    response = requests.get(
        f"{BASE_URL}/api-v2/tasks",
        headers=HEADERS
    )
    assert response.status_code == 200, f"Ошибка получения задач: {response.text}"

    # Получить задачу по ID
    response = requests.get(
        f"{BASE_URL}/api-v2/tasks/{new_task_id}",
        headers=HEADERS
    )
    assert response.status_code == 200, f"Ошибка получения задачи: {response.text}"

    # Изменить задачу
    update_data = {
        "title": "Проверка изменения",
        "columnId": "94307f8a-0409-4511-9b0d-30f2c663c160"
    }
    response = requests.put(
        f"{BASE_URL}/api-v2/tasks/{new_task_id}",
        headers=HEADERS,
        json=update_data
    )
    assert response.status_code == 200, f"Ошибка обновления задачи: {response.text}"

# ---- Проекты ----
def test_project_operations():
    # Создать проект
    project_data = {"title": "Интернет-магазин"}
    response = requests.post(
        f"{BASE_URL}/api-v2/projects",
        headers=HEADERS,
        json=project_data
    )
    assert response.status_code == 201, f"Ошибка создания проекта: {response.text}"
    project_id = response.json()["id"]

    # Получить проект
    response = requests.get(
        f"{BASE_URL}/api-v2/projects/{project_id}",
        headers=HEADERS
    )
    assert response.status_code == 200, f"Ошибка получения проекта: {response.text}"