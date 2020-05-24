from django.core.exceptions import ValidationError


def validate_link(data):
    print(type(data))
    if "sia://" in data:
        return data
    else:
        raise ValidationError(
            f"Link have to be starts with sia://, your link is: {data}",
            params={"value": data},
        )
