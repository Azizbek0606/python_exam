from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from .models import Ingredient, Meal, Recipe, Serving, UserRole
from rest_framework.authtoken.models import Token


class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Foydalanuvchilar yaratish
        self.admin_user = User.objects.create_user(username="admin", password="adminpass")
        UserRole.objects.create(user=self.admin_user, role="admin")
        self.manager_user = User.objects.create_user(username="manager", password="managerpass")
        UserRole.objects.create(user=self.manager_user, role="manager")
        self.regular_user = User.objects.create_user(username="user", password="userpass")
        UserRole.objects.create(user=self.regular_user, role="user")

        # Tokenlar yaratish
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.manager_token = Token.objects.create(user=self.manager_user)
        self.user_token = Token.objects.create(user=self.regular_user)

        # Test ma'lumotlari
        self.ingredient = Ingredient.objects.create(
            name="Tomato",
            quantity=1000,
            min_quantity=200,
            delivery_date=date.today()  # delivery_date qo'shildi
        )
        self.meal = Meal.objects.create(name="Salad", type="lunch")
        self.recipe = Recipe.objects.create(
            meal=self.meal, ingredient=self.ingredient, quantity=100
        )
        self.serving = Serving.objects.create(
            meal=self.meal, user=self.regular_user, portion_count=1
        )


class IngredientViewSetTests(BaseTestCase):
    def test_list_ingredients_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_token.key}")
        response = self.client.get(reverse("ingredient-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Tomato")

    def test_create_ingredient_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.manager_token.key}")
        data = {
            "name": "Onion",
            "quantity": 500,
            "min_quantity": 100,
            "delivery_date": date.today().isoformat()
        }
        response = self.client.post(reverse("ingredient-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ingredient.objects.count(), 2)

    def test_create_ingredient_regular_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_token.key}")
        data = {
            "name": "Onion",
            "quantity": 500,
            "min_quantity": 100,
            "delivery_date": date.today().isoformat()
        }
        response = self.client.post(reverse("ingredient-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MealViewSetTests(BaseTestCase):
    def test_list_meals(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_token.key}")
        response = self.client.get(reverse("meal-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Salad")


class ServingViewSetTests(BaseTestCase):
    def test_serve_meal_sufficient_ingredients(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        data = {"meal_id": self.meal.id, "portion_count": 2}
        response = self.client.post(reverse("serving-serve-meal"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.ingredient.refresh_from_db()
        self.assertEqual(self.ingredient.quantity, 800)  # 1000 - (100 * 2)

    def test_serve_meal_insufficient_ingredients(self):
        self.ingredient.quantity = 50
        self.ingredient.save()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        data = {"meal_id": self.meal.id, "portion_count": 1}
        response = self.client.post(reverse("serving-serve-meal"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("yetarli emas", response.data["error"])


class LoginViewTests(BaseTestCase):
    def test_login_valid_credentials(self):
        data = {"username": "user", "password": "userpass"}
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "user")

    def test_login_invalid_credentials(self):
        data = {"username": "user", "password": "wrongpass"}
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegisterViewTests(BaseTestCase):
    def test_register_new_user(self):
        data = {"username": "newuser", "password": "newpass", "confirm_password": "newpass"}
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "newuser")

    def test_register_existing_user(self):
        data = {"username": "user", "password": "userpass", "confirm_password": "userpass"}
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTests(BaseTestCase):
    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_token.key}")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.regular_user).exists())