def score_each_skills(ner_skills, pos_skills, sd_skills, w2v_score_dict):
    probable_skills = ner_skills.union(pos_skills.union(sd_skills))
    skill_with_score = {}
    for skill in probable_skills:
        if skill in ner_skills:
            if skill not in skill_with_score:
                skill_with_score[skill] = 5.0
            else:
                skill_with_score[skill] += 5.0
        if skill in pos_skills:
            if skill not in skill_with_score:
                skill_with_score[skill] = 1.0
            else:
                skill_with_score[skill] += 1.0

        if skill in sd_skills:
            if skill not in skill_with_score:
                skill_with_score[skill] = 10.0
            else:
                skill_with_score[skill] += 10.0
        if skill in w2v_score_dict:
            if skill not in skill_with_score:
                skill_with_score[skill] = 3.0 * w2v_score_dict[skill]
            else:
                skill_with_score[skill] += 3.0 * w2v_score_dict[skill]
    skill_with_score = dict(sorted(skill_with_score.items(), key=lambda item: item[1], reverse=True))
    return skill_with_score
