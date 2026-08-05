from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
#import os
import re  # 正则表达式库，用于文本清洗
import requests
from bs4 import BeautifulSoup


def clean_text(text):
    """清洗单条搜索结果文本，去掉无用内容，让文本更干净"""
    # 1. 去除多余空白：多个空格/换行 → 一个空格
    text = re.sub(r'\s+', ' ', text)

    # 2. 去除广告和导航类关键词所在的整条结果（直接返回空字符串）
    noise_keywords = ['广告', '推广', '百度首页', '大家都在搜', '相关搜索',
                      '登录', '注册', '设置', '帮助', '反馈']
    for kw in noise_keywords:
        if kw in text:
            return ""  # 这条是噪声，丢弃

    # 3. 去除特殊符号（只保留中文、英文、数字、常用标点）
    text = re.sub(r'[^\w\s\u4e00-\u9fff，。！？、；：""''（）().,!?;:\-]', '', text)

    # 4. 去除 URL 链接（http:// 或 https:// 开头）
    text = re.sub(r'https?://\S+', '', text)

    # 5. 再次清理空白并去除首尾空格
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def baidu_search(query):
    """用百度搜索关键词，返回搜索结果的文字摘要（已清洗）"""
    try:
        # 1. 打开百度网址，带上要搜索的关键词
        baidu_url = "https://www.baidu.com/s?wd=" + query

        # 2. 伪装成浏览器去访问（不然百度会拒绝爬虫）
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

        # 3. 发起请求，获取网页内容（最多等10秒）
        response = requests.get(baidu_url, headers=headers, timeout=10)
        response.encoding = "utf-8"  # 设置编码，防止中文乱码

        # 4. 用 BeautifulSoup 解析网页，就像用放大镜找文字
        soup = BeautifulSoup(response.text, "html.parser")

        # 5. 找到搜索结果的内容块，提取里面的文字
        result_texts = []
        seen_texts = set()  # 用于去重的集合（记录已经见过的文本）
        result_blocks = soup.find_all("div", class_="c-container")  # 每条搜索结果的容器

        for block in result_blocks[:5]:  # 取前5条结果（清洗后可能剩下3条左右）
            raw_text = block.get_text(" ", strip=True)  # 提取纯文本
            cleaned = clean_text(raw_text)  # ← 数据清洗

            # 6. 过滤：太短的、重复的、空的内容都跳过
            if len(cleaned) < 50:  # 清洗后太短的跳过
                continue
            if cleaned in seen_texts:  # 重复内容跳过
                continue

            seen_texts.add(cleaned)  # 记录已见过的文本
            result_texts.append(cleaned[:300])  # 每条截取前300字

        # 7. 把所有结果拼成一段文字返回
        return "\n\n".join(result_texts)

    except Exception as e:
        print("百度搜索出错了：", e)
        return ""


def generate_script(subject, video_length, creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")  # human：模拟用户发给AI的一段话
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("system",
            #这是多行字符串，不是注释！
            # """ 包裹的内容是 赋值给 ChatPromptTemplate.from_messages() 的参数，会被 Python 处理并传递给 AI
             """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下百度搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{baidu_search}```""")
        ]
    )

    model = ChatOpenAI(
        openai_api_key=api_key,
        temperature=creativity,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen-plus"
    )

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content
    
    search_result = baidu_search(subject)  

    script = script_chain.invoke({"title": title, "duration": video_length,
                                  "baidu_search": search_result}).content

    return search_result, title, script

#print(generate_script("sora模型", 1, 0.7, os.getenv("DASHSCOPE_API_KEY")))