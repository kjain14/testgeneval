# Generated by generate_dockerfiles.py

FROM aorwall/swe-bench-scikit-learn_scikit-learn-testbed:0.22

WORKDIR /opt/scikit-learn__scikit-learn

RUN git -c advice.detachedHead=false checkout d49a6f13af2f22228d430ac64ac2b518937800d0

RUN pip install -v --no-build-isolation -e .
RUN pip install coverage cosmic-ray

WORKDIR /opt
