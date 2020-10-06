import pytest
from serializers.lease import LeaseSerializer
from tests.time import Time


@pytest.mark.usefixtures('empty_test_db')
class TestLeaseSerializer:
    def test_serializer(self, create_lease):
        lease = create_lease()

        assert LeaseSerializer.serialize(lease) == {
                'id': lease.id,
                'name': lease.name,
                'dateTimeStart': Time.format_date(lease.dateTimeStart),
                'dateTimeEnd': Time.format_date(lease.dateTimeEnd),
                'dateUpdated': Time.format_date(lease.dateUpdated),
                'occupants': lease.occupants,
                'created_at': Time.format_date(lease.created_at),
                'updated_at': Time.format_date(lease.updated_at)
            }
