from google import genai # <--- CHANGED THIS LINE
import time
import json
import base64
import hashlib
import logging
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
# Assuming .models imports are correct for your Django project structure
from .models import AIConfig, ValidationRule, ValidationCache, ModelPerformance

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = settings.GOOGLE_AI_API_KEY
        self.model_cache = {}
        
        if self.api_key:
            # The configuration method remains the same
            genai.configure(api_key=self.api_key)
        else:
            logger.warning("GOOGLE_AI_API_KEY not set. AI validation will not work.")
    
    def get_model(self, model_name='gemini-2.5-flash'): # Recommended update to a current model
        """Get or create a Gemini model instance"""
        if model_name not in self.model_cache:
            try:
                # The model initialization remains the same
                self.model_cache[model_name] = genai.GenerativeModel(model_name)
            except Exception as e:
                logger.error(f"Failed to create model {model_name}: {str(e)}")
                raise
        return self.model_cache[model_name]
    
    def validate_checkin(self, checkin):
        """Main validation method for check-ins"""
        start_time = time.time()
        
        try:
            # Get appropriate validation rule
            validation_rule = self._get_validation_rule(checkin)
            if not validation_rule:
                return self._create_error_result("No validation rule found", start_time)
            
            # Check cache first
            cache_key = self._generate_cache_key(checkin, validation_rule)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                logger.info(f"Using cached validation result for checkin {checkin.id}")
                return cached_result
            
            # Perform validation based on type
            if checkin.habit.validation_method == 'photo':
                # Note: 'gemini-pro-vision' is now commonly aliased to a multimodel,
                # but 'gemini-2.5-flash' handles multimodal inputs and is faster/cheaper.
                result = self._validate_photo(checkin, validation_rule) 
            elif checkin.habit.validation_method == 'text':
                result = self._validate_text(checkin, validation_rule)
            elif checkin.habit.validation_method == 'audio':
                result = self._validate_audio(checkin, validation_rule)
            elif checkin.habit.validation_method == 'screen_recording':
                result = self._validate_screen_recording(checkin, validation_rule)
            else:
                result = self._create_error_result("Unsupported validation method", start_time)
            
            # Cache successful results
            if result.get('success') and result.get('confidence', 0) > 0.7:
                self._cache_result(cache_key, checkin, validation_rule, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Validation error for checkin {checkin.id}: {str(e)}")
            return self._create_error_result(str(e), start_time)
    
    def _validate_photo(self, checkin, validation_rule):
        """Validate photo evidence using Gemini"""
        if not checkin.photo_proof:
            return self._create_error_result("No photo proof provided")
        
        try:
            # Using the recommended 'gemini-2.5-flash' for multimodal tasks
            model = self.get_model('gemini-2.5-flash') 
            
            # Read image data
            checkin.photo_proof.open('rb')
            image_data = checkin.photo_proof.read()
            checkin.photo_proof.close()
            
            prompt = self._build_prompt(validation_rule, checkin.habit.validation_prompt)
            
            # Create a Part object for the image data
            # The 'data' key for the image content in the list of parts is still supported, 
            # but using genai.types.Part is the recommended modern approach for complex inputs.
            # For direct image bytes, the original dict structure works fine and is preserved here.
            
            response = model.generate_content([
                prompt,
                {"mime_type": "image/jpeg", "data": image_data}
            ])
            
            return self._parse_ai_response(response.text, validation_rule)
            
        except Exception as e:
            logger.error(f"Photo validation error: {str(e)}")
            return self._create_error_result(f"Photo validation failed: {str(e)}")
    
    def _validate_text(self, checkin, validation_rule):
        """Validate text evidence"""
        if not checkin.text_proof:
            return self._create_error_result("No text proof provided")
        
        try:
            model = self.get_model('gemini-2.5-flash')
            
            prompt = self._build_prompt(validation_rule, checkin.habit.validation_prompt)
            full_prompt = f"""
            {prompt}
            
            TEXT TO ANALYZE:
            "{checkin.text_proof}"
            
            REQUIREMENTS:
            - Minimum 50 characters for meaningful content
            - Relevant to the habit: {checkin.habit.validation_prompt}
            - Shows genuine effort/reflection
            - Appropriate length and depth
            
            Please analyze thoroughly and provide your assessment.
            """
            
            # The generate_content call remains the same
            response = model.generate_content(full_prompt)
            return self._parse_ai_response(response.text, validation_rule)
            
        except Exception as e:
            logger.error(f"Text validation error: {str(e)}")
            return self._create_error_result(f"Text validation failed: {str(e)}")
    
    def _validate_audio(self, checkin, validation_rule):
        """Validate audio evidence - placeholder implementation"""
        # Note: Actual audio processing would require additional services
        # For now, we'll use a text-based analysis of audio description
        try:
            model = self.get_model('gemini-2.5-flash')
            
            prompt = self._build_prompt(validation_rule, checkin.habit.validation_prompt)
            full_prompt = f"""
            {prompt}
            
            AUDIO CONTEXT:
            The user has submitted an audio recording for: {checkin.habit.validation_prompt}
            Audio duration: Available (placeholder)
            Content: User's audio submission
            
            Since we cannot process audio directly in this implementation, please provide a 
            general assessment based on typical audio submissions for this type of habit.
            
            Assume the audio has been verified to contain relevant content.
            """
            
            response = model.generate_content(full_prompt)
            result = self._parse_ai_response(response.text, validation_rule)
            
            # For audio, we might want to be more lenient in MVP
            if result.get('confidence', 0) > 0.6:
                result['is_approved'] = True
                result['confidence'] = max(result.get('confidence', 0), 0.7)
            
            return result
            
        except Exception as e:
            logger.error(f"Audio validation error: {str(e)}")
            return self._create_error_result(f"Audio validation failed: {str(e)}")
    
    def _validate_screen_recording(self, checkin, validation_rule):
        """Validate screen recording - placeholder implementation"""
        try:
            model = self.get_model('gemini-2.5-flash')
            
            prompt = self._build_prompt(validation_rule, checkin.habit.validation_prompt)
            full_prompt = f"""
            {prompt}
            
            SCREEN RECORDING CONTEXT:
            The user has submitted a screen recording for: {checkin.habit.validation_prompt}
            Content: User's screen activity related to the habit
            
            Since we cannot process screen recordings directly in this implementation, 
            please provide an assessment based on typical screen recordings for this habit type.
            
            Assume the screen recording shows relevant activity.
            """
            
            response = model.generate_content(full_prompt)
            result = self._parse_ai_response(response.text, validation_rule)
            
            # For screen recordings, be moderately confident in MVP
            if result.get('confidence', 0) > 0.65:
                result['is_approved'] = True
                result['confidence'] = max(result.get('confidence', 0), 0.75)
            
            return result
            
        except Exception as e:
            logger.error(f"Screen recording validation error: {str(e)}")
            return self._create_error_result(f"Screen recording validation failed: {str(e)}")
    
    def _build_prompt(self, validation_rule, habit_prompt):
        """Build the AI prompt from template and habit-specific prompt"""
        prompt_template = validation_rule.prompt_template
        return prompt_template.replace('{validation_prompt}', habit_prompt)
    
    # ... (other helper methods remain unchanged)
    # _parse_ai_response, _parse_unstructured_response, _get_validation_rule, 
    # _generate_cache_key, _get_cached_result, _cache_result, _create_error_result
    
    def _parse_ai_response(self, response_text, validation_rule):
        """Parse AI response and extract structured data"""
        try:
            # Try to parse as JSON first
            if response_text.strip().startswith('{'):
                result = json.loads(response_text)
            else:
                # Fallback: extract JSON from text
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = response_text[start_idx:end_idx]
                    result = json.loads(json_str)
                else:
                    # Final fallback: manual parsing
                    result = self._parse_unstructured_response(response_text)
            
            # Validate required fields
            confidence = result.get('confidence', 0.0)
            is_approved = result.get('is_approved', False)
            explanation = result.get('explanation', 'No explanation provided')
            
            # Apply confidence threshold
            if validation_rule and confidence < validation_rule.confidence_threshold:
                is_approved = False
            
            return {
                'success': True,
                'confidence': confidence,
                'is_approved': is_approved,
                'explanation': explanation,
                'raw_response': response_text,
                'parsed_data': result
            }
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to parse AI response: {str(e)}")
            return self._parse_unstructured_response(response_text)
    
    def _parse_unstructured_response(self, response_text):
        """Parse unstructured AI response"""
        # Simple heuristic parsing
        confidence = 0.5
        is_approved = False
        explanation = response_text[:500]  # Truncate long responses
        
        # Basic keyword analysis
        response_lower = response_text.lower()
        positive_keywords = ['approved', 'yes', 'correct', 'valid', 'good', 'proper', 'acceptable']
        negative_keywords = ['rejected', 'no', 'incorrect', 'invalid', 'poor', 'improper', 'unacceptable']
        
        positive_count = sum(1 for word in positive_keywords if word in response_lower)
        negative_count = sum(1 for word in negative_keywords if word in response_lower)
        
        if positive_count > negative_count:
            is_approved = True
            confidence = 0.7
        elif negative_count > positive_count:
            is_approved = False
            confidence = 0.6
        else:
            # Ambiguous response
            is_approved = False
            confidence = 0.4
        
        return {
            'success': True,
            'confidence': confidence,
            'is_approved': is_approved,
            'explanation': explanation,
            'raw_response': response_text,
            'parsed_data': {'fallback_parsing': True}
        }
    
    def _get_validation_rule(self, checkin):
        """Get appropriate validation rule for checkin type"""
        try:
            return ValidationRule.objects.get(
                validation_type=checkin.habit.validation_method,
                is_active=True
            )
        except ValidationRule.DoesNotExist:
            logger.warning(f"No validation rule found for {checkin.habit.validation_method}")
            return None
    
    def _generate_cache_key(self, checkin, validation_rule):
        """Generate cache key based on input data"""
        input_data = f"{checkin.habit.validation_prompt}-{validation_rule.id}"
        
        if checkin.text_proof:
            input_data += f"-{checkin.text_proof[:100]}"
        elif checkin.photo_proof:
            input_data += f"-photo-{checkin.photo_proof.name}"
        
        return hashlib.sha256(input_data.encode()).hexdigest()
    
    def _get_cached_result(self, cache_key):
        """Get result from cache"""
        try:
            cache_entry = ValidationCache.objects.get(input_hash=cache_key)
            cache_entry.usage_count += 1
            cache_entry.last_used = timezone.now()
            cache_entry.save()
            
            return {
                'success': True,
                'confidence': cache_entry.confidence_score,
                'is_approved': cache_entry.is_approved,
                'explanation': 'Result from cache',
                'from_cache': True,
                'cached_data': cache_entry.ai_response
            }
        except ValidationCache.DoesNotExist:
            return None
    
    def _cache_result(self, cache_key, checkin, validation_rule, result):
        """Cache validation result"""
        try:
            input_preview = f"{checkin.habit.validation_prompt}"
            if checkin.text_proof:
                input_preview += f" - {checkin.text_proof[:100]}..."
            
            ValidationCache.objects.create(
                input_hash=cache_key,
                validation_rule=validation_rule,
                input_data_preview=input_preview,
                ai_response=result.get('parsed_data', {}),
                confidence_score=result['confidence'],
                is_approved=result['is_approved']
            )
        except Exception as e:
            logger.warning(f"Failed to cache result: {str(e)}")
    
    def _create_error_result(self, error_message, start_time=None):
        """Create error result structure"""
        processing_time = time.time() - start_time if start_time else 0
        
        return {
            'success': False,
            'error': error_message,
            'confidence': 0.0,
            'is_approved': False,
            'explanation': f"Validation failed: {error_message}",
            'processing_time': processing_time
        }

class InsightGenerator:
    """Generate insights based on user progress data"""
    
    def __init__(self):
        self.ai_service = AIService()
    
    def generate_weekly_insights(self, user):
        """Generate weekly insights for a user"""
        try:
            model = self.ai_service.get_model()
            
            # Get user's recent activity
            from core.models import DailyCheckIn, Habit
            from django.utils import timezone
            from datetime import timedelta
            
            week_ago = timezone.now() - timedelta(days=7)
            
            recent_checkins = DailyCheckIn.objects.filter(
                habit__goal__user=user,
                created_at__gte=week_ago,
                is_approved=True
            ).select_related('habit')
            
            habits = Habit.objects.filter(goal__user=user, is_active=True)
            
            # Prepare data for AI analysis
            analysis_data = {
                'user_goals': [goal.title for goal in user.goals.all()],
                'active_habits': [habit.title for habit in habits],
                'recent_completions': len(recent_checkins),
                'completion_rate': self._calculate_completion_rate(habits, recent_checkins),
                'streak_info': self._get_streak_info(user),
                'common_times': self._get_common_completion_times(recent_checkins),
            }
            
            prompt = f"""
            Analyze this user's consistency data and provide helpful insights:
            
            USER DATA:
            {json.dumps(analysis_data, indent=2)}
            
            Please provide:
            1. One key strength or success pattern
            2. One area for improvement
            3. One specific, actionable suggestion
            4. Motivational note based on their progress
            
            Format as JSON:
            {{
                "strength": "key strength observed",
                "improvement_area": "area needing attention", 
                "suggestion": "specific actionable suggestion",
                "motivational_note": "encouraging message",
                "confidence": 0.85
            }}
            """
            
            response = model.generate_content(prompt)
            # Pass None for validation_rule in _parse_ai_response since this is an insight, not a validation
            result = self.ai_service._parse_ai_response(response.text, None) 
            
            if result['success']:
                return result['parsed_data']
            else:
                return self._generate_fallback_insights(analysis_data)
                
        except Exception as e:
            logger.error(f"Insight generation failed: {str(e)}")
            return self._generate_fallback_insights({})
    
    def _calculate_completion_rate(self, habits, checkins):
        """Calculate completion rate for recent period"""
        total_possible = len(habits) * 7  # 7 days
        if total_possible == 0:
            return 0.0
        return len(checkins) / total_possible
    
    def _get_streak_info(self, user):
        """Get streak information for user"""
        from core.models import Streak
        streaks = Streak.objects.filter(user=user).order_by('-current_streak')[:3]
        return [{'habit': s.habit.title, 'streak': s.current_streak} for s in streaks]
    
    def _get_common_completion_times(self, checkins):
        """Analyze common completion times"""
        if not checkins:
            return []
        
        times = [c.completed_at.hour for c in checkins if c.completed_at]
        if times:
            from collections import Counter
            common_hours = Counter(times).most_common(3)
            return [f"{hour}:00" for hour, count in common_hours]
        return []
    
    def _generate_fallback_insights(self, data):
        """Generate fallback insights when AI fails"""
        return {
            "strength": "You're building consistency by tracking your habits regularly",
            "improvement_area": "Try to maintain your current streak", 
            "suggestion": "Set a specific time each day for your habits",
            "motivational_note": "Every day you practice brings you closer to your goals!",
            "confidence": 0.5,
            "fallback": True
        }