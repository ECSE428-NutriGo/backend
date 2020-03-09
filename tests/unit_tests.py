from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from nutrition import controller
from nutrition.models import FoodItem, Meal

class EditFoodItem(APITestCase):
    def setUp(self):
        self.fooditem = FoodItem.objects.create()
        self.user = User.objects.create_user(username="test@user.com", email="test@user.com")
        self.id = self.fooditem.id
        self.protein = 1
        self.fat = 1
        self.carb = 1
        self.name = 'name'

    def tearDown(self):
        FoodItem.objects.all().delete()

    def test_edit_fooditem(self):
        # Assert Defaults
        self.assertEqual(self.fooditem.name, '')
        self.assertEqual(self.fooditem.carb, 0)
        self.assertEqual(self.fooditem.protein, 0)
        self.assertEqual(self.fooditem.fat, 0)
        self.assertEqual(self.fooditem.user, None)

        # Edit FoodItem
        self.fooditem.protein = self.protein
        self.fooditem.fat = self.fat
        self.fooditem.carb = self.carb
        self.fooditem.name = self.name
        self.fooditem.user = self.user
        self.fooditem.save()

        # Assert edit successful
        self.assertEqual(self.fooditem.name, self.name)
        self.assertEqual(self.fooditem.carb, self.carb)
        self.assertEqual(self.fooditem.protein, self.protein)
        self.assertEqual(self.fooditem.fat, self.fat)
        self.assertEqual(self.fooditem.user, self.user)
        
        # Assert user has fooditem
        self.assertEqual(self.user.fooditems.all()[0], self.fooditem)

class EditUserAttributes(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test@user.com", email="test@user.com")
        self.protein_target = 1
        self.fat_target = 2
        self.carb_target = 3
        self.hours_activity = 20
        self.age = 20

    def tearDown(self):
        FoodItem.objects.all().delete()
        User.objects.all().delete()

    def test_edit_fooditem(self):
        # Assert Defaults
        self.assertEqual(self.user.profile.protein_target, 0)
        self.assertEqual(self.user.profile.carb_target, 0)
        self.assertEqual(self.user.profile.fat_target, 0)
        self.assertEqual(self.user.profile.age, 0)
        self.assertEqual(self.user.profile.hours_activity, 0)
        self.assertEqual(self.user.profile.user, self.user)

        # Edit FoodItem
        self.user.profile.protein_target = self.protein_target
        self.user.profile.carb_target = self.carb_target
        self.user.profile.fat_target = self.fat_target
        self.user.profile.age = self.age
        self.user.profile.hours_activity = self.hours_activity
        self.user.profile.save()

        # Assert edit successful
        self.assertEqual(self.user.profile.protein_target, self.protein_target)
        self.assertEqual(self.user.profile.carb_target, self.carb_target)
        self.assertEqual(self.user.profile.fat_target, self.fat_target)
        self.assertEqual(self.user.profile.age, self.age)
        self.assertEqual(self.user.profile.hours_activity, self.hours_activity)
        
class EditCurrentWeight(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test@user.com", email="test@user.com")
        self.current_weight = 100

    def tearDown(self):
        User.objects.all().delete()

    def test_edit_fooditem(self):
        # Assert Defaults
        self.assertEqual(self.user.profile.current_weight, 0)

        # Edit FoodItem
        self.user.profile.current_weight = self.current_weight
        self.user.profile.save()

        # Assert edit successful
        self.assertEqual(self.user.profile.current_weight, self.current_weight)

class EditTargetWeight(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test@user.com", email="test@user.com")
        self.target_weight = 110

    def tearDown(self):
        User.objects.all().delete()

    def test_edit_fooditem(self):
        # Assert Defaults
        self.assertEqual(self.user.profile.target_weight, 0)

        # Edit FoodItem
        self.user.profile.target_weight = self.target_weight
        self.user.profile.save()

        # Assert edit successful
        self.assertEqual(self.user.profile.target_weight, self.target_weight)

class QueryFoodItemList(APITestCase):
    def setUp(self):
        self.fi1 = FoodItem.objects.create(name='one', fat=1, carb=2, protein=3)
        self.fi2 = FoodItem.objects.create(name='two', fat=4, carb=5, protein=6)
        self.fi3 = FoodItem.objects.create(name='three', fat=7, carb=8, protein=9)

    def tearDown(self):
        FoodItem.objects.all().delete()

    def test_edit_fooditem(self):
        # query list
        fooditem_query = FoodItem.objects.all()

        # Assert edit successful
        self.assertEqual(len(fooditem_query), 3)
        self.assertEqual(fooditem_query[0], self.fi1)
        self.assertEqual(fooditem_query[1], self.fi2)
        self.assertEqual(fooditem_query[2], self.fi3)

class RemoveFoodItemMeal(APITestCase):
    def setUp(self):
        self.fi1 = FoodItem.objects.create(name='one', fat=1, carb=2, protein=3)
        self.fi2 = FoodItem.objects.create(name='two', fat=4, carb=5, protein=6)
        self.fi3 = FoodItem.objects.create(name='three', fat=7, carb=8, protein=9)
        self.meal = Meal.objects.create(name='name')
        self.meal.fooditems.add(self.fi1)
        self.meal.fooditems.add(self.fi2)
        self.meal.fooditems.add(self.fi3)

    def tearDown(self):
        FoodItem.objects.all().delete()
        Meal.objects.all().delete()

    def test_edit_fooditem(self):
        # get fooditems
        fooditems = self.meal.fooditems.all()

        # Assert edit successful
        self.assertEqual(len(fooditems), 3)
        self.assertEqual(fooditems[0], self.fi1)
        self.assertEqual(fooditems[1], self.fi2)
        self.assertEqual(fooditems[2], self.fi3)

        # remove fooditem
        self.meal.fooditems.remove(self.fi2)

        # get fooditems
        fooditems = self.meal.fooditems.all()

        # Assert edit successful
        self.assertEqual(len(fooditems), 2)
        self.assertEqual(fooditems[0], self.fi1)
        self.assertEqual(fooditems[1], self.fi3)

class LockOutUser(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test@user.com", email="test@user.com")
        self.id = self.user.id

    def tearDown(self):
        User.objects.all().delete()

    def test_edit_fooditem(self):
        # Test lock
        self.user.is_active = False
        self.user.save()

        self.assertFalse(User.objects.get(pk=self.id).is_active)

        # Test unlock
        self.user.is_active = True
        self.user.save()

        self.assertTrue(User.objects.get(pk=self.id).is_active)

class QueryUser(APITestCase):
    def setUp(self):
        User.objects.create_user(username="test0@user.com", email="test0@user.com")
        User.objects.create_user(username="test1@user.com", email="test1@user.com")
        User.objects.create_user(username="test2@user.com", email="test2@user.com")
        User.objects.create_user(username="test3@user.com", email="test3@user.com")

    def tearDown(self):
        User.objects.all().delete()

    def test_edit_fooditem(self):
        user = User.objects.get(email="test2@user.com")

        self.assertEqual(user.email, "test2@user.com")
        self.assertEqual(user.username, "test2@user.com")

class QueryUser(APITestCase):
    def setUp(self):
        User.objects.create_user(username="test0@user.com", email="test0@user.com")
        User.objects.create_user(username="test1@user.com", email="test1@user.com")
        User.objects.create_user(username="test2@user.com", email="test2@user.com")
        User.objects.create_user(username="test3@user.com", email="test3@user.com")

    def tearDown(self):
        User.objects.all().delete()

    def test_edit_fooditem(self):
        user = User.objects.get(email="test2@user.com")

        self.assertEqual(user.email, "test2@user.com")
        self.assertEqual(user.username, "test2@user.com")
        self.assertEqual(user.profile.age, 0)

class QueryUserList(APITestCase):
    def setUp(self):
        User.objects.create_user(username="test0@user.com", email="test0@user.com")
        User.objects.create_user(username="test1@user.com", email="test1@user.com")
        User.objects.create_user(username="test2@user.com", email="test2@user.com")
        User.objects.create_user(username="test3@user.com", email="test3@user.com")

    def tearDown(self):
        User.objects.all().delete()

    def test_edit_fooditem(self):
        users = User.objects.all()

        self.assertEqual(len(users), 4)
        self.assertEqual(users[0].email, "test0@user.com")
        self.assertEqual(users[1].email, "test1@user.com")
        self.assertEqual(users[2].email, "test2@user.com")
        self.assertEqual(users[3].email, "test3@user.com")