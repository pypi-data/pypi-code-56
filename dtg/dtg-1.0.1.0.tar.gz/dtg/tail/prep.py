import numpy as np

from scipy.stats import norm

from dtg.tail.estimate.hill import HillEstimator
from dtg.tail.estimate.moment import MomentEstimator
from dtg.tail.estimate.pickands import PickandEstimator
from dtg.tail.estimate.ratio import RatioEstimator
from dtg.tail.mse import boot


def boot_estimate(entity, x, alp, beta, num, speed=True, pers=0.05):
    k = entity.get_k(x)
    x_ = entity.prepare(x)

    if speed:
        if len(k) == 0:
            return 1, 0, (0, 0)

        count = 0
        mse, alpr, dls = boot(entity, x_, alp, beta, num, k[0])
        k_opt = k[0]

        for k_ in k:
            mse_, alp_, dls_ = boot(entity, x_, alp, beta, num, k_)

            if mse_ < mse:
                mse = mse_
                alpr = alp_
                k_opt = k_
                count = 0
                dls = dls_
            else:
                count += 1

            if count == int(0.1 * k.size) or count == 100:
                break
        return (
            alpr,
            k_opt,
            (alpr - dls * norm.ppf(1 - pers), alpr - dls * norm.ppf(pers)),
        )

    mses, alps, dls = zip(*boot(entity, x_, alp, beta, num, k))
    if len(mses) == 1:
        return mses[0], alps[0], (alps[0], alps[0])
    ar = np.argmin(mses)
    return (
        alps[ar],
        k[ar],
        (
            alps[ar] - dls[ar] * norm.ppf(1 - (pers / 2)),
            alps[ar] - dls[ar] * norm.ppf(pers / 2),
        ),
    )


def basic_tail(data):
    alp = boot_estimate(HillEstimator, data, 1 / 2, 2 / 3, 100, speed=False)[0]
    print("hill", 1 / alp)

    alp = boot_estimate(RatioEstimator, data, 1 / 2, 2 / 3, 100, speed=False)[0]
    print("ratio", 1 / alp)

    alp = boot_estimate(MomentEstimator, data, 1 / 2, 2 / 3, 100, speed=False)[0]
    print("moment", 1 / alp)

    alp = boot_estimate(PickandEstimator, data, 1 / 2, 2 / 3, 100, speed=False)[0]
    print("pickands", 1 / alp)
