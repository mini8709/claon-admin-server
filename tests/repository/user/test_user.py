import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from claon_admin.common.enum import Role
from claon_admin.schema.user import User
from tests.repository.user.conftest import user_repository


@pytest.mark.describe("Test case for user repository")
class TestUserRepository(object):
    @pytest.mark.asyncio
    async def test_save_user(self, session: AsyncSession, user_fixture: User):
        # then
        assert user_fixture.oauth_id == "oauth_id"
        assert user_fixture.nickname == "nickname"
        assert user_fixture.profile_img == "profile_img"
        assert user_fixture.sns == "sns"
        assert user_fixture.email == "test@test.com"
        assert user_fixture.instagram_name == "instagram_name"
        assert user_fixture.role == Role.PENDING

    @pytest.mark.asyncio
    async def test_find_user_by_id(
            self,
            session: AsyncSession,
            user_fixture: User
    ):
        # given
        user_id = user_fixture.id

        # when
        result = await user_repository.find_by_id(session, user_id)

        # then
        assert result == user_fixture

    @pytest.mark.asyncio
    async def test_find_user_by_invalid_id(
            self,
            session: AsyncSession
    ):
        # given
        wrong_id = "wrong_id"

        # when
        result = await user_repository.find_by_id(session, wrong_id)

        # then
        assert result is None

    @pytest.mark.asyncio
    async def test_exist_user_by_valid_id(
            self,
            session: AsyncSession,
            user_fixture: User
    ):
        # given
        user_id = user_fixture.id

        # when
        result = await user_repository.exist_by_id(session, user_id)

        # then
        assert result is True

    @pytest.mark.asyncio
    async def test_exist_user_by_invalid_id(
            self,
            session: AsyncSession,
            user_fixture: User
    ):
        # given
        wrong_id = "wrong_id"

        # when
        result = await user_repository.exist_by_id(session, wrong_id)

        # then
        assert result is False

    @pytest.mark.asyncio
    async def test_find_user_by_not_existing_nickname(
            self,
            session: AsyncSession,
            user_fixture: User
    ):
        # given
        nickname = "not_existing_nickname"

        # when
        result = await user_repository.find_by_nickname(session, nickname)

        # then
        assert result is None

    @pytest.mark.asyncio
    async def test_find_user_by_existing_nickname(
            self,
            session: AsyncSession,
            user_fixture: User
    ):
        # given
        nickname = user_fixture.nickname

        # when
        result = await user_repository.find_by_nickname(session, nickname)

        # then
        assert result == user_fixture

    @pytest.mark.asyncio
    async def test_exist_user_by_not_existing_nickname(
            self,
            session: AsyncSession,
            user_fixture: User
    ):
        # given
        nickname = "not_existing_nickname"

        # when
        result = await user_repository.exist_by_nickname(session, nickname)

        # then
        assert result is False

    @pytest.mark.asyncio
    async def test_exist_user_by_existing_nickname(
            self,
            session: AsyncSession,
            user_fixture: User
    ):
        # given
        nickname = user_fixture.nickname

        # when
        result = await user_repository.exist_by_nickname(session, nickname)

        # then
        assert result is True

    async def test_find_by_oauth_id_and_sns(self, session: AsyncSession, user_fixture: User):
        # given
        user_oauth_id = user_fixture.oauth_id
        user_sns = user_fixture.sns

        # when
        result = await user_repository.find_by_oauth_id_and_sns(session, user_oauth_id, user_sns)

        # then
        assert result == user_fixture

    @pytest.mark.asyncio
    async def test_find_by_invalid_oauth_id_and_sns(self, session: AsyncSession, user_fixture: User):
        # given
        user_oauth_id = "wrong_id"
        user_sns = user_fixture.sns

        # when
        result = await user_repository.find_by_oauth_id_and_sns(session, user_oauth_id, user_sns)

        # then
        assert result is None

    async def test_find_by_oauth_id(self, session: AsyncSession, user_fixture: User):
        # given
        user_oauth_id = user_fixture.oauth_id

        # when
        result = await user_repository.find_by_oauth_id(session, user_oauth_id)

        # then
        assert result == user_fixture

    @pytest.mark.asyncio
    async def test_find_by_invalid_oauth_id(self, session: AsyncSession, user_fixture: User):
        # given
        user_oauth_id = "wrong_id"

        # when
        result = await user_repository.find_by_oauth_id(session, user_oauth_id)

        # then
        assert not result

    @pytest.mark.asyncio
    async def test_update_role(self, session: AsyncSession, user_fixture: User):
        # given
        role = Role.LECTOR

        # when
        result = await user_repository.update_role(session, user_fixture, Role.LECTOR)

        # then
        assert result.role == role
