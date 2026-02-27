#!/usr/bin/env python3
"""
链接校验脚本
自动检查 README.md 中的所有超链接是否有效
"""

import re
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict
import time

# 配置
TIMEOUT = 10  # 请求超时时间（秒）
MAX_WORKERS = 10  # 并发线程数
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def extract_links_from_markdown(file_path: str) -> List[Tuple[str, str]]:
    """
    从 Markdown 文件中提取所有链接
    返回: [(链接文本, URL), ...]
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 Markdown 链接格式: [text](url)
    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    matches = re.findall(pattern, content)
    
    # 过滤掉锚点链接和本地文件链接
    links = []
    for text, url in matches:
        # 跳过锚点链接
        if url.startswith('#'):
            continue
        # 跳过本地文件链接（不以 http:// 或 https:// 开头的相对路径）
        if not url.startswith(('http://', 'https://')):
            continue
        links.append((text, url))
    
    return links


def normalize_url(url: str) -> str:
    """标准化 URL"""
    # 如果没有协议，添加 https://
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url


def check_url(url: str, text: str) -> Dict:
    """
    检查单个 URL 是否有效
    返回: {
        'url': str,
        'text': str,
        'status': 'success' | 'error' | 'warning',
        'status_code': int | None,
        'message': str
    }
    """
    normalized_url = normalize_url(url)
    
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    try:
        response = requests.head(
            normalized_url,
            headers=headers,
            timeout=TIMEOUT,
            allow_redirects=True
        )
        
        # 如果 HEAD 请求失败，尝试 GET 请求
        if response.status_code >= 400:
            response = requests.get(
                normalized_url,
                headers=headers,
                timeout=TIMEOUT,
                allow_redirects=True
            )
        
        status_code = response.status_code
        
        if status_code == 200:
            return {
                'url': url,
                'text': text,
                'status': 'success',
                'status_code': status_code,
                'message': 'OK'
            }
        elif 300 <= status_code < 400:
            return {
                'url': url,
                'text': text,
                'status': 'warning',
                'status_code': status_code,
                'message': f'重定向到: {response.url}'
            }
        else:
            return {
                'url': url,
                'text': text,
                'status': 'error',
                'status_code': status_code,
                'message': f'HTTP {status_code}'
            }
            
    except requests.exceptions.Timeout:
        return {
            'url': url,
            'text': text,
            'status': 'error',
            'status_code': None,
            'message': '请求超时'
        }
    except requests.exceptions.ConnectionError:
        return {
            'url': url,
            'text': text,
            'status': 'error',
            'status_code': None,
            'message': '连接失败'
        }
    except requests.exceptions.TooManyRedirects:
        return {
            'url': url,
            'text': text,
            'status': 'error',
            'status_code': None,
            'message': '重定向次数过多'
        }
    except Exception as e:
        return {
            'url': url,
            'text': text,
            'status': 'error',
            'status_code': None,
            'message': f'错误: {str(e)}'
        }


def check_links_parallel(links: List[Tuple[str, str]]) -> List[Dict]:
    """并行检查所有链接"""
    results = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务
        future_to_link = {
            executor.submit(check_url, url, text): (text, url)
            for text, url in links
        }
        
        # 获取结果
        for i, future in enumerate(as_completed(future_to_link), 1):
            result = future.result()
            results.append(result)
            
            # 实时显示进度
            status_symbol = {
                'success': f'{Colors.GREEN}✓{Colors.END}',
                'warning': f'{Colors.YELLOW}⚠{Colors.END}',
                'error': f'{Colors.RED}✗{Colors.END}'
            }
            
            print(f"[{i}/{len(links)}] {status_symbol[result['status']]} {result['url']}")
    
    return results


def generate_report(results: List[Dict]) -> str:
    """生成检查报告"""
    success_count = sum(1 for r in results if r['status'] == 'success')
    warning_count = sum(1 for r in results if r['status'] == 'warning')
    error_count = sum(1 for r in results if r['status'] == 'error')
    
    report = []
    report.append("=" * 80)
    report.append("链接校验报告")
    report.append("=" * 80)
    report.append(f"\n总计: {len(results)} 个链接")
    report.append(f"{Colors.GREEN}✓ 成功: {success_count}{Colors.END}")
    report.append(f"{Colors.YELLOW}⚠ 警告: {warning_count}{Colors.END}")
    report.append(f"{Colors.RED}✗ 失败: {error_count}{Colors.END}")
    report.append("")
    
    # 成功的链接
    if success_count > 0:
        report.append(f"\n{Colors.GREEN}{'=' * 80}")
        report.append(f"成功的链接 ({success_count})")
        report.append(f"{'=' * 80}{Colors.END}")
        for r in results:
            if r['status'] == 'success':
                report.append(f"✓ [{r['text']}]({r['url']}) - {r['message']}")
    
    # 警告的链接
    if warning_count > 0:
        report.append(f"\n{Colors.YELLOW}{'=' * 80}")
        report.append(f"警告的链接 ({warning_count})")
        report.append(f"{'=' * 80}{Colors.END}")
        for r in results:
            if r['status'] == 'warning':
                report.append(f"⚠ [{r['text']}]({r['url']}) - {r['message']}")
    
    # 失败的链接
    if error_count > 0:
        report.append(f"\n{Colors.RED}{'=' * 80}")
        report.append(f"失败的链接 ({error_count})")
        report.append(f"{'=' * 80}{Colors.END}")
        for r in results:
            if r['status'] == 'error':
                report.append(f"✗ [{r['text']}]({r['url']}) - {r['message']}")
    
    report.append("\n" + "=" * 80)
    
    return "\n".join(report)


def save_report_to_file(results: List[Dict], filename: str = 'link_check_report.md'):
    """保存报告到文件"""
    success_count = sum(1 for r in results if r['status'] == 'success')
    warning_count = sum(1 for r in results if r['status'] == 'warning')
    error_count = sum(1 for r in results if r['status'] == 'error')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# 链接校验报告\n\n")
        f.write(f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 统计\n\n")
        f.write(f"- 总计: {len(results)} 个链接\n")
        f.write(f"- ✅ 成功: {success_count}\n")
        f.write(f"- ⚠️ 警告: {warning_count}\n")
        f.write(f"- ❌ 失败: {error_count}\n\n")
        
        if success_count > 0:
            f.write("## ✅ 成功的链接\n\n")
            for r in results:
                if r['status'] == 'success':
                    f.write(f"- [{r['text']}]({normalize_url(r['url'])}) - {r['message']}\n")
            f.write("\n")
        
        if warning_count > 0:
            f.write("## ⚠️ 警告的链接\n\n")
            for r in results:
                if r['status'] == 'warning':
                    f.write(f"- [{r['text']}]({normalize_url(r['url'])}) - {r['message']}\n")
            f.write("\n")
        
        if error_count > 0:
            f.write("## ❌ 失败的链接\n\n")
            for r in results:
                if r['status'] == 'error':
                    f.write(f"- [{r['text']}]({normalize_url(r['url'])}) - {r['message']}\n")
            f.write("\n")
    
    print(f"\n报告已保存到: {filename}")


def main():
    """主函数"""
    print(f"{Colors.BLUE}开始检查 README.md 中的链接...{Colors.END}\n")
    
    # 提取链接
    links = extract_links_from_markdown('README.md')
    print(f"找到 {len(links)} 个链接\n")
    
    # 去重
    unique_links = list(set(links))
    if len(unique_links) < len(links):
        print(f"去重后: {len(unique_links)} 个唯一链接\n")
    
    # 检查链接
    print("开始检查链接...\n")
    results = check_links_parallel(unique_links)
    
    # 生成并显示报告
    print("\n")
    report = generate_report(results)
    print(report)
    
    # 保存报告到文件
    save_report_to_file(results)
    
    # 返回退出码
    error_count = sum(1 for r in results if r['status'] == 'error')
    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    exit(main())
