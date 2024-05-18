from rest_framework.serializers import CurrentUserDefault


class CurrentClinicDefault(CurrentUserDefault):
    def __call__(self, serializer_field):
        if hasattr(serializer_field.context["request"].user, "staff"):
            return serializer_field.context["request"].user.staff.clinic
        return None
