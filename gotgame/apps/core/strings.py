from django.utils.crypto import get_random_string


def generate_random_unique_field(model, field_name='pk', length=30, not_in=[]):
    """
    Unil function which generates a random string checking that it's unique across
    <model>.<field_name>.
    It does not lock the table so it might happen that two process generate the same
    value but that is really unlikely.

    You can specify `not_in` as a list of extra values that the result value
    shouldn't be equal to.
    """
    new_value = get_random_string(length=length)

    if new_value not in not_in:
        try:
            model.objects.get(**{
                    field_name: new_value
                })
        except model.DoesNotExist:
            return new_value

    return generate_random_unique_field(
            model, field_name=field_name, length=length, not_in=not_in
        )
