"""
DU_v24_generate.py

Reproducible generator for v2.4 figures:
- Comparative phase diagrams for three coarse-grainings
- Redundancy vs fragment count curve

Toy universe:
- Microstates: binary spin chain length N=64
- Dynamics: independent bit flips with probability p
- Environment fragments: noisy macro-bit records with noise q

Functional:
F(C) = alpha*S_info(C) + lambda*R_info(C) - beta*L(M)

Outputs (written to ./figures and ./data):
- figures/DU_v24_phase_Block.png
- figures/DU_v24_phase_Global.png
- figures/DU_v24_phase_Hash.png
- figures/DU_v24_redundancy.png
- data/DU_v24_phase_grid_Block.csv (and Global/Hash)
- data/DU_v24_redundancy.csv
"""

import os, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(321)

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

def evolve_microstates(X, flip_prob):
    flips = (rng.random(size=X.shape) < flip_prob).astype(np.int8)
    return np.bitwise_xor(X, flips)

def C_block_majority(X, block=8):
    num_blocks=N//block
    blocks=X.reshape(-1,num_blocks,block)
    maj=(blocks.sum(axis=2) >= (block/2)).astype(np.int8)
    weights=(1<<np.arange(num_blocks,dtype=np.int64))
    return (maj*weights).sum(axis=1).astype(np.int64), num_blocks

def C_global_majority(X):
    m=(X.sum(axis=1) >= (N/2)).astype(np.int8)
    return m.astype(np.int64), 1

W_hash = rng.integers(0,2,size=(8,N),endpoint=False,dtype=np.int8)
def C_random_hash(X):
    proj=(X@W_hash.T)%2
    weights=(1<<np.arange(8,dtype=np.int64))
    return (proj*weights).sum(axis=1).astype(np.int64), 8

def env_fragment_records(M, bits, noise, fragments):
    M_bits=((M[:,None]>>np.arange(bits,dtype=np.int64)) & 1).astype(np.int8)
    weights=(1<<np.arange(bits,dtype=np.int64))
    recs=[]
    for _ in range(fragments):
        flips=(rng.random(size=M_bits.shape) < noise).astype(np.int8)
        noisy=np.bitwise_xor(M_bits, flips)
        recs.append((noisy*weights).sum(axis=1).astype(np.int64))
    return recs

def compute_F(C_fn, flip_prob, env_noise, fragments=8, num_samples=6000,
              alpha=1.0, lam=1.0, beta=0.5):
    X0=sample_microstates(num_samples)
    X1=evolve_microstates(X0, flip_prob)
    M0,bits=C_fn(X0)
    M1,_=C_fn(X1)

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
                sub[b]=sub.get(b,0)+c
        H_cond += (c0/num_samples)*entropy_from_counts(sub)

    S_info=-H_cond

    E_recs=env_fragment_records(M0,bits,env_noise,fragments)
    I_sum=0.0
    for Ei in E_recs:
        I_sum+=mutual_information(M0,Ei)
    R_info=(I_sum/H_M) if H_M>1e-12 else 0.0

    distinct=len(counts_M0)
    L = bits + (math.log2(distinct) if distinct>0 else 0.0)

    return alpha*S_info + lam*R_info - beta*L, R_info

def ensure_dirs():
    os.makedirs("figures", exist_ok=True)
    os.makedirs("data", exist_ok=True)

def save_phase(name, Cfn, flip_vals, env_vals):
    grid=np.zeros((len(env_vals),len(flip_vals)))
    for i,q in enumerate(env_vals):
        for j,p in enumerate(flip_vals):
            F,_=compute_F(Cfn,p,q,fragments=8)
            grid[i,j]=F
    # save data
    df=pd.DataFrame(grid, index=env_vals, columns=flip_vals)
    df.to_csv(f"data/DU_v24_phase_grid_{name}.csv")
    # plot
    plt.figure()
    plt.imshow(grid, origin="lower", aspect="auto",
               extent=[flip_vals.min(), flip_vals.max(), env_vals.min(), env_vals.max()])
    plt.xlabel("Flip probability")
    plt.ylabel("Environment noise")
    plt.title(f"Phase diagram F(C) — {name}")
    plt.colorbar(label="F(C)")
    plt.tight_layout()
    plt.savefig(f"figures/DU_v24_phase_{name}.png", dpi=200)
    plt.close()

def save_redundancy():
    frag_vals=[1,2,4,8,16]
    R_curve=[]
    for k in frag_vals:
        _,R=compute_F(lambda X:C_block_majority(X,8), flip_prob=0.05, env_noise=0.05, fragments=k)
        R_curve.append(R)
    pd.DataFrame({"fragments":frag_vals, "R_info":R_curve}).to_csv("data/DU_v24_redundancy.csv", index=False)
    plt.figure()
    plt.plot(frag_vals, R_curve)
    plt.xlabel("Number of fragments")
    plt.ylabel("R_info")
    plt.title("Redundancy growth vs fragment count")
    plt.tight_layout()
    plt.savefig("figures/DU_v24_redundancy.png", dpi=200)
    plt.close()

if __name__=="__main__":
    ensure_dirs()
    flip_vals=np.linspace(0,0.25,10)
    env_vals=np.linspace(0,0.25,10)
    save_phase("Block", lambda X:C_block_majority(X,8), flip_vals, env_vals)
    save_phase("Global", C_global_majority, flip_vals, env_vals)
    save_phase("Hash", C_random_hash, flip_vals, env_vals)
    save_redundancy()
    print("Done. See ./figures and ./data")
