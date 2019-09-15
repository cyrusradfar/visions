import pandas as pd

from tenzing.core.model.types.tenzing_object import tenzing_object


class tenzing_geometry(tenzing_object):
    """**Geometry** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> from shapely import wkt
    >>> x = pd.Series([wkt.loads('POINT (-92 42)'), wkt.loads('POINT (-92 42.1)'), wkt.loads('POINT (-92 42.2)')]
    >>> x in tenzing_geometry
    True
    """

    from shapely import geometry

    geom_types = [
        geometry.Point,
        geometry.Polygon,
        geometry.MultiPolygon,
        geometry.MultiPoint,
        geometry.LineString,
        geometry.LinearRing,
        geometry.MultiPoint,
        geometry.MultiLineString,
    ]

    @classmethod
    def contains_op(cls, series):
        if not super().contains_op(series):
            return False

        return all(
            any(isinstance(obj, geom_type) for geom_type in cls.geom_types)
            for obj in series
        )

    @classmethod
    def cast_op(cls, series, operation=None):
        from shapely import wkt

        return pd.Series([wkt.loads(value) for value in series])

    # @classmethod
    # @unique_summary
    # def summarization_op(cls, series):
    #     summary = super().summarization_op(series)
    #
    #     try:
    #         import geopandas as gpd
    #
    #         # summary['image'] = plotting.save_plot_to_str(gpd.GeoSeries(series).plot())
    #     except ImportError:
    #         pass
    #
    #     return summary