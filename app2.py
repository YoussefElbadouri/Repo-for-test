from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change cette clé pour plus de sécurité

# Configuration de Jenkins
JENKINS_URL = "http://13.39.160.42:8080"  # URL de Jenkins sur EC2
JENKINS_JOB = "sbiy3at"  # Nom de la pipeline Jenkins
JENKINS_USER = "admin"  # Ton utilisateur Jenkins
JENKINS_TOKEN = "5a0f1412f23b4300bd0c12e41b759747"  # Token API Jenkins

def get_crumb():
    """Récupère un Crumb pour éviter l'erreur CSRF"""
    crumb_url = f"{JENKINS_URL}/crumbIssuer/api/json"
    response = requests.get(crumb_url, auth=(JENKINS_USER, JENKINS_TOKEN))

    if response.status_code == 200:
        crumb_data = response.json()
        return crumb_data["crumbRequestField"], crumb_data["crumb"]
    else:
        return None, None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        github_repo = request.form["github_repo"]
        if not github_repo:
            flash("Veuillez entrer un lien GitHub valide.", "danger")
            return redirect(url_for("index"))

        # Récupération du Crumb Token pour Jenkins
        crumb_field, crumb_value = get_crumb()
        if not crumb_field:
            flash("Erreur: Impossible de récupérer un Crumb de Jenkins.", "danger")
            return redirect(url_for("index"))

        # Construire l'URL pour déclencher Jenkins
        jenkins_url = f"{JENKINS_URL}/job/{JENKINS_JOB}/buildWithParameters"
        params = {"GITHUB_REPO": github_repo}

        # Ajouter le Crumb Token dans les headers
        headers = {crumb_field: crumb_value}

        # Envoyer la requête POST
        response = requests.post(jenkins_url, params=params, auth=(JENKINS_USER, JENKINS_TOKEN), headers=headers)

        if response.status_code == 201:
            flash("Pipeline déclenchée avec succès !", "success")
        else:
            flash(f"Erreur lors du déclenchement : {response.text}", "danger")

        return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/report")
def report():
    """Redirige vers le dernier rapport généré sur Jenkins"""
    report_url = f"{JENKINS_URL}/job/{JENKINS_JOB}/lastSuccessfulBuild/artifact/security-reports.zip"
    return redirect(report_url)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
