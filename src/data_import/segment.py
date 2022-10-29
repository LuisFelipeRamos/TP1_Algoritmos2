import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def check_segment(file):
    """Checa se o dataset `segment` é separável."""

    col_names_segment = [
        "Region-centroid-col",
        "Region-centroid-row",
        "Region-pixel-count",
        "Short-line-density-5",
        "Short-line-density-2",
        "Vedge-mean",
        "Vegde-sd",
        "Hedge-mean",
        "Hedge-sd",
        "Intensity-mean",
        "Rawred-mean",
        "Rawblue-mean",
        "Rawgreen-mean",
        "Exred-mean",
        "Exblue-mean",
        "Exgreen-mean",
        "Value-mean",
        "Saturatoin-mean",
        "Hue-mean",
        "Class",
    ]
    segment = pd.read_csv(file, names=col_names_segment)

    segmentclass1 = segment[segment["Class"] == 1]
    segmentclass2 = segment[segment["Class"] == 2]
    segmentclass1 = segmentclass1[["Region-centroid-col", "Rawblue-mean"]]
    segmentclass2 = segmentclass2[["Region-centroid-col", "Rawblue-mean"]]

    D: DataProcessor = DataProcessor(
        ("1", "2"), "Segment", ("Region-centroid-col", "Rawblue-mean")
    )

    hull_1, hull_2 = D.process(segmentclass1, segmentclass2)

    D.plot(hull_1, hull_2, (10, 300))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull_1.convex_hull, hull_2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
