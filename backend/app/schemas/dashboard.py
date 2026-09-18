from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_accounts: int
    total_characters: int
    unlocked_achievements: int
    latest_news_count: int
    guides_count: int
