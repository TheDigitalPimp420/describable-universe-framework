"""
DU_toy_model.py

Toy universe stress test for the Describable Universe framework functional:

F(C) = alpha*S_info(C) + lambda*R_info(C) - beta*L(M)

- Microstates: binary spin chain length N=64
- Dynamics: independent bit flips with probability p
- Coarse-grainings tested:
  1) block-majority (block=8)
  2) global majority sign
  3) random hash (8 bits)
- Environment fragments: noisy copies of macrostate bits with noise q

Outputs:
- DU_toy_model_results.csv
- DU_toy_model_FC.png
"""

import numpy as np, math, pandas as pd

rng = np.random.default_rng(42)

def entropy_from_counts(counts):
    total = sum(counts.values())
    H = 0.0
    for c in counts.values():
        if c == 0: continue
        p = c/total
        H -= p*math.log2(p)
    return H

def mutual_information(m_vals, e_vals):
    n = len(m_vals)
    joint, pm, pe = {}, {}, {}
    for m,e in zip(m_vals, e_vals):
        m=int(m); e=int(e)
        joint[(m,e)] = joint.get((m,e),0)+1
        pm[m] = pm.get(m,0)+1
        pe[e] = pe.get(e,0)+1
    I=0.0
    for (m,e), c in joint.items():
        pme=c/n; pmv=pm[m]/n; pev=pe[e]/n
        I += pme*math.log2(pme/(pmv*pev))
    return I

N=64

def sample_microstates(num):
    return rng.integers(0,2,size=(num,N),endpoint=False,dtype=np.int8)

def evolve_microstates(X, flip_prob=0.05):
    flips = (rng.random(size=X.shape) < flip_prob).astype(np.int8)
    return np.bitwise_xor(X, flips)

def C_block_majority(X, block=8):
    num_blocks=N//block
    blocks=X.reshape(-1,num_blocks,block)
    maj=(blocks.sum(axis=2) >= (block/2)).astype(np.int8)
    weights=(1<<np.arange(num_blocks,dtype=np.int64))
    return (maj*weights).sum(axis=1).astype(np.int64), num_blocks

def C_global_majority_sign(X):
    m=(X.sum(axis=1) >= (N/2)).astype(np.int8)
    return m.astype(np.int64), 1

W_hash = rng.integers(0,2,size=(8,N),endpoint=False,dtype=np.int8)
def C_random_hash_8(X):
    proj=(X@W_hash.T) % 2
    weights=(1<<np.arange(8,dtype=np.int64))
    return (proj*weights).sum(axis=1).astype(np.int64), 8

def env_fragment_records(M, bits, noise=0.10, fragments=8):
    M_bits=((M[:,None]>>np.arange(bits,dtype=np.int64)) & 1).astype(np.int8)
    weights=(1<<np.arange(bits,dtype=np.int64))
    recs=[]
    for _ in range(fragments):
        flips=(rng.random(size=M_bits.shape) < noise).astype(np.int8)
        noisy=np.bitwise_xor(M_bits, flips)
        recs.append((noisy*weights).sum(axis=1).astype(np.int64))
    return recs

def evaluate_C(name, C_fn, num_samples=15000, flip_prob=0.05, env_noise=0.10, fragments=8,
               alpha=1.0, lam=1.0, beta=0.5):
    X0=sample_microstates(num_samples)
    X1=evolve_microstates(X0, flip_prob)
    M0,bits=C_fn(X0)
    M1,b2=C_fn(X1)
    assert bits==b2

    uniq,counts=np.unique(M0, return_counts=True)
    counts_M0={int(u):int(c) for u,c in zip(uniq,counts)}
    H_M=entropy_from_counts(counts_M0)

    joint={}
    counts_m0={}
    for a,b in zip(M0,M1):
        a=int(a); b=int(b)
        joint[(a,b)] = joint.get((a,b),0)+1
        counts_m0[a] = counts_m0.get(a,0)+1

    H_cond=0.0
    for m0,c0 in counts_m0.items():
        sub={}
        for (a,b),c in joint.items():
            if a==m0:
                sub[b] = sub.get(b,0)+c
        H_cond += (c0/num_samples)*entropy_from_counts(sub)

    S_info = -H_cond

    E_recs=env_fragment_records(M0,bits,noise=env_noise,fragments=fragments)
    I_sum=0.0
    for Ei in E_recs:
        I_sum += mutual_information(M0,Ei)
    R_info = (I_sum/H_M) if H_M>1e-12 else 0.0

    distinct=len(counts_M0)
    L = bits + (math.log2(distinct) if distinct>0 else 0.0)

    F = alpha*S_info + lam*R_info - beta*L

    return {"C":name,"bits":bits,"H(M)":H_M,"H(M1|M0)":H_cond,"S_info":S_info,"R_info":R_info,"L(M) proxy":L,"F(C)":F,"distinct":distinct}

if __name__=="__main__":
    results=[
        evaluate_C("Block-majority (8)", lambda X: C_block_majority(X,8)),
        evaluate_C("Global majority sign", C_global_majority_sign),
        evaluate_C("Random hash (8 bits)", C_random_hash_8),
    ]
    df=pd.DataFrame(results).sort_values("F(C)", ascending=False)
    df.to_csv("DU_toy_model_results.csv", index=False)
    print(df.to_string(index=False))
