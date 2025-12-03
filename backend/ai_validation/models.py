from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class AIConfig(models.Model):
    MODEL_CHOICES = [
        ('gemini-2.5-flash', 'Gemini Pro'),
        ('gemini-2.5-flash', 'Gemini Pro Vision'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=200, blank=True)
    model_name = models.CharField(max_length=50, choices=MODEL_CHOICES, default='gemini-2.5-flash')
    max_tokens = models.IntegerField(default=1000)
    temperature = models.FloatField(default=0.7, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_configs'
        verbose_name = 'AI Configuration'
        verbose_name_plural = 'AI Configurations'
    
    def __str__(self):
        return f"{self.name} ({self.model_name})"

class ValidationRule(models.Model):
    VALIDATION_TYPES = [
        ('photo', 'Photo Analysis'),
        ('audio', 'Audio Analysis'),
        ('text', 'Text Analysis'),
        ('screen_recording', 'Screen Recording Analysis'),
        ('general', 'General Validation'),
    ]
    
    name = models.CharField(max_length=100)
    validation_type = models.CharField(max_length=20, choices=VALIDATION_TYPES)
    prompt_template = models.TextField(help_text="Template for AI validation prompt. Use {validation_prompt} for habit-specific prompt.")
    confidence_threshold = models.FloatField(default=0.85, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    max_processing_time = models.IntegerField(default=15, help_text="Seconds")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'validation_rules'
        ordering = ['validation_type', 'name']
    
    def __str__(self):
        return f"{self.validation_type.title()} - {self.name}"

class ValidationLog(models.Model):
    checkin = models.ForeignKey('core.DailyCheckIn', on_delete=models.CASCADE, related_name='validation_logs')
    validation_rule = models.ForeignKey(ValidationRule, on_delete=models.CASCADE)
    
    # Input data
    input_data_preview = models.TextField(blank=True, help_text="Preview of the input data sent to AI")
    
    # AI Response
    ai_response_raw = models.TextField(blank=True, help_text="Raw response from AI")
    ai_response_parsed = models.JSONField(default=dict, help_text="Parsed JSON response from AI")
    
    # Validation results
    confidence_score = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    is_approved = models.BooleanField(default=False)
    processing_time = models.FloatField(null=True, blank=True, help_text="Processing time in seconds")
    
    # Status
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'validation_logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Validation for {self.checkin.habit.title} - {self.created_at}"

class AITrainingData(models.Model):
    DATA_TYPES = [
        ('photo', 'Photo'),
        ('audio', 'Audio'),
        ('text', 'Text'),
        ('screen_recording', 'Screen Recording'),
    ]
    
    data_type = models.CharField(max_length=20, choices=DATA_TYPES)
    input_data = models.TextField(help_text="Input data or description")
    expected_output = models.JSONField(help_text="Expected AI response in JSON format")
    actual_output = models.JSONField(blank=True, null=True, help_text="Actual AI response")
    is_correct = models.BooleanField(null=True, blank=True, help_text="Whether AI response was correct")
    confidence_score = models.FloatField(null=True, blank=True)
    used_for_training = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ai_training_data'
        verbose_name_plural = 'AI Training Data'
    
    def __str__(self):
        return f"{self.data_type} - {self.created_at.date()}"

class AIFeedback(models.Model):
    FEEDBACK_TYPES = [
        ('false_positive', 'False Positive - Wrongly Approved'),
        ('false_negative', 'False Negative - Wrongly Rejected'),
        ('accuracy', 'Accuracy Feedback'),
        ('suggestion', 'Suggestion'),
        ('bug', 'Bug Report'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_feedback')
    checkin = models.ForeignKey('core.DailyCheckIn', on_delete=models.CASCADE, related_name='feedback')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    description = models.TextField()
    expected_result = models.TextField(help_text="What the user expected")
    is_resolved = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_feedback'
    
    def __str__(self):
        return f"{self.user.email} - {self.feedback_type} - {self.created_at.date()}"

class ModelPerformance(models.Model):
    validation_rule = models.ForeignKey(ValidationRule, on_delete=models.CASCADE)
    date = models.DateField()
    
    # Performance metrics
    total_requests = models.IntegerField(default=0)
    successful_requests = models.IntegerField(default=0)
    failed_requests = models.IntegerField(default=0)
    average_confidence = models.FloatField(default=0.0)
    average_processing_time = models.FloatField(default=0.0)
    
    # Accuracy metrics (based on user feedback)
    false_positives = models.IntegerField(default=0)
    false_negatives = models.IntegerField(default=0)
    user_accuracy_score = models.FloatField(default=0.0, help_text="Based on user feedback")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'model_performance'
        unique_together = ['validation_rule', 'date']
        verbose_name_plural = 'Model Performance Metrics'
    
    def __str__(self):
        return f"{self.validation_rule.name} - {self.date}"

class ValidationCache(models.Model):
    """Cache for frequent validations to reduce API calls"""
    input_hash = models.CharField(max_length=64, unique=True, help_text="SHA256 hash of input data")
    validation_rule = models.ForeignKey(ValidationRule, on_delete=models.CASCADE)
    input_data_preview = models.TextField()
    ai_response = models.JSONField()
    confidence_score = models.FloatField()
    is_approved = models.BooleanField()
    usage_count = models.IntegerField(default=1)
    last_used = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'validation_cache'
        indexes = [
            models.Index(fields=['input_hash']),
            models.Index(fields=['last_used']),
        ]
    
    def __str__(self):
        return f"Cache: {self.input_hash[:16]}... ({self.usage_count} uses)"