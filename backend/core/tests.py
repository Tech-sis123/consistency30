from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta
from .models import Goal, Habit, DailyCheckIn, Streak, ProgressInsight, Milestone, UserStats

User = get_user_model()

class GoalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(
            user=self.user,
            title='Learn Python',
            description='Master Python programming',
            category='learning',
            project_type='30_day_challenge'
        )

    def test_goal_creation(self):
        self.assertEqual(self.goal.title, 'Learn Python')
        self.assertEqual(self.goal.user, self.user)
        self.assertTrue(self.goal.is_active)
        self.assertFalse(self.goal.is_completed)

    def test_goal_str(self):
        self.assertEqual(str(self.goal), f"{self.user.email} - Learn Python")

    def test_target_end_date_auto_set(self):
        self.assertIsNotNone(self.goal.target_end_date)
        expected_date = self.goal.start_date + timedelta(days=30)
        self.assertEqual(self.goal.target_end_date, expected_date)

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Fitness Goal', category='fitness')
        self.habit = Habit.objects.create(
            goal=self.goal,
            title='Daily Exercise',
            validation_method='photo',
            validation_prompt='Check if person is exercising',
            target_duration=30
        )

    def test_habit_creation(self):
        self.assertEqual(self.habit.title, 'Daily Exercise')
        self.assertEqual(self.habit.goal, self.goal)
        self.assertEqual(self.habit.validation_method, 'photo')
        self.assertTrue(self.habit.is_active)

    def test_habit_str(self):
        self.assertEqual(str(self.habit), f"{self.goal.title} - Daily Exercise")

class GoalAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.goals_url = reverse('goal-list')

    def test_create_goal(self):
        goal_data = {
            'title': 'Read Daily',
            'description': 'Read for 30 minutes daily',
            'category': 'learning',
            'project_type': '30_day_challenge'
        }
        response = self.client.post(self.goals_url, goal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Goal.objects.filter(title='Read Daily').exists())

    def test_list_user_goals(self):
        Goal.objects.create(user=self.user, title='Goal 1', category='fitness')
        Goal.objects.create(user=self.user, title='Goal 2', category='learning')
        response = self.client.get(self.goals_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_goal_detail_view(self):
        goal = Goal.objects.create(user=self.user, title='Test Goal', category='fitness')
        url = reverse('goal-detail', kwargs={'pk': goal.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Goal')

class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Fitness Goal', category='fitness')
        self.client.force_authenticate(user=self.user)
        self.habits_url = reverse('habit-list')

    def test_create_habit(self):
        habit_data = {
            'goal': self.goal.id,
            'title': 'Morning Run',
            'validation_method': 'photo',
            'validation_prompt': 'Check if running',
            'target_duration': 30
        }
        response = self.client.post(self.habits_url, habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.filter(title='Morning Run').exists())

    def test_list_user_habits(self):
        Habit.objects.create(goal=self.goal, title='Habit 1', validation_method='photo', validation_prompt='test')
        Habit.objects.create(goal=self.goal, title='Habit 2', validation_method='text', validation_prompt='test')
        response = self.client.get(self.habits_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class DailyCheckInTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Fitness Goal', category='fitness')
        self.habit = Habit.objects.create(
            goal=self.goal,
            title='Exercise',
            validation_method='self_report',
            validation_prompt='Did you exercise?'
        )

    def test_checkin_creation(self):
        checkin = DailyCheckIn.objects.create(
            habit=self.habit,
            date=timezone.now().date(),
            is_self_report=True,
            self_report_description='Completed 30 min workout'
        )
        self.assertEqual(checkin.habit, self.habit)
        self.assertTrue(checkin.is_self_report)

    def test_checkin_str(self):
        checkin = DailyCheckIn.objects.create(habit=self.habit, date=date.today())
        expected_str = f"{self.habit.title} - {date.today()}"
        self.assertEqual(str(checkin), expected_str)

class CheckInAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Fitness Goal', category='fitness')
        self.habit = Habit.objects.create(
            goal=self.goal,
            title='Exercise',
            validation_method='self_report',
            validation_prompt='Did you exercise?'
        )
        self.client.force_authenticate(user=self.user)
        self.checkins_url = reverse('checkin-list')

    def test_create_checkin(self):
        checkin_data = {
            'habit': self.habit.id,
            'is_self_report': True,
            'self_report_description': 'Completed workout'
        }
        response = self.client.post(self.checkins_url, checkin_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(DailyCheckIn.objects.filter(habit=self.habit).exists())

    def test_today_checkins_view(self):
        url = reverse('today-checkins')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('date', response.data)
        self.assertIn('habits', response.data)

class StreakTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Fitness Goal', category='fitness')
        self.habit = Habit.objects.create(goal=self.goal, title='Exercise', validation_method='self_report', validation_prompt='test')
        self.streak = Streak.objects.create(user=self.user, habit=self.habit, current_streak=5)

    def test_streak_creation(self):
        self.assertEqual(self.streak.current_streak, 5)
        self.assertEqual(self.streak.user, self.user)
        self.assertEqual(self.streak.habit, self.habit)

    def test_streak_str(self):
        expected_str = f"{self.user.email} - {self.habit.title} (5 days)"
        self.assertEqual(str(self.streak), expected_str)

class DashboardAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.dashboard_url = reverse('dashboard')

    def test_dashboard_view(self):
        # Create some test data
        goal = Goal.objects.create(user=self.user, title='Test Goal', category='fitness')
        habit = Habit.objects.create(goal=goal, title='Test Habit', validation_method='self_report', validation_prompt='test')
        
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('stats', response.data)
        self.assertIn('current_streaks', response.data)

class UserStatsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.stats_url = reverse('user-stats')

    def test_user_stats_view(self):
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_goals', response.data)

class CalendarAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_calendar_view(self):
        current_date = timezone.now()
        url = reverse('calendar', kwargs={'year': current_date.year, 'month': current_date.month})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('calendar', response.data)
        self.assertIn('year', response.data)
        self.assertIn('month', response.data)