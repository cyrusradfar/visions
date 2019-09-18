import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.types.tenzing_generic import tenzing_generic


class tenzing_integer(tenzing_generic):
    """**Integer** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in tenzing_integer
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)

        if pdt.is_integer_dtype(series):
            return super_mask

        # Note: this is required to support series with np.inf (as their representation is float)
        if pdt.is_float_dtype(series):
            return super_mask & series.eq(series.astype(int))

        return series.apply(lambda _: False)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype(int)
