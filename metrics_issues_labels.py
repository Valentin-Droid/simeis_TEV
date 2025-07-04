import urllib.request
import urllib.parse
import json
import os
from collections import Counter
from datetime import datetime

# Configuration
GITHUB_OWNER = "Valentin-Droid"
GITHUB_REPO = "simeis_TEV"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_issues(owner, repo):
    issues = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        params = {
            "state": "all",
            "per_page": 100,
            "page": page
        }
        
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        
        request = urllib.request.Request(full_url)
        if GITHUB_TOKEN:
            request.add_header("Authorization", f"token {GITHUB_TOKEN}")
        
        try:
            with urllib.request.urlopen(request) as response:
                if response.status != 200:
                    raise Exception(f"Erreur lors de la récupération des issues : {response.status}")
                
                data = json.loads(response.read().decode('utf-8'))
                if not data:
                    break
                issues.extend(data)
                page += 1
        except urllib.error.HTTPError as e:
            raise Exception(f"Erreur HTTP lors de la récupération des issues : {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            raise Exception(f"Erreur URL lors de la récupération des issues : {e.reason}")
    
    return issues

def generate_metrics(issues):
    label_counter = Counter()
    total_issues = 0
    open_issues = 0
    closed_issues = 0

    for issue in issues:
        if "pull_request" in issue:
            continue 

        total_issues += 1
        
        # Compter les issues ouvertes/fermées
        if issue.get("state") == "open":
            open_issues += 1
        else:
            closed_issues += 1
        
        labels = issue.get("labels", [])
        for label in labels:
            label_counter[label["name"]] += 1

    return total_issues, open_issues, closed_issues, label_counter

def print_metrics(total_issues, open_issues, closed_issues, label_counter):
    print("=" * 60)
    print("📊 MÉTRIQUES DES ISSUES GITHUB")
    print("=" * 60)
    print(f"📅 Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Dépôt : {GITHUB_OWNER}/{GITHUB_REPO}")
    print()
    
    # Tableau des statistiques générales
    print("📈 STATISTIQUES GÉNÉRALES")
    print("-" * 40)
    print(f"{'Total d\'issues (hors PR)':<25} : {total_issues:>8}")
    print(f"{'Issues ouvertes':<25} : {open_issues:>8}")
    print(f"{'Issues fermées':<25} : {closed_issues:>8}")
    if total_issues > 0:
        print(f"{'Taux de fermeture':<25} : {closed_issues/total_issues*100:>7.1f}%")
    print()
    
    # Tableau des labels
    if label_counter:
        print("🏷️  ISSUES PAR LABEL")
        print("-" * 40)
        print(f"{'Label':<20} | {'Nombre':<8} | {'Pourcentage'}")
        print("-" * 40)
        for label, count in label_counter.most_common():
            percentage = (count / total_issues * 100) if total_issues > 0 else 0
            print(f"{label:<20} | {count:>6} | {percentage:>9.1f}%")
    else:
        print("🏷️  Aucun label trouvé")
    
    print("=" * 60)

if __name__ == "__main__":
    issues = fetch_issues(GITHUB_OWNER, GITHUB_REPO)
    total_issues, open_issues, closed_issues, label_counter = generate_metrics(issues)
    print_metrics(total_issues, open_issues, closed_issues, label_counter)
