import warnings
warnings.simplefilter('ignore')


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp', nargs='+', type=int)
    parser.add_argument('--ccd', nargs='+', type=int)
    args = parser.parse_args()
    from .image_quality_model import ImageQualityModel
    for obs_id in args.exp:
        for ccd in args.ccd:
            iqm = ImageQualityModel(obs_id, ccd)
            print(obs_id, ccd, iqm.compute_image_quality())


if __name__ == '__main__':
    main()
