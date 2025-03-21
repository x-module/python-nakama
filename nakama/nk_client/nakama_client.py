# -*- coding: utf-8 -*-

from .account import Account
from nakama.interface.nakama_client_inter import WriteLeaderboardRecordResponse
from .leaderboard import Leaderboard
from .rpc import RPC
from .storage import Storage
from .users import Users
from ..common.common import Common
from nakama.interface import NakamaClientInter
from .session import Session
from nakama.nk_client.nakama_socket import NakamaSocket
from nakama.common.nakama import (
    SessionResponse, UsersResponse, FriendsResponse, FriendsRequest, LeaderboardRecordsResponse, LeaderboardRecordsRequest,
    MatchesResponse, MatchesRequest, NotificationsRequest,
    NotificationsResponse, StorageObjectsRequest, StorageObjectsResponse, ReadStorageObjectsResponse,
    ReadStorageObjectsRequest, UpdateAccountRequest, WriteLeaderboardRecordRequest,
    WriteStorageObjectsRequest, WriteStorageObjectsResponse, AccountResponse, DeleteStorageObjectsRequest
)
from ..interface.notice_handler_inter import NoticeHandlerInter


class NakamaClient(NakamaClientInter):
    def __init__(self, server: str, server_key: str, port=None) -> None:
        if port is not None:
            self._http_uri = f'{server}:{port}'
        else:
            self._http_uri = server
        self._common = Common(self._http_uri, server_key)
        self._session = Session(self._common)
        self._account = Account(self._common)
        self._users = Users(self._common)
        self._socket = NakamaSocket(self._common)
        self._rpc = RPC(self._common)
        self._storage = Storage(self._common)
        self._leaderboard = Leaderboard(self._common)

    async def logout(self):
        """结束当前会话"""
        await self.session_end()
        await self._session.logout()
        await self._common.http_session.close()

    async def token(self):
        """获取当前会话的token"""
        await self._session.refresh()
        return self._common.session.token

    async def session_start(self):
        """启动一个新的会话"""
        return await self._socket.connect_websocket()

    # self.connect_websocket()
    def send(self, data):
        return self._socket.send(data)

    async def session_end(self):
        """结束当前会话"""
        await self._socket.close()

    async def session_refresh(self, vars=None):
        """刷新当前会话"""
        return await self._session.refresh(vars=vars)

    async def session_logout(self):
        """登出当前会话"""
        return await self._session.logout()

    def session_token(self):
        """获取当前会话的令牌"""
        return self._common.session.token

    def session_refresh_token(self):
        """获取当前会话的刷新令牌"""
        return self._common.session.refresh_token

    async def account(self) -> AccountResponse:
        """获取当前用户的账户信息"""
        return await self._account.get()

    def set_notice_handler(self, handler: NoticeHandlerInter):
        self._socket.notice_handler.set_handler(handler)

    # ======================= authenticate ===========================

    async def authenticate_custom(self, id: str, create: bool = True, username: str = None, vars: None = None):
        """使用自定义 ID 进行认证"""
        return await self._account.authenticate.custom(id=id, create=create, username=username, vars=vars)

    async def authenticate_device(self, id: str, create: bool = True, username: str = True, vars: None = None) -> SessionResponse:
        """使用设备进行认证"""
        return await self._account.authenticate.device(id=id, create=create, username=username, vars=vars)

    async def authenticate_email(self, email, password: str, create: bool = True, username: str = None, vars: None = None) -> SessionResponse:
        """使用邮箱和密码进行认证"""
        return await self._account.authenticate.email(email=email, password=password, create=create, username=username, vars=vars)

    # ======================= group ===========================
    async def users(self, ids: str) -> UsersResponse:
        """根据用户 ID 列表获取用户信息"""
        return await self._users.get(ids=ids)

    async def users_usernames(self, usernames: str) -> UsersResponse:
        """根据用户名列表获取用户信息"""
        return await self._users.get(usernames=usernames)

    # ======================= link ===========================
    async def link_custom(self, id: str):
        """将自定义 ID 与当前用户关联"""
        return await self._account.account_link.custom(id=id)

    async def link_device(self, id: str):
        """将设备 ID 与当前用户关联"""
        return await self._account.account_link.device(id=id)

    async def link_email(self, email, password: str):
        """将邮箱账号与当前用户关联"""
        return await self._account.account_link.email(email=email, password=password)

    async def unlink_custom(self, id: str):
        """取消当前用户与自定义 ID 的关联"""
        return await self._account.account_unlink.custom(id=id)

    async def unlink_device(self, id: str):
        """取消当前用户与设备 ID 的关联"""
        return await self._account.account_unlink.custom(id=id)

    async def unlink_email(self, email, password: str):
        """取消当前用户与邮箱账号的关联"""
        return await self._account.account_unlink.email(email=email, password=password)

    def update_account(self, req: UpdateAccountRequest):
        """更新用户账户信息"""
        pass

    async def rpc(self, id: str, **kwargs):
        """执行远程过程调用（RPC）"""
        return await self._rpc.socket_call(id, **kwargs)

    async def client_rpc(self, id: str, **kwargs):
        """执行远程过程调用（RPC）"""
        return await self._rpc.client_call(id, **kwargs)

    async def storage_objects(self, req: StorageObjectsRequest) -> StorageObjectsResponse:
        """获取存储对象"""
        return await self._storage.list(req=req)

    async def read_storage_objects(self, req: ReadStorageObjectsRequest) -> ReadStorageObjectsResponse:
        """读取存储对象"""
        return await self._storage.read(req=req)

    async def write_storage_objects(self, req: WriteStorageObjectsRequest) -> WriteStorageObjectsResponse:
        """写入存储对象"""
        return await self._storage.write(req=req)

    async def delete_storage_objects(self, req: DeleteStorageObjectsRequest) -> WriteStorageObjectsResponse:
        """写入存储对象"""
        return await self._storage.delete(req=req)

    async def leaderboard_records(self, req: LeaderboardRecordsRequest) -> LeaderboardRecordsResponse:
        """获取排行榜记录"""
        return await self._leaderboard.get_records(req=req)

    async def write_leaderboard_record(self, req: WriteLeaderboardRecordRequest) -> WriteLeaderboardRecordResponse:
        """写入排行榜记录"""
        return await self._leaderboard.write_record(req=req)

    def notifications(self, req: NotificationsRequest) -> NotificationsResponse:
        """获取通知列表"""
        pass

    def friends(self, req: FriendsRequest) -> FriendsResponse:
        """获取好友列表"""
        pass

    def matches(self, req: MatchesRequest) -> MatchesResponse:
        """获取匹配列表"""
        pass
