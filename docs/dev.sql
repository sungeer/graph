


-- 检查点表：记录每次运行已完成到哪一步
CREATE TABLE IF NOT EXISTS checkpoints (
    run_id      TEXT PRIMARY KEY,   -- 一次运行的唯一标识
    step_index  INTEGER NOT NULL,   -- 下一个待执行的步骤索引
    state       TEXT NOT NULL,      -- JSON 序列化的状态
    updated_at  TEXT NOT NULL
);



-- 待审批表：记录暂停中的审批请求
CREATE TABLE IF NOT EXISTS pending_approvals (
    run_id      TEXT PRIMARY KEY,   -- 对应一次运行
    step_index  INTEGER NOT NULL,   -- 被暂停的步骤索引
    payload     TEXT NOT NULL,      -- JSON，展示给审批人的内容
    status      TEXT NOT NULL DEFAULT 'pending',  -- pending / approved / rejected
    created_at  TEXT NOT NULL,
    decided_at  TEXT
);



-- 副作用结果表：记录最终执行结果，便于验证
CREATE TABLE IF NOT EXISTS expense_results (
    run_id      TEXT PRIMARY KEY,
    status      TEXT NOT NULL,      -- approved / rejected
    reason      TEXT,
    created_at  TEXT NOT NULL
);




