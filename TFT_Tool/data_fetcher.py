import requests
import json
from bs4 import BeautifulSoup
import re

# 腾讯官方英雄数据接口
CHAMPION_URL = "https://game.gtimg.cn/images/lol/act/img/tft/js/chess.js"
# 大数据来源 (tactics.tools)
STATS_URL = "https://tactics.tools/units"
# CDragon 装备数据
ITEM_DATA_URL = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/zh_cn/v1/tftitems.json"

class TFTDataFetcher:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self._cached_stats = None
        self._cached_items = None
        self._item_map = {}

    def _fetch_items(self):
        """抓取并缓存装备数据 (CDragon)"""
        if self._cached_items:
            return self._cached_items
            
        try:
            resp = requests.get(ITEM_DATA_URL, timeout=10)
            if resp.status_code == 200:
                items = resp.json()
                self._cached_items = items
                
                # 构建映射：简化名 -> 图标/中文名
                # 例如: "GuinsoosRageblade" -> {name: "鬼索的狂暴之刃", icon: "..."}
                for item in items:
                    # CDragon tftitems.json 使用 nameId，如 TFT_Item_BFSword
                    # 也有部分项目用 apiName
                    raw_id = item.get('nameId') or item.get('apiName')
                    if not raw_id: continue
                    
                    # 简化 key (去掉 TFT_Item_ / TFTTutorial_Item_ 等前缀)
                    # 匹配 TFT 后跟任意字符，直到 _Item_
                    simple_key = re.sub(r'TFT\w*_Item_', '', raw_id)
                    # 还要去掉 TFT_Augment_ 前缀，虽然我们可能不需要 Augment，但以防万一
                    simple_key = re.sub(r'TFT\w*_Augment_', '', simple_key)
                    
                    # 处理图标路径
                    icon_path = item.get('squareIconPath') or item.get('icon', '')
                    icon_path = icon_path.lower()
                    
                    icon_url = ""
                    if '/lol-game-data/assets/' in icon_path:
                        # 修复图片路径：去除 /lol-game-data/assets/ 前缀，保留后续部分并转小写
                        # 例如: /lol-game-data/assets/ASSETS/Maps/... -> assets/maps/...
                        # 最终 URL: .../global/default/assets/maps/...
                        relative = icon_path.replace('/lol-game-data/assets/', '')
                        icon_url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/{relative}"
                        
                    item_data = {
                        "name": item.get('name'),
                        "icon": icon_url,
                        "desc": item.get('desc')
                    }
                    
                    self._item_map[simple_key] = item_data
                    self._item_map[raw_id] = item_data
                    
        except Exception as e:
            print(f"Error fetching items: {e}")
        return self._item_map

    def get_champion_list(self):
        """从官方接口获取英雄列表"""
        try:
            response = requests.get(CHAMPION_URL, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    # 过滤非英雄单位
                    raw_data = data['data']
                    champions = [
                        c for c in raw_data 
                        if c.get('raceIds') != "" and c.get('jobIds') != "" 
                    ]
                    return champions
            return []
        except Exception as e:
            print(f"Error fetching champion list: {e}")
            return []

    def _fetch_live_stats(self):
        """抓取 tactics.tools 的实时大数据"""
        if self._cached_stats:
            return self._cached_stats
            
        try:
            resp = requests.get(STATS_URL, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                script = soup.find('script', id='__NEXT_DATA__')
                if script:
                    data = json.loads(script.string)
                    stats = data.get('props', {}).get('pageProps', {}).get('statsData', {})
                    self._cached_stats = stats
                    return stats
        except Exception as e:
            print(f"Error fetching live stats: {e}")
        return {}
        
    def _fetch_unit_builds(self, unit_api_name):
        """抓取特定英雄的详细推荐出装 (itemTrios)"""
        # 尝试多种 slug 格式
        base_slug = unit_api_name.split('_')[-1].lower() # e.g. "MissFortune" -> "missfortune"
        
        # 候选 slugs: "missfortune", "miss-fortune"
        candidates = [base_slug]
        # 如果名字里有大写字母（驼峰），可能需要拆分？
        # 但通常 tactics.tools 是去除非字母符号
        
        # 针对一些特殊情况的手动映射
        special_map = {
            "renataglasc": "renata", # 假设 S16 只有 Renata
            "drmundo": "dr-mundo",
            "jarvaniv": "jarvan-iv",
            "kogmaw": "kog-maw",
            "reksai": "reksai", # usually reksai
            "tahmkench": "tahm-kench",
            "twistedfate": "twisted-fate",
            "missfortune": "miss-fortune",
            "xinzhao": "xin-zhao",
            "leesin": "lee-sin",
            "masteryi": "master-yi",
            "aurelionsol": "aurelion-sol",
            "belveth": "belveth",
            "chogath": "chogath",
            "kaisa": "kaisa",
            "khazix": "khazix",
            "leblanc": "leblanc",
            "nunu": "nunu-willump",
            "velkoz": "velkoz"
        }
        
        if base_slug in special_map:
            candidates.insert(0, special_map[base_slug])

        for slug in candidates:
            url = f"https://tactics.tools/unit/{slug}"
            try:
                resp = requests.get(url, headers=self.headers, timeout=5)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    script = soup.find('script', id='__NEXT_DATA__')
                    if script:
                        data = json.loads(script.string)
                        unit_data = data.get('props', {}).get('pageProps', {}).get('unitData', {})
                        if 'itemTrios' in unit_data:
                            return unit_data['itemTrios']
            except Exception as e:
                print(f"Error fetching builds for {slug}: {e}")
                
        return []

    def get_tier_list(self):
        """
        根据实时大数据计算评级
        """
        stats = self._fetch_live_stats()
        units = stats.get('units', {})
        
        if not units:
            return {}

        # 根据平均排名 (place) 进行分级
        tier_map = {"S": [], "A": [], "B": [], "C": [], "D": []}
        
        # 整理数据
        unit_list = []
        for api_name, s in units.items():
            unit_list.append({
                "apiName": api_name,
                "place": s.get('place', 5.0)
            })
        
        # 按排名升序排列 (越小越强)
        unit_list.sort(key=lambda x: x['place'])
        
        count = len(unit_list)
        for i, u in enumerate(unit_list):
            if i < count * 0.1: tier = "S"
            elif i < count * 0.3: tier = "A"
            elif i < count * 0.6: tier = "B"
            elif i < count * 0.8: tier = "C"
            else: tier = "D"
            tier_map[tier].append(u['apiName'])
            
        return tier_map

    def get_champion_stats(self, champion_name):
        """结合英雄信息和实时大数据"""
        champions = self.get_champion_list()
        live_stats = self._fetch_live_stats()
        units = live_stats.get('units', {})
        
        # 确保装备数据已加载
        if not self._item_map:
            self._fetch_items()
        
        # 匹配英雄
        champion_info = next((c for c in champions if c.get('displayName') == champion_name or c.get('title') == champion_name), None)
        if not champion_info:
            return None

        # 匹配大数据中的 API Name (通常是 TFT16_Jinx 这种格式)
        api_name = champion_info.get('hero_EN_name', '')
        # 尝试几种匹配方式
        unit_data = units.get(api_name) or units.get(f"TFT16_{api_name}") or units.get(api_name.split('_')[-1])
        
        # 如果还是没匹配到，遍历一下找包含关系的
        if not unit_data:
            for k in units.keys():
                if api_name in k or (champion_info.get('displayName') in k):
                    unit_data = units[k]
                    api_name = k # 更新为真实的 key
                    break
        
        # 获取详细推荐出装 (Trios)
        builds = []
        if unit_data:
             # 注意：unit_data 本身只有 topItems，要获取详细组合需要额外请求
             # 但为了性能，如果 unit_data 里没有 trios，我们可以单独请求一次详情页
             # 这里我们为了效果，单独请求一次详情页获取 itemTrios
             raw_builds = self._fetch_unit_builds(api_name)
             
             # 处理前3种推荐出装
             if raw_builds:
                 for build in raw_builds[:3]:
                     processed_items = []
                     for item_key in build['items']:
                         # 从映射中获取中文名和图标
                         # 尝试处理带 TFT_Item_ 的 key
                         simple_key = re.sub(r'TFT\d*_Item_', '', item_key)
                         item_info = self._item_map.get(simple_key) or self._item_map.get(item_key)
                         
                         if not item_info:
                             # 如果映射里没找到，用原始 key
                             item_info = {"name": item_key, "icon": ""}
                             
                         processed_items.append(item_info)
                     
                     builds.append({
                         "items": processed_items,
                         "place": build.get('place'),
                         "top4": build.get('top4'),
                         "pick_rate": build.get('count') # 这里暂时用 count 代替登场率
                     })
             
                # Fallback: 如果没有获取到 builds (可能是请求失败或没有数据)，尝试使用 topItems
             if not builds and 'topItems' in unit_data:
                 top_items = unit_data['topItems']
                 # 只展示一组，作为“核心装备”
                 if len(top_items) >= 1:
                     processed_items = []
                     # 取前3个作为核心装
                     count = min(3, len(top_items))
                     for item_key in top_items[:count]:
                         # 处理 key，去除可能的前缀
                         simple_key = re.sub(r'TFT\d*_Item_', '', item_key)
                         # 尝试获取 item_info
                         item_info = self._item_map.get(simple_key) or self._item_map.get(item_key)
                         
                         if not item_info:
                             item_info = {"name": item_key, "icon": ""}
                         
                         processed_items.append(item_info)
                     
                     builds.append({
                         "items": processed_items,
                         "place": unit_data.get('place', '-'),
                         "top4": unit_data.get('top4', '-'),
                         "pick_rate": "N/A (大数据统计)"
                     })

        res = {
            "name": champion_info.get('displayName'),
            "title": champion_info.get('title'),
            "cost": champion_info.get('price'),
            # 移除 tier 字段
            "live_stats": unit_data,
            "builds": builds # 新增推荐出装组合
        }
        return res

if __name__ == "__main__":
    fetcher = TFTDataFetcher()
    print("Fetching Champions...")
    champs = fetcher.get_champion_list()
    print(f"Found {len(champs)} champions.")
    if champs:
        print(f"Sample: {champs[0].get('displayName')}")
