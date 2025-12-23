# PRD — Application Flask de gestion de budget mensuel

## 1. Contexte et vision
L’objectif est de créer une application web **Flask** permettant de gérer finement un budget **par période mensuelle** (ex. janvier 2026, février 2026).  
L’utilisateur crée une période (un mois), saisit des **entrées d’argent** (revenus) et des **dépenses**, puis l’application calcule automatiquement le **résultat** de la période (solde).

## 2. Objectifs
- Permettre de **créer, consulter, modifier et supprimer** des périodes mensuelles.
- Permettre de **saisir et gérer** des transactions de deux types : **Entrée** et **Dépense**.
- Calculer automatiquement pour chaque période :
  - Total des entrées
  - Total des dépenses
  - Résultat (entrées – dépenses)
- Fournir une interface simple et rapide pour le suivi mensuel.

## 3. Non-objectifs (pour la V1)
- Connexion bancaire / agrégation automatique des transactions.
- Multi-devises.
- Budgets par catégories avec enveloppes avancées.
- Gestion collaborative / multi-utilisateur (sauf si explicitement souhaité).
- Prévisions et recommandations automatiques (IA).

## 4. Public cible & persona
### Persona principal
**Utilisateur individuel** souhaitant suivre ses finances personnelles mois par mois, sans complexité, avec une vision claire du solde.

## 5. Hypothèses & contraintes
- L’application est une **web app** locale ou hébergée (au choix).
- V1 centrée sur un **seul utilisateur** (simple).
- Les périodes correspondent à un mois calendaire, identifiées par **année + mois**.
- Les transactions appartiennent à **une période** (mois) et ne se partagent pas entre périodes.
- L’utilisateur veut une app **simple**, orientée saisie et bilan.

## 6. Définitions
- **Période** : un mois (ex. 2026-01) avec ses transactions.
- **Transaction** : un enregistrement financier avec : type (entrée/dépense), montant, date, libellé, catégorie optionnelle, notes optionnelles.
- **Résultat de période** : total entrées – total dépenses.

## 7. Parcours utilisateur (V1)
1. L’utilisateur arrive sur un **tableau de bord** listant les périodes existantes.
2. Il **crée une nouvelle période** (mois/année).
3. Il entre des **transactions** (entrées et dépenses) dans la période.
4. L’application affiche instantanément :
   - Total entrées, total dépenses, résultat
5. Il peut **modifier/supprimer** une transaction.
6. Il peut consulter l’historique des périodes et comparer visuellement (simple).

## 8. User stories
### Gestion des périodes
- En tant qu’utilisateur, je veux créer une période (mois/année) pour suivre mon budget sur ce mois.
- En tant qu’utilisateur, je veux voir la liste des périodes existantes et leur résultat pour naviguer rapidement.
- En tant qu’utilisateur, je veux supprimer une période pour retirer un mois inutile (avec suppression des transactions associées).

### Gestion des transactions
- En tant qu’utilisateur, je veux ajouter une entrée d’argent avec un montant et un libellé.
- En tant qu’utilisateur, je veux ajouter une dépense avec un montant et un libellé.
- En tant qu’utilisateur, je veux modifier une transaction si je me suis trompé.
- En tant qu’utilisateur, je veux supprimer une transaction si elle n’est plus pertinente.
- En tant qu’utilisateur, je veux filtrer/chercher mes transactions pour retrouver un achat/une entrée.

### Calculs & synthèse
- En tant qu’utilisateur, je veux voir le total des entrées, des dépenses et le solde pour chaque période.
- En tant qu’utilisateur, je veux visualiser la répartition des dépenses (option V1.1) pour comprendre où part mon argent.

## 9. Spécifications fonctionnelles

### 9.1 Périodes (mois)
**FR-1 — Création de période**
- L’utilisateur choisit **mois** et **année**.
- Règles :
  - Une période est **unique** par (année, mois).
  - Si la période existe déjà, afficher une erreur claire.

**FR-2 — Liste des périodes**
- Afficher : mois/année, total entrées, total dépenses, résultat.
- Trier par défaut : du plus récent au plus ancien.

**FR-3 — Consultation d’une période**
- Page dédiée avec :
  - Synthèse : total entrées / total dépenses / résultat
  - Liste des transactions (avec tri et filtres)
  - Bouton “Ajouter une entrée” / “Ajouter une dépense”

**FR-4 — Modification d’une période (optionnel V1)**
- Autoriser le renommage (ex. correction année/mois) uniquement si la nouvelle période n’existe pas déjà.

**FR-5 — Suppression d’une période**
- Confirmation explicite.
- Comportement :
  - Supprime la période et **toutes ses transactions** (cascade).

---

### 9.2 Transactions
**FR-6 — Ajout d’une transaction**
Champs minimaux :
- Type : `ENTREE` ou `DEPENSE`
- Montant : décimal positif (ex. 12.50)
- Date : par défaut la date du jour (modifiable)
- Libellé : texte court obligatoire

Champs optionnels :
- Catégorie (liste libre ou prédéfinie)
- Notes

Règles :
- Montant strictement > 0
- Date doit appartenir au mois de la période (option V1) :
  - soit contrainte stricte (recommandé) : empêcher une date en dehors du mois
  - soit souple : autoriser mais afficher un avertissement

**FR-7 — Modification d’une transaction**
- Modifier tous les champs.
- Historique des modifications : non requis V1.

**FR-8 — Suppression d’une transaction**
- Confirmation rapide (modal ou page).

**FR-9 — Recherche & filtres (V1)**
- Filtre par type (entrées/dépenses).
- Recherche textuelle sur libellé.
- Filtre par catégorie (si catégories activées).

**FR-10 — Tri**
- Tri par date (desc par défaut), montant, libellé.

---

### 9.3 Calculs & affichage du résultat
**FR-11 — Totaux de période**
- Total entrées = somme des montants des transactions type ENTREE
- Total dépenses = somme des montants des transactions type DEPENSE
- Résultat = total entrées – total dépenses

**FR-12 — Mise à jour instantanée**
- Après ajout/modification/suppression d’une transaction, les totaux affichés sont recalculés et cohérents.

**FR-13 — Arrondis**
- Affichage monétaire avec 2 décimales.
- Stockage décimal (éviter float).

---

### 9.4 Import / Export (V1.1 ou option)
**FR-14 — Export CSV**
- Export des transactions d’une période.
- Export de l’historique multi-périodes.

**FR-15 — Import CSV**
- Import guidé avec mapping des colonnes.

## 10. Spécifications non-fonctionnelles

### 10.1 Performance
- Page d’une période doit charger en < 1s pour ~200 transactions (objectif local).
- Pagination au-delà d’un seuil (optionnel si volumes importants).

### 10.2 Sécurité & confidentialité
- Données financières sensibles :
  - Si app locale : stockage local + conseils de sauvegarde.
  - Si app en ligne : HTTPS obligatoire.
- Authentification (V1 optionnel, recommandé si hébergé) :
  - Compte unique avec mot de passe (hash sécurisé).
- Protection CSRF pour formulaires.
- Validation serveur de toutes les entrées.

### 10.3 Qualité & fiabilité
- Tests unitaires sur :
  - règles d’unicité de période
  - calculs de totaux
  - validations montants/dates
- Backups :
  - recommandation export JSON/CSV ou backup DB (doc).

### 10.4 Accessibilité & UX
- Interface simple, lisible, responsive.
- Actions principales accessibles en 1–2 clics (ajout entrée/dépense).

## 11. Modèle de données (proposition)
### Entités
**Period**
- id (UUID ou int)
- year (int)
- month (int 1–12)
- created_at, updated_at

Contraintes :
- UNIQUE(year, month)

**Transaction**
- id
- period_id (FK)
- type (enum: ENTREE, DEPENSE)
- amount (decimal)
- date (date)
- label (string)
- category (string, nullable)
- notes (text, nullable)
- created_at, updated_at

Index recommandés :
- (period_id, date)
- (period_id, type)

## 12. Écrans (V1)

### 12.1 Dashboard — Liste des périodes
- Bouton : “Créer une période”
- Tableau : Mois, Entrées, Dépenses, Résultat, actions (ouvrir/supprimer)

### 12.2 Création de période
- Sélecteur mois + année
- Validation unicité
- CTA : “Créer”

### 12.3 Détail d’une période
- Bandeau synthèse : total entrées / total dépenses / résultat
- Boutons : “Ajouter une entrée”, “Ajouter une dépense”
- Liste des transactions avec :
  - filtres (type, recherche, catégorie)
  - tri
  - actions (éditer, supprimer)

### 12.4 Formulaire transaction (ajout/édition)
- Type (pré-sélectionné selon le bouton)
- Montant
- Date
- Libellé
- Catégorie (optionnelle)
- Notes (optionnelles)

### 12.5 Suppression (période/transaction)
- Confirmation explicite
- Message de succès/erreur

## 13. Règles de validation (résumé)
- Période :
  - month ∈ [1..12]
  - year ∈ plage raisonnable (ex. 2000–2100)
  - unicité (year, month)
- Transaction :
  - amount > 0 (decimal, 2 décimales max côté UI)
  - label non vide
  - date valide
  - period_id obligatoire
  - (option) date dans le mois de la période

## 14. Logs & audit (option)
- Log applicatif minimal : erreurs, exceptions, actions CRUD.
- Audit détaillé non requis V1.

## 15. Mesures de succès (KPIs)
- Nombre de périodes créées.
- Nombre de transactions saisies / mois.
- Taux d’utilisation récurrente (retour d’un mois sur l’autre).
- Erreurs de validation (pour améliorer UX).

## 16. Plan de livraison (suggestion)
### V1 — MVP
- CRUD périodes
- CRUD transactions
- Calculs + dashboard
- Filtres simples

### V1.1 — Qualité de vie
- Export CSV
- Catégories améliorées (liste prédéfinie + personnalisable)
- Graphiques simples (répartition des dépenses, évolution du solde)

### V2 — (option)
- Multi-utilisateur
- Import CSV avancé
- Budgets par catégorie avec objectifs
- Notifications / rappels

## 17. Risques & mitigations
- **Erreur de calcul** (arrondis/float) → utiliser decimal + tests.
- **Saisie fastidieuse** → formulaires rapides, duplications (option V1.1), raccourcis.
- **Perte de données** (si local) → export/backup facilité + doc.
- **Date hors période** → validation stricte ou avertissement clair.

## 18. Questions ouvertes (à trancher)
- L’application doit-elle être **mono-utilisateur** (recommandé V1) ou prévoir l’auth tout de suite ?
- Contrainte sur la date des transactions : strictement dans le mois, ou tolérance ?
- Catégories : libres, prédéfinies, ou mixte ?
- Hébergement : local (SQLite) vs serveur (PostgreSQL) ?

---

*Document PRD — Version 1.0 (23/12/2025, Europe/Paris)*
