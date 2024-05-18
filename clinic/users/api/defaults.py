from rest_framework.serializers import CurrentUserDefault


class CurrentClinicDefault(CurrentUserDefault):
    def __call__(self, serializer_field):
        return serializer_field.context["request"].user.staff.clinic
