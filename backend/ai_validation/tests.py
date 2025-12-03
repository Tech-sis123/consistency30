import json
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.base import ContentFile
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock
from datetime import date, timedelta
from decimal import Decimal

from ai_validation.services import AIService

from .models import (
    AIConfig, ValidationRule, ValidationLog, AITrainingData,
    AIFeedback, ModelPerformance, ValidationCache
)
from core.models import Goal, Habit, DailyCheckIn

User = get_user_model()

class AIConfigModelTest(TestCase):
    def test_aiconfig_creation(self):
        config = AIConfig.objects.create(
            name='Test Config',
            api_key='AIzaSyCsijuQ-0sV6Xqj89MZniJPJ1iEk15gPbg',
            model_name='gemini-2.5-flash',
            max_tokens=1000,
            temperature=0.7,
            is_active=True
        )
        self.assertEqual(config.name, 'Test Config')
        self.assertEqual(config.model_name, 'gemini-2.5-flash')
        self.assertTrue(config.is_active)
        self.assertIsNotNone(config.created_at)

    def test_aiconfig_str(self):
        config = AIConfig.objects.create(
            name='Test Config',
            model_name='gemini-2.5-flash'
        )
        self.assertEqual(str(config), "Test Config (gemini-2.5-flash)")

    def test_aiconfig_unique_name(self):
        AIConfig.objects.create(name='Unique Config', model_name='gemini-2.5-flash')
        with self.assertRaises(Exception):
            AIConfig.objects.create(name='Unique Config', model_name='gemini-2.5-flash')

class ValidationRuleModelTest(TestCase):
    def test_validationrule_creation(self):
        rule = ValidationRule.objects.create(
            name='Photo Validation',
            validation_type='photo',
            prompt_template='Analyze this photo for {validation_prompt}',
            confidence_threshold=0.85,
            max_processing_time=15,
            is_active=True
        )
        self.assertEqual(rule.name, 'Photo Validation')
        self.assertEqual(rule.validation_type, 'photo')
        self.assertTrue(rule.is_active)

    def test_validationrule_str(self):
        rule = ValidationRule.objects.create(
            name='Text Check',
            validation_type='text',
            prompt_template='Check text for {validation_prompt}'
        )
        self.assertEqual(str(rule), "Text - Text Check")

    def test_validationrule_ordering(self):
        rule1 = ValidationRule.objects.create(name='A Rule', validation_type='photo', prompt_template='test')
        rule2 = ValidationRule.objects.create(name='B Rule', validation_type='audio', prompt_template='test')
        rules = list(ValidationRule.objects.all())
        self.assertEqual(rules[0], rule2)  # Should be ordered by validation_type, then name ('audio' before 'photo')
        self.assertEqual(rules[1], rule1)

class ValidationLogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Test Goal', category='fitness')
        self.habit = Habit.objects.create(goal=self.goal, title='Test Habit', validation_method='photo', validation_prompt='test')
        self.checkin = DailyCheckIn.objects.create(habit=self.habit, date=timezone.now().date())

    def test_validationlog_creation(self):
        rule = ValidationRule.objects.create(name='Test Rule', validation_type='photo', prompt_template='test')
        log = ValidationLog.objects.create(
            checkin=self.checkin,
            validation_rule=rule,
            input_data_preview='test data',
            ai_response_raw='{"result": "approved"}',
            ai_response_parsed={'result': 'approved'},
            confidence_score=0.9,
            is_approved=True,
            processing_time=2.5,
            success=True
        )
        self.assertEqual(log.checkin, self.checkin)
        self.assertEqual(log.confidence_score, 0.9)
        self.assertTrue(log.success)

    def test_validationlog_str(self):
        rule = ValidationRule.objects.create(name='Test Rule', validation_type='photo', prompt_template='test')
        log = ValidationLog.objects.create(
            checkin=self.checkin,
            validation_rule=rule,
            confidence_score=0.8,
            is_approved=True,
            success=True,
            processing_time=1.5
        )
        expected_str = f"Validation for {self.habit.title} - {log.created_at}"
        self.assertEqual(str(log), expected_str)

class AITrainingDataModelTest(TestCase):
    def test_aitrainingdata_creation(self):
        data = AITrainingData.objects.create(
            data_type='photo',
            input_data='Test input',
            expected_output={'result': 'approved'},
            actual_output={'result': 'approved'},
            is_correct=True,
            confidence_score=0.95,
            used_for_training=False
        )
        self.assertEqual(data.data_type, 'photo')
        self.assertTrue(data.is_correct)
        self.assertFalse(data.used_for_training)

    def test_aitrainingdata_str(self):
        data = AITrainingData.objects.create(
            data_type='text',
            input_data='Sample text',
            expected_output={'approved': True}
        )
        expected_str = f"text - {data.created_at.date()}"
        self.assertEqual(str(data), expected_str)

class AIFeedbackModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Test Goal', category='fitness')
        self.habit = Habit.objects.create(goal=self.goal, title='Test Habit', validation_method='photo', validation_prompt='test')
        self.checkin = DailyCheckIn.objects.create(habit=self.habit, date=timezone.now().date())

    def test_aifeedback_creation(self):
        feedback = AIFeedback.objects.create(
            user=self.user,
            checkin=self.checkin,
            feedback_type='false_positive',
            description='AI incorrectly approved this',
            expected_result='Should have been rejected',
            is_resolved=False
        )
        self.assertEqual(feedback.feedback_type, 'false_positive')
        self.assertFalse(feedback.is_resolved)

    def test_aifeedback_str(self):
        feedback = AIFeedback.objects.create(
            user=self.user,
            checkin=self.checkin,
            feedback_type='accuracy',
            description='Test feedback'
        )
        expected_str = f"{self.user.email} - accuracy - {feedback.created_at.date()}"
        self.assertEqual(str(feedback), expected_str)

class ModelPerformanceModelTest(TestCase):
    def setUp(self):
        self.rule = ValidationRule.objects.create(name='Test Rule', validation_type='photo', prompt_template='test')

    def test_modelperformance_creation(self):
        perf = ModelPerformance.objects.create(
            validation_rule=self.rule,
            date=timezone.now().date(),
            total_requests=100,
            successful_requests=95,
            failed_requests=5,
            average_confidence=0.85,
            average_processing_time=2.1,
            false_positives=2,
            false_negatives=1,
            user_accuracy_score=0.92
        )
        self.assertEqual(perf.total_requests, 100)
        self.assertEqual(perf.average_confidence, 0.85)

    def test_modelperformance_unique_constraint(self):
        date_val = timezone.now().date()
        ModelPerformance.objects.create(validation_rule=self.rule, date=date_val)
        with self.assertRaises(Exception):
            ModelPerformance.objects.create(validation_rule=self.rule, date=date_val)

    def test_modelperformance_str(self):
        perf = ModelPerformance.objects.create(
            validation_rule=self.rule,
            date=timezone.now().date(),
            total_requests=50
        )
        expected_str = f"{self.rule.name} - {perf.date}"
        self.assertEqual(str(perf), expected_str)

class ValidationCacheModelTest(TestCase):
    def setUp(self):
        self.rule = ValidationRule.objects.create(name='Test Rule', validation_type='photo', prompt_template='test')

    def test_validationcache_creation(self):
        cache = ValidationCache.objects.create(
            input_hash='abc123',
            validation_rule=self.rule,
            input_data_preview='test input',
            ai_response={'result': 'approved'},
            confidence_score=0.9,
            is_approved=True,
            usage_count=1
        )
        self.assertEqual(cache.input_hash, 'abc123')
        self.assertEqual(cache.usage_count, 1)

    def test_validationcache_str(self):
        cache = ValidationCache.objects.create(
            input_hash='def456',
            validation_rule=self.rule,
            input_data_preview='test',
            ai_response={},
            confidence_score=0.8,
            is_approved=True
        )
        expected_str = f"Cache: def456... (1 uses)"
        self.assertEqual(str(cache), expected_str)

class AIServiceTest(TestCase):
    def setUp(self):
        from .services import AIService
        self.service = AIService()

    @patch('ai_validation.services.genai.configure')
    def test_service_initialization(self, mock_configure):
        service = AIService()
        mock_configure.assert_called_once()

    @patch('ai_validation.services.genai.GenerativeModel')
    def test_get_model_caching(self, mock_model):
        mock_instance = MagicMock()
        mock_model.return_value = mock_instance

        # First call
        model1 = self.service.get_model('gemini-2.5-flash')
        # Second call should use cache
        model2 = self.service.get_model('gemini-2.5-flash')

        self.assertEqual(model1, model2)
        mock_model.assert_called_once()

    @patch('backend.ai_validation.services.genai.GenerativeModel')
    def test_validate_text_success(self, mock_model):
        # Setup
        user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        goal = Goal.objects.create(user=user, title='Test Goal', category='learning')
        habit = Habit.objects.create(
            goal=goal,
            title='Reading',
            validation_method='text',
            validation_prompt='Check if this is a reading summary'
        )
        checkin = DailyCheckIn.objects.create(
            habit=habit,
            date=timezone.now().date(),
            text_proof='I read 30 pages of a Python book today.'
        )
        rule = ValidationRule.objects.create(
            name='Text Validation',
            validation_type='text',
            prompt_template='Analyze text for {validation_prompt}',
            confidence_threshold=0.7
        )

        # Mock AI response
        mock_response = MagicMock()
        mock_response.text = '{"confidence": 0.9, "is_approved": true, "explanation": "Good reading summary"}'
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance

        # Test
        result = self.service.validate_checkin(checkin)

        self.assertTrue(result['success'])
        self.assertTrue(result['is_approved'])
        self.assertEqual(result['confidence'], 0.9)

    def test_validate_text_no_proof(self):
        # Create validation rule first
        ValidationRule.objects.create(
            name='Text Validation',
            validation_type='text',
            prompt_template='Analyze text for {validation_prompt}',
            confidence_threshold=0.7
        )

        user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        goal = Goal.objects.create(user=user, title='Test Goal', category='learning')
        habit = Habit.objects.create(
            goal=goal,
            title='Reading',
            validation_method='text',
            validation_prompt='Check reading'
        )
        checkin = DailyCheckIn.objects.create(habit=habit, date=timezone.now().date())

        result = self.service.validate_checkin(checkin)

        self.assertFalse(result['success'])
        self.assertIn('No text proof provided', result['error'])

    @patch('ai_validation.services.genai.GenerativeModel')
    def test_validate_photo_success(self, mock_model):
        # Setup
        user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        goal = Goal.objects.create(user=user, title='Test Goal', category='fitness')
        habit = Habit.objects.create(
            goal=goal,
            title='Exercise',
            validation_method='photo',
            validation_prompt='Check if person is exercising'
        )
        checkin = DailyCheckIn.objects.create(habit=habit, date=timezone.now().date())
        # Create a mock image file
        checkin.photo_proof.save('test.jpg', ContentFile(b'fake image data'), save=True)

        rule = ValidationRule.objects.create(
            name='Photo Validation',
            validation_type='photo',
            prompt_template='Analyze photo for {validation_prompt}',
            confidence_threshold=0.7
        )

        # Mock AI response
        mock_response = MagicMock()
        mock_response.text = '{"confidence": 0.85, "is_approved": true, "explanation": "Person appears to be exercising"}'
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance

        # Test
        result = self.service.validate_checkin(checkin)

        self.assertTrue(result['success'])
        self.assertTrue(result['is_approved'])
        self.assertEqual(result['confidence'], 0.85)

    def test_parse_ai_response_json(self):
        rule = ValidationRule.objects.create(
            name='Test',
            validation_type='text',
            prompt_template='test',
            confidence_threshold=0.8
        )

        response_text = '{"confidence": 0.9, "is_approved": true, "explanation": "Good"}'
        result = self.service._parse_ai_response(response_text, rule)

        self.assertTrue(result['success'])
        self.assertTrue(result['is_approved'])
        self.assertEqual(result['confidence'], 0.9)

    def test_parse_ai_response_unstructured(self):
        response_text = "This looks approved. The content is good and meets requirements."
        result = self.service._parse_ai_response(response_text, None)

        self.assertTrue(result['success'])
        self.assertTrue(result['is_approved'])
        self.assertGreater(result['confidence'], 0.5)

    def test_get_validation_rule(self):
        rule = ValidationRule.objects.create(
            name='Photo Rule',
            validation_type='photo',
            prompt_template='test',
            is_active=True
        )

        user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        goal = Goal.objects.create(user=user, title='Test Goal', category='fitness')
        habit = Habit.objects.create(
            goal=goal,
            title='Exercise',
            validation_method='photo',
            validation_prompt='test'
        )
        checkin = DailyCheckIn.objects.create(habit=habit, date=timezone.now().date())

        found_rule = self.service._get_validation_rule(checkin)
        self.assertEqual(found_rule, rule)

    def test_cache_functionality(self):
        rule = ValidationRule.objects.create(
            name='Cache Test',
            validation_type='text',
            prompt_template='test'
        )

        # Create cache entry
        cache_key = 'test_key_123'
        ValidationCache.objects.create(
            input_hash=cache_key,
            validation_rule=rule,
            input_data_preview='test input',
            ai_response={'cached': True},
            confidence_score=0.8,
            is_approved=True
        )

        # Test cache retrieval
        cached_result = self.service._get_cached_result(cache_key)
        self.assertTrue(cached_result['from_cache'])
        self.assertEqual(cached_result['confidence'], 0.8)
        self.assertTrue(cached_result['is_approved'])

class InsightGeneratorTest(TestCase):
    def setUp(self):
        from .services import InsightGenerator
        self.generator = InsightGenerator()

    @patch('ai_validation.services.genai.GenerativeModel')
    def test_generate_weekly_insights_success(self, mock_model):
        user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        goal = Goal.objects.create(user=user, title='Test Goal', category='fitness')

        # Mock AI response
        mock_response = MagicMock()
        mock_response.text = '''{
            "strength": "Consistent daily tracking",
            "improvement_area": "Try evening workouts",
            "suggestion": "Schedule workouts for 6 PM",
            "motivational_note": "You're doing great!",
            "confidence": 0.85
        }'''
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance

        # Test
        insights = self.generator.generate_weekly_insights(user)

        self.assertIn('strength', insights)
        self.assertIn('suggestion', insights)
        self.assertEqual(insights['strength'], 'Consistent daily tracking')

    def test_generate_fallback_insights(self):
        insights = self.generator._generate_fallback_insights({})

        self.assertIn('strength', insights)
        self.assertIn('suggestion', insights)
        self.assertTrue(insights['fallback'])

class ValidateCheckInViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Test Goal', category='fitness')
        self.habit = Habit.objects.create(
            goal=self.goal,
            title='Exercise',
            validation_method='text',
            validation_prompt='Check exercise',
            min_confidence=0.7
        )
        self.checkin = DailyCheckIn.objects.create(
            habit=self.habit,
            date=timezone.now().date(),
            text_proof='I exercised for 30 minutes today.'
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('ai:validate-checkin')

    @patch('ai_validation.services.AIService.validate_checkin')
    def test_validate_checkin_success(self, mock_validate):
        mock_validate.return_value = {
            'success': True,
            'is_approved': True,
            'confidence': 0.9,
            'explanation': 'Good exercise log',
            'processing_time': 1.5
        }

        data = {'checkin_id': self.checkin.id}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertTrue(response.data['is_approved'])

        # Check that checkin was updated
        self.checkin.refresh_from_db()
        self.assertTrue(self.checkin.is_approved)
        self.assertEqual(self.checkin.ai_confidence, 0.9)

    def test_validate_already_approved_checkin(self):
        self.checkin.is_approved = True
        self.checkin.save()

        data = {'checkin_id': self.checkin.id}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_approved'])

    def test_validate_nonexistent_checkin(self):
        data = {'checkin_id': 99999}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ManualValidationViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        goal = Goal.objects.create(user=self.user, title='Test Goal', category='fitness')
        habit = Habit.objects.create(
            goal=goal,
            title='Test Habit',
            validation_method='self_report',
            validation_prompt='test'
        )
        self.checkin = DailyCheckIn.objects.create(habit=habit, date=timezone.now().date())
        self.client.force_authenticate(user=self.user)
        self.url = reverse('manual-validation')

    def test_manual_approval(self):
        data = {
            'checkin_id': self.checkin.id,
            'is_approved': True,
            'admin_notes': 'Manually approved'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_approved'])

        # Check that checkin was updated
        self.checkin.refresh_from_db()
        self.assertTrue(self.checkin.is_approved)
        self.assertEqual(self.checkin.ai_confidence, 1.0)

class GenerateInsightsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('ai:generate-insights')

    @patch('ai_validation.services.InsightGenerator.generate_weekly_insights')
    def test_generate_insights_success(self, mock_generate):
        mock_generate.return_value = {
            'strength': 'Good consistency',
            'suggestion': 'Keep it up',
            'improvement_area': 'Try harder',
            'motivational_note': 'You rock!'
        }

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('insights', response.data)
        self.assertIn('insight_id', response.data)

class AIFeedbackCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Test Goal', category='fitness')
        self.habit = Habit.objects.create(
            goal=self.goal,
            title='Exercise',
            validation_method='photo',
            validation_prompt='test'
        )
        self.checkin = DailyCheckIn.objects.create(habit=self.habit, date=timezone.now().date())
        self.client.force_authenticate(user=self.user)
        self.url = reverse('ai-feedback-list')

    def test_create_feedback(self):
        data = {
            'checkin': self.checkin.id,
            'feedback_type': 'false_positive',
            'description': 'AI incorrectly approved this check-in',
            'expected_result': 'Should have been rejected'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AIFeedback.objects.filter(user=self.user).exists())

class UserValidationLogsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('ai:validation-logs')

    def test_get_logs(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

class AIPerformanceViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('ai:ai-performance')

    def test_get_performance(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_metrics', response.data)

class ClearValidationCacheViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('clear-cache')

    def test_clear_cache(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('cleared_count', response.data)

class RetryFailedValidationViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.goal = Goal.objects.create(user=self.user, title='Test Goal', category='fitness')
        self.habit = Habit.objects.create(
            goal=self.goal,
            title='Exercise',
            validation_method='text',
            validation_prompt='test'
        )
        self.checkin = DailyCheckIn.objects.create(habit=self.habit, date=timezone.now().date())
        self.rule = ValidationRule.objects.create(
            name='Test Rule',
            validation_type='text',
            prompt_template='test'
        )
        self.failed_log = ValidationLog.objects.create(
            checkin=self.checkin,
            validation_rule=self.rule,
            success=False,
            retry_count=0
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('ai:retry-validation', kwargs={'log_id': self.failed_log.id})

    @patch('ai_validation.services.AIService.validate_checkin')
    def test_retry_validation_success(self, mock_validate):
        mock_validate.return_value = {
            'success': True,
            'is_approved': True,
            'confidence': 0.8,
            'explanation': 'Retry successful'
        }

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

        # Check log was updated
        self.failed_log.refresh_from_db()
        self.assertTrue(self.failed_log.success)
        self.assertEqual(self.failed_log.retry_count, 1)

class ValidateCheckInTaskTest(TestCase):
    def setUp(self):
        from .tasks import validate_checkin_task
        self.task = validate_checkin_task

    @patch('ai_validation.services.AIService.validate_checkin')
    def test_validate_checkin_task_success(self, mock_validate):
        user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        goal = Goal.objects.create(user=user, title='Test Goal', category='fitness')
        habit = Habit.objects.create(
            goal=goal,
            title='Exercise',
            validation_method='self_report',
            validation_prompt='test'
        )
        checkin = DailyCheckIn.objects.create(habit=habit, date=timezone.now().date())

        mock_validate.return_value = {
            'success': True,
            'is_approved': True,
            'confidence': 0.9
        }

        result = self.task(checkin.id)

        self.assertTrue(result['success'])
        self.assertEqual(result['checkin_id'], checkin.id)

        # Check checkin was updated
        checkin.refresh_from_db()
        self.assertTrue(checkin.is_approved)

    def test_validate_checkin_task_not_found(self):
        result = self.task(99999)

        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Check-in not found')

class GenerateWeeklyInsightsTaskTest(TestCase):
    def setUp(self):
        from .tasks import generate_weekly_insights_task
        self.task = generate_weekly_insights_task

    @patch('ai_validation.services.InsightGenerator.generate_weekly_insights')
    def test_generate_insights_task(self, mock_generate):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            is_active=True
        )
        goal = Goal.objects.create(user=user, title='Test Goal', category='fitness', is_active=True)

        mock_generate.return_value = {
            'strength': 'Good work',
            'suggestion': 'Keep going'
        }

        result = self.task()

        self.assertGreater(result['insights_created'], 0)
        self.assertTrue(result['total_users'] >= 1)

class CleanupOldCacheEntriesTaskTest(TestCase):
    def setUp(self):
        from .tasks import cleanup_old_cache_entries
        self.task = cleanup_old_cache_entries

    def test_cleanup_cache(self):
        # Create old cache entry
        rule = ValidationRule.objects.create(name='Test', validation_type='text', prompt_template='test')
        old_date = timezone.now() - timedelta(days=40)
        ValidationCache.objects.create(
            input_hash='old_hash',
            validation_rule=rule,
            input_data_preview='old data',
            ai_response={},
            confidence_score=0.8,
            is_approved=True,
            last_used=old_date
        )

        result = self.task()

        self.assertGreaterEqual(result['deleted_count'], 1)
