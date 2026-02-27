#!/usr/bin/env python3
"""
数据标注工具健康检查脚本
功能：
1. 检查所有链接的有效性
2. 检查 GitHub 仓库的健康状态（Stars、最后更新、版本、协议等）
3. 生成详细的 HTML 和 Markdown 报告
"""

import re
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import time
import argparse

# 配置
GITHUB_TOKEN = None  # 可选：设置 GitHub Token 提高 API 限制
TIMEOUT = 10
MAX_WORKERS = 10  # 并发线程数
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'


def extract_all_links(file_path: str) -> List[Tuple[str, str]]:
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
        # 跳过本地文件链接
        if not url.startswith(('http://', 'https://')):
            continue
        links.append((text, url))
    
    return links


def extract_github_repos(file_path: str) -> List[Tuple[str, str]]:
    """
    从 Markdown 文件中提取 GitHub 仓库链接
    返回: [(工具名称, GitHub URL), ...]
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    repos = []
    # 匹配表格行中的 GitHub 链接
    pattern = r'\|\s*([^|]+?)\s*\|\s*\[([^\]]+)\]\((https://github\.com/[^)]+)\)'
    matches = re.findall(pattern, content)
    
    for match in matches:
        tool_name = match[0].strip()
        url = match[2].strip()
        repos.append((tool_name, url))
    
    return repos


def normalize_url(url: str) -> str:
    """标准化 URL"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url


def check_url(url: str, text: str) -> Dict:
    """
    检查单个 URL 是否有效
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
        future_to_link = {
            executor.submit(check_url, url, text): (text, url)
            for text, url in links
        }
        
        for i, future in enumerate(as_completed(future_to_link), 1):
            result = future.result()
            results.append(result)
            
            status_symbol = {
                'success': f'{Colors.GREEN}✓{Colors.END}',
                'warning': f'{Colors.YELLOW}⚠{Colors.END}',
                'error': f'{Colors.RED}✗{Colors.END}'
            }
            
            print(f"[{i}/{len(links)}] {status_symbol[result['status']]} {result['url']}")
    
    return results


def check_github_repo(owner: str, repo: str) -> Dict:
    """检查 GitHub 仓库状态"""
    headers = {'User-Agent': USER_AGENT}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    
    try:
        # 获取仓库基本信息
        api_url = f'https://api.github.com/repos/{owner}/{repo}'
        response = requests.get(api_url, headers=headers, timeout=TIMEOUT)
        
        if response.status_code == 404:
            return {'status': 'not_found', 'message': '仓库不存在或已删除'}
        elif response.status_code == 403:
            return {'status': 'rate_limit', 'message': 'API 限制，请设置 GITHUB_TOKEN'}
        elif response.status_code != 200:
            return {'status': 'error', 'message': f'HTTP {response.status_code}'}
        
        data = response.json()
        
        # 检查是否归档
        if data.get('archived'):
            return {'status': 'archived', 'message': '仓库已归档'}
        
        # 获取最后提交时间
        last_push = datetime.strptime(data['pushed_at'], '%Y-%m-%dT%H:%M:%SZ')
        days_since_update = (datetime.now() - last_push).days
        
        # 获取最新 release
        release_url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
        release_response = requests.get(release_url, headers=headers, timeout=TIMEOUT)
        latest_release = None
        if release_response.status_code == 200:
            release_data = release_response.json()
            latest_release = release_data.get('tag_name')
        
        return {
            'status': 'active' if days_since_update < 180 else 'inactive',
            'stars': data.get('stargazers_count', 0),
            'forks': data.get('forks_count', 0),
            'license': data.get('license', {}).get('spdx_id', 'Unknown'),
            'last_push': last_push.strftime('%Y-%m-%d'),
            'days_since_update': days_since_update,
            'latest_release': latest_release,
            'message': 'OK'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def check_github_repos(repos: List[Tuple[str, str]]) -> List[Dict]:
    """检查所有 GitHub 仓库"""
    results = []
    
    for i, (name, url) in enumerate(repos, 1):
        # 解析 owner/repo
        match = re.match(r'https://github\.com/([^/]+)/([^/]+)', url)
        if not match:
            continue
        
        owner, repo = match.groups()
        print(f"[{i}/{len(repos)}] 检查 {name} ({owner}/{repo})...")
        
        result = check_github_repo(owner, repo)
        result['name'] = name
        result['url'] = url
        results.append(result)
        
        # 显示状态
        if result['status'] == 'active':
            print(f"  {Colors.GREEN}✓ 活跃{Colors.END} - {result.get('stars', 0)} stars, 最后更新: {result.get('last_push')}")
        elif result['status'] == 'inactive':
            print(f"  {Colors.YELLOW}⚠ 不活跃{Colors.END} - {result['days_since_update']} 天未更新")
        elif result['status'] == 'archived':
            print(f"  {Colors.RED}✗ 已归档{Colors.END}")
        else:
            print(f"  {Colors.RED}✗ {result['message']}{Colors.END}")
        
        time.sleep(0.5)  # 避免 API 限制
    
    return results


def generate_link_report_md(results: List[Dict], filename: str):
    """生成链接检查的 Markdown 报告"""
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
        
        if error_count > 0:
            f.write("## ❌ 失败的链接\n\n")
            for r in results:
                if r['status'] == 'error':
                    f.write(f"- [{r['text']}]({normalize_url(r['url'])}) - {r['message']}\n")
            f.write("\n")
        
        if warning_count > 0:
            f.write("## ⚠️ 警告的链接\n\n")
            for r in results:
                if r['status'] == 'warning':
                    f.write(f"- [{r['text']}]({normalize_url(r['url'])}) - {r['message']}\n")
            f.write("\n")
        
        if success_count > 0:
            f.write("## ✅ 成功的链接\n\n")
            for r in results:
                if r['status'] == 'success':
                    f.write(f"- [{r['text']}]({normalize_url(r['url'])}) - {r['message']}\n")
            f.write("\n")


def generate_html_report(link_results: List[Dict], repo_results: List[Dict], output_file: str):
    """生成综合 HTML 报告"""
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据标注工具健康检查报告</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ color: #333; margin-bottom: 10px; }}
        .timestamp {{ color: #666; margin-bottom: 30px; }}
        .section {{ background: white; padding: 25px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .summary-item {{ padding: 15px; border-radius: 6px; text-align: center; }}
        .summary-item h3 {{ margin: 0 0 10px 0; font-size: 14px; color: #666; }}
        .summary-item .number {{ font-size: 32px; font-weight: bold; margin: 0; }}
        .success {{ background: #d4edda; color: #155724; }}
        .warning {{ background: #fff3cd; color: #856404; }}
        .danger {{ background: #f8d7da; color: #721c24; }}
        .info {{ background: #d1ecf1; color: #0c5460; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #4CAF50; color: white; position: sticky; top: 0; }}
        tr:hover {{ background: #f5f5f5; }}
        .status-badge {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
        .badge-active {{ background: #28a745; color: white; }}
        .badge-inactive {{ background: #ffc107; color: #333; }}
        .badge-archived {{ background: #dc3545; color: white; }}
        .badge-error {{ background: #6c757d; color: white; }}
        .badge-success {{ background: #28a745; color: white; }}
        .badge-warning {{ background: #ffc107; color: #333; }}
        a {{ color: #007bff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 数据标注工具健康检查报告</h1>
        <p class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="section">
            <h2>📈 链接检查统计</h2>
            <div class="summary">
                <div class="summary-item success">
                    <h3>✅ 成功</h3>
                    <p class="number">{sum(1 for r in link_results if r.get('status') == 'success')}</p>
                </div>
                <div class="summary-item warning">
                    <h3>⚠️ 警告</h3>
                    <p class="number">{sum(1 for r in link_results if r.get('status') == 'warning')}</p>
                </div>
                <div class="summary-item danger">
                    <h3>❌ 失败</h3>
                    <p class="number">{sum(1 for r in link_results if r.get('status') == 'error')}</p>
                </div>
                <div class="summary-item info">
                    <h3>📊 总计</h3>
                    <p class="number">{len(link_results)}</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔧 GitHub 仓库健康状态</h2>
            <div class="summary">
                <div class="summary-item success">
                    <h3>✅ 活跃</h3>
                    <p class="number">{sum(1 for r in repo_results if r.get('status') == 'active')}</p>
                </div>
                <div class="summary-item warning">
                    <h3>⚠️ 不活跃</h3>
                    <p class="number">{sum(1 for r in repo_results if r.get('status') == 'inactive')}</p>
                </div>
                <div class="summary-item danger">
                    <h3>🔴 归档</h3>
                    <p class="number">{sum(1 for r in repo_results if r.get('status') == 'archived')}</p>
                </div>
                <div class="summary-item danger">
                    <h3>❌ 错误</h3>
                    <p class="number">{sum(1 for r in repo_results if r.get('status') in ['not_found', 'error'])}</p>
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>工具名称</th>
                        <th>状态</th>
                        <th>⭐ Stars</th>
                        <th>🍴 Forks</th>
                        <th>📅 最后更新</th>
                        <th>🏷️ 最新版本</th>
                        <th>📜 协议</th>
                        <th>说明</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for result in repo_results:
        status_map = {
            'active': 'badge-active',
            'inactive': 'badge-inactive',
            'archived': 'badge-archived',
            'not_found': 'badge-error',
            'error': 'badge-error'
        }
        badge_class = status_map.get(result['status'], 'badge-error')
        
        html += f"""                    <tr>
                        <td><a href="{result['url']}" target="_blank">{result['name']}</a></td>
                        <td><span class="status-badge {badge_class}">{result['status'].upper()}</span></td>
                        <td>{result.get('stars', 'N/A')}</td>
                        <td>{result.get('forks', 'N/A')}</td>
                        <td>{result.get('last_push', 'N/A')}</td>
                        <td>{result.get('latest_release', 'N/A')}</td>
                        <td>{result.get('license', 'N/A')}</td>
                        <td>{result.get('message', '')}</td>
                    </tr>
"""
    
    html += """                </tbody>
            </table>
        </div>
"""
    
    # 添加失败的链接表格
    failed_links = [r for r in link_results if r['status'] == 'error']
    if failed_links:
        html += """
        <div class="section">
            <h2>❌ 失败的链接</h2>
            <table>
                <thead>
                    <tr>
                        <th>链接文本</th>
                        <th>URL</th>
                        <th>错误信息</th>
                    </tr>
                </thead>
                <tbody>
"""
        for link in failed_links:
            html += f"""                    <tr>
                        <td>{link['text']}</td>
                        <td><a href="{normalize_url(link['url'])}" target="_blank">{link['url']}</a></td>
                        <td>{link['message']}</td>
                    </tr>
"""
        html += """                </tbody>
            </table>
        </div>
"""
    
    html += """    </div>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser(description='数据标注工具健康检查脚本')
    parser.add_argument('--links-only', action='store_true', help='仅检查链接有效性')
    parser.add_argument('--repos-only', action='store_true', help='仅检查 GitHub 仓库状态')
    parser.add_argument('--input', default='README.md', help='输入的 Markdown 文件 (默认: README.md)')
    parser.add_argument('--token', help='GitHub API Token (可选，用于提高 API 限制)')
    
    args = parser.parse_args()
    
    if args.token:
        global GITHUB_TOKEN
        GITHUB_TOKEN = args.token
    
    link_results = []
    repo_results = []
    
    # 检查链接
    if not args.repos_only:
        print(f"{Colors.CYAN}{'='*80}{Colors.END}")
        print(f"{Colors.CYAN}开始检查链接有效性...{Colors.END}")
        print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")
        
        links = extract_all_links(args.input)
        print(f"找到 {len(links)} 个链接\n")
        
        # 去重
        unique_links = list(set(links))
        if len(unique_links) < len(links):
            print(f"去重后: {len(unique_links)} 个唯一链接\n")
        
        link_results = check_links_parallel(unique_links)
        
        # 生成链接报告
        generate_link_report_md(link_results, 'link_check_report.md')
        print(f"\n{Colors.GREEN}✓ 链接检查报告已保存: link_check_report.md{Colors.END}\n")
    
    # 检查 GitHub 仓库
    if not args.links_only:
        print(f"{Colors.CYAN}{'='*80}{Colors.END}")
        print(f"{Colors.CYAN}开始检查 GitHub 仓库状态...{Colors.END}")
        print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")
        
        repos = extract_github_repos(args.input)
        print(f"找到 {len(repos)} 个 GitHub 仓库\n")
        
        repo_results = check_github_repos(repos)
        
        # 显示警告
        warnings = [r for r in repo_results if r['status'] in ['inactive', 'archived', 'not_found', 'error']]
        if warnings:
            print(f"\n{Colors.YELLOW}⚠️ 发现 {len(warnings)} 个需要关注的工具：{Colors.END}")
            for w in warnings:
                print(f"  - {w['name']}: {w['status']} - {w.get('message', '')}")
    
    # 生成综合 HTML 报告
    if link_results or repo_results:
        generate_html_report(link_results, repo_results, 'health_report.html')
        print(f"\n{Colors.GREEN}✓ 综合健康报告已生成: health_report.html{Colors.END}")
    
    # 返回退出码
    error_count = sum(1 for r in link_results if r['status'] == 'error')
    error_count += sum(1 for r in repo_results if r['status'] in ['not_found', 'error'])
    
    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    exit(main())
