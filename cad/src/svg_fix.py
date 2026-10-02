"""Local workaround for a build123d SVG export failure (reported as a kit issue).

Some projected views contain full ellipses whose start and end points coincide but that
OCCT does not flag as closed; svgpathtools then refuses a zero-length arc and the export
stops with an AssertionError. Importing this module draws such an ellipse as a fine
polyline instead. Used by cad/src/sheets.py and cad/src/concept_media.py.
"""
import svgpathtools as _spt
from build123d import ExportSVG

_ellipse_segments = ExportSVG._ellipse_segments


def _safe_ellipse_segments(self, edge, reverse):
    try:
        return _ellipse_segments(self, edge, reverse)
    except AssertionError:
        pts = [self._path_point(edge.position_at(i / 48)) for i in range(49)]
        if reverse:
            pts.reverse()
        return [_spt.Line(a, b) for a, b in zip(pts, pts[1:]) if a != b]


ExportSVG._ellipse_segments = _safe_ellipse_segments
