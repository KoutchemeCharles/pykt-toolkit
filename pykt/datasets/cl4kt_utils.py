import random
import numpy as np
import math

def augment_kt_seqs(
    q_seq,
    s_seq,
    r_seq,
    mask_prob,
    crop_prob,
    permute_prob,
    replace_prob,
    negative_prob,
    easier_skills,
    harder_skills,
    q_mask_id,
    s_mask_id,
    seq_len,
    seed=None,
    skill_rel=None,
    num_questions=-1
):
    # print(f"num_questions is {num_questions}")
    # masking (random or PMI 등을 활용해서)
    # 구글 논문의 Correlated Feature Masking 등...
    rng = random.Random(seed)
    np.random.seed(seed)
    masked_q_seq = []
    masked_s_seq = []
    masked_r_seq = []
    negative_r_seq = []
    # print(f"q_seq is {q_seq}, s_seq is {s_seq}, r_seq is {r_seq}")
    if mask_prob > 0:
        for q, s, r in zip(q_seq, s_seq, r_seq):
            prob = rng.random()
            if prob < mask_prob and s != 0:
                prob /= mask_prob
                if prob < 0.8:
                    if num_questions!=0:
                        masked_q_seq.append(q_mask_id)
                    masked_s_seq.append(s_mask_id)
                elif prob < 0.9:
                    if num_questions!=0:
                        masked_q_seq.append(
                            rng.randint(1, q_mask_id - 1)
                        )  # original BERT처럼 random한 확률로 다른 token으로 대체해줌
                    masked_s_seq.append(
                        rng.randint(1, s_mask_id - 1)
                    )  # randint(start, end) [start, end] 둘다 포함
                else:
                    if num_questions!=0:
                        masked_q_seq.append(q)
                    masked_s_seq.append(s)
            else:
                if num_questions!=0:
                    masked_q_seq.append(q)
                masked_s_seq.append(s)
            masked_r_seq.append(r)  # response는 나중에 hard negatives로 활용 (0->1, 1->0)

            # reverse responses
            neg_prob = rng.random()
            if neg_prob < negative_prob and r != -1:  # padding
                negative_r_seq.append(1 - r)
            else:
                negative_r_seq.append(r)
    else:
        masked_q_seq = q_seq[:]
        masked_s_seq = s_seq[:]
        masked_r_seq = r_seq[:]

        for r in r_seq:
            # reverse responses
            neg_prob = rng.random()
            if neg_prob < negative_prob and r != -1:  # padding
                negative_r_seq.append(1 - r)
            else:
                negative_r_seq.append(r)

    # print(f"masked_q_seq is {masked_q_seq}, masked_s_seq is {masked_s_seq}, masked_r_seq is {masked_r_seq}")
    """
    skill difficulty based replace
    """
    # print(harder_skills)
    if replace_prob > 0:
        for i, elem in enumerate(zip(masked_s_seq, masked_r_seq)):
            s, r = elem
            prob = rng.random()
            if prob < replace_prob and s != 0 and s != s_mask_id:
                if (
                    r == 0 and s in harder_skills
                ):  # if the response is wrong, then replace a skill with the harder one
                    masked_s_seq[i] = harder_skills[s]
                elif (
                    r == 1 and s in easier_skills
                ):  # if the response is correct, then replace a skill with the easier one
                    masked_s_seq[i] = easier_skills[s]

    true_seq_len = np.sum(np.asarray(s_seq) != 0)
    if permute_prob > 0:
        reorder_seq_len = math.floor(permute_prob * true_seq_len)
        start_idx = (np.asarray(s_seq) != 0).argmax()
        while True:
            # if seq_len - reorder_seq_len==0:
                # break
            start_pos = rng.randint(start_idx, true_seq_len - reorder_seq_len)
            # print(f"start_pos is {start_pos}")
            if start_pos + reorder_seq_len <= true_seq_len:
                break

        # reorder (permute)
        perm = np.random.permutation(reorder_seq_len)
        if num_questions!=0:
            masked_q_seq = (
                masked_q_seq[:start_pos]
                + np.asarray(masked_q_seq[start_pos : start_pos + reorder_seq_len])[
                    perm
                ].tolist()
                + masked_q_seq[start_pos + reorder_seq_len :]
            )
        masked_s_seq = (
            masked_s_seq[:start_pos]
            + np.asarray(masked_s_seq[start_pos : start_pos + reorder_seq_len])[
                perm
            ].tolist()
            + masked_s_seq[start_pos + reorder_seq_len :]
        )
        masked_r_seq = (
            masked_r_seq[:start_pos]
            + np.asarray(masked_r_seq[start_pos : start_pos + reorder_seq_len])[
                perm
            ].tolist()
            + masked_r_seq[start_pos + reorder_seq_len :]
        )

    if 0 < crop_prob < 1:
        crop_seq_len = math.floor(crop_prob * true_seq_len)
        if crop_seq_len == 0:
            crop_seq_len = 1
        start_idx = (np.asarray(q_seq) != 0).argmax()
        while True:
            start_pos = rng.randint(start_idx, true_seq_len - crop_seq_len)#Return random integer in range [a, b]
            if start_pos + crop_seq_len <= true_seq_len:
                break
        if num_questions!=0:
            masked_q_seq = masked_q_seq[start_pos : start_pos + crop_seq_len]
        masked_s_seq = masked_s_seq[start_pos : start_pos + crop_seq_len]
        masked_r_seq = masked_r_seq[start_pos : start_pos + crop_seq_len]

    pad_len = seq_len - len(masked_s_seq)
    attention_mask = [True] * len(masked_s_seq)+[False] * pad_len
    masked_q_seq = masked_q_seq+[0] * pad_len
    masked_s_seq = masked_s_seq+[0] * pad_len
    masked_r_seq = masked_r_seq+[0] * pad_len 
    #attention_mask is not used in here
    return masked_q_seq, masked_s_seq, masked_r_seq, negative_r_seq, attention_mask