from rest_framework.serializers import WritableField

from .models import MoneyInterval
from .fields import MoneyIntervalField


class MoneyIntervalDRFField(WritableField):
    type_name = 'MoneyIntervalDRFField'
    type_label = 'moneyIntervalDRFField'
    form_field_class = MoneyIntervalField

    def field_to_native(self, obj, field_name):

        moneyIntervalField = getattr(obj, field_name)

        if not moneyIntervalField:
            return None

        return {
            'interval_period': moneyIntervalField.interval_period,
            'per_interval_value': moneyIntervalField.per_interval_value,
        }

    def from_native(self, value):
        if not value:
            return None

        if isinstance(value, dict):
            interval_period, per_interval_value = value.get('interval_period'), value.get('per_interval_value')
            if not (interval_period and per_interval_value != None):
                return None

            mi = MoneyInterval(
                interval_period,
                pennies=per_interval_value or 0
            )
        else:
            # TODO - remove - only here for mock test - temporary
            mi = MoneyInterval('per_month', pennies=value)
        return mi


class MoneyIntervalModelSerializerMixin(object):
    def __init__(self, *args, **kwargs):
        # add a model serializer which is used throughout this project
        self.field_mapping = self.field_mapping.copy() # ouch
        self.field_mapping[MoneyIntervalField] = MoneyIntervalDRFField
        super(MoneyIntervalModelSerializerMixin, self).__init__(*args, **kwargs)
