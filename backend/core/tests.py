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

    def test_calculate_success_rate(self):
        # Test success rate calculation
        rate = self.goal.calculate_success_rate()
        self.assertIsInstance(rate, float)
        self.assertGreaterEqual(rate, 0.0)
        self.assertLessEqual(rate, 1.0)

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
        self.assertEqual(self.habit.difficulty_level, 3)  # Default value

    def test_habit_str(self):
        self.assertEqual(str(self.habit), f"{self.goal.title} - Daily Exercise")

    def test_habit_update_streak(self):
        # Test streak update method
        self.habit.update_streak()
        self.assertEqual(self.habit.current_streak, 0)  # No check-ins yet
        self.assertEqual(self.habit.longest_streak, 0)

# Update core/tests.py - fix the GoalAPITest

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
        self.assertEqual(Goal.objects.filter(title='Read Daily').first().user, self.user)

    def test_list_user_goals(self):
        Goal.objects.create(user=self.user, title='Goal 1', category='fitness')
        Goal.objects.create(user=self.user, title='Goal 2', category='learning')
        # Create a goal for another user to ensure isolation
        other_user = User.objects.create_user(email='other@example.com', username='otheruser', password='testpass123')
        Goal.objects.create(user=other_user, title='Other Goal', category='fitness')
        
        response = self.client.get(self.goals_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle pagination in response
        if 'results' in response.data:  # If pagination is enabled
            self.assertEqual(len(response.data['results']), 2)
            # Check that we only get user's goals
            user_goals = [goal['title'] for goal in response.data['results']]
            self.assertIn('Goal 1', user_goals)
            self.assertIn('Goal 2', user_goals)
            self.assertNotIn('Other Goal', user_goals)
        else:
            # No pagination
            self.assertEqual(len(response.data), 2)

    def test_goal_detail_view(self):
        goal = Goal.objects.create(user=self.user, title='Test Goal', category='fitness')
        url = reverse('goal-detail', kwargs={'pk': goal.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Goal')
        self.assertEqual(response.data['category'], 'fitness')

    def test_goal_update(self):
        goal = Goal.objects.create(user=self.user, title='Old Title', category='fitness')
        url = reverse('goal-detail', kwargs={'pk': goal.pk})
        update_data = {'title': 'Updated Title', 'description': 'Updated description'}
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        goal.refresh_from_db()
        self.assertEqual(goal.title, 'Updated Title')

    def test_goal_delete(self):
        goal = Goal.objects.create(user=self.user, title='To Delete', category='fitness')
        url = reverse('goal-detail', kwargs={'pk': goal.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Goal.objects.filter(pk=goal.pk).exists())

# In core/tests.py - fix HabitAPITest

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
        
        habit = Habit.objects.get(title='Morning Run')
        self.assertEqual(habit.goal, self.goal)
        self.assertEqual(habit.validation_method, 'photo')

    def test_create_habit_invalid_goal(self):
        # Try to create habit for goal that doesn't belong to user
        other_user = User.objects.create_user(email='other@example.com', username='otheruser', password='testpass123')
        other_goal = Goal.objects.create(user=other_user, title='Other Goal', category='fitness')
        
        habit_data = {
            'goal': other_goal.id,
            'title': 'Morning Run',
            'validation_method': 'photo',
            'validation_prompt': 'Check if running',
            'target_duration': 30
        }
        response = self.client.post(self.habits_url, habit_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_user_habits(self):
        Habit.objects.create(goal=self.goal, title='Habit 1', validation_method='photo', validation_prompt='test')
        Habit.objects.create(goal=self.goal, title='Habit 2', validation_method='text', validation_prompt='test')
        
        # Create habit for another user's goal
        other_user = User.objects.create_user(email='other@example.com', username='otheruser', password='testpass123')
        other_goal = Goal.objects.create(user=other_user, title='Other Goal', category='fitness')
        Habit.objects.create(goal=other_goal, title='Other Habit', validation_method='photo', validation_prompt='test')
        
        response = self.client.get(self.habits_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle pagination
        if 'results' in response.data:  # If pagination is enabled
            self.assertEqual(len(response.data['results']), 2)
            # Check that we only get user's habits
            user_habits = [habit['title'] for habit in response.data['results']]
            self.assertIn('Habit 1', user_habits)
            self.assertIn('Habit 2', user_habits)
            self.assertNotIn('Other Habit', user_habits)
        else:
            # No pagination
            self.assertEqual(len(response.data), 2)

    def test_habit_detail_view(self):
        habit = Habit.objects.create(
            goal=self.goal,
            title='Test Habit',
            validation_method='photo',
            validation_prompt='test'
        )
        url = reverse('habit-detail', kwargs={'pk': habit.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Habit')
        self.assertEqual(response.data['goal'], self.goal.id)

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
        self.assertEqual(checkin.self_report_description, 'Completed 30 min workout')

    def test_checkin_str(self):
        checkin = DailyCheckIn.objects.create(habit=self.habit, date=date.today())
        expected_str = f"{self.habit.title} - {date.today()}"
        self.assertEqual(str(checkin), expected_str)

    def test_checkin_save_auto_completed_at(self):
        checkin = DailyCheckIn.objects.create(
            habit=self.habit,
            date=date.today(),
            is_approved=True
        )
        self.assertIsNotNone(checkin.completed_at)

    def test_checkin_unique_together(self):
        # Should not be able to create two check-ins for same habit on same date
        DailyCheckIn.objects.create(habit=self.habit, date=date.today())
        with self.assertRaises(Exception):
            DailyCheckIn.objects.create(habit=self.habit, date=date.today())

# In core/tests.py - fix CheckInAPITest

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
            'self_report_description': 'Completed workout',
            'date': date.today().isoformat()  # Explicitly pass date as string
        }
        response = self.client.post(self.checkins_url, checkin_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(DailyCheckIn.objects.filter(habit=self.habit).exists())
        
        checkin = DailyCheckIn.objects.get(habit=self.habit)
        self.assertEqual(checkin.self_report_description, 'Completed workout')
        self.assertTrue(checkin.is_self_report)

    def test_create_checkin_with_photo_validation(self):
        photo_habit = Habit.objects.create(
            goal=self.goal,
            title='Photo Habit',
            validation_method='photo',
            validation_prompt='Show workout'
        )
        
        checkin_data = {
            'habit': photo_habit.id,
            'date': date.today().isoformat(),
            'text_proof': 'Workout description'
        }
        
        # Should fail because photo validation requires photo_proof
        response = self.client.post(self.checkins_url, checkin_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_today_checkins_view(self):
        # Create a check-in for today
        DailyCheckIn.objects.create(
            habit=self.habit,
            date=date.today(),
            is_self_report=True,
            self_report_description='Test'
        )
        
        url = reverse('today-checkins')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('date', response.data)
        self.assertIn('habits', response.data)
        self.assertIn('completed_checkins', response.data)
        
        # Should have one completed check-in
        self.assertEqual(len(response.data['completed_checkins']), 1)

    def test_checkin_detail_view(self):
        checkin = DailyCheckIn.objects.create(
            habit=self.habit,
            date=date.today(),
            is_self_report=True,
            self_report_description='Test'
        )
        url = reverse('checkin-detail', kwargs={'pk': checkin.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], checkin.id)

class StreakTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Fitness Goal', category='fitness')
        self.habit = Habit.objects.create(goal=self.goal, title='Exercise', validation_method='self_report', validation_prompt='test')
        self.streak = Streak.objects.create(user=self.user, habit=self.habit, current_streak=5, longest_streak=10)

    def test_streak_creation(self):
        self.assertEqual(self.streak.current_streak, 5)
        self.assertEqual(self.streak.longest_streak, 10)
        self.assertEqual(self.streak.user, self.user)
        self.assertEqual(self.streak.habit, self.habit)

    def test_streak_str(self):
        expected_str = f"{self.user.email} - {self.habit.title} (5 days)"
        self.assertEqual(str(self.streak), expected_str)

    def test_streak_unique_together(self):
        # Should not be able to create two streaks for same user and habit
        with self.assertRaises(Exception):
            Streak.objects.create(user=self.user, habit=self.habit)

# In core/tests.py - fix StreakAPITest

class StreakAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Fitness Goal', category='fitness')
        self.habit = Habit.objects.create(goal=self.goal, title='Exercise', validation_method='self_report', validation_prompt='test')
        self.streak = Streak.objects.create(user=self.user, habit=self.habit, current_streak=5)
        self.client.force_authenticate(user=self.user)
        self.streaks_url = reverse('streak-list')

    def test_list_streaks(self):
        response = self.client.get(self.streaks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle pagination
        if 'results' in response.data:  # If pagination is enabled
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['current_streak'], 5)
        else:
            # No pagination
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['current_streak'], 5)

class ProgressInsightTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Fitness Goal', category='fitness')
        self.habit = Habit.objects.create(goal=self.goal, title='Exercise', validation_method='self_report', validation_prompt='test')

    def test_insight_creation(self):
        insight = ProgressInsight.objects.create(
            user=self.user,
            habit=self.habit,
            insight_type='success_pattern',
            title='Great progress!',
            description='You\'ve been consistent with morning workouts',
            data={'pattern': 'morning', 'confidence': 0.85}
        )
        self.assertEqual(insight.title, 'Great progress!')
        self.assertEqual(insight.user, self.user)
        self.assertEqual(insight.insight_type, 'success_pattern')
        self.assertFalse(insight.is_read)

    def test_insight_str(self):
        insight = ProgressInsight.objects.create(
            user=self.user,
            insight_type='success_pattern',
            title='Test Insight',
            description='Test'
        )
        expected_str = f"{self.user.email} - success_pattern"
        self.assertEqual(str(insight), expected_str)

class MilestoneTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Fitness Goal', category='fitness')
        self.habit = Habit.objects.create(goal=self.goal, title='Exercise', validation_method='self_report', validation_prompt='test')

    def test_milestone_creation(self):
        milestone = Milestone.objects.create(
            user=self.user,
            habit=self.habit,
            milestone_type='streak',
            title='7 Day Streak',
            description='Completed 7 consecutive days',
            target_value=7,
            current_value=5,
            is_achieved=False
        )
        self.assertEqual(milestone.title, '7 Day Streak')
        self.assertEqual(milestone.user, self.user)
        self.assertEqual(milestone.milestone_type, 'streak')
        self.assertFalse(milestone.is_achieved)

    def test_milestone_str(self):
        milestone = Milestone.objects.create(
            user=self.user,
            milestone_type='streak',
            title='Test Milestone',
            description='Test',
            target_value=10,
            current_value=5
        )
        expected_str = f"{self.user.email} - Test Milestone"
        self.assertEqual(str(milestone), expected_str)

class DashboardAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.dashboard_url = reverse('dashboard')

    def test_dashboard_view(self):
        # Create test data
        goal = Goal.objects.create(user=self.user, title='Test Goal', category='fitness')
        habit = Habit.objects.create(goal=goal, title='Test Habit', validation_method='self_report', validation_prompt='test')
        streak = Streak.objects.create(user=self.user, habit=habit, current_streak=3)
        
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('stats', response.data)
        self.assertIn('current_streaks', response.data)
        self.assertIn('recent_insights', response.data)
        self.assertIn('upcoming_milestones', response.data)
        
        # Check stats
        stats = response.data['stats']
        self.assertEqual(stats['total_goals'], 1)
        self.assertEqual(stats['active_goals'], 1)
        self.assertEqual(stats['total_habits'], 1)

class UserStatsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.stats_url = reverse('user-stats')

    def test_user_stats_view(self):
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_goals', response.data)
        self.assertIn('completed_goals', response.data)
        self.assertIn('total_habits', response.data)
        self.assertIn('active_habits', response.data)
        self.assertIn('overall_success_rate', response.data)
        self.assertIn('current_streak', response.data)

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
        self.assertIn('total_completions', response.data)
        
        # Calendar should be a list of weeks
        calendar_data = response.data['calendar']
        self.assertIsInstance(calendar_data, list)
        self.assertGreater(len(calendar_data), 0)

# In core/tests.py - fix BulkCheckInTest

# In core/tests.py - update BulkCheckInTest

class BulkCheckInTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Fitness Goal', category='fitness')
        self.habit1 = Habit.objects.create(
            goal=self.goal,
            title='Exercise',
            validation_method='self_report',
            validation_prompt='Did you exercise?'
        )
        self.habit2 = Habit.objects.create(
            goal=self.goal,
            title='Meditation',
            validation_method='text',  # Changed to 'text' from 'self_report'
            validation_prompt='Describe your meditation'
        )
        self.client.force_authenticate(user=self.user)
        self.bulk_url = reverse('bulk-checkin')

    def test_bulk_checkin(self):
        bulk_data = [
            {
                'habit_id': self.habit1.id,
                'proof_data': {
                    'description': 'Completed 30 min workout'
                }
            },
            {
                'habit_id': self.habit2.id,
                'proof_data': {
                    'text': 'Meditated for 15 minutes, focused on breath'
                }
            }
        ]
        
        response = self.client.post(self.bulk_url, bulk_data, format='json')
        
        # Check response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if check-ins were created
        checkins = DailyCheckIn.objects.filter(habit__in=[self.habit1, self.habit2])
        self.assertEqual(checkins.count(), 2, 
                        f"Expected 2 check-ins, but got {checkins.count()}. Check-in IDs: {list(checkins.values_list('id', flat=True))}")
        
        # Verify the check-in data
        for checkin in checkins:
            if checkin.habit == self.habit1:
                self.assertTrue(checkin.is_self_report)
                self.assertEqual(checkin.self_report_description, 'Completed 30 min workout')
            elif checkin.habit == self.habit2:
                self.assertEqual(checkin.text_proof, 'Meditated for 15 minutes, focused on breath')

class AuthenticationTest(APITestCase):
    def test_unauthenticated_access(self):
        # Test that unauthenticated users cannot access protected endpoints
        goals_url = reverse('goal-list')
        response = self.client.get(goals_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        habits_url = reverse('habit-list')
        response = self.client.get(habits_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Test Goal', category='fitness')

    def test_habit_validation_method_choices(self):
        # Test valid validation methods
        valid_methods = ['photo', 'audio', 'text', 'screen_recording', 'self_report']
        for method in valid_methods:
            habit = Habit.objects.create(
                goal=self.goal,
                title=f'{method} Habit',
                validation_method=method,
                validation_prompt='test'
            )
            self.assertEqual(habit.validation_method, method)

    def test_goal_category_choices(self):
        # Test valid categories
        valid_categories = ['fitness', 'learning', 'productivity', 'health', 'creative', 'mindfulness', 'other']
        for category in valid_categories:
            goal = Goal.objects.create(
                user=self.user,
                title=f'{category} Goal',
                category=category
            )
            self.assertEqual(goal.category, category)