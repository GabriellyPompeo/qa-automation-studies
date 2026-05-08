"""
QA Automation Study - API Response Testing with Pytest
Author: Gabrielly Pompeo da Costa
Date: 2026-05-08

Demonstrates API testing patterns using Python requests + pytest.
Tests a public REST API (JSONPlaceholder) to validate response structure,
status codes, data types, and edge cases.
"""

import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


class TestPostsAPI:
    """Test suite for the /posts endpoint."""

    def test_get_all_posts_status_code(self):
        """Verify GET /posts returns HTTP 200."""
        response = requests.get(f"{BASE_URL}/posts")
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )

    def test_get_all_posts_returns_list(self):
        """Verify GET /posts returns a list."""
        response = requests.get(f"{BASE_URL}/posts")
        data = response.json()
        assert isinstance(data, list), "Response should be a list"

    def test_get_all_posts_count(self):
        """Verify GET /posts returns 100 posts."""
        response = requests.get(f"{BASE_URL}/posts")
        data = response.json()
        assert len(data) == 100, f"Expected 100 posts, got {len(data)}"

    def test_post_has_required_fields(self):
        """Verify each post has required fields: userId, id, title, body."""
        response = requests.get(f"{BASE_URL}/posts")
        data = response.json()
        required_fields = {"userId", "id", "title", "body"}
        for post in data:
            assert required_fields.issubset(post.keys()), (
                f"Post missing required fields: {required_fields - post.keys()}"
            )

    def test_post_field_types(self):
        """Verify field data types are correct."""
        response = requests.get(f"{BASE_URL}/posts/1")
        post = response.json()
        assert isinstance(post["userId"], int), "userId must be an integer"
        assert isinstance(post["id"], int), "id must be an integer"
        assert isinstance(post["title"], str), "title must be a string"
        assert isinstance(post["body"], str), "body must be a string"

    def test_get_single_post(self):
        """Verify GET /posts/1 returns the correct post."""
        response = requests.get(f"{BASE_URL}/posts/1")
        assert response.status_code == 200
        post = response.json()
        assert post["id"] == 1

    def test_get_nonexistent_post_returns_404(self):
        """Verify GET /posts/9999 returns HTTP 404."""
        response = requests.get(f"{BASE_URL}/posts/9999")
        assert response.status_code == 404, (
            f"Expected 404 for nonexistent post, got {response.status_code}"
        )

    def test_response_content_type_is_json(self):
        """Verify Content-Type header is application/json."""
        response = requests.get(f"{BASE_URL}/posts/1")
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, (
            f"Expected JSON content type, got: {content_type}"
        )

    def test_response_time_is_acceptable(self):
        """Verify API response time is under 3 seconds."""
        response = requests.get(f"{BASE_URL}/posts")
        elapsed = response.elapsed.total_seconds()
        assert elapsed < 3.0, f"Response too slow: {elapsed:.2f}s (limit: 3s)"

    @pytest.mark.parametrize("post_id", [1, 5, 10, 50, 100])
    def test_valid_post_ids(self, post_id):
        """Parametrized test: verify multiple valid post IDs return 200."""
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        assert response.status_code == 200, (
            f"Post ID {post_id} should exist but returned {response.status_code}"
        )


class TestPostsAPIEdgeCases:
    """Edge case tests for the /posts endpoint."""

    def test_post_title_is_not_empty(self):
        """Verify no post has an empty title."""
        response = requests.get(f"{BASE_URL}/posts")
        data = response.json()
        for post in data:
            assert post["title"].strip() != "", (
                f"Post ID {post['id']} has empty title"
            )

    def test_post_body_is_not_empty(self):
        """Verify no post has an empty body."""
        response = requests.get(f"{BASE_URL}/posts")
        data = response.json()
        for post in data:
            assert post["body"].strip() != "", (
                f"Post ID {post['id']} has empty body"
            )

    def test_post_ids_are_unique(self):
        """Verify all post IDs are unique (no duplicates)."""
        response = requests.get(f"{BASE_URL}/posts")
        data = response.json()
        ids = [post["id"] for post in data]
        assert len(ids) == len(set(ids)), "Duplicate post IDs found!"
