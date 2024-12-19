from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON


def sparql_query(request):
    results = None  # Initialiser les résultats comme None
    user_query = ""  # Stocker la requête utilisateur

    if request.method == 'POST':
        user_query = request.POST.get('query', '')  # Obtenir la requête SPARQL de l'utilisateur

        # Configurer l'endpoint SPARQL de DBpedia
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery(user_query)
        sparql.setReturnFormat(JSON)

        try:
            # Exécuter la requête et récupérer la réponse
            response = sparql.query().convert()
            raw_results = response.get('results', {}).get('bindings', [])

            # Transformer les résultats pour inclure des labels lisibles
            results = []
            for result in raw_results:
                subject = result.get('subject', {}).get('value', '')
                label = result.get('label', {}).get('value', subject)  # Utiliser le label si disponible
                results.append({
                    'subject': subject,
                    'label': label,
                })
        except Exception as e:
            results = [{'label': f'Erreur: {e}'}]

    return render(request, 'sparql_form.html', {'results': results, 'user_query': user_query})
