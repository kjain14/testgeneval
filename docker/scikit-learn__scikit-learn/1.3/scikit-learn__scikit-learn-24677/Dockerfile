# Generated by generate_dockerfiles.py

FROM aorwall/swe-bench-scikit-learn_scikit-learn-testbed:1.3

WORKDIR /opt/scikit-learn__scikit-learn

RUN git -c advice.detachedHead=false checkout 530dfc9631b2135412a048b5ec7cf01d155b6067

RUN pip install -v --no-use-pep517 --no-build-isolation -e .
RUN pip install coverage cosmic-ray

WORKDIR /opt
