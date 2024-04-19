from collections import namedtuple
from copy import deepcopy

Entity = namedtuple("Entity", "e_type start_offset end_offset")
def collect_ne(sents):
    """
    Extracts the entities of a given IO/BIO/BIOS/BIOES annotated data
    """
    
    ne = list()
    for phrase in sents:
        phrase.append(None) #Control end-phrase tokens
        phr_ents = list()

        ent_extracted = Entity(None, None, None)
        prev_BIO = None
        for i, word in enumerate(phrase):
            if word:
                tok, label = word
                curr_BIO, entity = label[0], label[2:]
                next_BIO = phrase[i + 1][1][0] if phrase[i + 1] else None

                if curr_BIO == 'O':
                    if (prev_BIO and prev_BIO != 'O'):
                        phr_ents.append(ent_extracted)
                
                else:
                    #Begin entity
                    if not prev_BIO or prev_BIO == 'O':
                        ent_extracted = Entity(entity, i, i)
    
                    else:
                        if entity == ent_extracted.e_type:
                            ent_extracted = ent_extracted._replace(end_offset = ent_extracted.end_offset + 1)
                        else:
                            #different entities together
                            phr_ents.append(ent_extracted)
                            ent_extracted = Entity(entity, i, i)
                    
                    #Also current word is end entity
                    if not next_BIO:
                        phr_ents.append(ent_extracted)

                prev_BIO = curr_BIO
        ne.append(phr_ents)
    return ne


def compute_metrics(true_sents, pred_sents):

    true_named_entities = collect_ne(true_sents)
    pred_named_entities = collect_ne(pred_sents)
     
    ents = ['ORG', 'PER', 'LOC', 'MISC']
    eval_metrics = {'correct': 0, 'incorrect': 0, 'partial': 0, 'missed': 0, 'spurious': 0}

    # results by entity type
    eval_agg_ent = {e: deepcopy(eval_metrics) for e in ents}

    for i, phrase in enumerate(pred_named_entities):

        # keep track of entities that overlapped
        true_which_overlapped_with_pred = []
        for pred in phrase:
            found_overlap = False

            #Correct: Start and End entity offsets match, also the type
            if pred in true_named_entities[i]:
                true_which_overlapped_with_pred.append(pred)
                eval_metrics['correct'] += 1
                eval_agg_ent[pred.e_type]['correct'] += 1

            else:

                # check for overlaps with any of the true entities
                for true in true_named_entities[i]:

                    pred_range = range(pred.start_offset, pred.end_offset)
                    true_range = range(true.start_offset, true.end_offset)

                    # Incorrect: Offsets match, but entity type is wrong
                    if true.start_offset == pred.start_offset and pred.end_offset == true.end_offset \
                            and true.e_type != pred.e_type:

                        eval_metrics['incorrect'] += 1
                        eval_agg_ent[pred.e_type]['incorrect'] += 1

                        true_which_overlapped_with_pred.append(true)
                        found_overlap = True
                        break

                    # check for an overlap i.e. not exact boundary match, with true entities
                    elif find_overlap(true_range, pred_range):

                        # Partial: There is an overlap and the entity type is the same
                        if pred.e_type == true.e_type:

                            eval_metrics['partial'] += 1
                            eval_agg_ent[pred.e_type]['partial'] += 1

                            true_which_overlapped_with_pred.append(true)
                            found_overlap = True
                            break
                        
                        #Entities overlap, but the entity type is different.
                        else:
                            eval_metrics['incorrect'] += 1
                            eval_agg_ent[pred.e_type]['incorrect'] += 1
                            found_overlap = True
                            break

                # Sporious: Entities are over-generated, not in test
                if not found_overlap:

                    eval_metrics['spurious'] += 1
                    eval_agg_ent[pred.e_type]['spurious'] += 1

        # Missing: Entity was missed entirely in pred.
        for true in true_named_entities[i]:
            if true in true_which_overlapped_with_pred:
                continue
            else:
                eval_metrics['missed'] += 1
                eval_agg_ent[true.e_type]['missed'] += 1

    # Compute 'possible', 'actual' according to SemEval-2013 Task 9.1 on the
    # overall results and at entity level.

    eval_metrics = compute_actual_possible(eval_metrics)
    eval_metrics = compute_precision_recall_F1(eval_metrics)
    for ent in ents:
        eval_agg_ent[ent] = compute_actual_possible(eval_agg_ent[ent])
        eval_agg_ent[ent] = compute_precision_recall_F1(eval_agg_ent[ent])

    return eval_metrics, eval_agg_ent


def compute_actual_possible(results):
    """
    Takes a result dict that has been output by compute metrics.
    Returns the results dict with actual, possible computed according to SemEval-2013 Task 9.1 on the overall results.
    """

    # Possible: number annotations in the gold-standard which contribute to the final score
    results["possible"] = results['correct'] + results['incorrect'] + results['partial'] + results['missed']

    # Actual: number of annotations produced by the NER model
    results["actual"] = results['correct'] + results['incorrect'] + results['partial'] + results['spurious']

    return results

def compute_precision_recall_F1(results, allow_partial = False):
    """
    Takes a result dict that has been output by compute actual possible.
    Returns the results dict with precison, recall and F1-score populated.
    """

    actual = results['actual']; possible = results['possible']
    correct = results['correct']; partial = results['partial']
    
    if allow_partial:
        precision = (correct + 0.5 * partial) / actual if actual > 0 else 0
        recall = (correct + 0.5 * partial) / possible if possible > 0 else 0

    else:
        precision = correct / actual if actual > 0 else 0
        recall = correct / possible if possible > 0 else 0

    results["precision"] = precision
    results["recall"] = recall
    results["F1-score"] = (2 * precision * recall) / (precision + recall)

    return results

def find_overlap(true_range, pred_range):
    
    true_set = set(true_range)
    pred_set = set(pred_range)

    return true_set.intersection(pred_set)
