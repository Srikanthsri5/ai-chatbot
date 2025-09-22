from urllib import response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User, AnonymousUser
from .models import Chat
from django.utils import timezone
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Make sure Django can see it
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# print(response.text)

import re
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from .models import Chat

def format_ai_response(response_text):
    """
    Format the AI response for better display
    """
    # Remove the prefix if it exists
    formatted = response_text.replace("🤖 Gemini Response:", "").strip()
    
    # Clean up excessive newlines
    formatted = re.sub(r'\n{3,}', '\n\n', formatted)
    
    # Ensure proper spacing after numbered/bulleted lists
    formatted = re.sub(r'(\d+\.\s.*?)(\n)([^\d\n])', r'\1\n\n\3', formatted)
    formatted = re.sub(r'(\*\s.*?)(\n)([^\*\n])', r'\1\n\n\3', formatted)
    
    return formatted.strip()

def ask_geminiai(message: str) -> str:
    """
    Get response from Gemini AI and format it properly
    """
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=message,
        )
        
        # Get the raw response
        raw_answer = response.text.strip()
        
        # Format the response for better display
        formatted_answer = format_ai_response(raw_answer)
        
        return formatted_answer
        
    except Exception as e:
        # Handle API errors gracefully
        return f"I apologize, but I encountered an error while processing your request: {str(e)}. Please try again."

import re
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from .models import Chat

def format_ai_response(response_text):
    """
    Format the AI response for better display - this will be processed by frontend JS
    """
    # Remove the prefix if it exists
    formatted = response_text.replace("🤖 Gemini Response:", "").strip()
    
    # Remove excessive newlines but preserve structure
    formatted = re.sub(r'\n{4,}', '\n\n\n', formatted)
    
    # Clean up any extra whitespace at the beginning of lines
    formatted = re.sub(r'\n\s+', '\n', formatted)
    
    return formatted.strip()

def ask_geminiai(message: str) -> str:
    """
    Get response from Gemini AI and format it properly
    """
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=message,
        )
        
        # Get the raw response
        raw_answer = response.text.strip()
        
        # Format the response for better display
        formatted_answer = format_ai_response(raw_answer)
        
        return formatted_answer
        
    except Exception as e:
        # Handle API errors gracefully
        return f"I apologize, but I encountered an error while processing your request: {str(e)}. Please try again."

def home(request):
    """
    Render the home page
    """
    return render(request, 'home.html')

def chatbot(request):
    """
    Main chatbot view that handles both GET and POST requests
    """
    # Get chat history for authenticated users
    if request.user.is_authenticated:
        chats = Chat.objects.filter(user=request.user).order_by('created_at')
    else:
        # For anonymous users, you might want to use session-based storage
        chats = []
    
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        
        if not message:
            return JsonResponse({
                'error': 'Please enter a message',
                'message': '',
                'response': ''
            }, status=400)
        
        # Get AI response
        try:
            ai_response = ask_geminiai(message)
            
            # Save to database
            if request.user.is_authenticated:
                chat = Chat(
                    user=request.user, 
                    message=message,
                    response=ai_response, 
                    created_at=timezone.now()
                )
                chat.save()
            else:
                # For anonymous users, you might want to handle differently
                # For now, we'll just not save to database
                pass
            
            return JsonResponse({
                'message': message, 
                'response': ai_response,
                'status': 'success'
            })
            
        except Exception as e:
            error_message = "I'm sorry, I'm having trouble processing your request right now. Please try again in a moment."
            return JsonResponse({
                'error': error_message,
                'message': message,
                'response': error_message
            }, status=500)
    
    # GET request - render the chatbot page
    return render(request, 'chatbot.html', {
        'chats': chats,
        'user': request.user
    })

# Additional utility functions for better chat experience

def get_welcome_message(username=None):
    """
    Generate a personalized welcome message
    """
    if username:
        return f"""
        Hello **{username}**! 👋
        
        I'm Jarvis, your AI assistant. I'm here to help you with:
        
        • **Programming & Technology** - Code help, debugging, best practices
        • **Learning & Education** - Explanations, tutorials, concept clarification  
        • **Problem Solving** - Analysis, troubleshooting, step-by-step solutions
        • **Creative Tasks** - Writing, brainstorming, content creation
        • **General Questions** - Research, facts, recommendations
        
        What would you like to explore today?
        """
    else:
        return """
        Welcome to Jarvis AI Assistant! 🤖
        
        I can help you with programming, learning, problem-solving, and much more.
        
        Feel free to ask me anything!
        """

def sanitize_user_input(message):
    """
    Basic input sanitization for security
    """
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\']', '', message)
    
    # Limit message length
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000] + "..."
    
    return sanitized.strip()

# Enhanced chatbot view with better error handling and features
def enhanced_chatbot(request):
    """
    Enhanced chatbot view with better error handling and features
    """
    # Get chat history
    if request.user.is_authenticated:
        chats = Chat.objects.filter(user=request.user).order_by('created_at')
        welcome_msg = get_welcome_message(request.user.username)
    else:
        chats = []
        welcome_msg = get_welcome_message()
    
    if request.method == 'POST':
        # Sanitize input
        raw_message = request.POST.get('message', '')
        message = sanitize_user_input(raw_message)
        
        if not message:
            return JsonResponse({
                'error': 'Please enter a valid message',
                'message': '',
                'response': ''
            }, status=400)
        
        # Rate limiting check (optional)
        # You can implement rate limiting here
        
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
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Chatbot error: {str(e)}")
            
            error_response = "I apologize, but I'm experiencing some technical difficulties. Please try again in a moment."
            
            return JsonResponse({
                'error': error_response,
                'message': message,
                'response': error_response,
                'status': 'error'
            }, status=500)
    
    return render(request, 'chatbot.html', {
        'chats': chats,
        'user': request.user,
        'welcome_message': welcome_msg
    })

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid Username or password'
            return render(request,'login.html',{'error_message':error_message})
    else:
        return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']  
        email = request.POST['email']  
        password1 = request.POST['password1']  
        password2 = request.POST['password2']  
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = "Error while creating account"
                return render(request,'register.html',{'error_message':error_message})
        else:
            error_message = "password doesn't match"
            return render(request,'register.html',{'error_message':error_message})
    return render(request,'register.html')

def logout(request):
    # return render(request,'logout.html')
    auth.logout(request)
    return redirect('home')
