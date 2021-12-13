from typing import List
import pytest

from app import schemas
from .conftest import client, test_posts, authorized_client

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts")
    posts = [schemas.PostOut(**post) for post in response.json()]
    
    assert len(posts) == len(test_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts")

    assert response.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/8888")

    assert response.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = schemas.PostOut(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize(
    "title, content, published", [
    ("New Title", "New Content", True),
    ("Good stuff", "Boring Blog", False),
    ("Maths Title", "What a interesting post", True),
    ]
)
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts/", json={"title":title, "content":content, "published":published})

    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    response = authorized_client.post("/posts/", json={"title":"title", "content":"content"})

    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_create_post(client, test_posts):
    response = client.post("/posts/", json={"title":"title", "content":"content"})

    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 204



def test_delete_not_existing_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/99999")

    assert response.status_code == 404


def test_delete_other_users_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert response.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
            "title":"first title",
            "content":"first content",
            "owner_id": test_user["id"]
        }

    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    post = schemas.Post(**response.json())

    assert response.status_code == 200
    assert post.title == data['title']
    assert post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title":"first title",
        "content":"first content",
        "owner_id": test_user["id"]
    }

    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    
    assert response.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401


def test_update_not_existing_post(authorized_client, test_user, test_posts):
    data = {
        "title":"first title",
        "content":"first content",
        "owner_id": test_user["id"]
    }
    
    response = authorized_client.put(f"/posts/99999", json=data)

    assert response.status_code == 404