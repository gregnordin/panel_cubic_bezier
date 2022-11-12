import numpy as np
import pandas as pd

# -------------------------------------------------------------------------------------------
# Cubic Bezier curve functions
# -------------------------------------------------------------------------------------------


def p(t, c0, c1, c2, c3):
    """Cubic 3D Bezier curve."""
    t0 = (1 - t) ** 3
    t1 = 3 * t * (1 - t) ** 2
    t2 = 3 * (t**2) * (1 - t)
    t3 = t**3
    # print(t0, t1, t2, t3)
    return t0 * c0 + t1 * c1 + t2 * c2 + t3 * c3


def dp(t, c0, c1, c2, c3):
    """Derivative of cubic 3D Bezier curve -> tangent at point for value of t."""
    a0 = -3 * c0 * (1 - t) ** 2
    a1 = 3 * c1 * (t * (2 * t - 2) + (1 - t) ** 2)
    a2 = 3 * c2 * (-1 * t**2 + 2 * t * (1 - t))
    a3 = 3 * c3 * t**2
    return a0 + a1 + a2 + a3


tt = np.linspace(0, 1, 101)


def bezier_curve(p0, p1, d0, d1, tt=tt):

    c0 = p0
    c1 = p0 + d0 / 3.0
    c2 = p1 - d1 / 3.0
    c3 = p1

    pt = np.array([p(t, c0, c1, c2, c3) for t in tt])

    df = pd.DataFrame(
        np.array([tt, pt[:, 0], pt[:, 1], pt[:, 2]]).T, columns=["t", "x", "y", "z"]
    )
    return df
