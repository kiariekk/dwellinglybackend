import pytest
from models.lease import LeaseModel


@pytest.fixture
def lease_attributes(faker):
    def _lease_attributes(unitNum, tenantId, propertyId, dateTimeStart, dateTimeEnd):
        return {
            "unitNum": unitNum,
            "tenantID": tenantId,
            "propertyID": propertyId,
            "dateTimeStart": dateTimeStart,
            "dateTimeEnd": dateTimeEnd,
            "occupants": faker.random_number(digits=2),
        }

    yield _lease_attributes


@pytest.fixture
def create_lease(faker, lease_attributes, create_property, create_tenant):
    def _create_lease(
        tenantId=None,
        unitNum=None,
        dateTimeStart=None,
        dateTimeEnd=None,
        propertyId=None,
    ):
        if not unitNum:
            unitNum = faker.building_number()
        if not dateTimeStart:
            dateTimeStart = faker.date_time_this_decade()
        if not dateTimeEnd:
            dateTimeEnd = faker.date_time_this_decade(before_now=False, after_now=True)
        if not tenantId:
            tenantId = create_tenant().id
        if not propertyId:
            propertyId = create_property().id
        lease = LeaseModel(
            **lease_attributes(
                unitNum, tenantId, propertyId, dateTimeStart, dateTimeEnd
            )
        )
        lease.save_to_db()
        return lease

    yield _create_lease
