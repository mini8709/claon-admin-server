import pytest
from fastapi_pagination import Params, Page

from claon_admin.common.enum import Role
from claon_admin.common.error.exception import UnauthorizedException, ErrorCode, NotFoundException
from claon_admin.common.util.pagination import Pagination
from claon_admin.model.auth import RequestUser
from claon_admin.model.center import CenterBriefResponseDto
from claon_admin.schema.center import Center
from claon_admin.service.center import CenterService


@pytest.mark.describe("Test case for find centers")
class TestFindCenters(object):
    @pytest.mark.asyncio
    @pytest.mark.it("Success case")
    async def test_find_centers(
            self,
            center_service: CenterService,
            mock_repo: dict,
            center_fixture: Center,
            another_center_fixture: Center
    ):
        # given
        request_user = RequestUser(id="123456", sns="test@claon.com", role=Role.CENTER_ADMIN)
        params = Params(page=1, size=10)
        items = [center_fixture, another_center_fixture]
        center_page = Page(items=items, params=params, total=2)
        mock_repo["center"].find_all_by_user_id.return_value = center_page
        mock_pagination = Pagination(
            next_page_num=2,
            previous_page_num=0,
            total_num=1,
            results=[CenterBriefResponseDto.from_entity(item) for item in items]
        )
        mock_repo["pagination_factory"].create.side_effect = [mock_pagination]

        # when
        pages = await center_service.find_centers(
            None,
            params=params,
            subject=request_user
        )

        # then
        assert len(pages.results) == 2
        assert pages.results[0].center_id == center_fixture.id
        assert pages.results[1].center_id == another_center_fixture.id

    @pytest.mark.asyncio
    @pytest.mark.it("Fail case: request user is not center admin")
    async def test_find_centers_with_not_center_admin(
            self,
            center_service: CenterService,
            mock_repo: dict
    ):
        # given
        request_user = RequestUser(id="111111", sns="test@claon.com", role=Role.LECTOR)
        params = Params(page=1, size=10)

        with pytest.raises(UnauthorizedException) as exception:
            # when
            await center_service.find_centers(None, params, request_user)

        # then
        assert exception.value.code == ErrorCode.NOT_ACCESSIBLE

    @pytest.mark.asyncio
    @pytest.mark.it("Fail case: center is not found")
    async def test_find_centers_with_not_exist_center(
            self,
            center_service: CenterService,
            mock_repo: dict
    ):
        # given
        request_user = RequestUser(id="123456", sns="test@claon.com", role=Role.CENTER_ADMIN)
        params = Params(page=1, size=10)
        center_page = Page(items=[], params=params, total=0)
        mock_repo["center"].find_all_by_user_id.return_value = center_page

        with pytest.raises(NotFoundException) as exception:
            # when
            await center_service.find_centers(None, params, request_user)

        # then
        assert exception.value.code == ErrorCode.DATA_DOES_NOT_EXIST
