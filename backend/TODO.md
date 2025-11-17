# TODO: Write Tests for AI Validation Subapp

## Overview
Expand `backend/ai_validation/tests.py` with comprehensive tests covering models, views, services, and tasks.

## Tasks

### 1. Model Tests
- [ ] AIConfig model tests (creation, validation, string representation)
- [ ] ValidationRule model tests (creation, validation, string representation)
- [ ] ValidationLog model tests (creation, relationships, string representation)
- [ ] AITrainingData model tests (creation, validation, string representation)
- [ ] AIFeedback model tests (creation, relationships, string representation)
- [ ] ModelPerformance model tests (creation, unique constraints, string representation)
- [ ] ValidationCache model tests (creation, caching logic, string representation)

### 2. Service Tests
- [ ] AIService initialization and model caching
- [ ] Photo validation method (_validate_photo)
- [ ] Text validation method (_validate_text)
- [ ] Audio validation method (_validate_audio)
- [ ] Screen recording validation method (_validate_screen_recording)
- [ ] Response parsing (_parse_ai_response, _parse_unstructured_response)
- [ ] Caching functionality (_get_cached_result, _cache_result)
- [ ] Error handling and edge cases
- [ ] InsightGenerator tests (weekly insights generation, fallback insights)

### 3. View Tests
- [ ] ValidateCheckInView (POST validation, approval logic, error handling)
- [ ] ManualValidationView (manual approval/rejection)
- [ ] GenerateInsightsView (insight generation and storage)
- [ ] AIFeedbackCreateView (feedback creation)
- [ ] UserValidationLogsView (log retrieval)
- [ ] AIPerformanceView (performance metrics)
- [ ] ClearValidationCacheView (cache cleanup)
- [ ] RetryFailedValidationView (retry logic)

### 4. Task Tests
- [ ] validate_checkin_task (async validation)
- [ ] generate_weekly_insights_task (bulk insight generation)
- [ ] cleanup_old_cache_entries (cache maintenance)

### 5. Integration Tests
- [ ] End-to-end validation workflow
- [ ] Cache hit/miss scenarios
- [ ] Error recovery and retry mechanisms

## Followup Steps
- [ ] Run tests to verify they pass
- [ ] Check for any missing dependencies or imports
- [ ] Update test coverage reports
