from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils import timezone
import re
import logging
from .ai_api import ask_geminiai
from chatbot.models import Chat


# Configure logger
logger = logging.getLogger(__name__)



def get_welcome_message(username: str = None) -> str:
    """
    Generate a personalized welcome message.

    Args:
        username: Optional username for personalization

    Returns:
        Formatted welcome message
    """
    if username:
        return f"""
        Hello **{username}**! 👋
        
        I'm your AI assistant. I'm here to help you with:
        
        • **Programming & Technology** - Code help, debugging, best practices
        • **Learning & Education** - Explanations, tutorials, concept clarification  
        • **Problem Solving** - Analysis, troubleshooting, step-by-step solutions
        • **Creative Tasks** - Writing, brainstorming, content creation
        • **General Questions** - Research, facts, recommendations
        
        What would you like to explore today?
        """
    else:
        return """
        Welcome to AI Assistant! 
        
        I can help you with programming, learning, problem-solving, and much more.
        
        Feel free to ask me anything!
        """


def sanitize_user_input(message: str) -> str:
    """
    Basic input sanitization for security.

    Args:
        message: Raw user input

    Returns:
        Sanitized and safe user input
    """
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\']', '', message)

    # Limit message length
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000] + "..."

    return sanitized.strip()


def get_user_chats(user):
    """
    Get chat history for user (authenticated or anonymous).

    Args:
        user: Django user object

    Returns:
        QuerySet or list of chats
    """
    if user.is_authenticated:
        return Chat.objects.filter(user=user).order_by('created_at')
    return []


def home(request):
    """Render the home page."""
    return render(request, 'home.html')


def chatbot(request):
    """
    Main chatbot view that handles both GET and POST requests.

    GET: Renders chatbot page with chat history
    POST: Processes user message and returns AI response
    """
    chats = get_user_chats(request.user)

    if request.method == 'POST':
        return handle_chatbot_post(request)

    # GET request - render the chatbot page
    welcome_msg = get_welcome_message(
        request.user.username if request.user.is_authenticated else None
    )

    return render(request, 'chatbot.html', {
        'chats': chats,
        'user': request.user,
        'welcome_message': welcome_msg
    })


def handle_chatbot_post(request):
    """
    Handle POST requests for chatbot functionality.

    Args:
        request: Django request object

    Returns:
        JsonResponse with AI response or error
    """
    # Sanitize input
    raw_message = request.POST.get('message', '')
    message = sanitize_user_input(raw_message)

    if not message:
        return JsonResponse({
            'error': 'Please enter a valid message',
            'message': '',
            'response': ''
        }, status=400)

    try:
        # Get AI response
        ai_response = ask_geminiai(message)

        # Save chat if user is authenticated
        if request.user.is_authenticated:
            Chat.objects.create(
                user=request.user,
                message=message,
                response=ai_response,
                created_at=timezone.now()
            )

        return JsonResponse({
            'message': message,
            'response': ai_response,
            'status': 'success',
            'timestamp': timezone.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}")
        error_response = "I apologize, but I'm experiencing technical difficulties. Please try again."

        return JsonResponse({
            'error': error_response,
            'message': message,
            'response': error_response,
            'status': 'error'
        }, status=500)


def enhanced_chatbot(request):
    """
    Enhanced chatbot view with better error handling and features.
    (Currently functions the same as chatbot - consider merging or removing)
    """
    return chatbot(request)


def delete_chat(request, chat_id):
    """
    Delete a specific chat entry.

    Args:
        request: Django request object
        chat_id: ID of the chat to delete

    Returns:
        Redirect to chatbot page
    """
    if request.user.is_authenticated:
        try:
            chat = Chat.objects.get(id=chat_id, user=request.user)
            chat.delete()
            logger.info(f"Chat {chat_id} deleted by user {request.user.username}")
            
        except Chat.DoesNotExist:
            logger.warning(f"Chat {chat_id} not found for user {request.user.username}")

    return redirect('home')