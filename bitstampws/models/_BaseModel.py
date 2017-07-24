class BaseModel:

    @classmethod
    def _NewFromJsonDict(cls, data, **kwargs):
        if kwargs:
            for key, val in kwargs.items():
                data[key] = val
        return cls(**data)

    def _repr(self, *attrs):
        v = lambda v: str(getattr(self, v, None))
        return ", ".join(
            map(lambda attr: "{k}={v}".format(k=attr, v=v(attr)), attrs)
        )

