import os
import re
from micromlgen import platforms
from sklearn.svm import SVC, LinearSVC, OneClassSVM
from skbayes.rvm_ard_models import RVC
from jinja2 import FileSystemLoader, Environment


def jinja(template_file, data):
    """Render Jinja template"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    loader = FileSystemLoader(dir_path + '/templates')
    template = Environment(loader=loader).get_template(template_file)
    code = template.render(data)
    code = re.sub(r'\n\s*\n', '\n', code)
    return code


def _port(template, data):
    """Add common template data before rendering"""
    data.update(**{
        'f': {
            'enumerate': enumerate,
            'round': lambda x: round(x, data.get('precision', 9) or 9),
            'zip': zip
        }
    })
    return jinja(template, data)


def port_rvm(clf, classname, **kwargs):
    """Port a RVM classifier"""
    assert classname is None or len(classname) > 0, 'Invalid class name'
    template_data = {
        **kwargs,
        'kernel': {
            'type': clf.kernel,
            'gamma': clf.gamma,
            'coef0': clf.coef0,
            'degree': clf.degree
        },
        'sizes': {
            'features': len(clf.relevant_vectors_[0]),
        },
        'arrays': {
            'vectors': clf.relevant_vectors_,
            'coefs': clf.coef_,
            'actives': clf.active_,
            'intercepts': clf.intercept_,
            'mean': clf._x_mean,
            'std': clf._x_std
        },
        'classname': classname if classname is not None else 'RVM',
    }
    return _port('rvm/rvm.jinja', template_data)


def port_svm(clf, classname=None, **kwargs):
    """Port a SVC / LinearSVC classifier"""
    assert isinstance(clf.gamma, float), 'You probably didn\'t set an explicit value for gamma: 0.001 is a good default'
    assert classname is None or len(classname) > 0, 'Invalid class name'
    support_v = clf.support_vectors_
    n_classes = len(clf.n_support_)
    template_data = {
        **kwargs,
        'kernel': {
            'type': clf.kernel,
            'gamma': clf.gamma,
            'coef0': clf.coef0,
            'degree': clf.degree
        },
        'sizes': {
            'features': len(support_v[0]),
            'vectors': len(support_v),
            'classes': n_classes,
            'decisions': n_classes * (n_classes - 1) // 2,
            'supports': clf.n_support_
        },
        'arrays': {
            'supports': support_v,
            'intercepts': clf.intercept_,
            'coefs': clf.dual_coef_
        },
        'classname': classname if classname is not None else 'SVM'
    }
    return _port('svm/svm.jinja', template_data)


def port(
        clf,
        classname=None,
        classmap=None,
        platform=platforms.ARDUINO,
        precision=None):
    assert platform in platforms.ALL, 'Unknown platform %s. Use one of %s' % (platform, ', '.join(platforms.ALL))
    if isinstance(clf, (SVC, LinearSVC, OneClassSVM)):
        return port_svm(**locals())
    elif isinstance(clf, RVC):
        return port_rvm(**locals())
    raise TypeError('clf MUST be one of SVC, LinearSVC, OneClassSVC, RVC')