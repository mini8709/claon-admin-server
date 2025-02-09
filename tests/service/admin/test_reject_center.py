import pytest

from claon_admin.common.enum import Role
from claon_admin.common.error.exception import UnauthorizedException, ErrorCode, BadRequestException
from claon_admin.model.auth import RequestUser
from claon_admin.schema.center import Center
from claon_admin.service.admin import AdminService


@pytest.mark.describe("Test case for reject center")
class TestRejectCenter(object):
    @pytest.mark.asyncio
    @pytest.mark.it("Success case")
    async def test_reject_center(
            self,
            mock_repo: dict,
            admin_service: AdminService,
            center_fixture: Center
    ):
        # given
        request_user = RequestUser(id="123456", sns="test@claon.com", role=Role.ADMIN)
        center_id = center_fixture.id

        mock_repo["center"].find_by_id.side_effect = [center_fixture]

        # when
        result = await admin_service.reject_center(None, request_user, center_id)

        # then
        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.it("Fail case: request user is not admin")
    async def test_reject_center_with_non_admin(
            self,
            mock_repo: dict,
            admin_service: AdminService,
            center_fixture: Center
    ):
        # given
        request_user = RequestUser(id="123456", sns="test@claon.com", role=Role.PENDING)
        center_id = center_fixture.id

        with pytest.raises(UnauthorizedException) as exception:
            # when
            await admin_service.reject_center(None, request_user, center_id)

        # then
        assert exception.value.code == ErrorCode.NONE_ADMIN_ACCOUNT

    @pytest.mark.asyncio
    @pytest.mark.it("Fail case: center is not found")
    async def test_reject_not_existing_center(
            self,
            mock_repo: dict,
            admin_service: AdminService
    ):
        # given
        request_user = RequestUser(id="123456", sns="test@claon.com", role=Role.ADMIN)
        center_id = "not_existing_id"

        mock_repo["center"].find_by_id.side_effect = [None]

        with pytest.raises(BadRequestException) as exception:
            # when
            await admin_service.reject_center(None, request_user, center_id)

        # then
        assert exception.value.code == ErrorCode.DATA_DOES_NOT_EXIST
