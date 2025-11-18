# 这份代码是基于baidu_sy_img.py的，但是修改了一些参数。
# 比如随机选择一页的结果，以及使用hash命名图片文件，避免重复下载。


import requests
import re
import os
import random
import hashlib
from urllib.parse import unquote

# 使用现代的请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 百度图片搜索的API地址
url = 'https://image.baidu.com/search/acjson'


def get_html(word, headers):
    """获取随机一页的搜索结果页面"""
    # 构造适用于新API的参数
    data = {
        'tn': 'resultjson_com',
        'ipn': 'rj',
        'ct': '201326592',
        'is': '',
        'fp': 'result',
        'queryWord': word,
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid': '',
        'st': '-1',
        'z': '',
        'ic': '0',
        'hd': '',
        'latest': '',
        'copyright': '',
        'word': word,
        's': '',
        'se': '',
        'tab': '',
        'width': '',
        'height': '',
        'face': '0',
        'istype': '2',
        'qc': '',
        'nc': '1',
        'fr': '',
        'pn': random.randint(1, 30) * 30,  # 随机选择一页 (结果从30到900之间)
        'rn': 30,  # 每页返回30条结果
        'gsm': '1e',
    }

    print(f"正在使用关键词: '{word}' (随机页) 进行搜索...")
    response = requests.get(url, params=data, headers=headers)
    response.raise_for_status()  # 如果请求失败则抛出异常
    page = response.text
    print("--- 成功获取百度返回数据 ---")
    return page


def get_img(page, headers):
    """从页面中解析并下载图片，使用hash命名以防重复"""
    save_dir = 'images'
    os.makedirs(save_dir, exist_ok=True)
    print(f"图片将保存在 '{save_dir}' 文件夹中。")

    reg = re.compile('"middleURL":"(.*?)"')
    img_urls = re.findall(reg, page)
    print(f"成功解析出 {len(img_urls)} 个图片链接。")

    if not img_urls:
        print("在返回的数据中未找到图片链接，可能是接口规则已更新。")
        return

    download_count = 0
    for img_url in img_urls:
        try:
            decoded_url = unquote(img_url)
            if not decoded_url:
                print("发现空的图片链接，跳过。")
                continue

            # 使用URL的MD5哈希值作为文件名，避免重复和覆盖
            file_hash = hashlib.md5(decoded_url.encode()).hexdigest()
            filepath = os.path.join(save_dir, f'{file_hash}.jpg')

            if os.path.exists(filepath):
                print(f"图片已存在，跳过: {filepath}")
                continue

            print(f"正在下载: {decoded_url} ...")
            response = requests.get(decoded_url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()

            content_type = response.headers.get('content-type')
            if not content_type or not content_type.startswith('image'):
                print(f"链接非图片格式，跳过: {decoded_url}")
                continue

            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"成功保存图片至: {filepath}")
            download_count += 1
        except requests.exceptions.RequestException as e:
            print(f"下载失败: {decoded_url}. 错误: {e}")
        except Exception as e:
            print(f"处理链接时发生未知错误: {decoded_url}. 错误: {e}")

    print(f"\n本次运行新下载了 {download_count} 张图片。")


if __name__ == '__main__':
    # 定义一个搜索关键词列表，可以按需修改或扩充
    search_terms = ['风景', '城市夜景', '科技', '自然风光', '小猫', '跑车', '星空', '海洋', '森林','美女']
    # 随机选择一个关键词
    search_term = random.choice(search_terms)

    try:
        html_page = get_html(search_term, headers)
        get_img(html_page, headers)
    except requests.exceptions.RequestException as e:
        print(f"无法从百度获取搜索结果. 错误: {e}")
    except Exception as e:
        print(f"程序运行出错: {e}")