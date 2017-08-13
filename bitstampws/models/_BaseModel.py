class BaseModel:

    def _repr(self, *attrs):
        v = lambda v: str(getattr(self, v, None))
        return ", ".join(
            map(lambda attr: "{k}={v}".format(k=attr, v=v(attr)), attrs)
        )

