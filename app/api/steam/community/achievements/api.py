import logging
import requests
from collections import defaultdict
from xml.etree import ElementTree

from app.api.steam.consts.consts import STEAM_USER_ID


class NotXmlError(Exception):
    pass


class GetAchivementUnlockedDateApi():
    @staticmethod
    def etree_to_dict(t):
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(GetAchivementUnlockedDateApi.etree_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if t.attrib:
            d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                    d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d

    @staticmethod
    def get_achievements_unlocked_date(appid: int) -> dict:
        try:
            response = requests.get(f"https://steamcommunity.com/id/{STEAM_USER_ID}/stats/{appid}/achievements/?xml=1")
            response.raise_for_status()
            if 'text/xml' not in response.headers['content-type']:
                raise NotXmlError("Content is not XML! Steam does not support xml for this game!")
            xml_tree = ElementTree.fromstring(response.content)
            xml_dict = GetAchivementUnlockedDateApi.etree_to_dict(xml_tree)
            result: dict = {}
            achievements_dirty: dict | list[dict] = xml_dict.get("playerstats").get("achievements").get("achievement")
            achievements: list[dict]
            if type(achievements_dirty) is not list:  # if single achievement
                achievements = [achievements_dirty]
            else:
                achievements = achievements_dirty
            for achievement in achievements:
                if achievement.get("@closed") == "1":
                    result[achievement.get("apiname").upper()] = int(achievement.get("unlockTimestamp"))
            return result
        except Exception:
            logging.exception(f"Error trying to fetch Achivement Unlocked Date for Game.")
            return None
