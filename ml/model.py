import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Sample job profiles
JOB_PROFILES = [

    {
        "title": "Python Full-Stack Developer",
        "skills": "python flask django html css javascript mysql rest api"
    },

    {
        "title": "Backend Python Developer",
        "skills": "python flask django mysql postgresql rest api docker"
    },

    {
        "title": "Frontend Developer",
        "skills": "html css javascript react typescript angular vue responsive ui gsap"
    },

    {
        "title": "Machine Learning Engineer",
        "skills": "python machine learning scikit-learn pandas numpy model training"
    },

    {
        "title": "Data Analyst",
        "skills": "python sql mysql pandas numpy excel statistics data visualization"
    },

    {
        "title": "AI Application Developer",
        "skills": "python flask api machine learning llm prompt engineering sql"
    },

    {
        "title": "QA Automation Engineer",
        "skills": "python selenium testing automation pytest javascript playwright cypress"
    },

    {
        "title": "Java Backend Developer",
        "skills": "java spring spring boot maven gradle microservices mysql postgresql rest api"
    },

    {
        "title": "JavaScript Full-Stack Developer",
        "skills": "javascript typescript react node express html css rest api mongodb postgresql"
    },

    {
        "title": ".NET Developer",
        "skills": "csharp c sharp dotnet asp net sql server azure api"
    },

    {
        "title": "C++ Systems Developer",
        "skills": "cplusplus c plus plus cpp systems programming linux performance memory safety"
    },

    {
        "title": "Go Backend Developer",
        "skills": "go golang microservices docker kubernetes rest api postgresql"
    },

    {
        "title": "Rust Systems Developer",
        "skills": "rust systems programming linux memory safety performance"
    },

    {
        "title": "PHP Web Developer",
        "skills": "php laravel symfony mysql javascript html css api"
    },

    {
        "title": "Mobile App Developer",
        "skills": "android kotlin swift ios java mobile app development"
    },

    {
        "title": "Cloud and DevOps Engineer",
        "skills": "aws azure gcp cloud docker kubernetes terraform linux ci cd git"
    },

    {
        "title": "Data Engineer",
        "skills": "sql spark hadoop airflow dbt python data pipelines aws"
    },

    {
        "title": "Cybersecurity Analyst",
        "skills": "cybersecurity security networking linux siem risk compliance"
    },

    {
        "title": "UI/UX Designer",
        "skills": "figma ui ux prototyping accessibility user research design"
    }

]


# Extract job skills
corpus = [
    job["skills"] for job in JOB_PROFILES
]


# Convert text into numerical vectors
vectorizer = TfidfVectorizer()

job_matrix = vectorizer.fit_transform(corpus)


# Recommendation function
def recommend_jobs(user_skills):

    normalized_skills = user_skills.lower()
    normalized_skills = re.sub(r"\bc\s*\+\s*\+", "cplusplus", normalized_skills)
    normalized_skills = re.sub(r"\bc\s*#", "csharp", normalized_skills)
    normalized_skills = re.sub(r"\.net\b", "dotnet", normalized_skills)

    # Convert user skills into a vector
    user_vector = vectorizer.transform([
        normalized_skills
    ])

    # Calculate similarity
    scores = cosine_similarity(
        user_vector,
        job_matrix
    ).flatten()

    # Rank jobs
    ranked = scores.argsort()[::-1][:5]

    recommendations = []

    for i in ranked:

        if scores[i] > 0:

            recommendations.append({

                "title": JOB_PROFILES[i]["title"],

                "match": round(
                    float(scores[i]) * 100, 1
                ),

                "matched_skills": JOB_PROFILES[i]["skills"]

            })

    return recommendations