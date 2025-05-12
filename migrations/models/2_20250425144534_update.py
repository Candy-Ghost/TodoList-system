from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `tasks` MODIFY COLUMN `updated` VARCHAR(200) COMMENT '更改的时间';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `tasks` MODIFY COLUMN `updated` VARCHAR(200) NOT NULL COMMENT '更改的时间';"""
