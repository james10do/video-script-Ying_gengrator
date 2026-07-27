from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
#import os
import requests
from bs4 import BeautifulSoup


def baidu_search(query):
    """用百度搜索关键词，返回搜索结果的文字摘要"""
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
        result_blocks = soup.find_all("div", class_="c-container")  # 每条搜索结果的容器

        for block in result_blocks[:3]:  # 只取前3条结果
            text = block.get_text(" ", strip=True)  # 提取纯文本，去掉多余空格
            if len(text) > 30:  # 太短的内容没用，跳过
                result_texts.append(text[:300])  # 每条截取前300字

        # 6. 把所有结果拼成一段文字返回
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