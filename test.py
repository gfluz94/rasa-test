#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

text_to_report = "## RESULTADOS DO TREINAMENTO\n\n"

text_to_report += "### 1. Intents\n\n"

with open("results/intent_report.json", "r") as file:
    intent_results = json.load(file)

intents = []
precision_results = []
recall_results = []
f1_results = []
support = []

global_results = {}

for k, v in intent_results.items():
    if k in ["accuracy", "macro avg", "weighted avg"]:
        global_results[k] = v
    else:
        intents.append(k)
        precision_results.append(v["precision"])
        recall_results.append(v["recall"])
        f1_results.append(v["f1-score"])
        support.append(v["support"])

text_to_report += "#### 1.1. Performance Geral\n\n"
headers = ("Métrica", "Valor")
table_rows = [headers, ["---"]*len(headers)]
for k, v in global_results.items():
    if k=="accuracy":
        to_add = ("Acurácia", f"{100*v:.2f}%")
    elif k=="weighted avg":
        to_add = ("Precisão (Ponderado)", f"{100*v['precision']:.2f}%")
        table_rows.append(to_add)
        table_rows.append(["---"]*len(headers))
        to_add = ("Recall (Ponderado)", f"{100*v['recall']:.2f}%")
        table_rows.append(to_add)
        table_rows.append(["---"]*len(headers))
        to_add = ("F1-Score (Ponderado)", f"{100*v['f1-score']:.2f}%")
    elif k=="macro avg":
        to_add = ("Precisão (Macro)", f"{100*v['precision']:.2f}%")
        table_rows.append(to_add)
        table_rows.append(["---"]*len(headers))
        to_add = ("Recall (Macro)", f"{100*v['recall']:.2f}%")
        table_rows.append(to_add)
        table_rows.append(["---"]*len(headers))
        to_add = ("F1-Score (Macro)", f"{100*v['f1-score']:.2f}%")
    table_rows.append(to_add)
    table_rows.append(["---"]*len(headers))
text_to_report += "\n".join([" | ".join(t) for t in table_rows[:-1]]) + "\n\n"


text_to_report += "#### 1.2. Performance por Intent\n\n"
headers = ("Intent", "Precisão", "Recall", "F1-Score", "# Exemplos", "% Exemplos")
table_rows = [headers, ["---"]*len(headers)]
for i, intent in enumerate(intents):
    precision = f"{100*precision_results[i]:.2f}%"
    recall = f"{100*recall_results[i]:.2f}%"
    f1 = f"{100*f1_results[i]:.2f}%"
    relevancy = f"{100*support[i]/sum(support):.0f}%"
    table_rows.append((intent, precision, recall, f1, str(support[i]), relevancy))
    table_rows.append(["---"]*len(headers))
text_to_report += "\n".join([" | ".join(t) for t in table_rows[:-1]]) + "\n\n"
text_to_report += "##### Matriz de confusão\n\n![](intent_confusion_matrix.png)\n\n"

with open("results/pull_request_report.md", "w") as file:
    file.write(text_to_report)
