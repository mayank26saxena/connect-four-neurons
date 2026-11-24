import numpy as np
import torch

from c4n import analysis as A


def test_chunked_equals_unchunked():
    g = torch.Generator().manual_seed(0)
    acts = torch.randn(3000, 2, 40, generator=g).half()
    C = (torch.rand(3000, 12, generator=g) < 0.3).numpy()
    q1 = A.percentiles(acts, [3, 50, 97], "cpu", col_chunk=7)
    q2 = A.percentiles(acts, [3, 50, 97], "cpu", col_chunk=1000)
    assert torch.equal(q1, q2)
    r1 = A.pole_concept_scores(acts, C, "cpu", col_chunk=7, min_concept_count=10)
    r2 = A.pole_concept_scores(acts, C, "cpu", col_chunk=1000, min_concept_count=10)
    for k in ("f1_sweep", "arg_sweep"):
        assert np.allclose(r1[k], r2[k])
    rot = A.random_rotations(2, 40, 3)
    a1 = A.pole_concept_scores(acts, C, "cpu", rotation=rot, col_chunk=7, min_concept_count=10)
    a2 = A.pole_concept_scores(acts, C, "cpu", rotation=rot, col_chunk=1000, min_concept_count=10)
    assert np.allclose(a1["f1_sweep"], a2["f1_sweep"], atol=1e-6)
