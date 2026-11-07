import time
import urllib.parse
from typing import List, Dict, Any

import requests

_CACHE: Dict[str, Any] = {}
CACHE_TTL = 300

HEADERS = {
    "User-Agent": "DevTrackAI-CareerPlatform/1.0 (Job Aggregator)",
    "Accept": "application/json",
}

EMPLOYMENT_TYPE_TERMS = {
    "fresher": "entry level",
    "internship": "internship",
    "part_time": "part time",
    "freelance": "freelance",
}

EMPLOYMENT_TYPE_KEYWORDS = {
    "fresher": ("entry level", "junior", "graduate", "new grad", "fresher", "trainee", "early career"),
    "internship": ("intern", "internship"),
    "part_time": ("part time", "parttime"),
    "freelance": ("freelance", "contractor", "contract"),
}


def _matches_employment_type(
    job: Dict[str, Any],
    title: str,
    tags: List[str],
    employment_type: str,
) -> bool:
    if employment_type == "all":
        return True

    text = " ".join(
        str(value)
        for value in [
            title,
            *tags,
            job.get("jobType"),
            job.get("job_type"),
            job.get("employmentType"),
            job.get("employment_type"),
            job.get("type"),
        ]
        if value
    ).lower().replace("-", " ").replace("_", " ")

    return any(
        keyword in text
        for keyword in EMPLOYMENT_TYPE_KEYWORDS.get(employment_type, ())
    )


def get_platform_search_links(
    role: str,
    location: str = "",
    employment_type: str = "all",
) -> List[Dict[str, str]]:
    query = role.strip()
    if employment_type in EMPLOYMENT_TYPE_TERMS:
        query = f"{query} {EMPLOYMENT_TYPE_TERMS[employment_type]}"
    loc = location.strip() if location else "Remote"
    encoded_q = urllib.parse.quote_plus(query)
    encoded_loc = urllib.parse.quote_plus(loc)

    return [
        {
            "platform": "LinkedIn",
            "name": "LinkedIn Jobs",
            "icon": "linkedin",
            "url": f"https://www.linkedin.com/jobs/search/?keywords={encoded_q}&location={encoded_loc}",
            "color": "#0a66c2",
        },
        {
            "platform": "Indeed",
            "name": "Indeed",
            "icon": "indeed",
            "url": f"https://www.indeed.com/jobs?q={encoded_q}&l={encoded_loc}",
            "color": "#2164f3",
        },
        {
            "platform": "Glassdoor",
            "name": "Glassdoor",
            "icon": "glassdoor",
            "url": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={encoded_q}",
            "color": "#0caa41",
        },
        {
            "platform": "GoogleJobs",
            "name": "Google Jobs",
            "icon": "google",
            "url": f"https://www.google.com/search?q={encoded_q}+jobs+{encoded_loc}&ibp=htl;jobs",
            "color": "#ea4335",
        },
        {
            "platform": "Wellfound",
            "name": "Wellfound (AngelList)",
            "icon": "wellfound",
            "url": f"https://wellfound.com/jobs?role={encoded_q}",
            "color": "#ff5a5f",
        },
        {
            "platform": "WeWorkRemotely",
            "name": "We Work Remotely",
            "icon": "remote",
            "url": f"https://weworkremotely.com/remote-jobs/search?term={encoded_q}",
            "color": "#e05342",
        },
    ]


def fetch_remoteok_jobs(
    keywords: List[str],
    employment_type: str = "all",
) -> List[Dict[str, Any]]:
    cache_key = "remoteok_all"
    now = time.time()

    raw_jobs = []
    if cache_key in _CACHE and (now - _CACHE[cache_key][0] < CACHE_TTL):
        raw_jobs = _CACHE[cache_key][1]
    else:
        try:
            resp = requests.get("https://remoteok.com/api", headers=HEADERS, timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                raw_jobs = [j for j in data if isinstance(j, dict) and j.get("position")]
                _CACHE[cache_key] = (now, raw_jobs)
        except Exception:
            raw_jobs = []

    results = []
    for job in raw_jobs:
        title = job.get("position", "")
        company = job.get("company", "")
        tags = job.get("tags") or []
        location = job.get("location") or "Remote"

        searchable = f"{title} {company} {' '.join(tags)}".lower()
        if (
            any(kw.lower() in searchable for kw in keywords)
            and _matches_employment_type(job, title, tags, employment_type)
        ):
            url = job.get("url") or f"https://remoteok.com/l/{job.get('id', '')}"
            if not url.startswith("http"):
                url = f"https://remoteok.com{url}"

            salary = ""
            if job.get("salary_min") and job.get("salary_max"):
                salary = f"${job['salary_min']:,} - ${job['salary_max']:,}"
            elif job.get("salary_min"):
                salary = f"From ${job['salary_min']:,}"

            results.append({
                "title": title,
                "company": company,
                "location": location,
                "platform": "RemoteOK",
                "url": url,
                "tags": tags[:5],
                "salary": salary,
                "posted": job.get("date", "")[:10] if job.get("date") else "Recent",
            })
            if len(results) >= 20:
                break

    return results


def fetch_jobicy_jobs(
    keywords: List[str],
    employment_type: str = "all",
) -> List[Dict[str, Any]]:
    cache_key = "jobicy_all"
    now = time.time()

    raw_jobs = []
    if cache_key in _CACHE and (now - _CACHE[cache_key][0] < CACHE_TTL):
        raw_jobs = _CACHE[cache_key][1]
    else:
        try:
            resp = requests.get("https://jobicy.com/api/v2/remote-jobs?count=40", headers=HEADERS, timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                raw_jobs = data.get("jobs", [])
                _CACHE[cache_key] = (now, raw_jobs)
        except Exception:
            raw_jobs = []

    results = []
    for job in raw_jobs:
        title = job.get("jobTitle", "")
        company = job.get("companyName", "")
        industry = job.get("jobIndustry") or []
        if isinstance(industry, list):
            tags = industry
        elif isinstance(industry, str):
            tags = [industry]
        else:
            tags = []

        searchable = f"{title} {company} {' '.join(tags)}".lower()
        if (
            any(kw.lower() in searchable for kw in keywords)
            and _matches_employment_type(job, title, tags, employment_type)
        ):
            salary = ""
            min_sal = job.get("annualSalaryMin")
            max_sal = job.get("annualSalaryMax")
            cur = job.get("salaryCurrency") or "$"
            if min_sal and max_sal:
                salary = f"{cur}{min_sal:,} - {cur}{max_sal:,}"

            results.append({
                "title": title,
                "company": company,
                "location": job.get("jobGeo") or "Remote",
                "platform": "Jobicy",
                "url": job.get("url", ""),
                "tags": tags[:4],
                "salary": salary,
                "posted": (job.get("pubDate") or "")[:10] or "Recent",
            })
            if len(results) >= 20:
                break

    return results


def fetch_arbeitnow_jobs(
    keywords: List[str],
    employment_type: str = "all",
) -> List[Dict[str, Any]]:
    cache_key = "arbeitnow_all"
    now = time.time()

    raw_jobs = []
    if cache_key in _CACHE and (now - _CACHE[cache_key][0] < CACHE_TTL):
        raw_jobs = _CACHE[cache_key][1]
    else:
        try:
            resp = requests.get("https://www.arbeitnow.com/api/job-board-api", headers=HEADERS, timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                raw_jobs = data.get("data", [])
                _CACHE[cache_key] = (now, raw_jobs)
        except Exception:
            raw_jobs = []

    results = []
    for job in raw_jobs:
        title = job.get("title", "")
        company = job.get("company_name", "")
        tags = job.get("tags") or []
        location = job.get("location") or ("Remote" if job.get("remote") else "Worldwide")

        searchable = f"{title} {company} {' '.join(tags)}".lower()
        if (
            any(kw.lower() in searchable for kw in keywords)
            and _matches_employment_type(job, title, tags, employment_type)
        ):
            results.append({
                "title": title,
                "company": company,
                "location": location,
                "platform": "Arbeitnow",
                "url": job.get("url", ""),
                "tags": tags[:4],
                "salary": "",
                "posted": "Recent",
            })
            if len(results) >= 20:
                break

    return results


def search_role_jobs(
    role: str,
    location: str = "Remote",
    platform: str = "all",
    employment_type: str = "all",
) -> Dict[str, Any]:
    clean_role = role.strip()
    if not clean_role:
        return {
            "query": "",
            "total_found": 0,
            "jobs": [],
            "platform_links": [],
        }

    keywords = [w for w in clean_role.lower().split() if len(w) > 2]
    if not keywords:
        keywords = [clean_role.lower()]

    aggregated: List[Dict[str, Any]] = []

    if platform in ("all", "remoteok"):
        try:
            aggregated.extend(fetch_remoteok_jobs(keywords, employment_type))
        except Exception:
            pass

    if platform in ("all", "jobicy"):
        try:
            aggregated.extend(fetch_jobicy_jobs(keywords, employment_type))
        except Exception:
            pass

    if platform in ("all", "arbeitnow"):
        try:
            aggregated.extend(fetch_arbeitnow_jobs(keywords, employment_type))
        except Exception:
            pass

    seen = set()
    unique_jobs = []
    for j in aggregated:
        key = (j["company"].lower(), j["title"].lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(j)

    platform_links = get_platform_search_links(clean_role, location, employment_type)

    return {
        "query": clean_role,
        "location": location,
        "employment_type": employment_type,
        "total_found": len(unique_jobs),
        "jobs": unique_jobs[:35],
        "platform_links": platform_links,
    }
