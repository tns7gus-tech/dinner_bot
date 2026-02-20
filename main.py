"""
Dinner Bot - Main Entry Point
토양체질 저녁 식단 추천봇 (매일 17:30 자동 발송)
"""
import asyncio
import os
import sys
from datetime import datetime
import pytz
from pathlib import Path

from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

# Add current dir to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from meal_recommender import MealRecommender
from telegram_notifier import TelegramNotifier


# Configure logging
logger.remove()
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>"
logger.add(sys.stderr, format=log_format, level=settings.log_level)


class DinnerBot:
    """
    매일 17:30 토양체질 저녁 식단 추천봇
    Gemini AI를 활용하여 단백질+면역력 중심 5가지 요리를 추천
    """
    
    def __init__(self):
        self.meal_recommender = MealRecommender()
        self.notifier = TelegramNotifier()
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone(settings.timezone))
        self.running = False
        
        logger.info("🍽️ DinnerBot 초기화 완료")
    
    async def start(self):
        """봇 시작"""
        await self.notifier.start()
        
        # 스케줄러 설정: 토양체질 저녁 식단 (매일 17:30)
        self.scheduler.add_job(
            self.send_dinner_recommendation,
            CronTrigger(
                hour=settings.meal_send_hour,
                minute=settings.meal_send_minute,
                timezone=pytz.timezone(settings.timezone)
            ),
            id="dinner_recommendation",
            name="Daily Dinner Recommendation",
            misfire_grace_time=3600  # 1시간 내 재시작 시 발송
        )
        
        self.scheduler.start()
        
        logger.success(
            f"🚀 저녁식단 추천봇 시작! "
            f"매일 {settings.meal_send_hour}:{settings.meal_send_minute:02d} 발송"
        )
        
        # 시작 알림
        try:
            await self.notifier.send_message(
                f"🚀 *저녁식단 추천봇 시작!*\n\n"
                f"🍽️ 토양체질 저녁 식단: 매일 {settings.meal_send_hour}:{settings.meal_send_minute:02d}\n\n"
                f"📅 시작 시각: {self.notifier.get_now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
        except Exception as e:
            logger.warning(f"시작 알림 발송 실패: {e}")
    
    async def stop(self):
        """봇 종료"""
        self.scheduler.shutdown()
        await self.notifier.close()
        logger.info("⏹️ 저녁식단 추천봇 종료")
    
    async def send_dinner_recommendation(self):
        """
        토양체질 저녁 식단 추천 발송 (매일 스케줄러)
        """
        logger.info("🍽️ 토양체질 저녁 식단 추천 생성 중...")
        
        try:
            menu = await self.meal_recommender.generate_dinner_menu()
            result = await self.notifier.send_meal(menu)
            
            if result:
                logger.success("✅ 저녁 식단 추천 발송 완료!")
            else:
                logger.error("❌ 저녁 식단 추천 발송 실패")
                
        except Exception as e:
            logger.error(f"❌ 저녁 식단 추천 발송 에러: {e}")

    async def send_test_meal(self):
        """
        테스트용 즉시 발송 (식단)
        """
        logger.info("🧪 테스트 식단 추천 생성 중...")
        
        menu = await self.meal_recommender.generate_dinner_menu()
        result = await self.notifier.send_meal(menu)
        return result

    async def send_leftover_recommendation(self):
        """
        잔반 활용 식단 추천 발송 (수동 실행)
        """
        ingredients = settings.leftover_ingredients
        if not ingredients:
            logger.error("❌ 잔반 재료가 설정되지 않았습니다. .env 파일의 LEFTOVER_INGREDIENTS를 확인하세요.")
            return False
            
        logger.info(f"🍽️ 잔반 활용 식단 추천 생성 중... (재료: {ingredients})")
        
        try:
            menu = await self.meal_recommender.generate_leftover_menu(ingredients)
            result = await self.notifier.send_meal(menu)
            
            if result:
                logger.success("✅ 잔반 식단 추천 발송 완료!")
                return True
            else:
                logger.error("❌ 잔반 식단 추천 발송 실패")
                return False
                
        except Exception as e:
            logger.error(f"❌ 잔반 식단 추천 발송 에러: {e}")
            return False


async def health_check(request):
    """Railway 헬스체크용"""
    return web.Response(text="OK", status=200)


async def on_startup(app):
    """서버 시작 시 봇 구동"""
    app['bot'] = DinnerBot()
    await app['bot'].start()

async def on_cleanup(app):
    """서버 종료 시 봇 정리"""
    if 'bot' in app:
        await app['bot'].stop()


def main():
    """Entry point"""
    logger.info("=" * 40)
    logger.info("🍽️ Dinner Bot v1.0.0")
    logger.info("   토양체질 저녁 식단 추천")
    logger.info("=" * 40)
    
    # CLI 모드 체크
    test_meal = "--test" in sys.argv
    leftover_meal = "--leftover" in sys.argv
    
    # 1. CLI 모드 실행 (서버 구동 없이 단발성 실행)
    if test_meal or leftover_meal:
        async def run_cli():
            bot = DinnerBot()
            await bot.notifier.start() # 봇 초기화
            
            if test_meal:
                logger.info("🧪 테스트 모드: 즉시 식단 추천 발송")
                result = await bot.send_test_meal()
                print(f"\n테스트 결과: {'[OK] 성공' if result else '[FAIL] 실패'}")
                
            elif leftover_meal:
                logger.info("🥘 잔반 활용 식단 추천 모드")
                result = await bot.send_leftover_recommendation()
                print(f"\n발송 결과: {'[OK] 성공' if result else '[FAIL] 실패'}")
            
            await bot.stop()
            
        asyncio.run(run_cli())
        return

    # 2. 서버 모드 실행 (Railway/Docker)
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    
    # Startup/Cleanup 핸들러 등록
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    
    port = int(os.environ.get("PORT", settings.port))
    logger.info(f"🌐 웹 서버 실행 준비 (포트: {port})")
    
    # aiohttp의 run_app은 블로킹 함수이며 시그널 처리를 자동으로 수행함
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
