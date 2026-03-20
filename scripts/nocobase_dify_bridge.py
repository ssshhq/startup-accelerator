"""
NocoBase + Dify 集成脚本
功能：从 NocoBase 获取待评估的创业项目 → 调用 Dify AI 评估 → 将报告写回 NocoBase
"""
import os
import requests
import json
import time
from datetime import datetime

# ============================================================
# 配置区域 - 请修改为你自己的信息
# ============================================================

# NocoBase 配置
NOCOBASE_URL = os.getenv("NOCOBASE_URL", "http://localhost:13000/api")
NOCOBASE_TOKEN = os.getenv("NOCOBASE_TOKEN", "在这里填你的Token")

PROJECT_TABLE = os.getenv("PROJECT_TABLE", "startup_projects")
REPORT_TABLE = os.getenv("REPORT_TABLE", "evaluation_reports")

DIFY_API_URL = os.getenv("DIFY_API_URL", "https://api.dify.ai/v1/workflows/run")
DIFY_API_KEY = os.getenv("DIFY_API_KEY", "在这里填你的Dify Key")

# ============================================================
# NocoBase API 操作函数
# ============================================================

def nocobase_headers():
    """返回 NocoBase 请求头"""
    return {
        "Authorization": f"Bearer {NOCOBASE_TOKEN}",
        "Content-Type": "application/json"
    }


def get_pending_projects():
    """从 NocoBase 获取所有状态为'待评估'的创业项目"""
    try:
        url = f"{NOCOBASE_URL}/{PROJECT_TABLE}:list"
        params = {
            "filter": json.dumps({"status": "待评估"})
        }
        response = requests.get(url, headers=nocobase_headers(), params=params)
        response.raise_for_status()
        data = response.json()

        # NocoBase 返回格式可能是 {"data": [...]} 或 {"data": {"data": [...]}}
        if isinstance(data.get("data"), list):
            projects = data["data"]
        elif isinstance(data.get("data"), dict):
            projects = data["data"].get("data", [])
        else:
            projects = []

        print(f"📋 找到 {len(projects)} 个待评估项目")
        return projects
    except Exception as e:
        print(f"❌ 获取项目列表失败：{e}")
        return []


def update_project_status(project_id, status):
    """更新项目的评估状态"""
    try:
        url = f"{NOCOBASE_URL}/{PROJECT_TABLE}:update"
        params = {"filterByTk": project_id}
        payload = {"status": status}
        response = requests.post(url, headers=nocobase_headers(),
                                 params=params, json=payload)
        response.raise_for_status()
        print(f"   ✅ 项目 {project_id} 状态更新为：{status}")
    except Exception as e:
        print(f"   ❌ 更新项目状态失败：{e}")


def save_report_to_nocobase(project_id, report_data):
    """将 AI 评估报告保存到 NocoBase 的评估报告表"""
    try:
        url = f"{NOCOBASE_URL}/{REPORT_TABLE}:create"

        payload = {
            "ai_report": str(report_data.get("report", ""))[:10000],
            "policy_match": str(report_data.get("policy_match", "")),
            "risk_level": str(report_data.get("risk_level", "C")),
            "benchmark_companies": str(report_data.get("benchmark_companies", ""))
        }

        try:
            payload["unicorn_score"] = int(report_data.get("unicorn_score", 25))
        except (ValueError, TypeError):
            payload["unicorn_score"] = 25

        payload["generated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        print(f"   📝 正在保存报告...")
        print(f"   📝 请求URL：{url}")
        print(f"   📝 字段列表：{list(payload.keys())}")

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {NOCOBASE_TOKEN}",
                "Content-Type": "application/json; charset=utf-8"
            },
            json=payload
        )

        print(f"   📝 响应状态码：{response.status_code}")
        print(f"   📝 响应内容：{response.text[:1000]}")

        if response.status_code == 200:
            print(f"   ✅ 评估报告已保存到 NocoBase")
        else:
            print(f"   ❌ 保存失败！")

    except Exception as e:
        print(f"   ❌ 保存报告异常：{e}")


# ============================================================
# Dify API 调用函数
# ============================================================

def call_dify_workflow(project):
    """调用 Dify Workflow API 进行 AI 评估（流式模式避免超时）"""
    try:
        headers = {
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json; charset=utf-8"
        }

        payload = {
            "inputs": {
                "project_name": str(project.get("project_name", "未知项目")),
                "project_stage": str(project.get("project_stage", "种子期")),
                "industry": str(project.get("industry", "其他")),
                "target_users": str(project.get("target_users", "")),
                "application_scenario": str(project.get("application_scenario", "")),
                "core_technology": str(project.get("core_technology", "")),
                "main_products": str(project.get("main_products", "")),
                "founder_name": str(project.get("founder_name", "未提供"))
            },
            "response_mode": "streaming",
            "user": "nocobase-integration"
        }

        print(f"   🤖 正在调用 Dify AI 进行评估（流式模式）...")

        response = requests.post(
            DIFY_API_URL,
            headers=headers,
            json=payload,
            timeout=300,
            stream=True
        )
        response.raise_for_status()

        # 收集流式返回的所有内容
        report_text = ""
        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8")
                if line_str.startswith("data: "):
                    try:
                        data = json.loads(line_str[6:])
                        event = data.get("event", "")

                        if event == "text_chunk":
                            chunk = data.get("data", {}).get("text", "")
                            report_text += chunk

                        elif event == "workflow_finished":
                            outputs = data.get("data", {}).get("outputs", {})
                            if outputs:
                                report_text = outputs.get("evaluation_report",
                                                          outputs.get("text", report_text))
                            print(f"   ✅ Dify AI 评估完成")

                        elif event == "node_finished":
                            node_title = data.get("data", {}).get("title", "")
                            if node_title:
                                print(f"   📍 节点完成：{node_title}")

                    except json.JSONDecodeError:
                        pass

        if not report_text:
            print(f"   ⚠️ 未获取到报告内容")
            return None

        return {
            "report": report_text,
            "policy_match": "详见完整报告",
            "risk_level": "C",
            "unicorn_score": 25,
            "benchmark_companies": "详见完整报告"
        }

    except requests.exceptions.Timeout:
        print(f"   ⏱️ 请求超时（5分钟），Dify 处理时间过长")
        return None
    except Exception as e:
        print(f"   ❌ Dify API 调用失败：{e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   响应内容：{e.response.text[:500]}")
        return None


# ============================================================
# 主流程
# ============================================================

def process_all_pending():
    """处理所有待评估项目的主流程"""
    print("\n" + "=" * 60)
    print(f"🚀 开始处理待评估项目... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 第1步：从 NocoBase 获取待评估项目
    projects = get_pending_projects()

    if not projects:
        print("💤 没有待评估的项目")
        return

    # 第2步：逐个处理
    for i, project in enumerate(projects, 1):
        project_id = project.get("id")
        project_name = project.get("project_name", "未知项目")

        print(f"\n--- [{i}/{len(projects)}] 处理项目：{project_name} (ID: {project_id}) ---")

        # 2.1 更新状态为"评估中"
        update_project_status(project_id, "评估中")

        # 2.2 调用 Dify 进行 AI 评估
        report_data = call_dify_workflow(project)

        if report_data:
            # 2.3 将报告保存到 NocoBase
            save_report_to_nocobase(project_id, report_data)

            # 2.4 更新项目状态为"已完成"
            update_project_status(project_id, "已完成")
        else:
            # 评估失败，状态改回"待评估"
            update_project_status(project_id, "待评估")
            print(f"   ⚠️ 项目 {project_name} 评估失败，已恢复为待评估状态")

        # 每个项目间隔2秒，避免频率过高
        if i < len(projects):
            time.sleep(2)

    print(f"\n✅ 所有项目处理完毕！")


def run_loop(interval=30):
    """循环运行模式：每隔 interval 秒检查一次新项目"""
    print("🔄 启动循环监控模式...")
    print(f"   每 {interval} 秒检查一次待评估项目")
    print("   按 Ctrl+C 停止\n")

    try:
        while True:
            process_all_pending()
            print(f"\n⏳ 等待 {interval} 秒后再次检查...")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n🛑 已停止监控")


# ============================================================
# 运行入口
# ============================================================




if __name__ == "__main__":
    print("=" * 60)
    print("  NocoBase + Dify 集成桥接脚本")
    print("  创业加速器 AI 评估系统")
    print("=" * 60)
    print("\n请选择运行模式：")
    print("  1. 处理一次当前所有待评估项目")
    print("  2. 循环监控模式（持续运行）")

    choice = input("\n请输入选择（1 或 2）：").strip()

    if choice == "2":
        run_loop(interval=30)
    else:
        process_all_pending()