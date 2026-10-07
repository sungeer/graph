import json
import sqlite3
import uuid
from datetime import datetime, timezone

DB_PATH = "agent_demo.db"


# ---------- 数据库初始化 ----------

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS checkpoints (
        run_id      TEXT PRIMARY KEY,
        step_index  INTEGER NOT NULL,
        state       TEXT NOT NULL,
        updated_at  TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS pending_approvals (
        run_id      TEXT PRIMARY KEY,
        step_index  INTEGER NOT NULL,
        payload     TEXT NOT NULL,
        status      TEXT NOT NULL DEFAULT 'pending',
        created_at  TEXT NOT NULL,
        decided_at  TEXT
    );
    CREATE TABLE IF NOT EXISTS expense_results (
        run_id      TEXT PRIMARY KEY,
        status      TEXT NOT NULL,
        reason      TEXT,
        created_at  TEXT NOT NULL
    );
    """)
    conn.commit()
    return conn


def now():
    return datetime.now(timezone.utc).isoformat()


# ---------- 检查点读写 ----------

def save_checkpoint(conn, run_id, step_index, state):
    conn.execute(
        "INSERT OR REPLACE INTO checkpoints(run_id, step_index, state, updated_at) "
        "VALUES (?,?,?,?)",
        (run_id, step_index, json.dumps(state), now())
    )
    conn.commit()


def load_checkpoint(conn, run_id):
    row = conn.execute(
        "SELECT step_index, state FROM checkpoints WHERE run_id=?", (run_id,)
    ).fetchone()
    if not row:
        return None, None
    return row[0], json.loads(row[1])


# ---------- 审批读写 ----------

def create_pending(conn, run_id, step_index, payload):
    conn.execute(
        "INSERT INTO pending_approvals(run_id, step_index, payload, status, created_at) "
        "VALUES (?,?,?,?,?)",
        (run_id, step_index, json.dumps(payload), "pending", now())
    )
    conn.commit()


def decide(conn, run_id, decision):
    conn.execute(
        "UPDATE pending_approvals SET status=?, decided_at=? WHERE run_id=?",
        (decision, now(), run_id)
    )
    conn.commit()


def get_pending(conn, run_id):
    row = conn.execute(
        "SELECT step_index, payload, status FROM pending_approvals WHERE run_id=?",
        (run_id,)
    ).fetchone()
    if not row:
        return None
    return {"step_index": row[0], "payload": json.loads(row[1]), "status": row[2]}


# ---------- Mock LLM（带调用计数，验证不重跑） ----------

LLM_CALL_COUNT = {"count": 0}


def mock_llm_review(expense):
    LLM_CALL_COUNT["count"] += 1
    print(f"  [LLM 被调用，累计 {LLM_CALL_COUNT['count']} 次]")
    issues = []
    if expense["amount"] > 5000:
        issues.append(f"金额 {expense['amount']} 超过 5000 需复核")
    return {
        "risk": "medium" if issues else "low",
        "issues": issues,
        "suggestion": "转人工复核" if issues else "可自动通过"
    }


# ---------- 副作用（mock） ----------

def execute_final_step(conn, run_id, state, decision):
    if decision == "approved":
        reason = "审批通过，打款"
    else:
        reason = "审批驳回"
    conn.execute(
        "INSERT OR REPLACE INTO expense_results(run_id, status, reason, created_at) "
        "VALUES (?,?,?,?)",
        (run_id, decision, reason, now())
    )
    conn.commit()
    print(f"  [副作用执行] run_id={run_id} 结果={decision} 原因={reason}")


# ---------- 主流程 ----------

def run_agent(conn, expense, run_id=None):
    """从头启动一次运行，遇到审批点就暂停退出。"""
    run_id = run_id or str(uuid.uuid4())
    state = {"expense": expense}
    step_index = 0

    # 步骤 0：读取报销单（已在 state 里，标记完成）
    save_checkpoint(conn, run_id, 1, state)
    print(f"步骤 0 完成：读取报销单 {expense['id']}")

    # 步骤 1：调用 LLM 审查
    review = mock_llm_review(expense)
    state["llm_review"] = review
    save_checkpoint(conn, run_id, 2, state)
    print(f"步骤 1 完成：LLM 审查结果 {review}")

    # 步骤 2：暂停，等审批
    payload = {
        "expense_id": expense["id"],
        "amount": expense["amount"],
        "review": review
    }
    create_pending(conn, run_id, 2, payload)
    print(f"步骤 2 暂停：等待审批，run_id={run_id}")
    return run_id


def resume_agent(conn, run_id):
    """审批后恢复，从检查点继续，不碰之前的步骤。"""
    step_index, state = load_checkpoint(conn, run_id)
    if state is None:
        print(f"找不到 run_id={run_id} 的检查点")
        return

    pending = get_pending(conn, run_id)
    if not pending or pending["status"] == "pending":
        print(f"run_id={run_id} 尚未审批，无法恢复")
        return

    print(f"恢复 run_id={run_id}，从步骤 {step_index} 继续")
    # step_index=2 表示步骤 2 是审批点，审批已通过，直接执行步骤 3
    execute_final_step(conn, run_id, state, pending["status"])
    print("恢复完成")


# ---------- Demo 入口 ----------

if __name__ == "__main__":
    conn = init_db()

    expense = {
        "id": "EXP-001",
        "amount": 8600,
        "category": "差旅",
        "reason": "客户现场支持",
        "invoice_text": "机票 4200，酒店 3800，餐饮 600"
    }

    print("=== 第一次运行：启动并暂停 ===")
    run_id = run_agent(conn, expense)

    print("\n=== 模拟审批人隔天处理，这里直接批准 ===")
    decide(conn, run_id, "approved")

    print("\n=== 恢复运行 ===")
    resume_agent(conn, run_id)

    print(f"\n=== 验证：LLM 总共被调用 {LLM_CALL_COUNT['count']} 次（应为 1）===")

    print("\n=== 查看最终结果 ===")
    for row in conn.execute("SELECT run_id, status, reason FROM expense_results"):
        print(row)

    conn.close()
