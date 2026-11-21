"""Task 6 clarify: decides when the bot must ask a question instead of answering."""

from Task_6.config import INTENT_CONFIDENCE_MIN, LANGUAGE_CONFIDENCE_MIN, SUPPORTED_LANGUAGES

ASK_LANGUAGE = ("Which language would you like to use? / आप किस भाषा में बात करना चाहेंगे? / "
                "¿En qué idioma prefiere hablar? / Dans quelle langue souhaitez-vous parler ? "
                "(English, Hindi, Spanish, French)")

ASK_INTENT = {
    "English": "Sorry, I am not sure what you need. Do you have a question about our policies, or a problem with an order?",
    "Hindi": "माफ़ कीजिए, मुझे ठीक से समझ नहीं आया। क्या आपका हमारी नीतियों के बारे में कोई सवाल है, या किसी ऑर्डर में समस्या है?",
    "Hinglish": "Sorry, mujhe theek se samajh nahi aaya. Kya aapka hamari policies ke baare mein koi sawal hai, ya kisi order mein problem hai?",
    "Spanish": "Lo siento, no estoy seguro de lo que necesita. ¿Tiene una pregunta sobre nuestras políticas o un problema con un pedido?",
    "French": "Désolé, je ne suis pas sûr de ce dont vous avez besoin. Avez-vous une question sur nos politiques ou un problème avec une commande ?",
}

UNSUPPORTED = f"Sorry, I can currently help in {', '.join(SUPPORTED_LANGUAGES)}. Could you write in one of these languages?"


def canonical_language(name):
    lowered = (name or "").strip().lower()
    for supported in SUPPORTED_LANGUAGES:
        if lowered == supported.lower() or lowered.startswith(supported.lower() + " "):
            return supported
    return name or "unknown"


def needs_clarification(analysis):
    if analysis.get("analyzer_failed"):
        return None
    language = canonical_language(analysis.get("language", "unknown"))
    if language == "unknown" or analysis.get("language_confidence", 1.0) < LANGUAGE_CONFIDENCE_MIN:
        return "language"
    if language not in SUPPORTED_LANGUAGES:
        return "unsupported_language"
    if analysis.get("intent_confidence", 1.0) < INTENT_CONFIDENCE_MIN:
        return "intent"
    return None


def clarification_text(reason, analysis):
    if reason == "language":
        return ASK_LANGUAGE
    if reason == "unsupported_language":
        return UNSUPPORTED
    return ASK_INTENT.get(canonical_language(analysis.get("language")), ASK_INTENT["English"])