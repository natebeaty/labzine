def lab_issues(request):
    "Returns all issues of LAB"
    from labzine.articles.models import Issue,Slogan
    # articles = Article.objects.all()
    # featured = Issue.objects.get(featured='1')
    try: 
        current_issue = Issue.objects.get(featured=True)
    except:
        current_issue = Issue.objects.filter(active=True).reverse()[0]
    
    return {
        'all_issues': Issue.objects.all(),
        'featured_issue': current_issue,
        'slogans': Slogan.objects.all(),
    }
