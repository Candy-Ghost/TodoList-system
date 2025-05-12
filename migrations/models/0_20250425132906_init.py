from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `tasks` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `users_id` INT NOT NULL UNIQUE,
    `title` VARCHAR(500) NOT NULL COMMENT '标题',
    `content` VARCHAR(1000) NOT NULL COMMENT '内容',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated` VARCHAR(200) NOT NULL COMMENT '更改的时间',
    `state` VARCHAR(50) NOT NULL COMMENT '状态'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(500) NOT NULL UNIQUE COMMENT '账号名',
    `password` VARCHAR(500) NOT NULL COMMENT '密码',
    `email` VARCHAR(500) NOT NULL UNIQUE COMMENT '邮件',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
