"""Task 6 config: languages, confidence thresholds and session timings."""

BASE_LANGUAGE = "English"
ADDITIONAL_LANGUAGES = ["Hindi", "Spanish", "French"]
MIXED_LANGUAGES = {"Hinglish": "Hindi"} 
SUPPORTED_LANGUAGES = [BASE_LANGUAGE] + ADDITIONAL_LANGUAGES + list(MIXED_LANGUAGES)

LANGUAGE_CONFIDENCE_MIN = 0.6  
INTENT_CONFIDENCE_MIN = 0.6    

SESSION_IDLE_MINUTES = 30      
SESSION_RESTORE_HOURS = 24     
CONTEXT_MESSAGES = 12          
SUMMARY_MARKER = "[Summary of the earlier conversation]"
FOLLOWUP_MAX_WORDS = 4 