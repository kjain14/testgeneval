# Generated by generate_dockerfiles.py

FROM aorwall/swe-bench-sympy_sympy:bookworm-slim

RUN git -c advice.detachedHead=false checkout 9a6104eab0ea7ac191a09c24f3e2d79dcd66bda5

RUN conda create -n sympy__sympy__1.11 python=3.9 mpmath flake8 -y
SHELL ["conda", "run", "-n", "sympy__sympy__1.11", "/bin/bash", "-c"]


RUN pip install mpmath==1.3.0 flake8-comprehensions coverage cosmic-ray

RUN pip install -e .


RUN git checkout 9a6104eab0ea7ac191a09c24f3e2d79dcd66bda5 .

ENV TESTBED_NAME=sympy__sympy__1.11
ENV IMAGE_TYPE=conda

WORKDIR /home/swe-bench

COPY swebench_docker swebench_docker

ENTRYPOINT ["./entrypoint.sh"]
