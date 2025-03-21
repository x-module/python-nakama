# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from nakama.common.nakama import (
    SessionResponse, AuthenticateGameCenterRequest, CreateGroupRequest, EventRequest,
    UsersResponse, ChannelMessagesRequest, ChannelMessagesResponse, GroupUsersRequest,
    GroupUsersResponse, UserGroupsResponse, GroupsRequest, GroupsResponse, AccountGameCenter,
    FriendsResponse, FriendsRequest, LeaderboardRecordsResponse, LeaderboardRecordsRequest,
    LeaderboardRecordsAroundOwnerRequest, MatchesResponse, MatchesRequest, NotificationsRequest,
    NotificationsResponse, StorageObjectsRequest, StorageObjectsResponse, ReadStorageObjectsResponse,
    ReadStorageObjectsRequest, UpdateAccountRequest, UpdateGroupRequest, WriteLeaderboardRecordRequest,
    WriteStorageObjectsRequest, WriteTournamentRecordRequest, WriteStorageObjectsResponse, LeaderboardRecord, AccountResponse, DeleteStorageObjectsRequest
)
from nakama.interface.notice_handler_inter import NoticeHandlerInter


class CreateGroupResponse:
    """响应类，表示创建群组操作的结果"""
    pass


class LinkGameCenterRequest(AccountGameCenter):
    """请求类，用于将 Game Center 账号与当前用户关联"""
    pass


class UnlinkGameCenterRequest(AccountGameCenter):
    """请求类，用于取消当前用户与 Game Center 账号的关联"""
    pass


class WriteLeaderboardRecordResponse(LeaderboardRecord):
    """响应类，表示写入排行榜记录操作的结果"""
    pass


class WriteTournamentRecordResponse(LeaderboardRecord):
    """响应类，表示写入锦标赛记录操作的结果"""
    pass


class NakamaClientInter(ABC):
    """Nakama 客户端的抽象接口类，定义了与 Nakama 服务器交互的方法"""

    @abstractmethod
    def logout(self):
        """抽象方法，用于用户登出"""
        pass

    @abstractmethod
    async def token(self):
        """获取当前用户的令牌"""
        pass

    # ======================= session ===========================

    @abstractmethod
    async def create_party(self, open: bool, max_size: int):
        """启动一个新的会话"""
        pass

    @abstractmethod
    async def session_start(self):
        """启动一个新的会话"""
        pass

    @abstractmethod
    async def session_end(self):
        """结束当前会话"""
        pass

    @abstractmethod
    async def session_refresh(self, vars=None):
        """刷新当前会话"""
        pass

    @abstractmethod
    def session_logout(self):
        """登出当前会话"""
        pass

    @abstractmethod
    def session_token(self):
        """获取当前会话的令牌"""
        pass

    @abstractmethod
    def session_refresh_token(self):
        """获取当前会话的刷新令牌"""
        pass

    # ======================= account ===========================

    @abstractmethod
    def account(self) -> AccountResponse:
        """获取当前用户的账户信息"""
        pass

    def set_notice_handler(self, handler: NoticeHandlerInter):
        pass

    # ======================= authenticate ===========================

    @abstractmethod
    async def authenticate_custom(self, id: str, create: bool = True, username: str = True, vars: None = None):
        """使用自定义 ID 进行认证"""
        pass

    @abstractmethod
    async def authenticate_device(self, id: str, create: bool = True, username: str = True, vars: None = None) -> SessionResponse:
        """使用设备 ID 进行认证"""
        pass

    @abstractmethod
    async def authenticate_email(self, email, password: str, create: bool = True, username: str = None, vars: None = None) -> SessionResponse:
        """使用邮箱和密码进行认证"""
        pass

    # ======================= group ===========================

    @abstractmethod
    async def users(self, ids: str) -> UsersResponse:
        """根据用户 ID 列表获取用户信息"""
        pass

    @abstractmethod
    async def users_usernames(self, usernames: str) -> UsersResponse:
        """根据用户名列表获取用户信息"""
        pass

    # ======================= link ===========================

    @abstractmethod
    async def link_custom(self, id: str):
        """将自定义 ID 与当前用户关联"""
        pass

    @abstractmethod
    async def link_device(self, id: str):
        """将设备 ID 与当前用户关联"""
        pass

    @abstractmethod
    async def link_email(self, email, password: str):
        """将邮箱账号与当前用户关联"""
        pass

    @abstractmethod
    async def unlink_custom(self, id: str):
        """取消当前用户与自定义 ID 的关联"""
        pass

    @abstractmethod
    async def unlink_device(self, id: str):
        """取消当前用户与设备 ID 的关联"""
        pass

    @abstractmethod
    async def unlink_email(self, email, password: str):
        """取消当前用户与邮箱账号的关联"""
        pass

    # ======================= friends ===========================

    @abstractmethod
    def friends(self, req: FriendsRequest) -> FriendsResponse:
        """获取好友列表"""
        pass

    @abstractmethod
    async def leaderboard_records(self, req: LeaderboardRecordsRequest) -> LeaderboardRecordsResponse:
        """获取排行榜记录"""
        pass

    @abstractmethod
    async def write_leaderboard_record(self, req: WriteLeaderboardRecordRequest) -> WriteLeaderboardRecordResponse:
        """写入排行榜记录"""
        pass

    @abstractmethod
    def matches(self, req: MatchesRequest) -> MatchesResponse:
        """获取匹配列表"""
        pass

    @abstractmethod
    def notifications(self, req: NotificationsRequest) -> NotificationsResponse:
        """获取通知列表"""
        pass

    @abstractmethod
    async def storage_objects(self, req: StorageObjectsRequest) -> StorageObjectsResponse:
        """获取存储对象"""
        pass

    @abstractmethod
    async def read_storage_objects(self, req: ReadStorageObjectsRequest) -> ReadStorageObjectsResponse:
        """读取存储对象"""
        pass

    @abstractmethod
    async def write_storage_objects(self, req: WriteStorageObjectsRequest) -> WriteStorageObjectsResponse:
        """写入存储对象"""
        pass

    @abstractmethod
    async def delete_storage_objects(self, req: DeleteStorageObjectsRequest) -> WriteStorageObjectsResponse:
        """写入存储对象"""
        pass

    @abstractmethod
    async def rpc(self, id: str, **kwargs):
        """执行远程过程调用（RPC）"""
        pass

    @abstractmethod
    async def client_rpc(self, id: str, **kwargs):
        """执行远程过程调用（RPC）"""
        pass

    @abstractmethod
    def update_account(self, req: UpdateAccountRequest):
        """更新用户账户信息"""
        pass
