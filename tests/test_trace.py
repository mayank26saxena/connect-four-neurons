import torch

from c4n.model import C4Transformer, tokens_from_moves
from c4n.trace import decompose, trace


def test_decomposition_is_exact():
    torch.manual_seed(0)
    m = C4Transformer(n_layer=3, d_model=64, n_head=4, d_ff=128).eval()
    for p in m.parameters():  # move away from the near-identity init so the test is not trivial
        p.data += 0.05 * torch.randn_like(p)
    moves = torch.randint(0, 7, (5, 42)); moves[:, 20:] = -1
    tok = tokens_from_moves(moves)
    tr = trace(m, tok)
    ref = m(tok)
    assert torch.allclose(tr["logits"], ref, atol=1e-4)
    bidx = torch.tensor([0, 1, 4, 2]); tidx = torch.tensor([0, 5, 19, 11])
    for layer, neuron in ((0, 3), (2, 77)):
        c, names = decompose(m, tr, layer, neuron, bidx, tidx)
        hn = m.blocks[layer].n2(tr["mid"][layer])[bidx, tidx]
        g = m.blocks[layer].mlp.gate(hn)[:, neuron]
        u = m.blocks[layer].mlp.up(hn)[:, neuron]
        assert torch.allclose(c[:, 0].sum(-1), g, atol=1e-4)
        assert torch.allclose(c[:, 1].sum(-1), u, atol=1e-4)
        assert len(names) == c.shape[-1]
