# Generated by generate_dockerfiles.py

FROM aorwall/swe-bench-scikit-learn_scikit-learn-testbed:0.21

WORKDIR /opt/scikit-learn__scikit-learn

RUN git -c advice.detachedHead=false checkout cdfca8cba33be63ef50ba9e14d8823cc551baf92

RUN pip install -v --no-build-isolation -e .
RUN pip install coverage cosmic-ray

WORKDIR /opt
