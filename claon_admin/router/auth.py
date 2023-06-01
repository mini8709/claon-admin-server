from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response
from fastapi_utils.cbv import cbv

from claon_admin.common.annotated import Session, CurrentUser
from claon_admin.common.util import header
from claon_admin.container import Container
from claon_admin.model.center import CenterAuthRequestDto, CenterResponseDto
from claon_admin.common.enum import OAuthProvider
from claon_admin.model.user import SignInRequestDto, LectorRequestDto, JwtResponseDto, \
    IsDuplicatedNicknameResponseDto, LectorResponseDto
from claon_admin.service.user import UserService

router = APIRouter()


@cbv(router)
class AuthRouter:
    @inject
    def __init__(self,
                 user_service: UserService = Depends(Provide[Container.user_service])):
        self.user_service = user_service

    # TODO: Need to be removed later
    @router.post('/test-sign-in', response_model=JwtResponseDto)
    async def test_sign_in(self,
                           session: Session,
                           dto: SignInRequestDto):
        return await self.user_service.test_sign_in(session, dto)

    @router.post('/{provider}/sign-in', response_model=JwtResponseDto)
    async def sign_in(self,
                      session: Session,
                      response: Response,
                      provider: OAuthProvider,
                      dto: SignInRequestDto):
        jwt_dto: JwtResponseDto = await self.user_service.sign_in(session, provider, dto)
        header.add_jwt_tokens(response, jwt_dto.access_token, jwt_dto.refresh_token)
        return jwt_dto

    @router.post('/center/sign-up', response_model=CenterResponseDto)
    async def center_sign_up(self,
                             session: Session,
                             subject: CurrentUser,
                             dto: CenterAuthRequestDto):
        return await self.user_service.sign_up_center(session, subject, dto)

    @router.post('/lector/sign-up', response_model=LectorResponseDto)
    async def lector_sign_up(self,
                             session: Session,
                             subject: CurrentUser,
                             dto: LectorRequestDto):
        return await self.user_service.sign_up_lector(session, subject, dto)

    @router.get('/nickname/{nickname}/is-duplicated', response_model=IsDuplicatedNicknameResponseDto)
    async def is_duplicated_nickname(self,
                                     session: Session,
                                     nickname: str):
        return await self.user_service.check_nickname_duplication(session, nickname)
