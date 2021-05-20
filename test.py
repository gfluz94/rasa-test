#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

def generate_metrics_report(results: dict, section="intents", index_number=1) -> str:
    names = []
    precision_results = []
    recall_results = []
    f1_results = []
    support = []
    global_results = {}

    for k, v in intent_results.items():
        if k in ["accuracy", "macro avg", "weighted avg"]:
            global_results[k] = v
        else:
            names.append(k)
            precision_results.append(v["precision"])
            recall_results.append(v["recall"])
            f1_results.append(v["f1-score"])
            support.append(v["support"])

    output = f"### {index_number}. {section.capitalize()}\n\n"
    output += f"#### {index_number}.1. Performance Geral\n\n"
    headers = ("Métrica", "Valor")
    table_rows = [headers, ["---"]*len(headers)]
    for k, v in global_results.items():
        if k=="accuracy":
            to_add = ("Acurácia", f"{100*v:.2f}%")
        elif k=="weighted avg":
            to_add = ("Precisão (Ponderado)", f"{100*v['precision']:.2f}%")
            table_rows.append(to_add)
            to_add = ("Recall (Ponderado)", f"{100*v['recall']:.2f}%")
            table_rows.append(to_add)
            to_add = ("F1-Score (Ponderado)", f"{100*v['f1-score']:.2f}%")
        elif k=="macro avg":
            to_add = ("Precisão (Macro)", f"{100*v['precision']:.2f}%")
            table_rows.append(to_add)
            to_add = ("Recall (Macro)", f"{100*v['recall']:.2f}%")
            table_rows.append(to_add)

            to_add = ("F1-Score (Macro)", f"{100*v['f1-score']:.2f}%")
        table_rows.append(to_add)
    output += "\n".join([" | ".join(t) for t in table_rows]) + "\n\n"

    output += "#### 1.2. Performance por Intent\n\n"
    headers = (section.capitalize(), "Precisão", "Recall", "F1-Score", "# Exemplos", "% Exemplos")
    table_rows = [headers, ["---"]*len(headers)]
    for i, name in enumerate(names):
        precision = f"{100*precision_results[i]:.2f}%"
        recall = f"{100*recall_results[i]:.2f}%"
        f1 = f"{100*f1_results[i]:.2f}%"
        relevancy = f"{100*support[i]/sum(support):.0f}%"
        table_rows.append((name, precision, recall, f1, str(support[i]), relevancy))
    output += "\n".join([" | ".join(t) for t in table_rows]) + "\n\n"
    output += f"##### Matriz de confusão\n\n![]({section}_confusion_matrix.png)\n\n"

    return output
    


if __name__ == "__main__":
    text_to_report = "## RESULTADOS DO TREINAMENTO\n\n"

    with open("results/intent_report.json", "r") as file:
        intent_results = json.load(file)
    with open("results/story_report.json", "r") as file:
        story_results = json.load(file)

    text_to_report += generate_metrics_report(intent_results, section="intent", index_number=1)
    text_to_report += generate_metrics_report(story_results, section="story", index_number=2)

    print(text_to_report)

# with open("results/pull_request_report.md", "w") as file:
#     file.write(text_to_report)
