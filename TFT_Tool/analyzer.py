from data_fetcher import TFTDataFetcher

class TFTAnalyzer:
    def __init__(self):
        self.fetcher = TFTDataFetcher()
        self.champions = self.fetcher.get_champion_list()
        self.champion_lookup = {c.get('displayName'): c for c in self.champions}
        for c in self.champions:
            if c.get('title'):
                self.champion_lookup[c.get('title')] = c

    def _to_float(self, value):
        try:
            if value is None or value == "-":
                return None
            return float(value)
        except (TypeError, ValueError):
            return None

    def _to_percent(self, value):
        numeric = self._to_float(value)
        if numeric is None:
            return None
        if numeric <= 1:
            return numeric * 100
        return numeric

    def _judge_tier(self, place):
        if place is None:
            return "未知"
        if place <= 3.9:
            return "S"
        if place <= 4.15:
            return "A"
        if place <= 4.45:
            return "B"
        if place <= 4.8:
            return "C"
        return "D"

    def _build_answer(self, champion_name, details):
        live_stats = details.get("live_stats") or {}
        place = self._to_float(live_stats.get("place"))
        top4 = self._to_percent(live_stats.get("top4"))
        win = self._to_percent(live_stats.get("win"))
        tier = self._judge_tier(place)

        metric_text = []
        if place is not None:
            metric_text.append(f"平均排名 {place:.2f}")
        if top4 is not None:
            metric_text.append(f"前四率 {top4:.1f}%")
        if win is not None:
            metric_text.append(f"吃鸡率 {win:.1f}%")

        metric_sentence = "，".join(metric_text) if metric_text else "暂无足够统计指标"
        summary = f"{champion_name} 当前强度评级：{tier}。{metric_sentence}。"

        if tier in ("S", "A"):
            advice = "结论：当前版本表现优秀，适合作为主力或核心输出。"
        elif tier == "B":
            advice = "结论：当前版本表现中等偏上，可根据阵容与来牌情况灵活选择。"
        elif tier in ("C", "D"):
            advice = "结论：当前版本偏弱，建议仅在特定羁绊或条件满足时使用。"
        else:
            advice = "结论：当前数据不足，建议结合对局环境谨慎判断。"

        return {
            "tier": tier,
            "place": place,
            "top4": top4,
            "win": win,
            "summary": summary,
            "advice": advice
        }

    def extract_champion_name(self, question):
        normalized = (question or "").strip()
        lowered = normalized.lower()
        for name in self.champion_lookup.keys():
            if not name:
                continue
            if name in normalized:
                return name
            if str(name).lower() in lowered:
                return name
        return None

    def analyze(self, question):
        champion_name = self.extract_champion_name(question)
        
        if not champion_name:
            sample_champs = [c.get('displayName') for c in self.champions[:5]]
            sample_str = "、".join(sample_champs)
            return {
                "status": "error",
                "message": f"未能识别出具体的英雄名称。当前赛季包含英雄如：{sample_str} 等。请尝试直接输入英雄名字（如：{sample_champs[0]}）。"
            }

        stats = self.fetcher.get_champion_stats(champion_name)
        
        if not stats:
             return {
                "status": "error",
                "message": f"找到了名字 '{champion_name}'，但在数据源中未找到详细信息。"
            }

        strength = self._build_answer(champion_name, stats)
        return {
            "status": "success",
            "champion": champion_name,
            "details": stats,
            "strength": strength,
            "answer": f"{strength['summary']}\n{strength['advice']}"
        }
