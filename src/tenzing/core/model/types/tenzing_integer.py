import pandas.api.types as pdt
import pandas as pd
import numpy as np

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model
from tenzing.utils.coercion import test_utils


def string_to_nullable_int(series: pd.Series) -> pd.Series:
    return series.astype(float).astype("Int64")


class tenzing_integer(tenzing_model):
    """**Integer** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in tenzing_integer
        True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_string, tenzing_generic, tenzing_float

        relations = {
            tenzing_generic: relation_conf(inferential=False),
            tenzing_float: relation_conf(
                relationship=test_utils.coercion_equality_test(lambda s: s.astype(int)),
                inferential=False,
            ),
            tenzing_string: relation_conf(
                relationship=test_utils.coercion_test(string_to_nullable_int),
                transformer=string_to_nullable_int,
                inferential=True,
            ),
        }

        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if pdt.is_integer_dtype(series):
            return True
        elif pdt.is_float_dtype(series):
            # Need this additional check because it's an Option[Int] which in
            # pandas land will result in integers with decimal trailing 0's
            try:
                return series.eq(series.astype(int)).all()
            except (ValueError, TypeError):
                return False
        else:
            return False

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("Int64")
