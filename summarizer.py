import os
import re
from typing import Optional

def summarize_article(title: str, content: str = "", use_openai: bool = False) -> Optional[str]:
    """
    Generate a one-sentence summary of an article in Vietnamese.
    
    Args:
        title: Article title
        content: Article content (optional)
        use_openai: Whether to use OpenAI API for summarization
    
    Returns:
        One-sentence summary in Vietnamese or None if summarization fails
    """
    if not title:
        return None
    
    # Simple rule-based summarization for basic cases
    if not use_openai:
        return create_simple_summary(title, content)
    
    # OpenAI-based summarization
    try:
        return create_openai_summary(title, content)
    except Exception as e:
        print(f"OpenAI summarization failed: {e}")
        return create_simple_summary(title, content)

def create_simple_summary(title: str, content: str = "") -> str:
    """Create a simple summary using rule-based approach"""
    # Extract key financial/policy terms
    financial_terms = [
        'tăng trưởng', 'kinh tế', 'GDP', 'lạm phát', 'lãi suất', 'tỷ giá',
        'chứng khoán', 'thị trường', 'đầu tư', 'ngân hàng', 'tài chính',
        'chính sách', 'thuế', 'ngân sách', 'nợ công', 'xuất khẩu', 'nhập khẩu',
        'doanh nghiệp', 'công ty', 'cổ phiếu', 'trái phiếu', 'bất động sản'
    ]
    
    policy_terms = [
        'chính sách', 'luật', 'nghị định', 'thông tư', 'quyết định',
        'chính phủ', 'bộ', 'ngành', 'cơ quan', 'quy định', 'hướng dẫn'
    ]
    
    # Check if title contains financial or policy terms
    title_lower = title.lower()
    
    found_terms = []
    for term in financial_terms + policy_terms:
        if term in title_lower:
            found_terms.append(term)
    
    if found_terms:
        if any(term in title_lower for term in financial_terms):
            return f"Tin tức về {', '.join(found_terms[:2])} trong lĩnh vực tài chính."
        else:
            return f"Thông tin chính sách liên quan đến {', '.join(found_terms[:2])}."
    
    # Default summary based on title length and content
    if len(title) > 50:
        return "Tin tức quan trọng về tài chính và chính sách."
    else:
        return "Cập nhật mới nhất từ thị trường tài chính."

def create_openai_summary(title: str, content: str = "") -> str:
    """Create summary using OpenAI API"""
    try:
        import openai
        
        # Check if OpenAI API key is available
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OpenAI API key not found")
        
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        prompt = f"""
        Tóm tắt ngắn gọn tin tức sau bằng một câu tiếng Việt (tối đa 20 từ):
        
        Tiêu đề: {title}
        Nội dung: {content[:500] if content else 'Không có nội dung chi tiết'}
        
        Tóm tắt:
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là một chuyên gia tóm tắt tin tức tài chính và chính sách bằng tiếng Việt."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.3
        )
        
        summary = response.choices[0].message.content.strip()
        
        # Clean up the summary
        summary = re.sub(r'^["\']|["\']$', '', summary)  # Remove quotes
        summary = re.sub(r'^Tóm tắt:\s*', '', summary, flags=re.IGNORECASE)  # Remove "Tóm tắt:" prefix
        
        return summary if summary else create_simple_summary(title, content)
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return create_simple_summary(title, content)

def is_financial_news(title: str, content: str = "") -> bool:
    """Check if the article is related to finance or policy"""
    financial_keywords = [
        'tài chính', 'kinh tế', 'ngân hàng', 'chứng khoán', 'đầu tư',
        'GDP', 'lạm phát', 'lãi suất', 'tỷ giá', 'thị trường',
        'chính sách', 'thuế', 'ngân sách', 'nợ công', 'xuất khẩu',
        'nhập khẩu', 'doanh nghiệp', 'cổ phiếu', 'trái phiếu',
        'bất động sản', 'tiền tệ', 'vốn', 'tín dụng'
    ]
    
    text_to_check = (title + " " + content).lower()
    return any(keyword in text_to_check for keyword in financial_keywords)

