# Generated by generate_dockerfiles.py

FROM aorwall/swe-bench-psf_requests:bookworm-slim



COPY --from=aorwall/swe-bench-pyenvs:bookworm-slim /opt/pyenv/versions/3.9.19 /opt/pyenv/versions/3.9.19

RUN pyenv rehash && \
    pyenv global 3.9.19 && \
    pyenv versions

WORKDIR /opt/psf__requests

RUN git -c advice.detachedHead=false checkout 27b55a74d7b9bd2f8c60fd0ee342bcbbf40e0a66


RUN pip install pytest
RUN pip install coverage cosmic-ray

RUN pip install -I --force-reinstall setuptools==71.0.0
RUN python -m pip install . --no-build-isolation --no-cache-dir


RUN git checkout 27b55a74d7b9bd2f8c60fd0ee342bcbbf40e0a66 .

ENV TESTBED_NAME=psf__requests__0.13
ENV IMAGE_TYPE=pyenv

WORKDIR /opt

COPY swebench_docker swebench_docker
COPY --chmod=0755 docker/pyenv/entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]
