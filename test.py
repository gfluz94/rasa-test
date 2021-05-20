#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

with open("results/intent_report.json", "r") as file:
    intent_results = json.load(file)

intents = []
precision_results = []
recall_results = []
f1_results = []

global_results = {}

for k, v in intent_results.items():
    if k in ["accuracy", "macro avg", "weighted avg"]:
        global_results[k] = v
    else:
        intents.append(k)
        precision_results.append(v["precision"])
        recall_results.append(v["recall"])
        f1_results.append(v["f1-score"])

text_to_report = "## RESULTADOS DO TREINAMENTO\n\n"

for i, intent in enumerate(intents):
    text_to_report += f"#### {i+1}. {intent.capitalize()}\n\n"
    text_to_report += f"+ Precisão: {100*precision_results[i]:.2f}%\n"
    text_to_report += f"+ Recall: {100*recall_results[i]:.2f}%\n"
    text_to_report += f"+ F1-Score: {100*f1_results[i]:.2f}%\n\n"

text_to_report += "-"*15+"\n\n"
for k, v in global_results.items():
    if k=="accuracy":
        text_to_report += f"Acurácia: {100*v:.2f}%\n"
    elif k=="weighted avg":
        text_to_report += f"Média Ponderada\n"
        text_to_report += f"- Precisão: {100*v['precision']:.2f}%\n"
        text_to_report += f"- Recall: {100*v['recall']:.2f}%\n"
        text_to_report += f"- F1-Score: {100*v['f1-score']:.2f}%\n\n"
    elif k=="macro avg":
        text_to_report += f"Média Macro\n"
        text_to_report += f"- Precisão: {100*v['precision']:.2f}%\n"
        text_to_report += f"- Recall: {100*v['recall']:.2f}%\n"
        text_to_report += f"- F1-Score: {100*v['f1-score']:.2f}%\n\n"

with open("results/pull_request_report.md", "w") as file:
    file.write(text_to_report)
