### Model Card : Prédiction d'Attrition Technova

## Détails du Modèle
* **Nom :** Technova XGBoost Recall-Optimized
* **Version :** 1.0.0
* **Type :** Classification Binaire (Supervisé)
* **Algorithme :** XGBoost (avec `scale_pos_weight=5.20`)
* **Auteur :** Fatih

## Objectif 
Ce modèle est un outil d'aide à la décision pour les RH de **Technova**. Il vise à identifier les employés à risque de départ afin de proposer des actions de rétention préventives.

## Données d'Entraînement
Le modèle a été entraîné sur un dataset interne consolidé (SIRH + Évaluations + Sondages).
* **Source :** Données simulées Technova.
* **Déséquilibre :** Fort déséquilibre des classes (84% Reste / 16% Départ).
* **Stratégie :** Utilisation de la pondération (`scale_pos_weight`) pour forcer le modèle à prêter attention à la classe minoritaire (les départs).

## Performances
Le modèle a été évalué sur un jeu de test avec une stratégie favorisant le **Rappel (Recall)**, jugé critique pour ne pas "rater" un démissionnaire potentiel.

### Métriques Clés (Test Set)
* **Accuracy (Précision globale) :** 81%
* **F1-Score (Weighted) :** 0.82

### Focus Classe "Départ" (Attrition = 1)
* **Recall (Rappel) :** 60% (Le modèle détecte 60% des départs réels).
* **Precision :** 44% (Lorsqu'il prédit un départ, il a raison dans 44% des cas).
* *Interprétation :* Le modèle est volontairement "prudent". Il préfère lever une fausse alerte (Faux Positif) plutôt que de manquer un départ réel (Faux Négatif).

## Variables Clés (SHAP Values)
L'analyse d'interprétabilité (SHAP) montre que les décisions du modèle reposent principalement sur :
1.  **Heures Supplémentaires** (`heure_supplementaires`) : Le facteur n°1. Les employés surchargés partent davantage.
2.  **Participation PEE** (`nombre_participation_pee`) : Un levier de rétention fort.
3.  **Âge** (`age`) : Corrélation avec la mobilité professionnelle.
4.  **Revenu Mensuel** (`revenu_mensuel`).
5.  **Ancienneté** (`annees_dans_l_entreprise`).

## Limites et Biais
* **Faux Positifs :** En raison de l'optimisation du Rappel, le modèle génère des fausses alertes. Une validation humaine est indispensable avant toute action.
* **Données Fictives :** Le modèle est calibré sur la culture d'entreprise spécifique de Technova et ne doit pas être appliqué à une autre structure sans réentraînement.

## Maintenance
Le modèle doit être surveillé via la table `prediction_logs` pour vérifier la stabilité des prédictions. Un réentraînement annuel est recommandé pour intégrer les évolutions salariales et structurelles de l'entreprise.
