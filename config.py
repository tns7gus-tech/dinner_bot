"""
Dinner Bot - Configuration
Settings management using Pydantic
"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """토양체질 저녁식단 추천봇 설정"""
    
    # Telegram
    telegram_bot_token: str = Field(default="", description="Telegram Bot Token")
    telegram_chat_id: str = Field(default="", description="Telegram Chat ID")
    
    # Gemini AI
    gemini_api_key: str = Field(default="", description="Google Gemini API Key")
    gemini_model: str = Field(default="gemini-1.5-pro", description="Gemini 모델")
    
    # Schedule - Meal Recommender
    meal_send_hour: int = Field(default=17, description="식단 추천 발송 시 (기본 17시)")
    meal_send_minute: int = Field(default=30, description="식단 추천 발송 분 (기본 30분)")
    timezone: str = Field(default="Asia/Seoul", description="타임존")
    
    # Server
    port: int = Field(default=8080, description="HTTP 포트")
    log_level: str = Field(default="INFO", description="로그 레벨")
    
    # Leftovers
    leftover_ingredients: str = Field(default="", description="냉장고 잔반 재료 (콤마 구분)")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
