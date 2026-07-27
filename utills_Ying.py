from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
#import os
import requests
from bs4 import BeautifulSoup


def baidu_search(query, max_results=3):
    """通过百度搜索获取相关信息，返回拼接后的文本摘要"""
    try:
        url = "https://www.baidu.com/s"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        params = {"wd": query, "rn": str(max_results)}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.encoding = "utf-8"

        soup = BeautifulSoup(resp.text, "html.parser")
        snippets = []
        # 百度搜索结果摘要通常在 class="c-abstract" 或 content 属性中
        for item in soup.select(".c-abstract, .content-right_8Zs40"):
            text = item.get_text(strip=True)
            if text:
                snippets.append(text)
        # 兜底：从 result blocks 中提取文本
        if not snippets:
            for div in soup.select(".result, .c-container"):
                text = div.get_text(" ", strip=True)
                if text and len(text) > 20:
                    snippets.append(text[:200])

        return "\n".join(snippets[:max_results]) if snippets else ""
    except Exception as e:
        print(f"[百度搜索失败] {e}")
        return ""


def generate_script(subject, video_length, creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")  # human：模拟用户发给AI的一段话
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
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