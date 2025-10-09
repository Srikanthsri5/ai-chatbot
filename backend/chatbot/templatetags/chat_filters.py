# Create this file as: your_app/templatetags/chat_filters.py

from django import template
import re
import html

register = template.Library()

@register.filter
def format_chat_response(text):
    """
    Format chat response text for HTML display with basic markdown conversion
    """
    if not text:
        return ""
    
    # Escape HTML first for security
    text = html.escape(text)
    
    # Remove the Gemini prefix if present
    text = re.sub(r'^🤖 Gemini Response:\s*\n*', '', text)
    
    # Convert markdown-style formatting to HTML
    # Headers
    text = re.sub(r'^### (.*$)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*$)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*$)', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Bold and italic text (be careful with overlapping patterns)
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^\*\n]+?)\*(?!\*)', r'<em>\1</em>', text)
    
    # Code formatting
    text = re.sub(r'```([\s\S]*?)```', r'<pre><code>\1</code></pre>', text)
    text = re.sub(r'`([^`\n]+?)`', r'<code>\1</code>', text)
    
    # Convert numbered lists
    lines = text.split('\n')
    formatted_lines = []
    in_ordered_list = False
    in_unordered_list = False
    
    for line in lines:
        line = line.strip()
        
        # Check for numbered list items
        if re.match(r'^\d+\.\s', line):
            if not in_ordered_list:
                formatted_lines.append('<ol>')
                in_ordered_list = True
                in_unordered_list = False
            item_text = re.sub(r'^\d+\.\s', '', line)
            formatted_lines.append(f'<li>{item_text}</li>')
        
        # Check for bullet list items
        elif re.match(r'^[•\-\*]\s', line):
            if not in_unordered_list:
                if in_ordered_list:
                    formatted_lines.append('</ol>')
                    in_ordered_list = False
                formatted_lines.append('<ul>')
                in_unordered_list = True
            item_text = re.sub(r'^[•\-\*]\s', '', line)
            formatted_lines.append(f'<li>{item_text}</li>')
        
        else:
            # Close lists if we're not in a list item anymore
            if in_ordered_list:
                formatted_lines.append('</ol>')
                in_ordered_list = False
            if in_unordered_list:
                formatted_lines.append('</ul>')
                in_unordered_list = False
            
            if line:
                formatted_lines.append(f'<p>{line}</p>')
            else:
                formatted_lines.append('<br>')
    
    # Close any remaining open lists
    if in_ordered_list:
        formatted_lines.append('</ol>')
    if in_unordered_list:
        formatted_lines.append('</ul>')
    
    result = '\n'.join(formatted_lines)
    
    # Clean up consecutive breaks and empty paragraphs
    result = re.sub(r'<br>\s*<br>', '<br>', result)
    result = re.sub(r'<p></p>', '', result)
    result = re.sub(r'</p>\s*<p>', '</p><p>', result)
    
    return result

@register.filter
def truncate_message(text, length=100):
    """
    Truncate message for preview
    """
    if len(text) <= length:
        return text
    return text[:length] + "..."

@register.filter
def clean_response(text):
    """
    Clean response text by removing API prefixes
    """
    if not text:
        return ""
    
    # Remove common prefixes
    prefixes_to_remove = [
        "🤖 Gemini Response:",
        "AI Response:",
        "Chatbot:",
    ]
    
    for prefix in prefixes_to_remove:
        text = text.replace(prefix, "").strip()
    
    return text