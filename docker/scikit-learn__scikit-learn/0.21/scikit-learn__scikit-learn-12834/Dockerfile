# Generated by generate_dockerfiles.py

FROM aorwall/swe-bench-scikit-learn_scikit-learn-testbed:0.21

WORKDIR /opt/scikit-learn__scikit-learn

RUN git -c advice.detachedHead=false checkout 55a98ab7e3b10966f6d00c3562f3a99896797964

RUN pip install -v --no-build-isolation -e .
RUN pip install coverage cosmic-ray

WORKDIR /opt
